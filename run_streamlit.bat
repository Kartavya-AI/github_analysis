@echo off
echo 🚀 GitCrew Streamlit UI Launcher
echo ================================

echo 📦 Installing dependencies...
pip install streamlit plotly pandas

echo 🌐 Starting Streamlit UI...
echo Access the dashboard at: http://localhost:8501
echo Press Ctrl+C to stop the server

streamlit run streamlit_app_new.py --server.address localhost --server.port 8501 --browser.gatherUsageStats false

pause
