#!/usr/bin/env python3
"""
GitCrew Streamlit UI - Interactive GitHub Developer Analysis Dashboard
"""

import streamlit as st
import json
import pandas as pd
from pathlib import Path
import sys
import os
from datetime import datetime

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Try to import dependencies
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("Plotly not installed. Some visualizations will not be available.")

# Try to import GitCrew
try:
    from src.crew.gitcrew import GitCrew
    GITCREW_AVAILABLE = True
except ImportError:
    GITCREW_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="GitCrew - AI HR System",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2e7d32;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #2e7d32;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #28a745;
    }
    .warning-box {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
    }
    .info-box {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #17a2b8;
    }
</style>
""", unsafe_allow_html=True)

def load_analysis_report(file_path):
    """Load analysis report from JSON file, handling markdown code blocks"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Parse markdown-wrapped JSON
        clean_content = parse_markdown_json(content)
        
        # Parse the JSON content
        data = json.loads(clean_content)
        
        # Validate report structure
        is_valid, message = validate_report_structure(data)
        if not is_valid:
            st.warning(f"Report structure issue: {message}")
            st.info("Attempting to load anyway...")
        
        return data
        
    except json.JSONDecodeError as e:
        st.error(f"Error parsing JSON: {e}")
        
        # Show debugging information
        with st.expander("🔍 Debug Information"):
            st.write("**Error details:**", str(e))
            st.write("**File path:**", str(file_path))
            
            # Show raw content preview
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    raw_content = file.read()
                    st.write("**Raw content preview (first 1000 chars):**")
                    st.code(raw_content[:1000] + ("..." if len(raw_content) > 1000 else ""))
                    
                    # Show after markdown parsing
                    parsed_content = parse_markdown_json(raw_content)
                    st.write("**After markdown parsing (first 500 chars):**")
                    st.code(parsed_content[:500] + ("..." if len(parsed_content) > 500 else ""))
            except Exception as debug_e:
                st.write(f"Could not read file for debugging: {debug_e}")
        
        return None
        
    except Exception as e:
        st.error(f"Error loading report: {e}")
        return None

def parse_markdown_json(content):
    """Parse JSON content that might be wrapped in markdown code blocks"""
    content = content.strip()
    
    # Handle different markdown code block formats
    patterns = [
        ('```json\n', '\n```'),  # Standard JSON code block
        ('```\n', '\n```'),      # Generic code block
        ('````json\n', '\n````'), # Quad backticks
        ('````\n', '\n````'),     # Quad backticks generic
    ]
    
    for start_pattern, end_pattern in patterns:
        if content.startswith(start_pattern) and content.endswith(end_pattern):
            content = content[len(start_pattern):-len(end_pattern)].strip()
            break
    
    return content

def validate_report_structure(data):
    """Validate that the loaded data has the expected report structure"""
    if not isinstance(data, dict):
        return False, "Report data must be a dictionary"
    
    # Check for new format (skill_assessment_report)
    if 'skill_assessment_report' in data:
        report = data['skill_assessment_report']
        required_sections = [
            'executive_summary',
            'developer_profile_overview',
            'technical_skills_analysis'
        ]
        report_type = 'skill_assessment'
    # Check for old format (report)
    elif 'report' in data:
        report = data['report']
        required_sections = [
            'executive_summary',
            'developer_profile_overview',
            'technical_skills_analysis'
        ]
        report_type = 'standard'
    else:
        return False, "Missing 'skill_assessment_report' or 'report' key in data"
    
    for section in required_sections:
        if section not in report:
            return False, f"Missing required section: {section}"
    
    return True, f"Report structure is valid (type: {report_type})"

