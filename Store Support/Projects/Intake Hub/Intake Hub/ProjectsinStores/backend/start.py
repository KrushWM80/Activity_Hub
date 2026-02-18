#!/usr/bin/env python3
"""
Startup script for Projects in Stores Dashboard
Checks dependencies and starts the server
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.10+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"❌ Python 3.10+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required = ['fastapi', 'uvicorn', 'pydantic']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("\nInstall with: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages installed")
    return True

def check_env_file():
    """Check if .env file exists"""
    if Path('.env').exists():
        print("✅ Configuration file found (.env)")
        return True
    else:
        print("⚠️  No .env file found - using mock data")
        print("   To use real data: copy .env.example to .env")
        return True

def start_server():
    """Start the FastAPI server"""
    print("\n" + "=" * 50)
    print("Starting Projects in Stores Dashboard Server")
    print("=" * 50)
    print("\nServer will be available at:")
    print("  API: http://localhost:8000")
    print("  Docs: http://localhost:8000/docs")
    print("\nTo stop the server, press Ctrl+C")
    print("=" * 50 + "\n")
    
    try:
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n\nServer stopped.")

def main():
    """Main startup routine"""
    print("Projects in Stores Dashboard - Startup Check\n")
    
    # Change to backend directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Run checks
    if not check_python_version():
        sys.exit(1)
    
    if not check_dependencies():
        sys.exit(1)
    
    check_env_file()
    
    # Start server
    print("\n✅ All checks passed!\n")
    start_server()

if __name__ == "__main__":
    main()
