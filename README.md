# GitHub Analysis Tools for CrewAI

A comprehensive set of GitHub API tools designed for CrewAI that enables intelligent analysis of GitHub repositories, trending projects, and comparative studies.

## 🚀 Features

### Core Capabilities
- **Repository Analysis**: Comprehensive analysis of any GitHub repository
- **Trending Research**: Discover trending repositories across different languages and timeframes
- **Comparative Analysis**: Compare multiple repositories with detailed metrics
- **Language Analysis**: Detailed breakdown of programming languages used
- **Commit Pattern Analysis**: Analyze commit history and development patterns
- **Community Health**: Assess contributor activity and project governance
- **Code Quality Metrics**: Evaluate project quality and maintainability

### Advanced Features
- **Multi-Repository Comparison**: Compare multiple projects side-by-side
- **Trend Identification**: Spot emerging technologies and popular frameworks
- **Activity Scoring**: Quantify project activity and health
- **Quality Recommendations**: Get actionable insights for improvement
- **CrewAI Integration**: Ready-to-use agents for automated analysis

## 📋 Prerequisites

1. **Python 3.8+** (recommended: Python 3.13)
2. **GitHub Personal Access Token** (for API access)
3. **CrewAI** (for AI agent functionality)

## 🛠️ Installation

1. **Clone or download the project**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your GitHub token:**
   - Create a `.env` file in the project root
   - Add your GitHub token:
     ```
     GITHUB_TOKEN=your_github_token_here
     ```
   - Get a token at: https://github.com/settings/tokens

## 🔧 Quick Start

### Individual Tools Usage

```python
from src.crew.tools.github import GitHubAnalyzerTool, GitHubTrendingTool

# Initialize tools
github_analyzer = GitHubAnalyzerTool()
github_trending = GitHubTrendingTool()

# Analyze a repository
result = github_analyzer._execute("microsoft/vscode", "full")

# Get trending repositories
trending = github_trending._execute("python", "weekly", 10)
```

### GitCrew Class Usage

```python
from src.crew.gitcrew import GitCrew

# Initialize GitCrew
git_crew = GitCrew()

# Quick repository stats
stats = git_crew.quick_repo_stats("facebook/react")

# Comprehensive analysis with CrewAI agents
analysis = git_crew.analyze_repository("microsoft/vscode")

# Compare multiple repositories
comparison = git_crew.compare_repositories([
    "facebook/react", 
    "vuejs/vue", 
    "angular/angular"
])

# Research trending repositories
trends = git_crew.research_trending_repos(["python", "javascript"])
```

### CrewAI Agents Integration

```python
from crewai import Agent, Task, Crew
from src.crew.tools.github import GitHubAnalyzerTool

# Create a specialized agent
github_analyst = Agent(
    role='GitHub Repository Analyst',
    goal='Analyze repositories and provide insights',
    backstory='Expert in software development and repository analysis',
    tools=[GitHubAnalyzerTool()],
    verbose=True
)

# Create analysis task
task = Task(
    description="Analyze the 'microsoft/vscode' repository",
    agent=github_analyst,
    expected_output="Comprehensive analysis report"
)

# Execute with CrewAI
crew = Crew(agents=[github_analyst], tasks=[task])
result = crew.kickoff()
```

## 📊 Analysis Types

### 1. Repository Analysis (`analyze_repository`)
- **Basic Info**: Stars, forks, description, creation date
- **Languages**: Programming languages with percentages
- **Commits**: Recent activity, patterns, and statistics
- **Contributors**: Top contributors and activity distribution
- **Issues & PRs**: Open/closed counts and recent activity
- **Code Quality**: Quality indicators and recommendations

### 2. Trending Analysis (`research_trending_repos`)
- **Language-specific**: Trending repos by programming language
- **Time-based**: Daily, weekly, or monthly trends
- **Emerging Tech**: Identification of new technologies
- **Popularity Metrics**: Stars, forks, and growth rates

