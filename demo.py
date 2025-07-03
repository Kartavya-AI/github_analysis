#!/usr/bin/env python3
"""
GitCrew Demo Script
Demonstrates the GitCrew AI HR System for GitHub Developer Analysis
"""

import os
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from crew.gitcrew import GitCrew


def main():
    """Run GitCrew demo"""
    print("🚀 GitCrew AI HR System Demo")
    print("=" * 50)
    
    try:
        # Initialize GitCrew
        print("Initializing GitCrew...")
        git_crew = GitCrew()
        print("✅ GitCrew initialized successfully!")
        
        # Get username input
        print("\nEnter a GitHub username to analyze:")
        print("(Examples: torvalds, gvanrossum, octocat, or any GitHub user)")
        username = input("Username: ").strip()
        
        if not username:
            print("❌ No username provided. Exiting.")
            return
        
        print(f"\n🔍 Analyzing GitHub user: {username}")
        print("-" * 30)
        
        # Show available analysis options
        print("\nAvailable analysis types:")
        print("1. Quick Stats (instant)")
        print("2. Quick Developer Analysis (AI-powered)")
        print("3. Comprehensive Analysis (full AI crew)")
        
        choice = input("\nSelect analysis type (1-3): ").strip()
        
        if choice == "1":
            print(f"\n📊 Getting quick stats for {username}...")
            stats = git_crew.get_developer_stats(username)
            
            if stats and 'error' not in stats:
                print("\n✅ Analysis Complete!")
                print("=" * 30)
                
                profile = stats.get('profile', {})
                print(f"👤 Name: {profile.get('name', 'N/A')}")
                print(f"🔗 Username: @{profile.get('login', 'N/A')}")
                print(f"📝 Bio: {profile.get('bio', 'N/A')}")
                print(f"📍 Location: {profile.get('location', 'N/A')}")
                print(f"🏢 Company: {profile.get('company', 'N/A')}")
                print(f"📦 Public Repos: {profile.get('public_repos', 'N/A')}")
                print(f"👥 Followers: {profile.get('followers', 'N/A')}")
                print(f"➡️ Following: {profile.get('following', 'N/A')}")
                
                repos = stats.get('repositories', {})
                print(f"⭐ Total Stars: {repos.get('total_stars', 'N/A')}")
                print(f"🍴 Total Forks: {repos.get('total_forks', 'N/A')}")
                print(f"💻 Primary Language: {repos.get('primary_language', 'N/A')}")
                
                activity = stats.get('activity', {})
                print(f"📅 Account Age: {activity.get('account_age_days', 'N/A')} days")
                print(f"🔄 Recent Activity: {activity.get('recent_activity', 'N/A')}")
                
                hr_rating = stats.get('hr_rating', {})
                print(f"📊 HR Rating: {hr_rating.get('overall_score', 'N/A')}/10")
                print(f"📈 Experience Level: {hr_rating.get('experience_level', 'N/A')}")
                
            else:
                print(f"❌ Error: {stats.get('error', 'User not found or API error') if stats else 'No response'}")
        
        elif choice == "2":
            print(f"\n🤖 Running quick AI analysis for {username}...")
            print("This will use GitHub Data Collector + Skills Assessment Analyst")
            print("⏱️ This may take 1-2 minutes...")
            
            try:
                result = git_crew.quick_developer_analysis(username)
                print("\n✅ Quick Analysis Complete!")
                print("=" * 40)
                print(result)
            except Exception as e:
                print(f"❌ Analysis failed: {e}")
        
        elif choice == "3":
            print(f"\n🚀 Running comprehensive AI analysis for {username}...")
            print("This will use the full AI crew:")
            print("- GitHub Data Collector")
            print("- Skills Assessment Analyst") 
            print("- Technical Profiler")
            print("- Report Generator")
            print("⏱️ This may take 3-5 minutes...")
            
            try:
                result = git_crew.analyze_developer(username)
                print("\n✅ Comprehensive Analysis Complete!")
                print("=" * 40)
                print(result)
            except Exception as e:
                print(f"❌ Analysis failed: {e}")
        
        else:
            print("❌ Invalid choice. Please select 1, 2, or 3.")
            
    except KeyboardInterrupt:
        print("\n\n👋 Analysis interrupted by user.")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check your internet connection")
        print("2. Ensure all dependencies are installed")
        print("3. Try with a different GitHub username")


