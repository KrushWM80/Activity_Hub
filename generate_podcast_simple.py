"""Generate podcast with proper WAV file creation using pyttsx3 or similar."""

import os
import sys
import json
from datetime import datetime
import subprocess

# Get the message body (from our previous extraction)
message_body = """
WEEK 2 - 2/21 - 2/27

FOOD & CONSUMABLES UPDATE:
The following items need your attention this week:

Beauty Department:
- Complete lipstick reset project
- Organize nail polish section alphabetically
- Review expiration dates on all beauty products
- Restock beauty sample section
- Feature end cap with new skincare line

Food Department:
- Organize dairy section for better visibility
- Rebrand organic product section
- Stock high-demand items from backroom
- Deep clean cooler units
- Process new vendor deliveries

Fresh Department:
- Reset produce display for holiday promotion
- Verify all expiration dates
- Organize frozen items by category
- Clean and sanitize all prep areas
- Update pricing labels

GENERAL MERCHANDISE:
Entertainment: Reset movie and gaming section, organize by release date
Fashion: Feature new spring collection, reorganize by size and color
Hardlines: Stock shelves with seasonal items
Home: Reset home décor for current season
Seasonal: Create eye-catching seasonal displays

OPERATIONS PRIORITIES:
Asset Protection: Complete daily security walk-throughs, monitor high-theft areas
Backroom: Organize and label all inventory, implement FIFO rotation
Front End: Process transactions efficiently, maintain checkout cleanliness
Store Fulfillment: Pick online orders accurately, maintain shipping schedule
People: Ensure all team members are scheduled appropriately, conduct brief training
""".strip()

def generate_wav_python(text, output_file):
    """Generate WAV file using raw PCM audio (simple approach)."""
    import wave
    import struct
    
    # Audio parameters
    sample_rate = 16000
    duration_per_char = 0.05  # 50ms per character (adjust for speed)
    num_samples = int(sample_rate * len(text) * duration_per_char)
    
    # Create simple audio pattern (frequency sweep based on text content)
    with wave.open(output_file, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)   # 16-bit
        wav_file.setframerate(sample_rate)
        
        # Generate audio data
        freq_base = 400  # Base frequency in Hz
        for i in range(num_samples):
            # Vary frequency based on position (creates varying tone)
            freq = freq_base + (200 * (i % 100) / 100)
            phase = 2.0 * 3.14159 * freq * i / sample_rate
            # Generate sine wave
            sample = int(32767 * 0.3 * __import__('math').sin(phase))
            wav_file.writeframes(struct.pack('<h', sample))

def generate_with_edge_tts():
    """Try using edge-tts library if available."""
    try:
        import subprocess
        import asyncio
        
        # Install edge-tts if needed
        try:
            import edge_tts
        except ImportError:
            print("Installing edge-tts...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "edge-tts"])
        
        # Use edge-tts to generate speech
        output_file = os.path.join(
            "Store Support/Projects/AMP/Zorro/output/podcasts",
            f"amp_podcast_91202b13_Your_Week_4_Messages_Are__edge_tts.mp3"
        )
        
        # Run edge-tts via subprocess
        cmd = f'python -m edge_tts --text "{message_body}" --write-media "{output_file}" --rate -20'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Generated with edge-tts: {output_file}")
            return output_file
        else:
            print(f"edge-tts error: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"edge-tts approach failed: {e}")
        return None

# Ensure output directory exists
os.makedirs("Store Support/Projects/AMP/Zorro/output/podcasts", exist_ok=True)

# Try edge-tts first (free, no API key needed)
print("Attempting edge-tts (Microsoft Azure free tier)...")
result = generate_with_edge_tts()

if not result:
    print("\n⚠️  edge-tts failed. Generating simple audio test file...")
    output_file = os.path.join(
        "Store Support/Projects/AMP/Zorro/output/podcasts",
        f"amp_podcast_91202b13_simple_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    )
    generate_wav_python(message_body, output_file)
    print(f"✅ Generated test audio: {output_file}")
    print(f"   File size: {os.path.getsize(output_file) / 1024 / 1024:.2f} MB")
    
    # Verify it's valid WAV
    with open(output_file, 'rb') as f:
        header = f.read(4)
        print(f"   Header: {header}")
        if header == b'RIFF':
            print("   ✅ Valid WAV file header!")
        else:
            print(f"   ⚠️ Unexpected header: {header}")

print("\nDone!")
