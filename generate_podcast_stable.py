"""Generate podcast using direct Python TTS approach."""

import os
import sys
import json
from datetime import datetime
import subprocess
import time

message_body = """
WEEK 2 - 2/21 - 2/27

FOOD & CONSUMABLES UPDATE:
The following items need your attention this week:
Beauty Department - Complete lipstick reset, organize nail polish alphabetically, review expiration dates, restock samples, feature new skincare line.
Food Department - Organize dairy section, rebrand organic products, stock items, deep clean coolers, process deliveries.
Fresh Department - Reset produce display for promotion, verify dates, organize frozen items, clean prep areas, update labels.

GENERAL MERCHANDISE:
Entertainment - Reset movie and gaming section by release date.
Fashion - Feature spring collection, organize by size and color.
Hardlines - Stock seasonal items.
Home - Reset décor for season.
Seasonal - Create eye-catching displays.

OPERATIONS PRIORITIES:
Asset Protection - Daily security walks, monitor theft areas.
Backroom - Organize and label, FIFO rotation.
Front End - Process efficiently, maintain checkout.
Store Fulfillment - Pick accurately, maintain schedule.
People - Proper scheduling and training.
""".strip()

def generate_with_pyttsx3():
    """Generate using pyttsx3 - pure Python, works offline."""
    try:
        import pyttsx3
        
        output_file = os.path.join(
            "Store Support/Projects/AMP/Zorro/output/podcasts",
            f"amp_podcast_91202b13_pyttsx3_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        )
        
        engine = pyttsx3.init()
        engine.setProperty('rate', 120)  # Words per minute
        engine.setProperty('volume', 0.9)
        
        # List available voices and select female if available
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'female' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        
        engine.save_to_file(message_body, output_file)
        engine.runAndWait()
        
        if os.path.exists(output_file):
            size_mb = os.path.getsize(output_file) / 1024 / 1024
            print(f"✅ Generated with pyttsx3: {output_file}")
            print(f"   Size: {size_mb:.2f} MB")
            return output_file
        
    except ImportError:
        print("pyttsx3 not available, will install...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "pyttsx3"])
            return generate_with_pyttsx3()  # Retry after install
        except:
            print("Could not install pyttsx3")
            return None
    except Exception as e:
        print(f"pyttsx3 error: {e}")
        return None

def generate_with_sapi5_direct():
    """Direct approach using Windows SAPI5 via PowerShell."""
    
    output_file = os.path.join(
        "Store Support/Projects/AMP/Zorro/output/podcasts",
        f"amp_podcast_91202b13_sapi5_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    )
    
    # Escape the message for PowerShell
    ps_message = message_body.replace('"', '\"').replace('\n', ' ')
    
    # More robust PowerShell script with better error handling
    ps_script = f'''
$text = @"
{message_body}
"@

$outputFile = "{output_file}"

# Create SAPI5 synthesizer
$synthesizer = New-Object System.Speech.Synthesis.SpeechSynthesizer

# Configure speech
$synthesizer.Rate = -2
$synthesizer.Volume = 100

# Select female voice if available
$voices = $synthesizer.GetInstalledVoices()
foreach ($voice in $voices) {{
    if ($voice.VoiceInfo.Gender -eq 'Female') {{
        $synthesizer.SelectVoice($voice.VoiceInfo.Name)
        break
    }}
}}

# Generate audio file
try {{
    $synthesizer.SetOutputToWaveFile($outputFile)
    $synthesizer.Speak($text)
    $synthesizer.SetOutputToNull()
    
    # Verify file was created
    if (Test-Path $outputFile) {{
        $size = (Get-Item $outputFile).Length / 1024 / 1024
        Write-Host "✅ Audio generated: $outputFile"
        Write-Host "   Size: $($size.ToString('F2')) MB"
        Write-Host "   Duration estimate: $(($size * 8 / 128).ToString('F1')) seconds"
    }} else {{
        Write-Host "❌ File not created"
    }}
}} catch {{
    Write-Host "❌ Error: $_"
}}
'''
    
    # Write and execute PowerShell script
    ps_file = "temp_generate_podcast.ps1"
    with open(ps_file, 'w', encoding='utf-8') as f:
        f.write(ps_script)
    
    try:
        result = subprocess.run(
            [
                "powershell",
                "-ExecutionPolicy", "Bypass",
                "-File", ps_file
            ],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        print(result.stdout)
        if result.stderr:
            print("Warnings:", result.stderr)
        
        if os.path.exists(output_file):
            return output_file
            
    finally:
        if os.path.exists(ps_file):
            os.remove(ps_file)
    
    return None

# Ensure output directory
os.makedirs("Store Support/Projects/AMP/Zorro/output/podcasts", exist_ok=True)

print("=" * 60)
print("PODCAST GENERATION - STABLE AUDIO APPROACH")
print("=" * 60)

# Try pyttsx3 first (pure Python, offline)
print("\n1️⃣  Attempting pyttsx3 (pure Python)...")
result = generate_with_pyttsx3()

# If pyttsx3 failed, try SAPI5 direct
if not result:
    print("\n2️⃣  Attempting Windows SAPI5 (direct PowerShell)...")
    result = generate_with_sapi5_direct()

if result:
    print(f"\n✅ SUCCESS! Podcast generated: {result}")
    print("\n📻 Access via: http://localhost:8888")
else:
    print("\n❌ All approaches failed")
    sys.exit(1)
