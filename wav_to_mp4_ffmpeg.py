#!/usr/bin/env python3
"""Convert Jenny voice WAV files to MP4 using FFmpeg"""

import sys
import os
from pathlib import Path
import subprocess

print("\n" + "="*70)
print("JENNY VOICE WAV -> MP4 CONVERSION")
print("="*70 + "\n")

# Find latest WAV file from synthesis
temp_dir = Path(os.getenv('TEMP', 'C:\\Windows\\Temp'))
wav_files = sorted(temp_dir.glob('jenny_synthesis_*.wav'), key=lambda x: x.stat().st_mtime, reverse=True)

if not wav_files:
    print("✗ No Jenny synthesis WAV files found in temp directory")
    print(f"  Checked: {temp_dir}")
    sys.exit(1)

latest_wav = wav_files[0]
print(f"✓ Found WAV file: {latest_wav.name}")
print(f"  Size: {latest_wav.stat().st_size:,} bytes")
print(f"  Created: {latest_wav.stat().st_mtime}\n")

# Create output directory
output_dir = Path("Store Support/Projects/AMP/Zorro/Audio/output").resolve()
output_dir.mkdir(parents=True, exist_ok=True)

# Create output MP4
base_name = latest_wav.stem.replace('jenny_synthesis_', 'jenny_audio_')
output_mp4 = output_dir / f"{base_name}.mp4"

print(f"[1/3] Converting WAV to MP4 (audio-only)...")
print(f"  Input:  {latest_wav.name}")
print(f"  Output: {output_mp4.name}\n")

# FFmpeg command: WAV to MP4 (audio-only, high quality)
cmd = [
    'C:\\ffmpeg\\bin\\ffmpeg.exe',
    '-i', str(latest_wav),
    '-q:a', '0',              # Highest audio quality
    '-codec:a', 'aac',        # AAC codec
    '-b:a', '256k',           # 256kbps bitrate
    '-vn',                    # No video
    '-y',                     # Overwrite
    str(output_mp4)
]

try:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        print("✗ Conversion failed:")
        print(result.stderr)
        sys.exit(1)
    print("✓ Audio conversion successful\n")
except subprocess.TimeoutExpired:
    print("✗ Conversion timed out")
    sys.exit(1)
except FileNotFoundError:
    print("✗ FFmpeg not found at C:\\ffmpeg\\bin\\ffmpeg.exe")
    sys.exit(1)

# Verify output
if not output_mp4.exists():
    print("✗ Output file not created")
    sys.exit(1)

output_size = output_mp4.stat().st_size
print(f"[2/3] Audio MP4 verified")
print(f"  File: {output_mp4.name}")
print(f"  Size: {output_size:,} bytes ({output_size/1024:.1f} KB)\n")

# Now create video MP4 with black background + audio
print(f"[3/3] Creating full video MP4 with background...")

output_video_mp4 = output_dir / f"{base_name.replace('_audio_', '_video_')}.mp4"

# Create black background + audio
cmd_video = [
    'C:\\ffmpeg\\bin\\ffmpeg.exe',
    '-f', 'lavfi',
    '-i', 'color=c=black:s=1920x1080:d=100',  # Black 1920x1080 for 100 seconds
    '-i', str(output_mp4),
    '-c:v', 'libx264',        # H.264 video codec
    '-preset', 'fast',        # Speed vs quality
    '-c:a', 'aac',            # AAC audio
    '-map', '0:v:0',          # Map video from color filter
    '-map', '1:a:0',          # Map audio from MP4
    '-shortest',              # Stop at shortest stream
    '-pix_fmt', 'yuv420p',    # Pixel format for compatibility
    '-y',                     # Overwrite
    str(output_video_mp4)
]

try:
    result = subprocess.run(cmd_video, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        print("⚠ Video creation failed, but audio MP4 is ready")
        print(f"  Error: {result.stderr[:200]}")
    elif output_video_mp4.exists():
        video_size = output_video_mp4.stat().st_size
        print(f"✓ Video MP4 created successfully")
        print(f"  File: {output_video_mp4.name}")
        print(f"  Size: {video_size:,} bytes ({video_size/1024:.1f} KB)\n")
    else:
        print("⚠ Video creation reported success but file not found")
except subprocess.TimeoutExpired:
    print("⚠ Video creation timed out")
except Exception as e:
    print(f"⚠ Video creation error: {e}")

# Summary
print("="*70)
print("✓ MP4 CONVERSION COMPLETE\n")
print(f"Audio-Only MP4 (for AMP integration):")
print(f"  {output_mp4}")
print(f"  Size: {output_size:,} bytes\n")

if output_video_mp4.exists():
    video_size = output_video_mp4.stat().st_size
    print(f"Full Video MP4 (with background):")
    print(f"  {output_video_mp4}")
    print(f"  Size: {video_size:,} bytes\n")

print("✓ Ready for AMP podcast generator integration")
print("="*70 + "\n")
