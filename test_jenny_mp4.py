#!/usr/bin/env python3
"""Test Jenny voice MP4 generation for AMP platform"""

import sys
import os
from pathlib import Path

# Add Zorro Audio path
audio_dir = Path("Store Support/Projects/AMP/Zorro/Audio").resolve()
sys.path.insert(0, str(audio_dir))

from audio_pipeline import synthesize_activity_message, Voice

print("\n" + "="*60)
print("JENNY VOICE MP4 GENERATION TEST")
print("="*60 + "\n")

# Create output directory
output_dir = audio_dir / "output"
output_dir.mkdir(exist_ok=True)

# Test 1: Generate MP4 directly
print("[1/2] Generating Jenny voice MP4...")
test_message = "Welcome to Walmart Activity Hub. This is a test of the Jenny neural voice for audio podcasts."

try:
    success, mp4_file = synthesize_activity_message(
        message_text=test_message,
        voice=Voice.JENNY,
        output_dir=str(output_dir),
        format="mp4"
    )
    
    if success and mp4_file:
        file_size = os.path.getsize(mp4_file)
        print(f"✓ MP4 Generated Successfully")
        print(f"  File: {Path(mp4_file).name}")
        print(f"  Size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
        print(f"  Path: {mp4_file}\n")
    else:
        print(f"✗ FAILED: Could not generate MP4")
        sys.exit(1)
        
except Exception as e:
    print(f"✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Generate another MP4
print("[2/2] Generating second MP4...")
test_message_2 = "This is a second test message. AMP podcasts are now ready with Jenny neural voice."

try:
    success, mp4_file_2 = synthesize_activity_message(
        message_text=test_message_2,
        voice=Voice.JENNY,
        output_dir=str(output_dir),
        format="mp4"
    )
    
    if success and mp4_file_2:
        file_size = os.path.getsize(mp4_file_2)
        print(f"✓ Second MP4 Generated")
        print(f"  File: {Path(mp4_file_2).name}")
        print(f"  Size: {file_size:,} bytes ({file_size/1024:.1f} KB)\n")
    else:
        print(f"✗ FAILED")
        sys.exit(1)
        
except Exception as e:
    print(f"✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# List all generated MP4s
print("="*60)
print("✓ MP4 GENERATION COMPLETE\n")
print("Generated files:")
for mp4 in sorted(output_dir.glob("*.mp4")):
    size = mp4.stat().st_size
    print(f"  {mp4.name} ({size:,} bytes)")

print(f"\nOutput directory: {output_dir}")
print("✓ Ready for AMP podcast integration")
print("="*60 + "\n")
