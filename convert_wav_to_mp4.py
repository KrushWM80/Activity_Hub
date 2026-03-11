#!/usr/bin/env python3
"""Convert Jenny voice WAV files to MP4 for AMP podcast delivery"""

import sys
import os
from pathlib import Path
import subprocess

print("\n" + "="*70)
print("JENNY VOICE WAV -> MP4 CONVERSION")
print("="*70 + "\n")

# Check if FFmpeg is available
try:
    result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=5)
    if 'ffmpeg version' not in result.stdout:
        raise FileNotFoundError("FFmpeg not found in PATH")
    print("✓ FFmpeg is available")
    ffmpeg_available = True
except (FileNotFoundError, subprocess.TimeoutExpired):
    ffmpeg_available = False
    print("⚠ FFmpeg not found - attempting to install...")

# If FFmpeg not available, try to install it
if not ffmpeg_available:
    print("\nInstalling FFmpeg-python and dependencies...\n")
    # Try using chocolatey on Windows
    try:
        result = subprocess.run(['choco', 'install', 'ffmpeg', '-y'], capture_output=True, timeout=60)
        if result.returncode == 0:
            print("✓ FFmpeg installed via Chocolatey")
            ffmpeg_available = True
    except:
        pass

if not ffmpeg_available:
    print("\n" + "!"*70)
    print("FFmpeg is required for MP4 conversion.")
    print("\nTo install FFmpeg:")
    print("  Option 1 (Recommended - via Chocolatey):")
    print("    choco install ffmpeg")
    print("\n  Option 2 (Manual):")
    print("    1. Visit: https://ffmpeg.org/download.html")
    print("    2. Download Windows build")
    print("    3. Extract to C:/ffmpeg")
    print("    4. Add to PATH environment variable")
    print("\n  Option 3 (Portable):")
    print("    Download: https://ffmpeg.org/download.html#build-windows")
    print("    Extract to workspace/ffmpeg folder")
    print("!"*70 + "\n")
    sys.exit(1)

# Find latest WAV file from synthesis
temp_dir = Path(os.getenv('TEMP', 'C:\\Windows\\Temp'))
wav_files = sorted(temp_dir.glob('jenny_synthesis_*.wav'), key=lambda x: x.stat().st_mtime, reverse=True)

if not wav_files:
    print("✗ No Jenny synthesis WAV files found in temp directory")
    sys.exit(1)

latest_wav = wav_files[0]
print(f"✓ Found WAV file: {latest_wav.name}")
print(f"  Size: {latest_wav.stat().st_size:,} bytes\n")

# Create output MP4
output_mp4 = latest_wav.parent / latest_wav.stem.replace('_synthesis_', '_final_').replace('.wav', '.mp4')

print(f"[1/3] Converting to MP4...")
print(f"  Output: {output_mp4.name}\n")

# FFmpeg command to convert WAV to MP4 (audio only)
cmd = [
    'ffmpeg',
    '-i', str(latest_wav),
    '-q:a', '0',                          # Highest audio quality
    '-map', 'a',                           # Map audio stream
    '-c:a', 'aac',                         # AAC codec
    '-b:a', '256k',                        # 256kbps bitrate
    '-vn',                                 # No video
    '-y',                                  # Overwrite output
    str(output_mp4)
]

try:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        print("✗ Conversion failed:")
        print(result.stderr)
        sys.exit(1)
    print("✓ Conversion successful\n")
except subprocess.TimeoutExpired:
    print("✗ Conversion timed out")
    sys.exit(1)

# Verify output
if not output_mp4.exists():
    print("✗ Output file not created")
    sys.exit(1)

output_size = output_mp4.stat().st_size
print(f"[2/3] Verifying output...")
print(f"  File: {output_mp4.name}")
print(f"  Size: {output_size:,} bytes\n")

print(f"[3/3] Summary")
print("="*70)
print(f"✓ WAV to MP4 conversion complete")
print(f"✓ Output ready for AMP delivery")
print(f"  Location: {output_mp4}")
print(f"  Size: {output_size/1024:.1f} KB")
print("="*70 + "\n")

# Also create a simple MP4 with static image (for proper video container)
print("Creating final MP4 with static image background...\n")

try:
    # Create a simple black 1920x1080 image as placeholder
    import struct
    
    # For now, just use ffmpeg to add a color background
    final_mp4 = output_mp4.parent / output_mp4.stem.replace('_final_', '_complete_') + '.mp4'
    
    cmd_final = [
        'ffmpeg',
        '-f', 'lavfi',
        '-i', 'color=c=black:s=1920x1080:d=100',  # Black background, 100s duration
        '-i', str(output_mp4),
        '-c:v', 'h264',
        '-c:a', 'aac',
        '-map', '0:v:0',
        '-map', '1:a:0',
        '-shortest',
        '-y',
        str(final_mp4)
    ]
    
    result = subprocess.run(cmd_final, capture_output=True, text=True, timeout=60)
    if result.returncode == 0 and final_mp4.exists():
        final_size = final_mp4.stat().st_size
        print(f"✓ Final MP4 with video track created")
        print(f"  Location: {final_mp4.name}")
        print(f"  Size: {final_size/1024:.1f} KB\n")
except:
    print("⚠ Could not create video background (audio-only MP4 still available)\n")

print("\n✓ All conversions complete! Ready for next steps...")
