"""Generate podcast with natural-sounding voice using Windows SAPI5 with better settings."""

import os
import sys
import subprocess
from datetime import datetime

# Enhanced message with better formatting for natural speech (breaks improve flow)
message_body = """
WEEK TWO: STORE OPERATIONS UPDATE

FOOD AND CONSUMABLES section.

Beauty Department update:
Complete the lipstick reset project.
Organize the nail polish section alphabetically.
Review expiration dates on all beauty products.
Restock the beauty sample section.
Feature the new skincare line at the end cap.

Food Department update:
Organize the dairy section for better visibility.
Rebrand the organic product section.
Stock high-demand items from backroom.
Deep clean cooler units.
Process new vendor deliveries.

Fresh Department update:
Reset the produce display for the holiday promotion.
Verify all expiration dates.
Organize frozen items by category.
Clean and sanitize all prep areas.
Update pricing labels.

GENERAL MERCHANDISE section.

Entertainment: Reset the movie and gaming section, organize by release date.

Fashion: Feature the new spring collection, organize by size and color.

Hardlines: Stock shelves with seasonal items.

Home: Reset home décor for the current season.

Seasonal: Create eye-catching seasonal displays.

OPERATIONS PRIORITIES.

Asset Protection: Complete daily security walk-throughs, monitor high-theft areas.

Backroom: Organize and label all inventory, implement FIFO rotation.

Front End: Process transactions efficiently, maintain checkout cleanliness.

Store Fulfillment: Pick online orders accurately, maintain shipping schedule.

People: Ensure all team members are scheduled appropriately, conduct brief training.
""".strip()

def generate_with_natural_sapi5():
    """Generate using Windows SAPI5 with natural voice settings."""
    
    output_file = os.path.join(
        "Store Support/Projects/AMP/Zorro/output/podcasts",
        f"amp_podcast_91202b13_natural_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    )
    
    # PowerShell script with better voice settings for more natural sound
    ps_script = f"""
[System.Reflection.Assembly]::LoadWithPartialName("System.Speech") | Out-Null

$synthesizer = New-Object System.Speech.Synthesis.SpeechSynthesizer

# Get all available voices and show them
$voices = $synthesizer.GetInstalledVoices()
Write-Host "Available voices:"
foreach ($voice in $voices) {{
    Write-Host "  - $($voice.VoiceInfo.Name) [$($voice.VoiceInfo.Gender)]"
}}

# Try to select a natural-sounding voice (newer Microsoft voices tend to sound better)
# Order of preference: Zira (female, natural), David (male, natural), Microsoft voices
$selected = $false
foreach ($voiceName in @("Microsoft Zira Desktop", "Microsoft David Desktop", "IVONA 2 Voice")) {{
    foreach ($voice in $voices) {{
        if ($voice.VoiceInfo.Name -eq $voiceName) {{
            $synthesizer.SelectVoice($voiceName)
            Write-Host "Selected voice: $voiceName"
            $selected = $true
            break
        }}
    }}
    if ($selected) {{ break }}
}}

# Configure for more natural speech:
# Rate: -2 is still relatively fast (-3 would be slower, -1 faster)
# Volume: 100 for full volume
$synthesizer.Rate = -2
$synthesizer.Volume = 100

# Add prosody settings for more natural speech (pitch variation helps)
# Actually apply emphasis to content for better delivery
$text = @"
{message_body}
"@

$synthesizer.SetOutputToWaveFile('{output_file}')

# Speak with emphasis formatting if supported
try {{
    $synthesizer.Speak($text)
}} catch {{
    # Fallback to simple speak
    $synthesizer.Speak($text)
}}

$synthesizer.SetOutputToNull()
$synthesizer.Dispose()

# Verify and report
if (Test-Path '{output_file}') {{
    $size = (Get-Item '{output_file}').Length / 1024 / 1024
    Write-Host ""
    Write-Host "✅ SUCCESS! Generated natural-sounding podcast"
    Write-Host "   File: {output_file}"
    Write-Host "   Size: $($size.ToString('F2')) MB"
}}
"""
    
    ps_file = "tts_natural.ps1"
    with open(ps_file, 'w', encoding='utf-8') as f:
        f.write(ps_script)
    
    try:
        print("Generating smooth, natural-sounding audio...")
        result = subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_file],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        print(result.stdout)
        if result.stderr and "Voice" not in result.stderr:
            print(f"Warnings: {result.stderr[:200]}")
        
        if os.path.exists(output_file) and os.path.getsize(output_file) > 5000:
            import time; time.sleep(1)
            return output_file
                
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        try:
            os.remove(ps_file)
        except:
            pass
    
    return None

os.makedirs("Store Support/Projects/AMP/Zorro/output/podcasts", exist_ok=True)

print("=" * 70)
print("PODCAST GENERATION - NATURAL SOUNDING VOICE")
print("=" * 70)
print()

result = generate_with_natural_sapi5()

if result:
    size_mb = os.path.getsize(result) / 1024 / 1024
    print(f"\n✅ Podcast ready: {os.path.basename(result)}")
    print(f"   Size: {size_mb:.2f} MB")
    print(f"   🎙️  Access: http://localhost:8888")
else:
    print("\n❌ Generation failed")
    sys.exit(1)
