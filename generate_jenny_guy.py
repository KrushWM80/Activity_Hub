"""Generate podcast with the newly installed voices: Jenny and Guy."""

import os
import subprocess
from datetime import datetime

message_body = """WEEK TWO: STORE OPERATIONS UPDATE

FOOD AND CONSUMABLES section.

Beauty Department: Complete lipstick reset. Organize nail polish alphabetically. Review expiration dates. Restock sample section. Feature new skincare line.

Food Department: Organize dairy section. Rebrand organic products. Stock high-demand items. Deep clean coolers. Process new deliveries.

Fresh Department: Reset produce display. Verify expiration dates. Organize frozen items. Clean prep areas. Update pricing labels.

GENERAL MERCHANDISE: Entertainment reset, Fashion spring collection, Hardlines seasonal stock, Home décor, and Seasonal displays.

OPERATIONS: Asset Protection security walks, Backroom organization and FIFO, Front End efficiency, Store Fulfillment accuracy, and People scheduling."""

def generate_voice(voice_name, label):
    """Generate podcast with specified voice."""
    
    output_file = f"Store Support/Projects/AMP/Zorro/output/podcasts/amp_podcast_91202b13_{label}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    
    ps_commands = f"""
$text = @'
{message_body}
'@

[System.Reflection.Assembly]::LoadWithPartialName("System.Speech") | Out-Null
$tts = New-Object System.Speech.Synthesis.SpeechSynthesizer
$tts.SelectVoice('{voice_name}')
$tts.Rate = -2
$tts.Volume = 100
$tts.SetOutputToWaveFile('{output_file}')
$tts.Speak($text)
$tts.SetOutputToNull()
$tts.Dispose()

if (Test-Path '{output_file}') {{
    $size = [math]::Round((Get-Item '{output_file}').Length / 1MB, 2)
    Write-Host "✓ Generated: $size MB"
}}
"""
    
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_commands],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        print(result.stdout.strip())
        if result.stderr:
            print(f"  Note: {result.stderr[:150]}")
        
        import time
        time.sleep(1)
        
        if os.path.exists(output_file) and os.path.getsize(output_file) > 5000:
            return os.path.basename(output_file)
            
    except Exception as e:
        print(f"  Error: {e}")
    
    return None

os.makedirs("Store Support/Projects/AMP/Zorro/output/podcasts", exist_ok=True)

print("=" * 70)
print("GENERATING PODCAST WITH NEW VOICES")
print("=" * 70)
print()

print("1️⃣  Microsoft JENNY (Female, US)...")
jenny = generate_voice("Microsoft Jenny", "jenny_female")
print()

print("2️⃣  Microsoft GUY (Male, US)...")
guy = generate_voice("Microsoft Guy", "guy_male")
print()

print("=" * 70)
print("✅ COMPLETE")
print("=" * 70)
print()

if jenny:
    print(f"Jenny: {jenny}")
if guy:
    print(f"Guy:   {guy}")

print()
print("🎙️  Listen and compare at: http://localhost:8888")
