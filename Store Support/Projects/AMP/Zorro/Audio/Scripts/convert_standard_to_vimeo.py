#!/usr/bin/env python3
"""
Generate Vimeo-compatible MP4 for Your Week 4 Messages - David & Zira
Converts existing standard MP4s to Vimeo format with thumbnail
"""

import subprocess
from pathlib import Path
from datetime import datetime

def create_vimeo_version(standard_mp4_filename, voice_name):
    """Convert standard MP4 to Vimeo-compatible format"""
    
    output_folder = Path("../output/podcasts")
    output_folder.mkdir(parents=True, exist_ok=True)
    
    standard_mp4_path = output_folder / standard_mp4_filename
    vimeo_filename = standard_mp4_filename.replace('.mp4', ' - Vimeo.mp4')
    vimeo_filepath = output_folder / vimeo_filename
    thumbnail_path = output_folder / "merch_msg_thumbnail.jpeg"
    
    print(f"\nProcessing: {standard_mp4_filename}")
    print(f"             Voice: {voice_name}")
    
    # Check if standard MP4 exists
    if not standard_mp4_path.exists():
        # Need to generate from message_body script
        print(f"⚠️  Standard MP4 not found: {standard_mp4_filename}")
        print(f"    Need to generate from generate_both_voices.py first")
        return False
    
    # Check if thumbnail exists
    if not thumbnail_path.exists():
        print(f"❌ Thumbnail not found: {thumbnail_path}")
        return False
    
    try:
        ffmpeg_cmd = [
            "ffmpeg",
            "-y",
            "-loop", "1",
            "-i", str(thumbnail_path),
            "-i", str(standard_mp4_path),
            "-c:v", "libx264",
            "-tune", "stillimage",
            "-preset", "medium",
            "-r", "25",
            "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "128k",
            "-shortest",
            str(vimeo_filepath)
        ]
        
        result = subprocess.run(
            ffmpeg_cmd,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if vimeo_filepath.exists():
            vimeo_size_mb = vimeo_filepath.stat().st_size / (1024 * 1024)
            print(f"✅ Vimeo Format Created: {vimeo_filename}")
            print(f"   Size: {vimeo_size_mb:.2f} MB")
            return True
        else:
            print(f"❌ Failed to create Vimeo format")
            if result.stderr:
                print(f"   Error: {result.stderr[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n" + "=" * 100)
    print("STANDARD MP4 → VIMEO-COMPATIBLE MP4 CONVERTER")
    print("=" * 100)
    print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    files_to_convert = [
        ("Your Week 4 Messages are Here - Audio - Reading - David.mp4", "David"),
        ("Your Week 4 Messages are Here - Audio - Reading - Zira.mp4", "Zira"),
    ]
    
    successful = 0
    failed = 0
    
    for filename, voice in files_to_convert:
        if create_vimeo_version(filename, voice):
            successful += 1
        else:
            failed += 1
    
    print("\n" + "=" * 100)
    print("CONVERSION COMPLETE")
    print("=" * 100)
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print("=" * 100 + "\n")

if __name__ == "__main__":
    main()
