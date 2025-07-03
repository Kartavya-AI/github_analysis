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
    
    if 'report' not in data:
        return False, "Missing 'report' key in data"
    
    report = data['report']
    required_sections = [
        'executive_summary',
        'developer_profile_overview',
        'technical_skills_analysis'
    ]
    
    for section in required_sections:
        if section not in report:
            return False, f"Missing required section: {section}"
    
    return True, "Report structure is valid"

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
        exec_summary = report_data['report']['executive_summary']
        
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.write(exec_summary.get('overview', 'No overview available'))
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.subheader("🎯 Key Recommendations")
        recommendations = exec_summary.get('recommendations', [])
        if recommendations:
            for i, recommendation in enumerate(recommendations, 1):
                st.write(f"{i}. {recommendation}")
        else:
            st.info("No recommendations available")
            
    except KeyError as e:
        st.error(f"Missing section in report: {e}")
    except Exception as e:
        st.error(f"Error displaying executive summary: {e}")

def display_developer_profile(report_data):
    """Display developer profile overview"""
    st.markdown('<div class="section-header">👤 Developer Profile Overview</div>', unsafe_allow_html=True)
    
    profile = report_data['report']['developer_profile_overview']
    
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

def display_technical_skills(report_data):
    """Display technical skills analysis"""
    st.markdown('<div class="section-header">⚡ Technical Skills Analysis</div>', unsafe_allow_html=True)
    
    skills = report_data['report']['technical_skills_analysis']
    
    # Programming Languages
    st.subheader("💻 Programming Languages")
    lang_data = []
    for lang, description in skills.get('programming_languages', {}).items():
        level = description.split(' - ')[0] if ' - ' in description else "Unknown"
        lang_data.append({"Language": lang, "Level": level, "Description": description})
    
    if lang_data:
        df_langs = pd.DataFrame(lang_data)
        st.dataframe(df_langs, use_container_width=True)
    
    # Skill Gaps
    st.subheader("🎯 Areas for Development")
    for gap in skills.get('skill_gaps', []):
        st.write(f"• {gap}")

def display_repository_analysis(report_data):
    """Display repository portfolio analysis"""
    st.markdown('<div class="section-header">📁 Repository Portfolio Analysis</div>', unsafe_allow_html=True)
    
    repo_data = report_data['report']['repository_portfolio_review']
    
    # Top Repositories
    st.subheader("🌟 Top Repositories")
    for repo in repo_data.get('top_repositories', []):
        with st.expander(f"📦 {repo.get('name', 'Unknown')} ({repo.get('language', 'N/A')})"):
            st.write(f"**Description:** {repo.get('description', 'No description')}")
            st.write(f"**Recent Commits:** {repo.get('recent_commits_count', 'N/A')}")
            st.write(f"**Purpose:** {repo.get('purpose', 'N/A')}")
            st.write(f"**Key Aspects:** {repo.get('key_aspects', 'N/A')}")
    
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

def display_activity_engagement(report_data):
    """Display activity and engagement assessment"""
    st.markdown('<div class="section-header">📊 Activity & Engagement Assessment</div>', unsafe_allow_html=True)
    
    activity = report_data['report']['activity_and_engagement_assessment']
    
    st.subheader("📈 Activity Metrics")
    for metric, value in activity.get('activity_metrics', {}).items():
        st.write(f"**{metric.replace('_', ' ').title()}:** {value}")
    
    st.subheader("🤝 Engagement Patterns")
    for pattern, description in activity.get('engagement_patterns', {}).items():
        st.write(f"**{pattern.replace('_', ' ').title()}:** {description}")
    
    st.subheader("💡 Recommendations")
    for rec in activity.get('recommendations', []):
        st.write(f"• {rec}")

def display_strengths_development(report_data):
    """Display strengths and development areas"""
    st.markdown('<div class="section-header">💪 Strengths & Development Areas</div>', unsafe_allow_html=True)
    
    strengths_dev = report_data['report']['strengths_and_development_areas']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ Strengths")
        for strength in strengths_dev.get('strengths', []):
            st.markdown(f'<div class="success-box">• {strength}</div>', unsafe_allow_html=True)
    
    with col2:
        st.subheader("🎯 Development Areas")
        for area in strengths_dev.get('development_areas', []):
            st.markdown(f'<div class="warning-box">• {area}</div>', unsafe_allow_html=True)

def display_hiring_recommendations(report_data):
    """Display hiring and project fit recommendations"""
    st.markdown('<div class="section-header">🎯 Hiring & Project Fit Recommendations</div>', unsafe_allow_html=True)
    
    hiring = report_data['report']['hiring_and_project_fit_recommendations']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💼 Suitable Roles")
        for role in hiring.get('suitable_roles', []):
            st.write(f"• {role}")
    
    with col2:
        st.subheader("🚀 Suitable Projects")
        for project in hiring.get('suitable_projects', []):
            st.write(f"• {project}")
    
    st.subheader("📋 Hiring Recommendations")
    for rec in hiring.get('recommendations', []):
        st.write(f"• {rec}")

def display_risk_analysis(report_data):
    """Display risk analysis and considerations"""
    st.markdown('<div class="section-header">⚠️ Risk Analysis & Considerations</div>', unsafe_allow_html=True)
    
    risk = report_data['report']['risk_analysis_and_considerations']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚨 Identified Risks")
        for risk_item in risk.get('risks', []):
            st.markdown(f'<div class="warning-box">• {risk_item}</div>', unsafe_allow_html=True)
    
    with col2:
        st.subheader("🛡️ Mitigation Strategies")
        for strategy in risk.get('mitigation_strategies', []):
            st.markdown(f'<div class="info-box">• {strategy}</div>', unsafe_allow_html=True)

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
