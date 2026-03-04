#!/usr/bin/env python3
"""
Zorro Project - Setup Verification Script
Checks if all required packages and system dependencies are installed
"""

import sys
import subprocess
from pathlib import Path

def check_python_package(package_name, import_name=None):
    """Check if a Python package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        return True, f"✓ {package_name}"
    except ImportError:
        return False, f"✗ {package_name} - NOT INSTALLED"

def check_system_tool(tool_name, command=None):
    """Check if a system tool is available"""
    if command is None:
        command = tool_name
    
    try:
        result = subprocess.run(
            [command, "--version"],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            return True, f"✓ {tool_name} found"
        else:
            return False, f"✗ {tool_name} - NOT FOUND"
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False, f"✗ {tool_name} - NOT FOUND"

def main():
    print("\n" + "="*70)
    print("ZORRO PROJECT - SETUP VERIFICATION")
    print("="*70)
    
    all_checks_passed = True
    
    # Python Packages - Core
    print("\n📦 CORE PACKAGES (Required)")
    print("-" * 70)
    core_packages = [
        ("numpy", "numpy"),
        ("pandas", "pandas"),
        ("pydantic", "pydantic"),
        ("requests", "requests"),
        ("PyYAML", "yaml"),
        ("python-dotenv", "dotenv"),
    ]
    
    for package_name, import_name in core_packages:
        passed, message = check_python_package(package_name, import_name)
        print(message)
        if not passed:
            all_checks_passed = False
    
    # Python Packages - Web UI
    print("\n🌐 WEB UI (Required)")
    print("-" * 70)
    web_packages = [
        ("streamlit", "streamlit"),
    ]
    
    for package_name, import_name in web_packages:
        passed, message = check_python_package(package_name, import_name)
        print(message)
        if not passed:
            all_checks_passed = False
    
    # Python Packages - Video Processing
    print("\n🎬 VIDEO PROCESSING (Required)")
    print("-" * 70)
    video_packages = [
        ("torch", "torch"),
        ("diffusers", "diffusers"),
        ("transformers", "transformers"),
        ("moviepy", "moviepy"),
        ("opencv-python", "cv2"),
        ("Pillow", "PIL"),
        ("imageio", "imageio"),
        ("imageio-ffmpeg", "imageio_ffmpeg"),
    ]
    
    for package_name, import_name in video_packages:
        passed, message = check_python_package(package_name, import_name)
        print(message)
        if not passed:
            all_checks_passed = False
    
    # Python Packages - Audio
    print("\n🔊 AUDIO PROCESSING (Required)")
    print("-" * 70)
    audio_packages = [
        ("pydub", "pydub"),
        ("gTTS", "gtts"),
        ("pyttsx3", "pyttsx3"),
    ]
    
    for package_name, import_name in audio_packages:
        passed, message = check_python_package(package_name, import_name)
        print(message)
        if not passed:
            all_checks_passed = False
    
    # Python Packages - Subtitles & Data
    print("\n📝 SUBTITLES & VALIDATION (Required)")
    print("-" * 70)
    subtitle_packages = [
        ("webvtt-py", "webvtt"),
        ("srt", "srt"),
        ("jsonschema", "jsonschema"),
        ("validators", "validators"),
    ]
    
    for package_name, import_name in subtitle_packages:
        passed, message = check_python_package(package_name, import_name)
        print(message)
        if not passed:
            all_checks_passed = False
    
    # Python Packages - Database
    print("\n💾 DATABASE PACKAGES (Phase 2)")
    print("-" * 70)
    db_packages = [
        ("sqlalchemy", "sqlalchemy"),
        ("psycopg2-binary", "psycopg2"),
        ("alembic", "alembic"),
        ("redis", "redis"),
    ]
    
    for package_name, import_name in db_packages:
        passed, message = check_python_package(package_name, import_name)
        print(message)
        if not passed:
            print("  (Phase 2 only - not blocking)")
    
    # Python Packages - Async
    print("\n⚙️ ASYNC PROCESSING (Phase 2)")
    print("-" * 70)
    async_packages = [
        ("celery", "celery"),
    ]
    
    for package_name, import_name in async_packages:
        passed, message = check_python_package(package_name, import_name)
        print(message)
        if not passed:
            print("  (Phase 2 only - not blocking)")
    
    # Python Packages - LLM & Security
    print("\n🔐 LLM & SECURITY PACKAGES (Required)")
    print("-" * 70)
    llm_packages = [
        ("openai", "openai"),
        ("anthropic", "anthropic"),
        ("cryptography", "cryptography"),
        ("bleach", "bleach"),
    ]
    
    for package_name, import_name in llm_packages:
        passed, message = check_python_package(package_name, import_name)
        print(message)
        if not passed:
            all_checks_passed = False
    
    # Python Packages - Logging
    print("\n📊 LOGGING & MONITORING (Required)")
    print("-" * 70)
    logging_packages = [
        ("structlog", "structlog"),
        ("python-json-logger", "pythonjsonlogger"),
        ("tenacity", "tenacity"),
    ]
    
    for package_name, import_name in logging_packages:
        passed, message = check_python_package(package_name, import_name)
        print(message)
        if not passed:
            all_checks_passed = False
    
    # System Tools
    print("\n⚙️ SYSTEM TOOLS")
    print("-" * 70)
    
    ffmpeg_passed, ffmpeg_msg = check_system_tool("FFmpeg", "ffmpeg")
    print(ffmpeg_msg)
    if not ffmpeg_passed:
        print("\n⚠️  FFmpeg not found! To install on Windows:")
        print("   Option 1: choco install ffmpeg")
        print("   Option 2: Download from https://ffmpeg.org/download.html")
        all_checks_passed = False
    
    # Summary
    print("\n" + "="*70)
    if all_checks_passed:
        print("✅ ALL CHECKS PASSED - System is ready for Zorro!")
        print("="*70)
        print("\nNext Steps:")
        print("1. Configure .env file with API keys:")
        print("   - Copy .env.example to .env")
        print("   - Add WALMART_SSO_TOKEN from Retina GenAI team")
        print("   - Set WALMART_SSL_VERIFY=false")
        print("\n2. Start the application:")
        print("   streamlit run app.py")
        print("\n3. Open browser to http://localhost:8501")
        print("="*70 + "\n")
        return 0
    else:
        print("❌ SOME CHECKS FAILED - Please install missing packages")
        print("="*70)
        print("\nTo install missing packages:")
        print("  pip install -r requirements.txt")
        print("\nFor FFmpeg:")
        print("  choco install ffmpeg")
        print("="*70 + "\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
