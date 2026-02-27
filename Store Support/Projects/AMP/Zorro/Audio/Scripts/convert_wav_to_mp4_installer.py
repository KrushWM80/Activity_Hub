"""
Convert WAV to MP4 with automatic ffmpeg setup.
Includes fallback methods for systems without ffmpeg.
"""

import os
import subprocess
import sys
from pathlib import Path

PODCASTS_DIR = Path("../output/podcasts")

def check_ffmpeg():
    """Check if ffmpeg is available."""
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except:
        return False

def install_ffmpeg_instructions():
    """Provide instructions for installing ffmpeg."""
    print()
    print("=" * 70)
    print("❌ FFMPEG NOT FOUND - INSTALLATION REQUIRED")
    print("=" * 70)
    print()
    print("FFmpeg is needed to convert WAV files to MP4 format.")
    print()
    print("Option 1: Download Pre-built FFmpeg (Recommended)")
    print("-" * 70)
    print("1. Visit: https://ffmpeg.org/download.html")
    print("2. Download 'Full build' for Windows")
    print("3. Extract to: C:\\ffmpeg")
    print("4. Add to PATH:")
    print("   - Right-click 'This PC' → Properties")
    print("   - Advanced system settings → Environment Variables")
    print("   - New System Variable:")
    print("     Name: PATH")
    print("     Value: C:\\ffmpeg\\bin")
    print("   - Click OK and restart terminal")
    print()
    print("Option 2: Use Windows Package Manager")
    print("-" * 70)
    print("winget install ffmpeg")
    print("(May require admin PowerShell)")
    print()
    print("Option 3: Use Scoop Package Manager")
    print("-" * 70)
    print("scoop install ffmpeg")
    print()
    print("After installing ffmpeg, run this script again:")
    print(f"  python {sys.argv[0]}")
    print()

def convert_wav_to_mp4_ffmpeg():
    """Convert using ffmpeg (preferred method)."""
    wav_files = list(PODCASTS_DIR.glob("*.wav"))
    
    print("Converting to MP4 format using ffmpeg...")
    print("-" * 70)
    
    converted = 0
    for wav_file in wav_files:
        mp4_filename = wav_file.stem + ".mp4"
        mp4_path = PODCASTS_DIR / mp4_filename
        
        print(f"\nProcessing: {wav_file.name}")
        
        try:
            # ffmpeg command: WAV → MP4 with AAC audio
            cmd = [
                "ffmpeg",
                "-i", str(wav_file),
                "-c:a", "aac",
                "-b:a", "192k",
                "-movflags", "faststart",
                "-y",
                str(mp4_path)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0 and mp4_path.exists():
                size_mb = round(mp4_path.stat().st_size / (1024 * 1024), 2)
                print(f"  ✅ {mp4_filename} ({size_mb} MB)")
                converted += 1
            else:
                print(f"  ❌ Failed")
                print(f"     {result.stderr[:100]}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    return converted, len(wav_files)

# ============================================================================

print("=" * 70)
print("WAV ↔ MP4 CONVERTER")
print("=" * 70)
print()

# Check WAV files exist
wav_files = list(PODCASTS_DIR.glob("*.wav"))
if not wav_files:
    print(f"No WAV files found in {PODCASTS_DIR}")
    exit(1)

print(f"Found {len(wav_files)} WAV file(s)")
print()

# Check ffmpeg
if check_ffmpeg():
    print("✅ FFmpeg is available")
    print()
    converted, total = convert_wav_to_mp4_ffmpeg()
else:
    print("❌ FFmpeg not found")
    install_ffmpeg_instructions()
    exit(1)

# Summary
print()
print("=" * 70)
print(f"✅ CONVERSION COMPLETE: {converted}/{total} files converted")
print("=" * 70)
print()
print("Files in podcasts directory:")
print()

# List all audio files
for ext in [".wav", ".mp4"]:
    files = sorted(PODCASTS_DIR.glob(f"*{ext}"))
    if files:
        for file in files:
            size_mb = round(file.stat().st_size / (1024 * 1024), 2)
            format_type = "WAV" if ext == ".wav" else "MP4"
            print(f"  • {file.name}")
            print(f"    [{format_type}] {size_mb} MB")
            print()
