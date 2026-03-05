#!/usr/bin/env python3
"""Test Jenny voice synthesis after Windows restart"""

import sys
import os
from pathlib import Path

# Add Zorro Audio path
audio_dir = Path("Store Support/Projects/AMP/Zorro/Audio").resolve()
sys.path.insert(0, str(audio_dir))

from audio_pipeline import synthesize_activity_message, Voice

print("\n" + "="*60)
print("JENNY VOICE SYNTHESIS TEST")
print("="*60 + "\n")

# Test message
test_message = "Welcome to Walmart Activity Hub. This is a test of the Jenny neural voice."

print(f"Test Message: {test_message}\n")

print("[1/3] Synthesizing with Jenny voice using Default engine...")
try:
    success, audio_file = synthesize_activity_message(
        message_text=test_message,
        voice=Voice.JENNY
    )
    
    if success and audio_file:
        file_size = os.path.getsize(audio_file)
        print(f"✓ SUCCESS")
        print(f"  Audio file: {audio_file}")
        print(f"  File size: {file_size:,} bytes")
    else:
        print(f"✗ FAILED: No audio file generated")
        sys.exit(1)
        
except Exception as e:
    print(f"✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n[2/3] Synthesizing with explicit Voice.JENNY...")
try:
    success, audio_file_2 = synthesize_activity_message(
        message_text="This message uses Jenny voice explicitly.",
        voice=Voice.JENNY
    )
    
    if success and audio_file_2:
        file_size = os.path.getsize(audio_file_2)
        print(f"✓ SUCCESS")
        print(f"  Audio file: {audio_file_2}")
        print(f"  File size: {file_size:,} bytes")
    else:
        print(f"✗ FAILED")
        sys.exit(1)
        
except Exception as e:
    print(f"✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n[3/3] Summary")
print("="*60)
print("✓ Jenny voice synthesis is WORKING")
print("✓ Audio files generated successfully")
print("✓ Ready for production MP4 conversion")
print("="*60 + "\n")