### 3. Comparative Analysis (`compare_repositories`)
- **Side-by-side**: Direct comparison of multiple repositories
- **Metrics Matrix**: Comprehensive comparison table
- **Strengths/Weaknesses**: Detailed analysis of each project
- **Recommendations**: Which project to choose for different use cases

## 🎯 Use Cases

### For Developers
- **Technology Selection**: Choose between competing frameworks
- **Learning Opportunities**: Find trending projects to study
- **Contribution**: Identify projects that need help
- **Architecture**: Learn from successful project structures

### For Teams
- **Due Diligence**: Evaluate open-source dependencies
- **Competitive Analysis**: Understand competitor projects
- **Technology Adoption**: Make informed technology choices
- **Project Health**: Monitor project sustainability

### For Organizations
- **Vendor Assessment**: Evaluate open-source solutions
- **Risk Management**: Assess project longevity and support
- **Innovation Tracking**: Stay ahead of technology trends
- **Investment Decisions**: Identify promising projects

## 📈 Example Outputs

### Repository Analysis
```json
{
  "repository_info": {
    "name": "vscode",
    "stars": 150000,
    "forks": 25000,
    "primary_language": "TypeScript"
  },
  "languages": {
    "TypeScript": {"percentage": 85.2},
    "JavaScript": {"percentage": 10.1}
  },
  "commits": {
    "total_commits": 95000,
    "recent_commits_30_days": 342
  },
  "quality_score": 95.5
}
```

### Trending Analysis
```json
{
  "repositories": [
    {
      "name": "awesome-ai-tool",
      "stars": 5000,
      "language": "Python",
      "growth_rate": "500% this week"
    }
  ]
}
```

## 🔍 API Reference

### GitHubAnalyzerTool Methods

- `_execute(repo_name, analysis_type)`: Main analysis method
- `analyze_multiple_repos(repo_names)`: Compare multiple repositories
- `_analyze_commits(repo)`: Detailed commit analysis
- `_analyze_languages(repo)`: Language breakdown
- `_analyze_contributors(repo)`: Contributor analysis
- `_analyze_code_quality(repo)`: Quality assessment

### GitHubTrendingTool Methods

- `_execute(language, timeframe, limit)`: Get trending repositories
- Parameters:
  - `language`: Programming language filter
  - `timeframe`: "daily", "weekly", "monthly"
  - `limit`: Number of repositories to return

### GitCrew Methods

- `analyze_repository(repo_name)`: Full repository analysis with AI agents
- `research_trending_repos(languages, timeframe)`: Trending research with AI
- `compare_repositories(repo_names, focus)`: AI-powered comparison
- `comprehensive_analysis(repo_names, languages)`: Complete analysis suite
- `quick_repo_stats(repo_name)`: Fast statistics retrieval

## 🚦 Rate Limiting

GitHub API has rate limits:
- **Authenticated**: 5,000 requests per hour
- **Unauthenticated**: 60 requests per hour

The tools implement smart caching and batching to minimize API calls.

## 🔒 Security

- Never commit your GitHub token to version control
- Use environment variables or `.env` files
- Consider using GitHub Apps for production use
- Rotate tokens regularly

## 🧪 Testing

Run the demo to test functionality:

```bash
python demo.py
```

Run tests:
```bash
pytest tests/
```

## 📚 Documentation

### Configuration Options

```python
# Custom configuration
github_analyzer = GitHubAnalyzerTool(
    github_token="your_token_here"
)

# Environment variables
GITHUB_TOKEN=your_token
GITHUB_API_BASE_URL=https://api.github.com
MAX_REQUESTS_PER_HOUR=5000
```

### Error Handling

The tools provide comprehensive error handling:
- API rate limiting
- Repository not found
- Network issues
- Authentication problems

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **CrewAI** for the AI agent framework
- **PyGithub** for GitHub API integration
- **GitHub** for providing the comprehensive API

## 📞 Support

For issues and questions:
1. Check the documentation
2. Run the demo script
3. Check GitHub issues
4. Create a new issue with details

---

**Happy analyzing! 🚀**
