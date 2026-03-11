#!/usr/bin/env python3
"""Download and setup FFmpeg for Windows"""

import os
import sys
import shutil
import zipfile
from pathlib import Path
import urllib.request
import subprocess

print("\n" + "="*70)
print("FFMPEG SETUP - AUTOMATIC DOWNLOAD")
print("="*70 + "\n")

# Check if already installed
try:
    result = subprocess.run(['ffmpeg', '-version'], capture_output=True, timeout=5)
    if 'ffmpeg version' in result.stdout.decode():
        print("✓ FFmpeg is already installed and accessible")
        sys.exit(0)
except:
    pass

# Setup ffmpeg directory
ffmpeg_dir = Path("C:/ffmpeg")
ffmpeg_exe = ffmpeg_dir / "bin" / "ffmpeg.exe"

if ffmpeg_exe.exists():
    print(f"✓ FFmpeg found at: {ffmpeg_exe}")
    sys.exit(0)

print("Downloading FFmpeg for Windows...\n")

# Download portable FFmpeg build from BtbN (most reliable)
url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
zip_path = Path.home() / "ffmpeg-download.zip"

try:
    print(f"URL: {url}")
    print(f"Saving to: {zip_path}\n")
    
    # Download with progress
    def download_with_progress(url, filepath):
        def report_hook(blocknum, blocksize, totalsize):
            downloaded = blocknum * blocksize
            percent = min(downloaded * 100 // totalsize, 100)
            print(f"\r[{'='*int(percent/2):<50}] {percent}%", end='', flush=True)
        
        urllib.request.urlretrieve(url, filepath, report_hook)
        print()  # New line after progress
    
    download_with_progress(url, zip_path)
    print(f"✓ Download complete ({zip_path.stat().st_size / 1024 / 1024:.1f} MB)\n")
    
except Exception as e:
    print(f"✗ Download failed: {e}")
    print("\nAlternative: Download manually from:")
    print("  https://www.gyan.dev/ffmpeg/builds/")
    print("  (recommended: ffmpeg-full.zip)")
    sys.exit(1)

# Extract
print(f"[1/3] Extracting FFmpeg...")
ffmpeg_dir.mkdir(parents=True, exist_ok=True)

try:
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Extract to temp location first
        temp_extract = Path.home() / "ffmpeg_temp"
        zip_ref.extractall(temp_extract)
        print(f"✓ Extracted\n")
        
        # Find the ffmpeg-* folder
        folders = [d for d in temp_extract.iterdir() if d.is_dir() and 'ffmpeg' in d.name]
        if not folders:
            raise Exception("Could not find ffmpeg folder in zip")
        
        source_folder = folders[0]
        
        # Copy bin folder
        print(f"[2/3] Installing to {ffmpeg_dir}...")
        src_bin = source_folder / "bin"
        dst_bin = ffmpeg_dir / "bin"
        
        if dst_bin.exists():
            shutil.rmtree(dst_bin)
        shutil.copytree(src_bin, dst_bin)
        print(f"✓ Installed\n")
        
        # Cleanup
        shutil.rmtree(temp_extract)
        zip_path.unlink()
        
except Exception as e:
    print(f"✗ Extraction failed: {e}")
    sys.exit(1)

# Add to PATH
print(f"[3/3] Configuring PATH...")
ffmpeg_bin_path = str(ffmpeg_dir / "bin")

# Check current PATH
current_path = os.environ.get('PATH', '')
if ffmpeg_bin_path not in current_path:
    # Add to current session
    os.environ['PATH'] = ffmpeg_bin_path + ";" + current_path
    print(f"✓ Added to PATH (current session)")
    
    # Also set permanently in registry (requires admin)
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Environment', 0, winreg.KEY_WRITE) as key:
            existing_path = winreg.QueryValueEx(key, 'PATH')[0]
            if ffmpeg_bin_path not in existing_path:
                new_path = ffmpeg_bin_path + ";" + existing_path
                winreg.SetValueEx(key, 'PATH', 0, winreg.REG_EXPAND_SZ, new_path)
                print(f"✓ Added to system PATH (persistent)")
    except:
        print(f"⚠ Could not add to system PATH (requires admin)")
        print(f"  Manual fix: Add '{ffmpeg_dir}\\bin' to your PATH environment variable")
else:
    print(f"✓ Already in PATH")

# Verify
print(f"\n[✓] Verifying FFmpeg...")
try:
    result = subprocess.run([str(ffmpeg_exe), '-version'], capture_output=True, text=True, timeout=5)
    if 'ffmpeg version' in result.stdout:
        version = result.stdout.split('\n')[0]
        print(f"✓ FFmpeg ready: {version}")
        print(f"✓ Location: {ffmpeg_exe}\n")
        print("="*70)
        print("FFmpeg installation complete!")
        print("="*70 + "\n")
        sys.exit(0)
except:
    pass

print("✗ FFmpeg verification failed")
sys.exit(1)
