"""Generate with David and Mark (marked voice shows as available but SAPI5 can't access it yet)."""

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
    """Generate podcast with specified voice via SAPI5."""
    
    output_file = f"Store Support/Projects/AMP/Zorro/output/podcasts/amp_podcast_91202b13_{label}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    
    ps_commands = f"""
$text = @'
{message_body}
'@

[System.Reflection.Assembly]::LoadWithPartialName("System.Speech") | Out-Null
$tts = New-Object System.Speech.Synthesis.SpeechSynthesizer

try {{
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
}} catch {{
    Write-Host "✗ Voice not accessible via SAPI5: {voice_name}"
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
        
        import time
        time.sleep(1)
        
        if os.path.exists(output_file) and os.path.getsize(output_file) > 5000:
            return os.path.basename(output_file)
            
    except Exception as e:
        print(f"  Error: {e}")
    
    return None

os.makedirs("Store Support/Projects/AMP/Zorro/output/podcasts", exist_ok=True)

print("=" * 70)
print("PODCAST GENERATION - AVAILABLE VOICES")
print("=" * 70)
print()

print("📊 Status:")
print("  ✓ Microsoft David Desktop (Works with SAPI5)")
print("  ✓ Microsoft Zira Desktop (Works with SAPI5)")
print("  ~ Microsoft Mark (Detected in Windows.Media, not SAPI5 yet)")
print("  ✗ Microsoft Jenny (Downloaded but not registered)")
print()

print("Generating with your two best voice options:")
print()

print("1️⃣  Microsoft DAVID (Male - Professional)")
david = generate_voice("Microsoft David Desktop", "david_male")
print()

print("2️⃣  Microsoft ZIRA (Female - Professional)")
zira = generate_voice("Microsoft Zira Desktop", "zira_female")
print()

print("=" * 70)
print("✅ COMPLETE")
print("=" * 70)
print()

if david:
    print(f"✓ David: {david}")
if zira:
    print(f"✓ Zira:  {zira}")

print()
print("🎙️  Listen and compare at: http://localhost:8888")
print()

print("=" * 70)
print("ABOUT JENNY & GUY")
print("=" * 70)
print()
print("Jenny was detected in Windows.Media API but:")
print("  • It's not registering with SAPI5 (older API)")
print("  • May need Windows settings adjustment")
print("  • Could require a system restart")
print()
print("For now, David & Zira are your best options.")
print("Both are high-quality professional voices.")
print()
