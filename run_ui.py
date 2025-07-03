#!/usr/bin/env python3
"""
Run GitCrew Streamlit UI
"""

import subprocess
import sys
import os

def main():
    """Run the Streamlit application"""
    try:
        print("🚀 Starting GitCrew Streamlit UI...")
        print("📊 Access the dashboard at: http://localhost:8501")
        print("🔄 Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.address", "localhost",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 GitCrew UI stopped by user")
    except Exception as e:
        print(f"❌ Error running Streamlit UI: {e}")
        print("\n🔍 Troubleshooting:")
        print("1. Make sure streamlit is installed: pip install streamlit")
        print("2. Make sure you're in the correct directory")
        print("3. Check if port 8501 is available")

if __name__ == "__main__":
    main()
