from pydantic import BaseModel, Field, HttpUrl
from typing import List, Dict, Optional, Union
from datetime import datetime
from enum import Enum


class ExperienceLevel(str, Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    EXPERT = "Expert"


class ActivityLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class SkillLevel(str, Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    PROFICIENT = "Proficient"
    ADVANCED = "Advanced"
    EXPERT = "Expert"


class ExecutiveSummary(BaseModel):
    overview: str = Field(..., description="High-level overview of the developer's profile")
    recommendations: List[str] = Field(..., description="Key recommendations for improvement")


class DeveloperProfileOverview(BaseModel):
    github_profile: HttpUrl = Field(..., description="GitHub profile URL")
    name: str = Field(..., description="Developer's name")
    account_age_days: int = Field(..., description="Age of GitHub account in days")
    followers: int = Field(..., description="Number of followers")
    following: int = Field(..., description="Number of accounts being followed")
    public_repos: int = Field(..., description="Number of public repositories")
    primary_languages: List[str] = Field(..., description="Primary programming languages")
    experience_level: ExperienceLevel = Field(..., description="Overall experience level")
    activity_level: ActivityLevel = Field(..., description="Activity level on GitHub")
    community_involvement: ActivityLevel = Field(..., description="Level of community engagement")
    summary: str = Field(..., description="Summary of the developer's profile")


class TechnicalSkillsAnalysis(BaseModel):
    programming_languages: Dict[str, str] = Field(..., description="Programming languages and skill levels")
    frameworks_and_libraries: Dict[str, str] = Field(..., description="Frameworks and libraries expertise")
    tools_and_technologies: Dict[str, str] = Field(..., description="Tools and technologies proficiency")
    skill_gaps: List[str] = Field(..., description="Identified skill gaps")


class Repository(BaseModel):
    name: str = Field(..., description="Repository name")
    description: str = Field(..., description="Repository description")
    language: Optional[str] = Field(None, description="Primary programming language")
    recent_commits_count: int = Field(..., description="Number of recent commits")
    purpose: str = Field(..., description="Purpose of the repository")
    key_aspects: str = Field(..., description="Key aspects and observations")


class CodingPatterns(BaseModel):
    languages_used: Dict[str, int] = Field(..., description="Languages used and their frequency")
    documentation_rate: float = Field(..., description="Percentage of repositories with documentation")
    license_usage_rate: float = Field(..., description="Percentage of repositories with licenses")
    activity_rate: float = Field(..., description="Activity rate percentage")


class RepositoryPortfolioReview(BaseModel):
    top_repositories: List[Repository] = Field(..., description="Top repositories analysis")
    coding_patterns: CodingPatterns = Field(..., description="Coding patterns analysis")
    repository_patterns: List[str] = Field(..., description="Observed repository patterns")


class ActivityMetrics(BaseModel):
    recent_commits_count: str = Field(..., description="Recent commits activity description")
    open_issues_count: str = Field(..., description="Open issues description")
    pull_requests_count: str = Field(..., description="Pull requests activity")
    code_reviews_count: str = Field(..., description="Code reviews activity")


class EngagementPatterns(BaseModel):
    community_interaction: str = Field(..., description="Community interaction level and description")
    contribution_frequency: str = Field(..., description="Contribution frequency description")


class ActivityAndEngagementAssessment(BaseModel):
    activity_metrics: ActivityMetrics = Field(..., description="Activity metrics analysis")
    engagement_patterns: EngagementPatterns = Field(..., description="Engagement patterns analysis")
    recommendations: List[str] = Field(..., description="Recommendations for improvement")


class StrengthsAndDevelopmentAreas(BaseModel):
    strengths: List[str] = Field(..., description="Identified strengths")
    development_areas: List[str] = Field(..., description="Areas for development")


class HiringAndProjectFitRecommendations(BaseModel):
    suitable_roles: List[str] = Field(..., description="Suitable job roles")
    suitable_projects: List[str] = Field(..., description="Suitable project types")
    recommendations: List[str] = Field(..., description="Hiring and project fit recommendations")


class RiskAnalysisAndConsiderations(BaseModel):
    risks: List[str] = Field(..., description="Identified risks")
    mitigation_strategies: List[str] = Field(..., description="Risk mitigation strategies")


class ActionableNextSteps(BaseModel):
    developer_actions: List[str] = Field(..., description="Actions for the developer to take")
    managerial_actions: List[str] = Field(..., description="Actions for managers/team leads")


class UserProfile(BaseModel):
    username: str = Field(..., description="GitHub username")
    name: Optional[str] = Field(None, description="User's real name")
    bio: Optional[str] = Field(None, description="User's bio")
    location: Optional[str] = Field(None, description="User's location")
    company: Optional[str] = Field(None, description="User's company")
    blog: Optional[str] = Field(None, description="User's blog URL")
    public_repos: int = Field(..., description="Number of public repositories")
    public_gists: int = Field(..., description="Number of public gists")
    followers: int = Field(..., description="Number of followers")
    following: int = Field(..., description="Number of accounts being followed")
    created_at: datetime = Field(..., description="Account creation date")
    updated_at: datetime = Field(..., description="Last update date")
    account_age_days: int = Field(..., description="Account age in days")
    avatar_url: HttpUrl = Field(..., description="Avatar URL")
    html_url: HttpUrl = Field(..., description="Profile URL")


class RepositoryOverview(BaseModel):
    total_public_repos: int = Field(..., description="Total number of public repositories")
    analyzed_repos: int = Field(..., description="Number of repositories analyzed")
    top_repositories: List[Dict[str, Union[str, int, None]]] = Field(..., description="Top repositories data")


class SkillMetrics(BaseModel):
    experience_score: float = Field(..., description="Overall experience score")
    language_diversity: int = Field(..., description="Number of different languages used")
    average_repo_size_kb: float = Field(..., description="Average repository size in KB")
    repos_per_year: float = Field(..., description="Repositories created per year")
    community_engagement: int = Field(..., description="Community engagement score")
    project_maintenance: float = Field(..., description="Project maintenance score")


class RawDataSummary(BaseModel):
    user_profile: UserProfile = Field(..., description="Raw user profile data")
    repository_overview: RepositoryOverview = Field(..., description="Repository overview data")
    coding_patterns: CodingPatterns = Field(..., description="Coding patterns data")
    skill_metrics: SkillMetrics = Field(..., description="Calculated skill metrics")


class Appendices(BaseModel):
    raw_data_summary: RawDataSummary = Field(..., description="Raw data summary")
    rate_limit_considerations: str = Field(..., description="Rate limit considerations")


class GitHubDeveloperAnalysisReport(BaseModel):
    """
    Complete GitHub Developer Analysis Report model for CrewAI integration.
    
    This model structures the entire analysis report with proper validation
    and type hints for seamless integration with CrewAI workflows.
    """
    
    executive_summary: ExecutiveSummary = Field(..., description="Executive summary of the analysis")
    developer_profile_overview: DeveloperProfileOverview = Field(..., description="Developer profile overview")
    technical_skills_analysis: TechnicalSkillsAnalysis = Field(..., description="Technical skills analysis")
    repository_portfolio_review: RepositoryPortfolioReview = Field(..., description="Repository portfolio review")
    activity_and_engagement_assessment: ActivityAndEngagementAssessment = Field(..., description="Activity and engagement assessment")
    strengths_and_development_areas: StrengthsAndDevelopmentAreas = Field(..., description="Strengths and development areas")
    hiring_and_project_fit_recommendations: HiringAndProjectFitRecommendations = Field(..., description="Hiring and project fit recommendations")
    risk_analysis_and_considerations: RiskAnalysisAndConsiderations = Field(..., description="Risk analysis and considerations")
    actionable_next_steps: ActionableNextSteps = Field(..., description="Actionable next steps")
    appendices: Appendices = Field(..., description="Appendices with raw data")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
        schema_extra = {
            "example": {
                "executive_summary": {
                    "overview": "Mid-level developer with strong TypeScript skills...",
                    "recommendations": ["Focus on contributing to open-source projects..."]
                },
                "developer_profile_overview": {
                    "github_profile": "https://github.com/wpsadi",
                    "name": "Aditya",
                    "account_age_days": 962,
                    "followers": 16,
                    "following": 19,
                    "public_repos": 77,
                    "primary_languages": ["TypeScript", "JavaScript", "HTML"],
                    "experience_level": "Intermediate",
                    "activity_level": "Low",
                    "community_involvement": "Medium",
                    "summary": "Solid understanding of web development principles..."
                }
            }
        }


# Wrapper model for the complete report
class ReportWrapper(BaseModel):
    """
    Wrapper model that matches the exact structure of your JSON data.
    """
    report: GitHubDeveloperAnalysisReport = Field(..., description="The complete GitHub developer analysis report")


# Usage example for CrewAI integration
class CrewAITask(BaseModel):
    """
    Example task model for CrewAI integration
    """
    task_id: str = Field(..., description="Unique task identifier")
    github_username: str = Field(..., description="GitHub username to analyze")
    analysis_depth: str = Field(default="comprehensive", description="Analysis depth level")
    output_format: str = Field(default="json", description="Output format")
    
    def create_analysis_prompt(self) -> str:
        """Generate prompt for CrewAI agent"""
        return f"""
        Analyze the GitHub profile for user '{self.github_username}' and provide a comprehensive 
        developer analysis report. The output should conform to the GitHubDeveloperAnalysisReport 
        Pydantic model structure with the following sections:
        
        1. Executive Summary with overview and recommendations
        2. Developer Profile Overview with basic stats and assessment
        3. Technical Skills Analysis with language proficiency and skill gaps
        4. Repository Portfolio Review with top repositories and coding patterns
        5. Activity and Engagement Assessment 
        6. Strengths and Development Areas
        7. Hiring and Project Fit Recommendations
        8. Risk Analysis and Considerations
        9. Actionable Next Steps
        10. Appendices with raw data summary
        
        Ensure all fields are properly populated and follow the enum constraints where applicable.
        """


# Additional utility models for specific use cases
class SkillAssessment(BaseModel):
    """Simplified skill assessment model for quick evaluations"""
    language: str = Field(..., description="Programming language")
    level: SkillLevel = Field(..., description="Skill level")
    projects_count: int = Field(..., description="Number of projects using this language")
    experience_months: Optional[int] = Field(None, description="Estimated experience in months")


class DeveloperSummary(BaseModel):
    """Condensed developer summary for quick reviews"""
    name: str = Field(..., description="Developer name")
    github_username: str = Field(..., description="GitHub username")
    experience_level: ExperienceLevel = Field(..., description="Experience level")
    primary_skills: List[str] = Field(..., description="Primary technical skills")
    strengths: List[str] = Field(..., description="Key strengths")
    recommended_roles: List[str] = Field(..., description="Recommended job roles")
    hire_recommendation: str = Field(..., description="Overall hiring recommendation")
    confidence_score: float = Field(..., ge=0, le=100, description="Confidence score (0-100)")