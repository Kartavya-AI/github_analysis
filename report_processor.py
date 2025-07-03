#!/usr/bin/env python3
"""
GitCrew Analysis Report Processor
Helper functions for processing and visualizing GitHub analysis reports
"""

import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import streamlit as st

def create_skill_radar_chart(skills_data):
    """Create a radar chart for technical skills"""
    if not skills_data or 'programming_languages' not in skills_data:
        return None
    
    languages = skills_data['programming_languages']
    
    # Map skill levels to numeric values
    level_mapping = {
        'Beginner': 1,
        'Intermediate': 2,
        'Advanced': 3,
        'Expert': 4
    }
    
    categories = []
    values = []
    
    for lang, description in languages.items():
        categories.append(lang)
        # Extract level from description
        level = 'Beginner'  # default
        for key in level_mapping.keys():
            if key.lower() in description.lower():
                level = key
                break
        values.append(level_mapping.get(level, 1))
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Skill Level',
        line_color='rgb(32, 201, 151)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 4],
                tickvals=[1, 2, 3, 4],
                ticktext=['Beginner', 'Intermediate', 'Advanced', 'Expert']
            )),
        showlegend=True,
        title="Technical Skills Radar"
    )
    
    return fig

def create_repository_metrics_chart(coding_patterns):
    """Create a metrics chart for repository statistics"""
    if not coding_patterns:
        return None
    
    metrics = ['Documentation Rate', 'License Usage Rate', 'Activity Rate']
    values = [
        coding_patterns.get('documentation_rate', 0),
        coding_patterns.get('license_usage_rate', 0),
        coding_patterns.get('activity_rate', 0)
    ]
    
    # Create color coding based on values
    colors = []
    for value in values:
        if value >= 80:
            colors.append('green')
        elif value >= 50:
            colors.append('orange')
        else:
            colors.append('red')
    
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

def create_language_timeline_chart(languages_used):
    """Create a timeline-style chart for language usage"""
    if not languages_used:
        return None
    
    # Sort languages by usage count
    sorted_langs = sorted(languages_used.items(), key=lambda x: x[1], reverse=True)
    
    languages = [lang for lang, count in sorted_langs]
    counts = [count for lang, count in sorted_langs]
    
    fig = px.bar(
        x=counts,
        y=languages,
        orientation='h',
        title="Programming Language Usage",
        labels={'x': 'Number of Repositories', 'y': 'Programming Languages'},
        color=counts,
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(height=max(400, len(languages) * 40))
    
    return fig

def create_experience_gauge(skill_metrics):
    """Create a gauge chart for experience level"""
    if not skill_metrics or 'experience_score' not in skill_metrics:
        return None
    
    score = skill_metrics['experience_score']
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Experience Score"},
        delta = {'reference': 50},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 25], 'color': "lightgray"},
                {'range': [25, 50], 'color': "gray"},
                {'range': [50, 75], 'color': "lightblue"},
                {'range': [75, 100], 'color': "blue"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    return fig

def format_recommendations_as_tasks(recommendations):
    """Format recommendations as actionable tasks"""
    if not recommendations:
        return []
    
    formatted_tasks = []
    priority_keywords = {
        'high': ['critical', 'important', 'urgent', 'immediately'],
        'medium': ['should', 'recommended', 'improve', 'enhance'],
        'low': ['consider', 'explore', 'may', 'could']
    }
    
    for i, rec in enumerate(recommendations, 1):
        # Determine priority
        priority = 'medium'  # default
        rec_lower = rec.lower()
        for p, keywords in priority_keywords.items():
            if any(keyword in rec_lower for keyword in keywords):
                priority = p
                break
        
        formatted_tasks.append({
            'id': i,
            'task': rec,
            'priority': priority,
            'status': 'pending'
        })
    
    return formatted_tasks

def display_task_board(tasks):
    """Display recommendations as a task board"""
    if not tasks:
        return
    
    st.subheader("📋 Action Items Task Board")
    
    # Group by priority
    high_priority = [t for t in tasks if t['priority'] == 'high']
    medium_priority = [t for t in tasks if t['priority'] == 'medium']
    low_priority = [t for t in tasks if t['priority'] == 'low']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🔴 High Priority")
        for task in high_priority:
            st.markdown(f"**{task['id']}.** {task['task']}")
    
    with col2:
        st.markdown("#### 🟡 Medium Priority")
        for task in medium_priority:
            st.markdown(f"**{task['id']}.** {task['task']}")
    
    with col3:
        st.markdown("#### 🟢 Low Priority")
        for task in low_priority:
            st.markdown(f"**{task['id']}.** {task['task']}")

def generate_summary_metrics(report_data):
    """Generate key summary metrics from the report"""
    try:
        raw_data = report_data['report']['appendices']['raw_data_summary']
        profile = raw_data['user_profile']
        skills = raw_data['skill_metrics']
        
        return {
            'developer_name': profile.get('name', profile.get('username', 'Unknown')),
            'github_username': profile.get('username', ''),
            'account_age_years': round(profile.get('account_age_days', 0) / 365.25, 1),
            'total_repos': profile.get('public_repos', 0),
            'total_followers': profile.get('followers', 0),
            'experience_score': skills.get('experience_score', 0),
            'language_diversity': skills.get('language_diversity', 0),
            'community_engagement': skills.get('community_engagement', 0),
            'activity_level': report_data['report']['developer_profile_overview'].get('activity_level', 'Unknown'),
            'experience_level': report_data['report']['developer_profile_overview'].get('experience_level', 'Unknown')
        }
    except Exception as e:
        st.error(f"Error generating summary metrics: {e}")
        return {}

def export_report_summary(report_data, format='markdown'):
    """Export report summary in different formats"""
    summary = generate_summary_metrics(report_data)
    
    if format == 'markdown':
        md_content = f"""
# GitHub Developer Analysis Report

## Developer Overview
- **Name:** {summary.get('developer_name', 'N/A')}
- **GitHub:** [@{summary.get('github_username', 'N/A')}](https://github.com/{summary.get('github_username', '')})
- **Experience Level:** {summary.get('experience_level', 'N/A')}
- **Activity Level:** {summary.get('activity_level', 'N/A')}

## Key Metrics
- **Account Age:** {summary.get('account_age_years', 0)} years
- **Public Repositories:** {summary.get('total_repos', 0)}
- **Followers:** {summary.get('total_followers', 0)}
- **Experience Score:** {summary.get('experience_score', 0)}/100
- **Language Diversity:** {summary.get('language_diversity', 0)} languages
- **Community Engagement:** {summary.get('community_engagement', 0)} points

## Executive Summary
{report_data['report']['executive_summary']['overview']}

## Key Recommendations
"""
        for i, rec in enumerate(report_data['report']['executive_summary']['recommendations'], 1):
            md_content += f"{i}. {rec}\n"
        
        return md_content
    
    elif format == 'csv':
        # Create a CSV-friendly summary
        csv_data = {
            'Metric': [],
            'Value': []
        }
        
        for key, value in summary.items():
            csv_data['Metric'].append(key.replace('_', ' ').title())
            csv_data['Value'].append(value)
        
        return pd.DataFrame(csv_data)
    
    return None
