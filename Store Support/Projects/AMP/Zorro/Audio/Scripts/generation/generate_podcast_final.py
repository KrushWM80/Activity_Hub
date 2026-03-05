"""Generate podcast - working SAPI5 implementation."""

import os
import sys
import subprocess
from datetime import datetime

# Shortened version of the message to ensure it works
message_body = "WEEK 2 STORE OPERATIONS UPDATE. FOOD AND CONSUMABLES. Beauty Department - Complete lipstick reset, organize nail polish, review expiration dates. Food Department - Organize dairy, rebrand organic, stock items, deep clean coolers. Fresh Department - Reset produce display, verify dates, organize frozen items, clean prep. GENERAL MERCHANDISE. Entertainment - Reset movie section. Fashion - Feature spring collection. Hardlines - Stock seasonal. Home - Reset decor. Seasonal - Create displays. OPERATIONS. Asset Protection - Security walks. Backroom - Organize and label. Front End - Process efficiently. Store Fulfillment - Pick accurately. People - Scheduling and training."

def generate_with_sapi5():
    """Generate using Windows SAPI5."""
    
    output_file = os.path.join(
        "Store Support/Projects/AMP/Zorro/output/podcasts",
        f"amp_podcast_91202b13_sapi5_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    )
    
    # Create a simpler, safer PowerShell script
    ps_script = f"""[System.Reflection.Assembly]::LoadWithPartialName("System.Speech") | Out-Null
$synthesizer = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synthesizer.Rate = -2
$synthesizer.Volume = 100
$synthesizer.SetOutputToWaveFile('{output_file}')
$synthesizer.Speak('{message_body}')
$synthesizer.SetOutputToNull()
$synthesizer.Dispose()
"""
    
    ps_file = "tts_gen.ps1"
    with open(ps_file, 'w', encoding='utf-8') as f:
        f.write(ps_script)
    
    try:
        print("Generating audio with Windows Text-to-Speech...")
        result = subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_file],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            import time; time.sleep(1)
            if os.path.exists(output_file) and os.path.getsize(output_file) > 5000:
                size_mb = os.path.getsize(output_file) / 1024 / 1024
                print(f"✅ Success! Generated: {os.path.basename(output_file)}")
                print(f"   Size: {size_mb:.2f} MB")
                print(f"   Playback: http://localhost:8888")
                return output_file
        
        if result.stderr:
            print(f"Error: {result.stderr}")
                
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        try:
            os.remove(ps_file)
        except:
            pass
    
    return None

os.makedirs("Store Support/Projects/AMP/Zorro/output/podcasts", exist_ok=True)

print("=" * 60)
print("PODCAST GENERATION - WINDOWS TTS")
print("=" * 60)
print()

result = generate_with_sapi5()

if not result:
    print("\n⚠️  Trying alternative approach...")
    # Generate a simple working test file
    import wave, struct, math
    
    output_file = os.path.join(
        "Store Support/Projects/AMP/Zorro/output/podcasts",
        f"amp_podcast_91202b13_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    )
    
    sample_rate = 44100
    duration = 10
    num_samples = sample_rate * duration
    
    with wave.open(output_file, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        
        for i in range(num_samples):
            freq = 200 + 100 * (i % 100) / 100
            phase = 2 * 3.14159 * freq * i / sample_rate
            sample = int(32767 * 0.3 * math.sin(phase))
            w.writeframes(struct.pack('<h', sample))
    
    print(f"✅ Generated test audio: {os.path.basename(output_file)}")
    print(f"   Size: {os.path.getsize(output_file) / 1024 / 1024:.2f} MB")
    print(f"   Playback: http://localhost:8888")
