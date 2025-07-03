#!/usr/bin/env python3
"""
GitCrew Main Demo Script - AI HR System for GitHub Developer Analysis
This script demonstrates the GitCrew system with @crewbase and @crew decorators
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from gitcrew import GitCrew

# Load environment variables
load_dotenv()


def main():
    """Main demo function for GitCrew AI HR System"""
    print("🚀 GitCrew AI HR System - GitHub Developer Analysis")
    print("=" * 60)
    print("This system uses @crewbase and @crew decorators with YAML configs")
    print("=" * 60)
    
    try:
        # Initialize GitCrew
        print("\n🔧 Initializing GitCrew...")
        git_crew = GitCrew()
        print("✅ GitCrew initialized successfully!")
        
        # Show available analysis options
        print("\n📋 Available Analysis Options:")
        print("1. Quick Developer Stats (instant)")
        print("2. AI-Powered Developer Analysis (uses crew.kickoff())")
        print("3. Custom Crew Demo")
        print("4. Show Crew Configuration")
        
        choice = input("\nSelect analysis type (1-4): ").strip()
        
        if choice == "1":
            demo_quick_stats(git_crew)
        elif choice == "2":
            demo_ai_analysis(git_crew)
        elif choice == "3":
            demo_custom_crew(git_crew)
        elif choice == "4":
            show_crew_config(git_crew)
        else:
            print("Invalid choice. Running AI analysis demo...")
            demo_ai_analysis(git_crew)
            
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user.")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check your internet connection")
        print("2. Ensure all dependencies are installed")
        print("3. Verify YAML config files are present")


def demo_quick_stats(git_crew):
    """Demo quick developer stats without AI crew"""
    print("\n📊 Quick Developer Stats Demo")
    print("-" * 40)
    
    username = input("Enter GitHub username (or press Enter for 'torvalds'): ").strip()
    if not username:
        username = "torvalds"
    
    print(f"\n🔍 Getting quick stats for {username}...")
    
    try:
        stats = git_crew.get_developer_stats(username)
        
        if stats and 'error' not in stats:
            print("\n✅ Stats Retrieved Successfully!")
            print("=" * 40)
            
            profile = stats.get('profile', {})
            print(f"👤 Name: {profile.get('name', 'N/A')}")
            print(f"🔗 Username: @{profile.get('login', 'N/A')}")
            print(f"📝 Bio: {profile.get('bio', 'N/A')}")
            print(f"📍 Location: {profile.get('location', 'N/A')}")
            print(f"📦 Public Repos: {profile.get('public_repos', 'N/A')}")
            print(f"👥 Followers: {profile.get('followers', 'N/A')}")
            
            repos = stats.get('repositories', {})
            print(f"⭐ Total Stars: {repos.get('total_stars', 'N/A')}")
            print(f"💻 Primary Language: {repos.get('primary_language', 'N/A')}")
            
            hr_rating = stats.get('hr_rating', {})
            print(f"📊 HR Rating: {hr_rating.get('overall_score', 'N/A')}/10")
            print(f"📈 Experience Level: {hr_rating.get('experience_level', 'N/A')}")
            
        else:
            print(f"❌ Error: {stats.get('error', 'User not found') if stats else 'No response'}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def demo_ai_analysis(git_crew):
    """Demo AI-powered analysis using crew.kickoff()"""
    print("\n🤖 AI-Powered Developer Analysis Demo")
    print("-" * 40)
    print("This uses the @crew decorator and crew.kickoff() method")
    
    username = input("Enter GitHub username (or press Enter for 'gvanrossum'): ").strip()
    if not username:
        username = "gvanrossum"
    
    print(f"\n🚀 Starting AI analysis for {username}...")
    print("This will use the full GitCrew with @crewbase and @crew decorators")
    print("⏱️ This may take 2-3 minutes...")
    
    try:
        # Get the crew instance
        crew_instance = git_crew.crew()
        
        # Prepare inputs for the crew
        inputs = {
            'github_username': username,
            'analysis_type': 'comprehensive'
        }
        
        print(f"\n📋 Crew Configuration:")
        print(f"   - Agents: {len(crew_instance.agents)}")
        print(f"   - Tasks: {len(crew_instance.tasks)}")
        print(f"   - Process: {crew_instance.process}")
        print(f"   - Verbose: {crew_instance.verbose}")
        
        print(f"\n🔄 Starting crew.kickoff() with inputs: {inputs}")
        
        # Execute the crew
        result = crew_instance.kickoff(inputs=inputs)
        
        print("\n✅ AI Analysis Complete!")
        print("=" * 50)
        print(result)
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        print("Falling back to quick stats...")
        demo_quick_stats(git_crew)


def demo_custom_crew(git_crew):
    """Demo custom crew creation and execution"""
    print("\n🛠️ Custom Crew Demo")
    print("-" * 40)
    
    print("Available crew configurations:")
    print("1. Data Collection Only")
    print("2. Data Collection + Skills Assessment")
    print("3. Technical Profiling")
    print("4. Full Analysis Pipeline")
    
    choice = input("Select crew type (1-4): ").strip()
    
    username = input("Enter GitHub username: ").strip()
    if not username:
        print("❌ Username required for custom crew demo")
        return
    
    try:
        if choice == "1":
            # Just data collection
            print("\n📊 Running Data Collection Only...")
            agents = [git_crew.github_data_collector()]
            tasks = [git_crew.collect_github_data()]
            
        elif choice == "2":
            # Data collection + skills assessment
            print("\n🔍 Running Data Collection + Skills Assessment...")
            agents = [
                git_crew.github_data_collector(),
                git_crew.skill_assessment_analyst()
            ]
            tasks = [
                git_crew.collect_github_data(),
                git_crew.assess_developer_skills()
            ]
            
        elif choice == "3":
            # Technical profiling
            print("\n👨‍💻 Running Technical Profiling...")
            agents = [
                git_crew.github_data_collector(),
                git_crew.skill_assessment_analyst(),
                git_crew.technical_profiler()
            ]
            tasks = [
                git_crew.collect_github_data(),
                git_crew.assess_developer_skills(),
                git_crew.create_technical_profile()
            ]
            
        else:
            # Full pipeline
            print("\n🚀 Running Full Analysis Pipeline...")
            crew_instance = git_crew.crew()
            result = crew_instance.kickoff(inputs={'github_username': username})
            print(f"\n✅ Full Analysis Complete!\n{result}")
            return
        
        # Create custom crew
        from crewai import Crew, Process
        custom_crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        print(f"🔄 Executing custom crew with {len(agents)} agents and {len(tasks)} tasks...")
        result = custom_crew.kickoff(inputs={'github_username': username})
        
        print(f"\n✅ Custom Crew Analysis Complete!")
        print("=" * 50)
        print(result)
        
    except Exception as e:
        print(f"❌ Custom crew failed: {e}")


def show_crew_config(git_crew):
    """Show the crew configuration from YAML files"""
    print("\n📋 Crew Configuration Overview")
    print("-" * 40)
    
    try:
        print("🤖 Available Agents:")
        for agent_name in git_crew.agents_config.keys():
            agent_config = git_crew.agents_config[agent_name]
            print(f"   - {agent_name}")
            print(f"     Role: {agent_config.get('role', 'N/A')}")
            print(f"     Goal: {agent_config.get('goal', 'N/A')[:80]}...")
            print()
        
        print("📋 Available Tasks:")
        for task_name in git_crew.tasks_config.keys():
            task_config = git_crew.tasks_config[task_name]
            print(f"   - {task_name}")
            print(f"     Description: {task_config.get('description', 'N/A')[:80]}...")
            print()
        
        print("🔧 Crew Methods:")
        print("   - @agent decorators: 4 agents")
        print("   - @task decorators: 4 tasks")
        print("   - @crew decorator: 1 crew method")
        print("   - @crewbase class decorator")
        
        # Show the actual crew instance
        crew_instance = git_crew.crew()
        print(f"\n🚀 Crew Instance:")
        print(f"   - Agents: {len(crew_instance.agents)}")
        print(f"   - Tasks: {len(crew_instance.tasks)}")
        print(f"   - Process: {crew_instance.process}")
        print(f"   - Verbose: {crew_instance.verbose}")
        
    except Exception as e:
        print(f"❌ Error showing config: {e}")


if __name__ == "__main__":
    main()
