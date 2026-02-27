"""
Quick launcher for Zorro GUI.
Ensures proper configuration and launches the Streamlit app.
"""

import sys
import os
from pathlib import Path
import subprocess

def main():
    """Launch the Zorro GUI."""
    
    # Ensure we're in the correct directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Check if streamlit is installed
    try:
        import streamlit
    except ImportError:
        print("❌ Streamlit not installed!")
        print("\nInstalling required dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit>=1.28.0", "watchdog>=3.0.0"])
        print("✅ Installation complete!\n")
    
    # Launch Streamlit
    print("🎬 Launching Zorro Video Generator GUI...")
    print("=" * 60)
    print("📱 The application will open in your default web browser")
    print("🔗 URL: http://localhost:8501")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    try:
        subprocess.run([
            sys.executable, 
            "-m", 
            "streamlit", 
            "run", 
            "app.py",
            "--server.port=8501",
            "--server.headless=true",
            "--browser.gatherUsageStats=false"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down Zorro GUI...")
        print("✅ Goodbye!")

if __name__ == "__main__":
    main()
