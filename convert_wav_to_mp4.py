"""
Convert WAV audio files to MP4 format.
Supports both Windows system installation and programmatic conversion.
"""

import os
import subprocess
from pathlib import Path

PODCASTS_DIR = Path("Store Support/Projects/AMP/Zorro/output/podcasts")

print("=" * 70)
print("WAV TO MP4 CONVERSION")
print("=" * 70)
print()

# Check for ffmpeg
print("Checking for ffmpeg...")
try:
    result = subprocess.run(
        ["ffmpeg", "-version"],
        capture_output=True,
        timeout=5
    )
    if result.returncode == 0:
        print("✅ ffmpeg found and ready")
        ffmpeg_available = True
    else:
        print("❌ ffmpeg not responding correctly")
        ffmpeg_available = False
except Exception as e:
    print(f"❌ ffmpeg not found: {e}")
    print()
    print("Install ffmpeg using one of these methods:")
    print()
    print("1️⃣  Using Chocolatey (recommended):")
    print("    choco install ffmpeg")
    print()
    print("2️⃣  Using Windows Package Manager:")
    print("    winget install ffmpeg")
    print()
    print("3️⃣  Manual download:")
    print("    https://ffmpeg.org/download.html")
    print()
    ffmpeg_available = False

if not ffmpeg_available:
    print()
    print("After installing ffmpeg, run this script again.")
    exit(1)

print()

# Find WAV files
wav_files = list(PODCASTS_DIR.glob("*.wav"))
print(f"Found {len(wav_files)} WAV file(s)")
print()

if not wav_files:
    print("No WAV files found in podcasts directory")
    exit(1)

# Convert each WAV to MP4
print("Converting to MP4 format...")
print("-" * 70)

converted = 0
for wav_file in wav_files:
    # Create MP4 filename
    mp4_filename = wav_file.stem + ".mp4"
    mp4_path = PODCASTS_DIR / mp4_filename
    
    print(f"\nConverting: {wav_file.name}")
    
    try:
        # Use ffmpeg to convert WAV to MP4
        # MP4 container with AAC audio codec
        cmd = [
            "ffmpeg",
            "-i", str(wav_file),           # Input WAV
            "-c:a", "aac",                  # Audio codec: AAC
            "-b:a", "192k",                 # Bitrate: 192 kbps
            "-y",                           # Overwrite output
            str(mp4_path)
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes per file
        )
        
        if result.returncode == 0 and mp4_path.exists():
            size_mb = round(mp4_path.stat().st_size / (1024 * 1024), 2)
            print(f"  ✅ Created: {mp4_filename} ({size_mb} MB)")
            converted += 1
        else:
            print(f"  ❌ Conversion failed")
            if result.stderr:
                print(f"     Error: {result.stderr[:100]}")
    
    except subprocess.TimeoutExpired:
        print(f"  ❌ Conversion timed out")
    except Exception as e:
        print(f"  ❌ Error: {e}")

print()
print("=" * 70)
print(f"CONVERSION COMPLETE: {converted}/{len(wav_files)} files successfully converted")
print("=" * 70)
print()

# Show results
print("Files in podcasts directory:")
print()
for file in sorted(PODCASTS_DIR.glob("*")):
    if file.suffix in [".wav", ".mp4"]:
        size_mb = round(file.stat().st_size / (1024 * 1024), 2)
        format_type = "WAV" if file.suffix == ".wav" else "MP4"
        print(f"  • {file.name}")
        print(f"    Format: {format_type} | Size: {size_mb} MB")
        print()
