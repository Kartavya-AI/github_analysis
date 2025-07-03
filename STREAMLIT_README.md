# GitCrew Streamlit UI

A comprehensive web-based dashboard for viewing and interacting with GitCrew AI HR system analysis reports.

## 🌟 Features

### 📊 Interactive Dashboard
- **Executive Summary**: Key insights and recommendations
- **Developer Profile**: Comprehensive overview with metrics
- **Technical Skills**: Programming languages and competencies analysis
- **Repository Analysis**: Portfolio review with interactive charts
- **Activity Assessment**: Engagement patterns and recommendations
- **Strengths & Development**: Clear breakdown of abilities and improvement areas
- **Hiring Recommendations**: Role fit and project suitability
- **Risk Analysis**: Potential concerns and mitigation strategies
- **Action Steps**: Concrete next steps for developers and managers

### 📈 Visualizations
- **Language Distribution**: Interactive pie charts showing programming language usage
- **Repository Metrics**: Bar charts for documentation, licensing, and activity rates
- **Skill Assessment**: Visual representation of technical competencies
- **Timeline Views**: Activity patterns over time

### 🔧 Analysis Tools
- **Report Viewer**: Load and display existing JSON analysis reports
- **New Analysis**: Run GitHub analysis directly from the UI
- **Export Options**: Download reports in various formats
- **Raw Data Access**: Detailed inspection of underlying data

## 🚀 Quick Start

### Option 1: Automated Launch (Windows)
```bash
# Double-click run_streamlit.bat
# This will install dependencies and start the UI
```

### Option 2: Manual Setup
```bash
# Install dependencies
pip install streamlit plotly pandas

# Run the Streamlit app
streamlit run streamlit_app_new.py
```

### Option 3: Using Python
```bash
python run_ui.py
```

## 📋 Requirements

### Core Dependencies
- `streamlit >= 1.28.0`
- `plotly >= 5.15.0`
- `pandas >= 2.0.0`

### Optional Dependencies (for full functionality)
- GitCrew system (`crewai`, `python-dotenv`)
- GitHub analysis tools

## 🎯 Usage Guide

### Viewing Existing Reports
1. Launch the Streamlit UI
2. Select "📊 View Analysis Report" in the sidebar
3. Choose a report from the dropdown
4. Navigate through different sections using the structured layout

### Running New Analysis
1. Select "🔍 Run New Analysis" in the sidebar
2. Enter a GitHub username
3. Choose analysis type:
   - **Quick Tool Analysis**: Fast GitHub API analysis
   - **Full AI Crew Analysis**: Complete AI-powered assessment
4. Click "🚀 Start Analysis"

### Navigation
- **Sidebar**: Main navigation and report selection
- **Sections**: Organized analysis components
- **Expandable Cards**: Detailed information for repositories
- **Interactive Charts**: Hover and zoom functionality
- **Export Options**: Download and sharing capabilities

## 📊 Report Sections Explained

### 📋 Executive Summary
- **Overview**: High-level assessment of the developer
- **Key Recommendations**: Priority actions for improvement

### 👤 Developer Profile Overview
- **Basic Metrics**: Account age, repositories, followers
- **Experience Assessment**: Skill level and activity rating
- **Primary Technologies**: Main programming languages

### ⚡ Technical Skills Analysis
- **Programming Languages**: Proficiency levels and descriptions
- **Framework Knowledge**: Web development and specialized skills
- **Skill Gaps**: Areas for development and learning

### 📁 Repository Portfolio Analysis
- **Top Repositories**: Most significant projects with analysis
- **Language Distribution**: Visual breakdown of technology usage
- **Quality Metrics**: Documentation, licensing, and maintenance rates

### 📊 Activity & Engagement Assessment
- **Activity Patterns**: Commit frequency and project involvement
- **Community Engagement**: Collaboration and open-source participation
- **Improvement Recommendations**: Specific actions for better engagement

### 💪 Strengths & Development Areas
- **Current Strengths**: Proven capabilities and assets
- **Development Opportunities**: Areas for skill enhancement

### 🎯 Hiring & Project Fit Recommendations
- **Suitable Roles**: Job positions that match the profile
- **Project Types**: Ideal project characteristics
- **Team Integration**: Recommendations for successful onboarding

### ⚠️ Risk Analysis & Considerations
- **Potential Risks**: Areas of concern for hiring managers
- **Mitigation Strategies**: Ways to address identified risks

### 🚀 Actionable Next Steps
- **Developer Actions**: Personal development tasks
- **Managerial Actions**: Team lead and HR recommendations

## 🔧 Customization

### Styling
The UI uses custom CSS for enhanced visual appeal:
- Color-coded sections and metrics
- Responsive design for different screen sizes
- Professional color scheme with clear hierarchy

### Adding New Visualizations
```python
# Example: Add a new chart function
def create_custom_chart(data):
    fig = px.line(data, x='date', y='commits')
    return fig

# Use in display functions
if PLOTLY_AVAILABLE:
    fig = create_custom_chart(activity_data)
    st.plotly_chart(fig, use_container_width=True)
```

### Extending Report Sections
```python
def display_custom_section(report_data):
    st.markdown('<div class="section-header">🔥 Custom Analysis</div>', unsafe_allow_html=True)
    # Add your custom analysis here
```

## 🐛 Troubleshooting

### Common Issues

1. **"GitCrew not available" error**
   - Ensure the GitCrew system is properly installed
   - Check that you're in the correct directory
   - Verify environment variables are set

2. **"Plotly not installed" warning**
   - Install Plotly: `pip install plotly`
   - Charts will fall back to simple metrics display

3. **No reports found**
   - Check that analysis reports are in the correct directory
   - Report files should match pattern: `github_analysis_report_*.json`

4. **Port already in use**
   - Change the port: `streamlit run streamlit_app_new.py --server.port 8502`
   - Or kill the existing process

### Performance Tips
- For large reports, use the collapsible sections
- Enable caching for frequently accessed data
- Use the quick analysis for faster results

## 📁 File Structure
```
📦 GitCrew UI Files
├── 📄 streamlit_app_new.py      # Main Streamlit application
├── 📄 report_processor.py       # Enhanced visualization functions
├── 📄 run_ui.py                 # Python launcher script
├── 📄 run_streamlit.bat         # Windows batch launcher
├── 📄 requirements.txt          # Python dependencies
└── 📁 src/crew/                 # GitCrew system files
    ├── 📄 gitcrew.py           # Main GitCrew class
    ├── 📄 main.py              # CLI interface
    └── 📁 tools/               # Analysis tools
```

## 🤝 Contributing

To add new features or improve the UI:

1. Fork the repository
2. Create a feature branch
3. Add your enhancements
4. Test thoroughly with sample reports
5. Submit a pull request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt
pip install streamlit plotly

# Run in development mode
streamlit run streamlit_app_new.py --server.runOnSave true
```

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the GitCrew main documentation
3. Ensure all dependencies are properly installed
4. Verify your report files are valid JSON

## 🎉 Success!

Once running, you should see:
- ✅ GitCrew Available: Yes (if system is properly installed)
- ✅ Plotly Available: Yes (if plotly is installed)
- 📊 Interactive charts and visualizations
- 🚀 Ability to run new analyses

The dashboard provides a comprehensive view of GitHub developer analysis, making it easy for HR teams, technical recruiters, and engineering managers to assess developer profiles and make informed hiring decisions.