def create_language_pie_chart(languages_data):
    """Create a pie chart for programming languages"""
    if not PLOTLY_AVAILABLE or not languages_data:
        return None
    
    fig = px.pie(
        values=list(languages_data.values()),
        names=list(languages_data.keys()),
        title="Programming Languages Distribution",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def create_metrics_bar_chart(metrics_data):
    """Create a bar chart for repository metrics"""
    if not PLOTLY_AVAILABLE:
        return None
    
    metrics = ['Documentation Rate', 'License Usage Rate', 'Activity Rate']
    values = [
        metrics_data.get('documentation_rate', 0),
        metrics_data.get('license_usage_rate', 0),
        metrics_data.get('activity_rate', 0)
    ]
    
    colors = ['green' if v >= 70 else 'orange' if v >= 40 else 'red' for v in values]
    
    fig = go.Figure(data=[
        go.Bar(
            x=metrics,
            y=values,
            marker_color=colors,
            text=[f'{v}%' for v in values],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Repository Quality Metrics",
        xaxis_title="Metrics",
        yaxis_title="Percentage (%)",
        yaxis=dict(range=[0, 100])
    )
    
    return fig

def display_executive_summary(report_data):
    """Display executive summary section"""
    st.markdown('<div class="section-header">📋 Executive Summary</div>', unsafe_allow_html=True)
    
    try:
        report, report_type = get_report_data(report_data)
        if not report:
            st.error("Could not extract report data")
            return
        
        exec_summary = report.get('executive_summary', {})
        
        # Display overview
        overview = exec_summary.get('overview', 'No overview available')
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.write(overview)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display recommendations
        recommendations = exec_summary.get('recommendations', [])
        if isinstance(recommendations, str):
            # New format has recommendations as a string
            st.subheader("🎯 Recommendations")
            st.write(recommendations)
        elif isinstance(recommendations, list):
            # Old format has recommendations as a list
            st.subheader("🎯 Key Recommendations")
            for i, recommendation in enumerate(recommendations, 1):
                st.write(f"{i}. {recommendation}")
        else:
            st.info("No recommendations available")
        
        # Display strengths and weaknesses if available (new format)
        col1, col2 = st.columns(2)
        with col1:
            strengths = exec_summary.get('summary_of_strengths')
            if strengths:
                st.markdown(f'<div class="success-box"><strong>Strengths:</strong> {strengths}</div>', unsafe_allow_html=True)
        
        with col2:
            weaknesses = exec_summary.get('summary_of_weaknesses')
            if weaknesses:
                st.markdown(f'<div class="warning-box"><strong>Areas for Improvement:</strong> {weaknesses}</div>', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error displaying executive summary: {e}")

def display_developer_profile(report_data):
    """Display developer profile overview"""
    st.markdown('<div class="section-header">👤 Developer Profile Overview</div>', unsafe_allow_html=True)
    
    try:
        report, report_type = get_report_data(report_data)
        if not report:
            st.error("Could not extract report data")
            return
        
        profile = report.get('developer_profile_overview', {})
        
        # Handle different profile formats
        if report_type == 'skill_assessment':
            # New format with separate personal_information and github_metrics
            personal_info = profile.get('personal_information', {})
            github_metrics = profile.get('github_metrics', {})
            
            # Display personal information
            st.subheader("👨‍💼 Personal Information")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Username", personal_info.get('username', 'N/A'))
                st.metric("Name", personal_info.get('name', 'N/A'))
            
            with col2:
                st.metric("Location", personal_info.get('location', 'N/A'))
                st.metric("Company", personal_info.get('company', 'N/A'))
            
            with col3:
                account_age = personal_info.get('account_age_days', 0)
                account_years = round(account_age / 365.25, 1) if account_age else 0
                st.metric("Account Age", f"{account_years} years")
                st.metric("Profile URL", "GitHub" if personal_info.get('profile_url') else 'N/A')
            
            with col4:
                if personal_info.get('avatar_url'):
                    st.image(personal_info['avatar_url'], width=100, caption="Avatar")
            
            # Display GitHub metrics
            st.subheader("📊 GitHub Metrics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Public Repos", github_metrics.get('public_repos', 'N/A'))
                st.metric("Public Gists", github_metrics.get('public_gists', 'N/A'))
            
            with col2:
                st.metric("Followers", github_metrics.get('followers', 'N/A'))
                st.metric("Following", github_metrics.get('following', 'N/A'))
            
            with col3:
                created_at = github_metrics.get('created_at', '')
                if created_at:
                    created_year = created_at[:4]
                    st.metric("Joined", created_year)
                
                updated_at = github_metrics.get('updated_at', '')
                if updated_at:
                    updated_year = updated_at[:4]
                    st.metric("Last Updated", updated_year)
            
            # Display bio if available
            bio = personal_info.get('bio')
            if bio:
                st.subheader("📝 Bio")
                st.markdown(f'<div class="info-box">{bio}</div>', unsafe_allow_html=True)
            
            # Display summary
            summary = profile.get('summary')
            if summary:
                st.subheader("📋 Profile Summary")
                st.write(summary)
        
        else:
            # Old format - keep existing logic
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Account Age", f"{profile.get('account_age_days', 'N/A')} days")
                st.metric("Public Repos", profile.get('public_repos', 'N/A'))
            
            with col2:
                st.metric("Followers", profile.get('followers', 'N/A'))
                st.metric("Following", profile.get('following', 'N/A'))
            
            with col3:
                st.metric("Experience Level", profile.get('experience_level', 'N/A'))
                st.metric("Activity Level", profile.get('activity_level', 'N/A'))
            
            with col4:
                st.metric("Community Involvement", profile.get('community_involvement', 'N/A'))
            
            st.subheader("💻 Primary Languages")
            languages_text = ", ".join(profile.get('primary_languages', []))
            st.markdown(f'<div class="success-box"><strong>Languages:</strong> {languages_text}</div>', unsafe_allow_html=True)
            
            st.subheader("📝 Profile Summary")
            st.write(profile.get('summary', 'No summary available'))
            
    except Exception as e:
        st.error(f"Error displaying developer profile: {e}")

def display_technical_skills(report_data):
    """Display technical skills analysis"""
    st.markdown('<div class="section-header">⚡ Technical Skills Analysis</div>', unsafe_allow_html=True)
    
    try:
        report, report_type = get_report_data(report_data)
        if not report:
            st.error("Could not extract report data")
            return
        
        skills = report.get('technical_skills_analysis', {})
        
        # Programming Languages
        st.subheader("💻 Programming Languages")
        prog_languages = skills.get('programming_languages', {})
        
        if prog_languages:
            if report_type == 'skill_assessment':
                # New format with detailed proficiency info
                lang_data = []
                for lang, details in prog_languages.items():
                    if isinstance(details, dict):
                        proficiency = details.get('proficiency', 'Unknown')
                        evidence = details.get('evidence', 'No evidence provided')
                        lang_details = details.get('details', 'No additional details')
                        lang_data.append({
                            "Language": lang,
                            "Proficiency": proficiency,
                            "Evidence": evidence,
                            "Details": lang_details
                        })
                    else:
                        # Fallback for simple string format
                        lang_data.append({
                            "Language": lang,
                            "Proficiency": "Unknown",
                            "Evidence": str(details),
                            "Details": ""
                        })
                
                # Display as expandable cards
                for lang_info in lang_data:
                    with st.expander(f"🔧 {lang_info['Language']} - {lang_info['Proficiency']}"):
                        st.write(f"**Evidence:** {lang_info['Evidence']}")
                        if lang_info['Details']:
                            st.write(f"**Details:** {lang_info['Details']}")
            else:
                # Old format
                lang_data = []
                for lang, description in prog_languages.items():
                    level = description.split(' - ')[0] if ' - ' in description else "Unknown"
                    lang_data.append({"Language": lang, "Level": level, "Description": description})
                
                if lang_data:
                    df_langs = pd.DataFrame(lang_data)
                    st.dataframe(df_langs, use_container_width=True)
        
        # Technologies and Frameworks (new format)
        if report_type == 'skill_assessment':
            tech_frameworks = skills.get('technologies_and_frameworks', {})
            if tech_frameworks:
                st.subheader("🛠️ Technologies & Frameworks")
                for tech, details in tech_frameworks.items():
                    if isinstance(details, dict):
                        proficiency = details.get('proficiency', 'Unknown')
                        evidence = details.get('evidence', 'No evidence provided')
                        tech_details = details.get('details', 'No additional details')
                        
                        with st.expander(f"⚙️ {tech} - {proficiency}"):
                            st.write(f"**Evidence:** {evidence}")
                            if tech_details:
                                st.write(f"**Details:** {tech_details}")
            
            # Language Summary
            lang_summary = skills.get('language_summary')
            if lang_summary:
                st.subheader("📊 Language Summary")
                st.markdown(f'<div class="info-box">{lang_summary}</div>', unsafe_allow_html=True)
        
        # Skill Gaps
        skill_gaps = skills.get('skill_gaps', [])
        if skill_gaps:
            st.subheader("🎯 Areas for Development")
            for gap in skill_gaps:
                st.write(f"• {gap}")
        
    except Exception as e:
        st.error(f"Error displaying technical skills: {e}")

def display_repository_analysis(report_data):
    """Display repository portfolio analysis"""
    st.markdown('<div class="section-header">📁 Repository Portfolio Analysis</div>', unsafe_allow_html=True)
    
    try:
        # Try to get repository data from either format
        repo_data = None
        if 'report' in report_data and 'repository_portfolio_review' in report_data['report']:
            repo_data = report_data['report']['repository_portfolio_review']
        elif 'skill_assessment_report' in report_data and 'repository_portfolio_review' in report_data['skill_assessment_report']:
            repo_data = report_data['skill_assessment_report']['repository_portfolio_review']
        
        if not repo_data:
            st.info("Repository portfolio analysis not available in this report format")
            return
        
        # Top Repositories
        st.subheader("🌟 Top Repositories")
        top_repos = repo_data.get('top_repositories', [])
        if top_repos:
            for repo in top_repos:
                with st.expander(f"📦 {repo.get('name', 'Unknown')} ({repo.get('language', 'N/A')})"):
                    st.write(f"**Description:** {repo.get('description', 'No description')}")
                    st.write(f"**Recent Commits:** {repo.get('recent_commits_count', 'N/A')}")
                    st.write(f"**Purpose:** {repo.get('purpose', 'N/A')}")
                    st.write(f"**Key Aspects:** {repo.get('key_aspects', 'N/A')}")
        else:
            st.info("No repository information available")
        
        # Coding Patterns Visualization
        coding_patterns = repo_data.get('coding_patterns', {})
        languages = coding_patterns.get('languages_used', {})
        
        if languages and PLOTLY_AVAILABLE:
            st.subheader("📊 Language Usage Distribution")
            fig = create_language_pie_chart(languages)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        # Repository Metrics
        st.subheader("📈 Repository Metrics")
        if PLOTLY_AVAILABLE:
            fig = create_metrics_bar_chart(coding_patterns)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Documentation Rate", f"{coding_patterns.get('documentation_rate', 0)}%")
            with col2:
                st.metric("License Usage Rate", f"{coding_patterns.get('license_usage_rate', 0)}%")
            with col3:
                st.metric("Activity Rate", f"{coding_patterns.get('activity_rate', 0)}%")
                
    except KeyError as e:
        st.error(f"Missing section in report: {e}")
    except Exception as e:
        st.error(f"Error displaying repository analysis: {e}")

def display_activity_engagement(report_data):
    """Display activity and engagement assessment"""
    st.markdown('<div class="section-header">📊 Activity & Engagement Assessment</div>', unsafe_allow_html=True)
    
    try:
        # Try to get activity data from either format
        activity = None
        if 'report' in report_data and 'activity_and_engagement_assessment' in report_data['report']:
            activity = report_data['report']['activity_and_engagement_assessment']
        elif 'skill_assessment_report' in report_data and 'activity_and_engagement_assessment' in report_data['skill_assessment_report']:
            activity = report_data['skill_assessment_report']['activity_and_engagement_assessment']
        
        if not activity:
            st.info("Activity and engagement assessment not available in this report format")
            return
        
        st.subheader("📈 Activity Metrics")
        activity_metrics = activity.get('activity_metrics', {})
        if activity_metrics:
            for metric, value in activity_metrics.items():
                st.write(f"**{metric.replace('_', ' ').title()}:** {value}")
        else:
            st.info("No activity metrics available")
        
        st.subheader("🤝 Engagement Patterns")
        engagement_patterns = activity.get('engagement_patterns', {})
        if engagement_patterns:
            for pattern, description in engagement_patterns.items():
                st.write(f"**{pattern.replace('_', ' ').title()}:** {description}")
        else:
            st.info("No engagement patterns available")
        
        st.subheader("💡 Recommendations")
        recommendations = activity.get('recommendations', [])
        if recommendations:
            for rec in recommendations:
                st.write(f"• {rec}")
        else:
            st.info("No recommendations available")
            
    except KeyError as e:
        st.error(f"Missing section in report: {e}")
    except Exception as e:
        st.error(f"Error displaying activity engagement: {e}")

def display_activity_engagement_new(report_data):
    """Display activity and engagement assessment for new format"""
    st.markdown('<div class="section-header">📊 Activity & Engagement Assessment</div>', unsafe_allow_html=True)
    
    try:
        report, report_type = get_report_data(report_data)
        if not report:
            return
        
        activity = report.get('activity_and_engagement_assessment', {})
        
        # Metrics section
        metrics = activity.get('metrics', {})
        
        # Coding Patterns
        coding_patterns = metrics.get('coding_patterns', {})
        if coding_patterns:
            st.subheader("💻 Coding Patterns")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Documentation Rate", f"{coding_patterns.get('documentation_rate', 0)}%")
                st.metric("Total Stars", coding_patterns.get('total_stars_received', 0))
            
            with col2:
                st.metric("License Usage Rate", f"{coding_patterns.get('license_usage_rate', 0)}%")
                st.metric("Total Forks", coding_patterns.get('total_forks_received', 0))
            
            with col3:
                st.metric("Activity Rate", f"{coding_patterns.get('activity_rate', 0)}%")
                st.metric("Active Repos (6m)", coding_patterns.get('active_repos_last_6_months', 0))
            
            # Language usage chart
            languages_used = coding_patterns.get('languages_used', {})
            if languages_used and PLOTLY_AVAILABLE:
                fig = create_language_pie_chart(languages_used)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
        
        # Skill Metrics
        skill_metrics = metrics.get('skill_metrics', {})
        if skill_metrics:
            st.subheader("📈 Skill Metrics")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Experience Score", f"{skill_metrics.get('experience_score', 0)}/100")
                st.metric("Language Diversity", skill_metrics.get('language_diversity', 0))
            
            with col2:
                st.metric("Community Engagement", skill_metrics.get('community_engagement', 0))
                st.metric("Repos per Year", round(skill_metrics.get('repos_per_year', 0), 1))
            
            with col3:
                st.metric("Project Maintenance", f"{skill_metrics.get('project_maintenance', 0)}%")
                avg_size = skill_metrics.get('average_repo_size_kb', 0)
                st.metric("Avg Repo Size", f"{round(avg_size, 1)} KB")
        
        # Activity Summary
        activity_summary = activity.get('activity_summary')
        if activity_summary:
            st.subheader("📋 Activity Summary")
            st.write(activity_summary)
        
        # Engagement Summary
        engagement_summary = activity.get('engagement_summary')
        if engagement_summary:
            st.subheader("🤝 Engagement Summary")
            st.write(engagement_summary)
        
    except Exception as e:
        st.error(f"Error displaying activity assessment: {e}")

def display_strengths_development(report_data):
    """Display strengths and development areas"""
    st.markdown('<div class="section-header">💪 Strengths & Development Areas</div>', unsafe_allow_html=True)
    
    try:
        report, report_type = get_report_data(report_data)
        if not report:
            st.error("Could not extract report data")
            return
        
        strengths_dev = report.get('strengths_and_development_areas', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("✅ Strengths")
            strengths = strengths_dev.get('strengths', [])
            for strength in strengths:
                st.markdown(f'<div class="success-box">• {strength}</div>', unsafe_allow_html=True)
        
        with col2:
            st.subheader("🎯 Areas for Improvement")
            improvements = strengths_dev.get('areas_for_improvement', [])
            for area in improvements:
                st.markdown(f'<div class="warning-box">• {area}</div>', unsafe_allow_html=True)
        
        # Recommendations
        recommendations = strengths_dev.get('recommendations', [])
        if recommendations:
            st.subheader("💡 Recommendations")
            for rec in recommendations:
                st.write(f"• {rec}")
        
        # Summary
        summary = strengths_dev.get('summary')
        if summary:
            st.subheader("📋 Summary")
            st.markdown(f'<div class="info-box">{summary}</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error displaying strengths and development: {e}")

def display_strengths_development_new(report_data):
    """Display strengths and development areas for new format"""
    st.markdown('<div class="section-header">💪 Strengths & Development Areas</div>', unsafe_allow_html=True)
    
    try:
        report, report_type = get_report_data(report_data)
        if not report:
            return
        
        strengths_dev = report.get('strengths_and_development_areas', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("✅ Strengths")
            strengths = strengths_dev.get('strengths', [])
            for strength in strengths:
                st.markdown(f'<div class="success-box">• {strength}</div>', unsafe_allow_html=True)
        
        with col2:
            st.subheader("🎯 Areas for Improvement")
            improvements = strengths_dev.get('areas_for_improvement', [])
            for area in improvements:
                st.markdown(f'<div class="warning-box">• {area}</div>', unsafe_allow_html=True)
        
        # Recommendations
        recommendations = strengths_dev.get('recommendations', [])
        if recommendations:
            st.subheader("💡 Recommendations")
            for rec in recommendations:
                st.write(f"• {rec}")
        
        # Summary
        summary = strengths_dev.get('summary')
        if summary:
            st.subheader("📋 Summary")
            st.markdown(f'<div class="info-box">{summary}</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error displaying strengths and development: {e}")

def display_hiring_recommendations(report_data):
    """Display hiring and project fit recommendations"""
    st.markdown('<div class="section-header">🎯 Hiring & Project Fit Recommendations</div>', unsafe_allow_html=True)
    
    try:
        # Try to get hiring data from either format
        hiring = None
        if 'report' in report_data and 'hiring_and_project_fit_recommendations' in report_data['report']:
            hiring = report_data['report']['hiring_and_project_fit_recommendations']
        elif 'skill_assessment_report' in report_data and 'hiring_and_project_fit_recommendations' in report_data['skill_assessment_report']:
            hiring = report_data['skill_assessment_report']['hiring_and_project_fit_recommendations']
        
        if not hiring:
            st.info("Hiring recommendations not available in this report format")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💼 Suitable Roles")
            suitable_roles = hiring.get('suitable_roles', [])
            if suitable_roles:
                for role in suitable_roles:
                    st.write(f"• {role}")
            else:
                st.info("No suitable roles specified")
        
        with col2:
            st.subheader("🚀 Suitable Projects")
            suitable_projects = hiring.get('suitable_projects', [])
            if suitable_projects:
                for project in suitable_projects:
                    st.write(f"• {project}")
            else:
                st.info("No suitable projects specified")
        
        st.subheader("📋 Hiring Recommendations")
        recommendations = hiring.get('recommendations', [])
        if recommendations:
            for rec in recommendations:
                st.write(f"• {rec}")
        else:
            st.info("No hiring recommendations available")
            
    except KeyError as e:
        st.error(f"Missing section in report: {e}")
    except Exception as e:
        st.error(f"Error displaying hiring recommendations: {e}")

def display_hiring_recommendations_new(report_data):
    """Display hiring and project fit recommendations for new format"""
    st.markdown('<div class="section-header">🎯 Hiring & Project Fit Recommendations</div>', unsafe_allow_html=True)
    
    try:
        report, report_type = get_report_data(report_data)
        if not report:
            return
        
        hiring = report.get('hiring_and_project_fit_recommendations', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💼 Suitable Roles")
            roles = hiring.get('roles', [])
            for role in roles:
                st.write(f"• {role}")
        
        with col2:
            st.subheader("🚀 Suitable Project Types")
            projects = hiring.get('project_types', [])
            for project in projects:
                st.write(f"• {project}")
        
        # Considerations
        considerations = hiring.get('considerations')
        if considerations:
            st.subheader("🤔 Considerations")
            st.markdown(f'<div class="warning-box">{considerations}</div>', unsafe_allow_html=True)
        
        # Summary
        summary = hiring.get('summary')
        if summary:
            st.subheader("📋 Summary")
            st.markdown(f'<div class="info-box">{summary}</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error displaying hiring recommendations: {e}")

def display_risk_analysis(report_data):
    """Display risk analysis and considerations"""
    st.markdown('<div class="section-header">⚠️ Risk Analysis & Considerations</div>', unsafe_allow_html=True)
    
    try:
        # Try to get risk data from either format
        risk = None
        if 'report' in report_data and 'risk_analysis_and_considerations' in report_data['report']:
            risk = report_data['report']['risk_analysis_and_considerations']
        elif 'skill_assessment_report' in report_data and 'risk_analysis_and_considerations' in report_data['skill_assessment_report']:
            risk = report_data['skill_assessment_report']['risk_analysis_and_considerations']
        
        if not risk:
            st.info("Risk analysis not available in this report format")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🚨 Identified Risks")
            risks = risk.get('risks', [])
            if risks:
                for risk_item in risks:
                    st.markdown(f'<div class="warning-box">• {risk_item}</div>', unsafe_allow_html=True)
            else:
                st.info("No risks identified")
        
        with col2:
            st.subheader("🛡️ Mitigation Strategies")
            strategies = risk.get('mitigation_strategies', [])
            if strategies:
                for strategy in strategies:
                    st.markdown(f'<div class="info-box">• {strategy}</div>', unsafe_allow_html=True)
            else:
                st.info("No mitigation strategies provided")
                
    except KeyError as e:
        st.error(f"Missing section in report: {e}")
    except Exception as e:
        st.error(f"Error displaying risk analysis: {e}")

def display_risk_analysis_new(report_data):
    """Display risk analysis for new format"""
    st.markdown('<div class="section-header">⚠️ Risk Analysis & Considerations</div>', unsafe_allow_html=True)
    
    try:
        report, report_type = get_report_data(report_data)
        if not report:
            return
        
        risk = report.get('risk_analysis_and_considerations', {})
        
        # Code Quality Assessment
        code_quality = risk.get('code_quality_and_best_practices_adherence', {})
        if code_quality:
            st.subheader("🔍 Code Quality & Best Practices")
            for aspect, description in code_quality.items():
                if aspect not in ['risks', 'mitigations', 'summary']:
                    st.write(f"**{aspect.replace('_', ' ').title()}:** {description}")
        
        # Collaboration Assessment
        collaboration = risk.get('collaboration_and_communication_skills_assessment', {})
        if collaboration:
            st.subheader("🤝 Collaboration & Communication")
            for aspect, description in collaboration.items():
                if aspect not in ['risks', 'mitigations', 'summary']:
                    st.write(f"**{aspect.replace('_', ' ').title()}:** {description}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🚨 Identified Risks")
            risks = risk.get('risks', [])
            for risk_item in risks:
                st.markdown(f'<div class="warning-box">• {risk_item}</div>', unsafe_allow_html=True)
        
        with col2:
            st.subheader("🛡️ Mitigation Strategies")
            mitigations = risk.get('mitigations', [])
            for strategy in mitigations:
                st.markdown(f'<div class="info-box">• {strategy}</div>', unsafe_allow_html=True)
        
        # Summary
        summary = risk.get('summary')
        if summary:
            st.subheader("📋 Summary")
            st.markdown(f'<div class="info-box">{summary}</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error displaying risk analysis: {e}")

def display_action_steps(report_data):
    """Display actionable next steps"""
    st.markdown('<div class="section-header">🚀 Actionable Next Steps</div>', unsafe_allow_html=True)
    
    actions = report_data['report']['actionable_next_steps']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👨‍💻 Developer Actions")
        for action in actions.get('developer_actions', []):
            st.write(f"• {action}")
    
    with col2:
        st.subheader("👔 Managerial Actions")
        for action in actions.get('managerial_actions', []):
            st.write(f"• {action}")

def display_actionable_steps_new(report_data):
    """Display actionable next steps for new format"""
    st.markdown('<div class="section-header">🚀 Actionable Next Steps</div>', unsafe_allow_html=True)
    
    try:
        report, report_type = get_report_data(report_data)
        if not report:
            return
        
        actions = report.get('actionable_next_steps', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👨‍💻 Developer Actions")
            dev_actions = actions.get('developer', [])
            for action in dev_actions:
                st.write(f"• {action}")
        
        with col2:
            st.subheader("👔 Hiring Manager Actions")
            mgr_actions = actions.get('hiring_manager', [])
            for action in mgr_actions:
                st.write(f"• {action}")
        
        # Summary
        summary = actions.get('summary')
        if summary:
            st.subheader("📋 Summary")
            st.markdown(f'<div class="info-box">{summary}</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error displaying actionable steps: {e}")

def display_experience_classification(report_data):
    """Display experience level classification"""
    st.markdown('<div class="section-header">🎓 Experience Level Classification</div>', unsafe_allow_html=True)
    
    try:
        report, report_type = get_report_data(report_data)
        if not report:
            return
        
        exp_class = report.get('experience_level_classification', {})
        
        if exp_class:
            level = exp_class.get('level', 'Unknown')
            evidence = exp_class.get('evidence', 'No evidence provided')
            reasoning = exp_class.get('reasoning', 'No reasoning provided')
            
            st.metric("Experience Level", level)
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📊 Evidence")
                st.write(evidence)
            
            with col2:
                st.subheader("🤔 Reasoning")
                st.write(reasoning)
        
    except Exception as e:
        st.error(f"Error displaying experience classification: {e}")

def display_specialization_areas(report_data):
    """Display specialization areas and domain expertise"""
    st.markdown('<div class="section-header">🎯 Specialization Areas</div>', unsafe_allow_html=True)
    
    try:
        report, report_type = get_report_data(report_data)
        if not report:
            return
        
        specialization = report.get('specialization_areas_and_domain_expertise', {})
        
        if specialization:
            areas = specialization.get('areas', [])
            details = specialization.get('details', '')
            
            if areas:
                st.subheader("🏆 Areas of Expertise")
                for area in areas:
                    st.write(f"• {area}")
            
            if details:
                st.subheader("📋 Details")
                st.write(details)
        
    except Exception as e:
        st.error(f"Error displaying specialization areas: {e}")

def run_new_analysis():
    """Run new GitHub analysis"""
    st.markdown('<div class="section-header">🔍 Run New Analysis</div>', unsafe_allow_html=True)
    
    if not GITCREW_AVAILABLE:
        st.error("GitCrew is not available. Please ensure the GitCrew module is properly installed.")
        return
    
    username = st.text_input("Enter GitHub Username", placeholder="e.g., octocat")
    
    analysis_type = st.selectbox(
        "Select Analysis Type",
        ["Quick Tool Analysis", "Full AI Crew Analysis"]
    )
    
    if st.button("🚀 Start Analysis"):
        if username:
            try:
                with st.spinner(f"Analyzing GitHub user: {username}..."):
                    git_crew = GitCrew()
                    
                    if analysis_type == "Quick Tool Analysis":
                        result = git_crew.github_analyzer._run(username)
                        st.subheader("📊 Quick Analysis Result")
                        st.json(json.loads(result))
                    else:
                        inputs = {"github_username": username}
                        result = git_crew.crew().kickoff(inputs=inputs)
                        st.subheader("🤖 Full AI Crew Analysis Result")
                        st.write(result)
                        
            except Exception as e:
                st.error(f"Analysis failed: {e}")
        else:
            st.warning("Please enter a GitHub username")

def test_report_parsing():
    """Test function to verify report parsing works correctly"""
    st.markdown("### 🧪 Test Report Parsing")
    
    # Sample markdown-wrapped JSON for testing
    test_content = '''```json
{
  "report": {
    "executive_summary": {
      "overview": "Test overview",
      "recommendations": ["Test recommendation 1", "Test recommendation 2"]
    }
  }
}
```'''
    
    st.write("**Test markdown content:**")
    st.code(test_content)
    
    try:
        parsed = parse_markdown_json(test_content)
        st.write("**Parsed content:**")
        st.code(parsed)
        
        data = json.loads(parsed)
        st.write("**JSON object:**")
        st.json(data)
        
        is_valid, message = validate_report_structure(data)
        st.write(f"**Validation result:** {is_valid} - {message}")
        
    except Exception as e:
        st.error(f"Test failed: {e}")

def upload_and_view_report():
    """Allow users to upload and view their own report files"""
    st.markdown('<div class="section-header">📤 Upload Report File</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a report file",
        type=['json', 'txt'],
        help="Upload a JSON report file (can be markdown-wrapped)"
    )
    
    if uploaded_file is not None:
        try:
            # Read the uploaded file
            content = uploaded_file.read().decode('utf-8')
            
            # Show file info
            st.write(f"**File name:** {uploaded_file.name}")
            st.write(f"**File size:** {len(content)} characters")
            
            # Parse the content
            clean_content = parse_markdown_json(content)
            data = json.loads(clean_content)
            
            # Validate structure
            is_valid, message = validate_report_structure(data)
            if is_valid:
                st.success("✅ Report uploaded and validated successfully!")
                
                # Display the report
                st.markdown("---")
                display_executive_summary({'report': data['report']})
                display_developer_profile({'report': data['report']})
                display_technical_skills({'report': data['report']})
                
            else:
                st.warning(f"⚠️ Validation warning: {message}")
                st.info("Displaying available sections...")
                
                # Try to display what we can
                if 'report' in data:
                    st.json(data['report'])
                else:
                    st.json(data)
            
        except json.JSONDecodeError as e:
            st.error(f"❌ Error parsing JSON: {e}")
            
            with st.expander("🔍 Debug Information"):
                st.code(content[:1000] + ("..." if len(content) > 1000 else ""))
                
        except Exception as e:
            st.error(f"❌ Error processing file: {e}")

def get_report_data(data):
    """Extract report data regardless of format (new or old)"""
    if 'skill_assessment_report' in data:
        return data['skill_assessment_report'], 'skill_assessment'
    elif 'report' in data:
        return data['report'], 'standard'
    else:
        return None, 'unknown'

def get_nested_value(data, path, default=None):
    """Safely get nested dictionary values using dot notation"""
    keys = path.split('.')
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<div class="main-header">🚀 GitCrew - AI HR System</div>', unsafe_allow_html=True)
    st.markdown("### GitHub Developer Analysis Dashboard")
    
    # Sidebar
    st.sidebar.title("📋 Navigation")
    
    # Check for existing reports
    report_files = list(Path(".").glob("**/github_analysis_report_*.json"))
    
    if report_files:
        st.sidebar.subheader("📁 Existing Reports")
        selected_report = st.sidebar.selectbox(
            "Select a report to view:",
            ["None"] + [f.name for f in report_files]
        )
    else:
        selected_report = "None"
    
    page = st.sidebar.radio(
        "Choose Action:",
        ["📊 View Analysis Report", "� Upload Report", "�🔍 Run New Analysis", "🧪 Test Parser"]
    )
    
    if page == "📊 View Analysis Report":
        if selected_report != "None":
            report_path = next(f for f in report_files if f.name == selected_report)
            report_data = load_analysis_report(report_path)
            
            if report_data:
                # Validate report structure
                is_valid, validation_message = validate_report_structure(report_data)
                if not is_valid:
                    st.error(f"Report structure is invalid: {validation_message}")
                else:
                    # Display sections
                    display_executive_summary(report_data)
                    display_developer_profile(report_data)
                    display_technical_skills(report_data)
                    display_repository_analysis(report_data)
                    display_activity_engagement(report_data)
                    display_strengths_development(report_data)
                    display_hiring_recommendations(report_data)
                    display_risk_analysis(report_data)
                    display_action_steps(report_data)
                    
                    # Export options
                    st.markdown("---")
                    st.subheader("📤 Export Options")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("📄 Download as JSON"):
                            st.download_button(
                                label="Download JSON Report",
                                data=json.dumps(report_data, indent=2),
                                file_name=f"report_{selected_report.replace('.json', '')}.json",
                                mime="application/json"
                            )
                    
                    with col2:
                        if st.button("📋 Copy Summary"):
                            summary_text = f"GitHub Analysis Summary for {report_data['report']['developer_profile_overview'].get('name', 'Unknown')}"
                            st.text_area("Summary (copy this text):", summary_text, height=100)
                    
                    # Raw data in expander
                    with st.expander("🔍 View Raw Data"):
                        st.json(report_data['report']['appendices']['raw_data_summary'])
        else:
            st.info("Please select a report from the sidebar or run a new analysis.")
    
    elif page == "� Upload Report":
        upload_and_view_report()
    
    elif page == "�🔍 Run New Analysis":
        run_new_analysis()
    
    elif page == "🧪 Test Parser":
        test_report_parsing()
    
    # Footer
    st.markdown("---")
    st.markdown("### ℹ️ About GitCrew")
    st.write("""
    GitCrew is an AI-powered HR system that analyzes GitHub developer profiles to provide comprehensive 
    insights for recruitment and team building. It uses CrewAI to orchestrate multiple AI agents for 
    data collection, skill assessment, technical profiling, and report generation.
    """)
    
    # System status
    with st.expander("🔧 System Status"):
        st.write(f"**GitCrew Available:** {'✅ Yes' if GITCREW_AVAILABLE else '❌ No'}")
        st.write(f"**Plotly Available:** {'✅ Yes' if PLOTLY_AVAILABLE else '❌ No'}")
        st.write(f"**Reports Found:** {len(report_files) if report_files else 0}")

if __name__ == "__main__":
    main()
