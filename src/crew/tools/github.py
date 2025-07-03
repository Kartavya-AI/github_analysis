import requests
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import Counter
from crewai.tools import BaseTool


class GitHubProfileAnalyzer(BaseTool):
    name: str = "GitHub Profile Analyzer"
    description: str = """
    Analyzes a GitHub user's profile using only public API endpoints to extract comprehensive 
    information about their coding skills, activity patterns, and repository structure. 
    Provides insights into programming languages used, contribution patterns, project complexity, 
    and overall development experience without requiring authentication.
    """
    
    def __init__(self):
        """Initialize the GitHub Profile Analyzer tool for public data only."""
        super().__init__()
        # Use instance variables instead of class attributes
        self._base_url = "https://api.github.com"
        self._headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHubProfileAnalyzer/1.0"
        }
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Any]:
        """Make a request to GitHub API with error handling and rate limiting."""
        try:
            url = f"{self._base_url}/{endpoint}"
            response = requests.get(url, headers=self._headers, params=params)
            
            if response.status_code == 403:
                print("Rate limit reached. GitHub API allows 60 requests per hour for unauthenticated requests.")
                return None
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                print(f"Resource not found: {endpoint}")
                return None
            else:
                print(f"Error fetching {endpoint}: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None
    
    def _get_user_info(self, username: str) -> Dict:
        """Get basic user information from public profile."""
        user_data = self._make_request(f"users/{username}")
        if not user_data:
            return {}
        
        return {
            "username": user_data.get("login", ""),
            "name": user_data.get("name", ""),
            "bio": user_data.get("bio", ""),
            "location": user_data.get("location", ""),
            "company": user_data.get("company", ""),
            "blog": user_data.get("blog", ""),
            "public_repos": user_data.get("public_repos", 0),
            "public_gists": user_data.get("public_gists", 0),
            "followers": user_data.get("followers", 0),
            "following": user_data.get("following", 0),
            "created_at": user_data.get("created_at", ""),
            "updated_at": user_data.get("updated_at", ""),
            "account_age_days": self._calculate_account_age(user_data.get("created_at", "")),
            "avatar_url": user_data.get("avatar_url", ""),
            "html_url": user_data.get("html_url", "")
        }
    
    def _calculate_account_age(self, created_at: str) -> int:
        """Calculate account age in days."""
        if not created_at:
            return 0
        try:
            created_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            return (datetime.now().replace(tzinfo=created_date.tzinfo) - created_date).days
        except:
            return 0
    
    def _get_repositories(self, username: str, max_repos: int = 100) -> List[Dict]:
        """Get public repositories for a user (limited to avoid rate limits)."""
        repos = []
        page = 1
        per_page = min(30, max_repos)  # Limit to avoid rate limiting
        
        while len(repos) < max_repos:
            repo_data = self._make_request(
                f"users/{username}/repos",
                params={
                    "page": page, 
                    "per_page": per_page, 
                    "sort": "updated",
                    "type": "owner"  # Only owned repositories
                }
            )
            
            if not repo_data or len(repo_data) == 0:
                break
                
            repos.extend(repo_data)
            
            if len(repo_data) < per_page:
                break
                
            page += 1
            
        return repos[:max_repos]
    
    def _analyze_repository_languages(self, username: str, repo_name: str) -> Dict:
        """Get languages used in a repository."""
        languages = self._make_request(f"repos/{username}/{repo_name}/languages")
        return languages or {}
    
    def _get_repository_stats(self, username: str, repo_name: str) -> Dict:
        """Get basic stats for a repository."""
        repo_data = self._make_request(f"repos/{username}/{repo_name}")
        if not repo_data:
            return {}
        
        # Get recent commits (limited to avoid rate limits)
        commits = self._make_request(
            f"repos/{username}/{repo_name}/commits",
            params={"per_page": 10}  # Limited to recent commits
        )
        
        return {
            "name": repo_name,
            "description": repo_data.get("description", ""),
            "language": repo_data.get("language", ""),
            "size": repo_data.get("size", 0),
            "stargazers_count": repo_data.get("stargazers_count", 0),
            "watchers_count": repo_data.get("watchers_count", 0),
            "forks_count": repo_data.get("forks_count", 0),
            "open_issues_count": repo_data.get("open_issues_count", 0),
            "created_at": repo_data.get("created_at", ""),
            "updated_at": repo_data.get("updated_at", ""),
            "pushed_at": repo_data.get("pushed_at", ""),
            "default_branch": repo_data.get("default_branch", ""),
            "has_wiki": repo_data.get("has_wiki", False),
            "has_pages": repo_data.get("has_pages", False),
            "has_issues": repo_data.get("has_issues", False),
            "archived": repo_data.get("archived", False),
            "disabled": repo_data.get("disabled", False),
            "license": repo_data.get("license", {}).get("name", "") if repo_data.get("license") else "",
            "topics": repo_data.get("topics", []),
            "recent_commits_count": len(commits) if commits else 0
        }
    
    def _analyze_coding_patterns(self, repos: List[Dict]) -> Dict:
        """Analyze coding patterns from repository data."""
        languages = Counter()
        topics = Counter()
        total_stars = 0
        total_forks = 0
        total_issues = 0
        has_documentation = 0
        has_license = 0
        active_repos = 0
        
        # Calculate activity threshold (last 6 months)
        six_months_ago = datetime.now() - timedelta(days=180)
        
        for repo in repos:
            # Count languages
            if repo.get("language"):
                languages[repo["language"]] += 1
            
            # Count topics
            topics.update(repo.get("topics", []))
            
            # Aggregate stats
            total_stars += repo.get("stargazers_count", 0)
            total_forks += repo.get("forks_count", 0)
            total_issues += repo.get("open_issues_count", 0)
            
            # Check for documentation and license
            if repo.get("has_wiki") or repo.get("has_pages"):
                has_documentation += 1
            
            if repo.get("license"):
                has_license += 1
            
            # Check activity (updated in last 6 months)
            try:
                last_push = datetime.fromisoformat(repo.get("pushed_at", "").replace('Z', '+00:00'))
                if last_push.replace(tzinfo=None) > six_months_ago:
                    active_repos += 1
            except:
                pass
        
        return {
            "languages_used": dict(languages.most_common()),
            "popular_topics": dict(topics.most_common(10)),
            "total_stars_received": total_stars,
            "total_forks_received": total_forks,
            "total_open_issues": total_issues,
            "repos_with_documentation": has_documentation,
            "repos_with_license": has_license,
            "active_repos_last_6_months": active_repos,
            "documentation_rate": round(has_documentation / len(repos) * 100, 2) if repos else 0,
            "license_usage_rate": round(has_license / len(repos) * 100, 2) if repos else 0,
            "activity_rate": round(active_repos / len(repos) * 100, 2) if repos else 0
        }
    
    def _calculate_skill_metrics(self, user_info: Dict, repos: List[Dict], coding_patterns: Dict) -> Dict:
        """Calculate skill metrics based on available data."""
        total_repos = len(repos)
        account_age_years = user_info.get("account_age_days", 0) / 365.25
        
        # Experience level estimation
        experience_score = 0
        if account_age_years > 0:
            experience_score += min(account_age_years * 10, 30)  # Max 30 points for age
        
        experience_score += min(total_repos * 2, 40)  # Max 40 points for repo count
        experience_score += min(coding_patterns.get("total_stars_received", 0), 30)  # Max 30 points for stars
        
        # Language diversity
        num_languages = len(coding_patterns.get("languages_used", {}))
        
        # Project complexity estimation
        avg_repo_size = sum(repo.get("size", 0) for repo in repos) / total_repos if repos else 0
        
        return {
            "experience_score": round(experience_score, 1),
            "language_diversity": num_languages,
            "average_repo_size_kb": round(avg_repo_size, 2),
            "repos_per_year": round(total_repos / account_age_years, 2) if account_age_years > 0 else 0,
            "community_engagement": user_info.get("followers", 0) + user_info.get("following", 0),
            "project_maintenance": coding_patterns.get("activity_rate", 0)
        }
    
    def _run(self, username: str) -> str:
        """
        Main method to analyze a GitHub user's profile.
        
        Args:
            username (str): GitHub username to analyze
            
        Returns:
            str: JSON string containing comprehensive analysis
        """
        if not username:
            return json.dumps({"error": "Username is required"}, indent=2)
        
        print(f"Analyzing GitHub profile for: {username}")
        
        # Get user information
        user_info = self._get_user_info(username)
        if not user_info:
            return json.dumps({"error": f"User '{username}' not found"}, indent=2)
        
        print(f"Found user with {user_info.get('public_repos', 0)} public repositories")
        
        # Get repositories (limited to avoid rate limits)
        repos = self._get_repositories(username, max_repos=50)
        
        # Analyze detailed repository data for top repositories
        detailed_repos = []
        for i, repo in enumerate(repos[:10]):  # Limit to top 10 to avoid rate limits
            repo_name = repo.get("name", "")
            print(f"Analyzing repository {i+1}/10: {repo_name}")
            
            repo_stats = self._get_repository_stats(username, repo_name)
            if repo_stats:
                # Get languages for this repository
                languages = self._analyze_repository_languages(username, repo_name)
                repo_stats["languages"] = languages
                detailed_repos.append(repo_stats)
        
        # Analyze coding patterns
        coding_patterns = self._analyze_coding_patterns(repos)
        
        # Calculate skill metrics
        skill_metrics = self._calculate_skill_metrics(user_info, repos, coding_patterns)
        
        # Compile comprehensive analysis
        analysis = {
            "user_profile": user_info,
            "repository_overview": {
                "total_public_repos": len(repos),
                "analyzed_repos": len(detailed_repos),
                "top_repositories": detailed_repos[:5]  # Show top 5
            },
            "coding_patterns": coding_patterns,
            "skill_metrics": skill_metrics,
            "summary": {
                "primary_languages": list(coding_patterns.get("languages_used", {}).keys())[:3],
                "specialization_areas": list(coding_patterns.get("popular_topics", {}).keys())[:5],
                "activity_level": "High" if coding_patterns.get("activity_rate", 0) > 50 else "Medium" if coding_patterns.get("activity_rate", 0) > 20 else "Low",
                "experience_level": "Senior" if skill_metrics.get("experience_score", 0) > 70 else "Mid-level" if skill_metrics.get("experience_score", 0) > 40 else "Junior",
                "community_involvement": "High" if skill_metrics.get("community_engagement", 0) > 100 else "Medium" if skill_metrics.get("community_engagement", 0) > 20 else "Low"
            },
            "analysis_metadata": {
                "analyzed_at": datetime.now().isoformat(),
                "data_source": "GitHub Public API",
                "rate_limit_considerations": "Analysis limited to public data only"
            }
        }
        
        return json.dumps(analysis, indent=2, default=str)