from gitcrew import GitCrew
from dotenv import load_dotenv

def main():
    """Main function for GitCrew"""
    load_dotenv()
    git_crew = GitCrew()
    print("🚀 GitCrew AI HR System - GitHub Developer Analysis")
    print("=" * 60)

    inputs = {
        "github_username": "wpsadi"
    }
    print("🔍 Analyzing GitHub profile...")

    # Get the crew from GitCrew and then call kickoff
    crew = git_crew.crew()
    result = crew.kickoff(inputs=inputs)
    
    print("✅ Analysis complete!")
    print("📊 Analysis Result:")
    print(result)

if __name__ == "__main__":
    main()