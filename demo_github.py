#!/usr/bin/env python3
"""
Demo script for GitHub Repository Analysis Tools
This script demonstrates how to use the GitHub tools with CrewAI
"""

from src.crew.tools.github import GitHubAnalyzerTool, GitHubTrendingTool
import json


def demo_repo_analysis():
    """Demo repository analysis functionality"""
    print("🔍 GitHub Repository Analysis Demo")
    print("=" * 50)
    
    # Create GitHub analyzer tool
    analyzer = GitHubAnalyzerTool()
    
    # Test repositories
    test_repos = [
        "microsoft/vscode",
        "facebook/react",
        "pytorch/pytorch"
    ]
    
    for repo in test_repos:
        print(f"\n📊 Analyzing repository: {repo}")
        print("-" * 40)
        
        # Get basic repository info
        repo_info = analyzer._execute(repo, "stats")
        if "error" not in repo_info:
            print(f"⭐ Stars: {repo_info['stars']:,}")
            print(f"🍴 Forks: {repo_info['forks']:,}")
            print(f"👁️ Watchers: {repo_info['watchers']:,}")
            print(f"🐛 Open Issues: {repo_info['open_issues']:,}")
        else:
            print(f"❌ Error: {repo_info['error']}")
        
        # Analyze languages
        languages = analyzer._execute(repo, "languages")
        if "error" not in languages and languages.get("languages"):
            print(f"💻 Primary Language: {languages['primary_language']}")
            print("📈 Language Distribution:")
            for lang, data in list(languages["languages"].items())[:3]:
                print(f"   {lang}: {data['percentage']}%")
        
        # Get recent commits info
        commits = analyzer._execute(repo, "commits")
        if "error" not in commits:
            print(f"📝 Recent Commits (30 days): {commits['recent_commits_30_days']}")
            print(f"📅 Average Commits/Day: {commits['average_commits_per_day']}")
        
        print()


def demo_trending_repos():
    """Demo trending repositories functionality"""
    print("\n🔥 GitHub Trending Repositories Demo")
    print("=" * 50)
    
    # Create trending tool
    trending_tool = GitHubTrendingTool()
    
    # Get trending Python repositories
    print("\n🐍 Trending Python Repositories (Weekly)")
    print("-" * 40)
    
    trending = trending_tool._execute("python", "weekly", 5)
    if "error" not in trending:
        for i, repo in enumerate(trending["repositories"], 1):
            print(f"{i}. {repo['full_name']}")
            print(f"   ⭐ {repo['stars']} stars | 🍴 {repo['forks']} forks")
            print(f"   📝 {repo['description'][:80]}...")
            print()
    else:
        print(f"❌ Error: {trending['error']}")
    
    # Get trending JavaScript repositories
    print("\n🟨 Trending JavaScript Repositories (Daily)")
    print("-" * 40)
    
    trending = trending_tool._execute("javascript", "daily", 3)
    if "error" not in trending:
        for i, repo in enumerate(trending["repositories"], 1):
            print(f"{i}. {repo['full_name']}")
            print(f"   ⭐ {repo['stars']} stars | 🍴 {repo['forks']} forks")
            print(f"   📝 {repo['description'][:80]}...")
            print()
    else:
        print(f"❌ Error: {trending['error']}")


def demo_full_analysis():
    """Demo full repository analysis"""
    print("\n🔬 Full Repository Analysis Demo")
    print("=" * 50)
    
    analyzer = GitHubAnalyzerTool()
    
    # Analyze a popular repository
    repo_name = "openai/whisper"
    print(f"\n📊 Full Analysis of: {repo_name}")
    print("-" * 40)
    
    analysis = analyzer._execute(repo_name, "full")
    
    if "error" not in analysis:
        # Repository info
        if "repository_info" in analysis:
            repo_info = analysis["repository_info"]
            print(f"📖 Description: {repo_info.get('description', 'N/A')}")
            print(f"⭐ Stars: {repo_info['stars']:,}")
            print(f"🍴 Forks: {repo_info['forks']:,}")
            print(f"📅 Created: {repo_info['created_at'][:10]}")
            print(f"🔄 Last Updated: {repo_info['updated_at'][:10]}")
        
        # Languages
        if "languages" in analysis:
            languages = analysis["languages"]
            if languages.get("languages"):
                print(f"\n💻 Primary Language: {languages['primary_language']}")
                print("📊 Language Breakdown:")
                for lang, data in languages["languages"].items():
                    print(f"   {lang}: {data['percentage']}%")
        
        # Contributors
        if "contributors" in analysis:
            contributors = analysis["contributors"]
            print(f"\n👥 Total Contributors: {contributors['total_contributors']}")
            if contributors.get("top_contributors"):
                print("🏆 Top Contributors:")
                for contrib in contributors["top_contributors"][:3]:
                    print(f"   {contrib['login']}: {contrib['contributions']} contributions")
        
        # Recent activity
        if "recent_activity" in analysis:
            activity = analysis["recent_activity"]
            print(f"\n📈 Activity Score: {activity['activity_score']}/100")
            print(f"🔥 Is Active: {'Yes' if activity['is_active'] else 'No'}")
            print(f"📝 Recent Commits: {activity['recent_commits_count']}")
    else:
        print(f"❌ Error: {analysis['error']}")


if __name__ == "__main__":
    try:
        demo_repo_analysis()
        demo_trending_repos()
        demo_full_analysis()
        
        print("\n✅ Demo completed successfully!")
        print("\n💡 Tips for using these tools:")
        print("- Use GitHubAnalyzerTool for detailed repository analysis")
        print("- Use GitHubTrendingTool to discover popular repositories")
        print("- Combine multiple analysis types for comprehensive insights")
        print("- Handle rate limits by adding delays between requests")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        print("Make sure you have the required dependencies installed:")
        print("pip install -r requirements.txt")
