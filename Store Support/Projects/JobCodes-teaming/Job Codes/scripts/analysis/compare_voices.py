"""Generate podcast with both available voices for comparison."""

import os
import subprocess
from datetime import datetime

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

def generate_podcast_with_voice(voice_name, output_suffix):
    """Generate podcast with specified voice."""
    
    output_file = os.path.join(
        "Store Support/Projects/AMP/Zorro/output/podcasts",
        f"amp_podcast_91202b13_{output_suffix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    )
    
    # Escape text for PowerShell
    ps_text = message_body.replace('"', '\"').replace('\n', '" + [Environment]::NewLine + "')
    
    ps_script = f"""
[System.Reflection.Assembly]::LoadWithPartialName("System.Speech") | Out-Null

$synthesizer = New-Object System.Speech.Synthesis.SpeechSynthesizer

# Select voice
$synthesizer.SelectVoice("{voice_name}")
Write-Host "Synthesizing with: {voice_name}"

# Configure for natural speech
$synthesizer.Rate = -2
$synthesizer.Volume = 100

$text = "{ps_text}"

$synthesizer.SetOutputToWaveFile('{output_file}')
$synthesizer.Speak($text)
$synthesizer.SetOutputToNull()
$synthesizer.Dispose()

# Report result
if (Test-Path '{output_file}') {{
    $size = (Get-Item '{output_file}').Length / 1024 / 1024
    Write-Host "✓ Generated: {output_suffix}"
    Write-Host "  Size: $($size.ToString('F2')) MB"
}}
"""
    
    ps_file = f"tts_{output_suffix}.ps1"
    with open(ps_file, 'w', encoding='utf-8') as f:
        f.write(ps_script)
    
    try:
        result = subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_file],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        print(result.stdout)
        
        if os.path.exists(output_file) and os.path.getsize(output_file) > 5000:
            return output_file
            
    finally:
        try:
            os.remove(ps_file)
        except:
            pass
    
    return None

os.makedirs("Store Support/Projects/AMP/Zorro/output/podcasts", exist_ok=True)

print("=" * 70)
print("COMPARING AVAILABLE VOICES")
print("=" * 70)
print()

results = []

# Generate with both voices
voices = [
    ("Microsoft Zira Desktop", "zira_female"),
    ("Microsoft David Desktop", "david_male"),
]

for voice_name, suffix in voices:
    print(f"Generating with {voice_name}...")
    result = generate_podcast_with_voice(voice_name, suffix)
    if result:
        results.append((voice_name, result))
    print()

print("=" * 70)
print("GENERATED FILES")
print("=" * 70)

for voice_name, file_path in results:
    size_mb = os.path.getsize(file_path) / 1024 / 1024
    file_name = os.path.basename(file_path)
    print(f"\n{voice_name}:")
    print(f"  File: {file_name}")
    print(f"  Size: {size_mb:.2f} MB")

print(f"\n🎙️  Listen at: http://localhost:8888")
print(f"   Compare both files to choose your preferred voice!")