if __name__ == "__main__":
    main()
    
    try:
        # Initialize tools
        github_analyzer = GitHubAnalyzerTool()
        github_trending = GitHubTrendingTool()
        
        print("\n1. 📊 Repository Analysis Demo")
        print("-" * 30)
        
        # Analyze a popular repository
        repo_name = "microsoft/vscode"
        print(f"Analyzing repository: {repo_name}")
        
        # Get basic stats
        stats = github_analyzer._execute(repo_name, "basic")
        if stats and "error" not in stats:
            print(f"✅ Repository found: {stats.get('full_name', 'N/A')}")
            print(f"   Stars: {stats.get('stargazers_count', 'N/A')}")
            print(f"   Forks: {stats.get('forks_count', 'N/A')}")
            print(f"   Language: {stats.get('language', 'N/A')}")
            print(f"   Description: {stats.get('description', 'N/A')[:100]}...")
        else:
            print(f"❌ Error: {stats.get('error', 'Unknown error') if stats else 'No response'}")
        
        print("\n2. 🔥 Trending Repositories Demo")
        print("-" * 30)
        
        # Get trending Python repositories
        trending = github_trending._execute("python", "weekly", 5)
        if trending and "error" not in trending:
            repos = trending.get('items', [])
            print(f"✅ Found {len(repos)} trending Python repositories")
            for i, repo in enumerate(repos[:3], 1):
                print(f"   {i}. {repo['full_name']} - {repo['stargazers_count']} stars")
                print(f"      {repo.get('description', 'No description')[:80]}...")
        else:
            print(f"❌ Error: {trending.get('error', 'Unknown error') if trending else 'No response'}")
        
        print("\n3. 🔍 Language Analysis Demo")
        print("-" * 30)
        
        # Analyze languages in a repository
        languages = github_analyzer._execute(repo_name, "languages")
        if languages and "error" not in languages:
            print(f"✅ Language analysis for {repo_name}:")
            lang_data = languages
            # Since we're using public API, the format might be different
            if isinstance(lang_data, dict):
                for lang, bytes_count in list(lang_data.items())[:3]:
                    if isinstance(bytes_count, int):
                        total = sum(lang_data.values())
                        percentage = (bytes_count / total * 100) if total > 0 else 0
                        print(f"   {lang}: {percentage:.1f}%")
        else:
            print(f"❌ Error: {languages.get('error', 'Unknown error') if languages else 'No response'}")
        
    except Exception as e:
        print(f"❌ Error in individual tools demo: {e}")


def demo_gitcrew():
    """Demo GitCrew capabilities"""
    print("\n🚀 GITCREW DEMONSTRATION")
    print("=" * 50)
    
    try:
        # Initialize GitCrew
        git_crew = GitCrew()
        print("✅ GitCrew initialized successfully!")
        
        print("\n1. 📈 Quick Repository Stats")
        print("-" * 30)
        
        # Get quick stats for a repository
        repo_name = "facebook/react"
        stats = git_crew.quick_repo_stats(repo_name)
        
        if stats and "error" not in stats:
            print(f"Repository: {stats.get('full_name', 'N/A')}")
            print(f"Description: {stats.get('description', 'N/A')[:100]}...")
            print(f"Stars: {stats.get('stargazers_count', 'N/A')}")
            print(f"Forks: {stats.get('forks_count', 'N/A')}")
            print(f"Language: {stats.get('language', 'N/A')}")
            print(f"Created: {stats.get('created_at', 'N/A')[:10]}")
        else:
            print(f"❌ Error: {stats.get('error', 'Unknown error') if stats else 'No response'}")
        
        print("\n2. 🔥 Trending Repositories")
        print("-" * 30)
        
        # Get trending repositories
        trending = git_crew.get_trending_repos("javascript", "weekly", 3)
        if trending and "error" not in trending:
            repos = trending.get('items', [])
            print(f"Top trending JavaScript repositories (weekly):")
            for i, repo in enumerate(repos, 1):
                print(f"   {i}. {repo['full_name']} - {repo['stargazers_count']} stars")
                print(f"      {repo.get('description', 'No description')[:80]}...")
        else:
            print(f"❌ Error: {trending.get('error', 'Unknown error') if trending else 'No response'}")
        
        print("\n3. 🎯 CrewAI Analysis Demo")
        print("-" * 30)
        
        print("CrewAI analysis would use AI agents for detailed analysis.")
        print("This includes technical metrics, community health, and strategic insights.")
        print("To run full CrewAI analysis, use: python src/crew/main.py")
        
    except Exception as e:
        print(f"❌ Error in GitCrew demo: {e}")


def demo_crewai_integration():
    """Demo CrewAI integration with sample analysis"""
    print("\n🧠 CREWAI INTEGRATION DEMONSTRATION")
    print("=" * 50)
    
    try:
        print("To run full CrewAI analysis with AI agents:")
        print("1. Navigate to the project directory")
        print("2. Run: python src/crew/main.py")
        print("3. Choose from the analysis options:")
        print("   - Repository Analysis")
        print("   - Trending Research")
        print("   - Comparative Analysis")
        print("   - Comprehensive Analysis")
        
        print("\nExample CrewAI workflow:")
        print("- AI agents analyze repository data")
        print("- Generate insights and recommendations")
        print("- Compare multiple repositories")
        print("- Identify trends and patterns")
        print("- Provide strategic recommendations")
        
    except Exception as e:
        print(f"❌ Error in CrewAI demo: {e}")


def main():
    """Main demo function"""
    print("🐙 GITHUB ANALYSIS TOOLS DEMONSTRATION")
    print("=" * 60)
    
    print("✅ Using publicly available GitHub API (no authentication required)")
    print("=" * 60)
    
    try:
        # Run demonstrations
        demo_individual_tools()
        demo_gitcrew()
        demo_crewai_integration()
        
        print("\n🎉 DEMONSTRATION COMPLETE!")
        print("=" * 60)
        print("You can now use these tools in your CrewAI projects!")
        print("\nNext steps:")
        print("1. Run: python src/crew/main.py for full CrewAI analysis")
        print("2. Customize agents and tasks in config/ directory")
        print("3. Use GitCrew class for programmatic access")
        print("4. Create custom CrewAI agents with these tools")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")


if __name__ == "__main__":
    main()
