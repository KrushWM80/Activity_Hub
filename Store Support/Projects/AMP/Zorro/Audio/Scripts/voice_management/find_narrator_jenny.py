"""Detect and use Narrator-installed Microsoft Jenny voice."""

import subprocess
import os
from datetime import datetime

message_body = """WEEK TWO: STORE OPERATIONS UPDATE

FOOD AND CONSUMABLES section.

Beauty Department: Complete lipstick reset. Organize nail polish alphabetically. Review expiration dates. Restock sample section. Feature new skincare line.

Food Department: Organize dairy section. Rebrand organic products. Stock high-demand items. Deep clean coolers. Process new deliveries.

Fresh Department: Reset produce display. Verify expiration dates. Organize frozen items. Clean prep areas. Update pricing labels.

GENERAL MERCHANDISE: Entertainment reset, Fashion spring collection, Hardlines seasonal stock, Home décor, and Seasonal displays.

OPERATIONS: Asset Protection security walks, Backroom organization and FIFO, Front End efficiency, Store Fulfillment accuracy, and People scheduling."""

# First, discover what voices are available including Narrator voices
print("=" * 70)
print("SCANNING FOR NARRATOR-INSTALLED VOICES")
print("=" * 70)
print()

ps_discover = r"""
[System.Reflection.Assembly]::LoadWithPartialName("System.Speech") | Out-Null
$tts = New-Object System.Speech.Synthesis.SpeechSynthesizer

Write-Host "SAPI5 Voices Currently Available:"
$voices = $tts.GetInstalledVoices()
foreach ($v in $voices) {
    Write-Host "  - $($v.VoiceInfo.Name)"
}

Write-Host ""
Write-Host "Checking Windows Registry for ALL speech voices..."

# Check the registry for voice tokens
$regPath = "HKLM:\SOFTWARE\Microsoft\Speech\Voices\Tokens"
$voiceTokens = Get-ChildItem $regPath -ErrorAction SilentlyContinue

if ($voiceTokens) {
    Write-Host "All voice tokens in registry:"
    foreach ($token in $voiceTokens) {
        $name = $token.PSChildName
        Write-Host "  - $name"
        
        # Try to use it
        try {
            $tts.SelectVoice($name)
            Write-Host "    ✓ Can use via SAPI5"
        } catch {
            Write-Host "    ✗ Cannot use via SAPI5"
        }
    }
}

# Also check for OneCore voices
Write-Host ""
Write-Host "Checking for OneCore/Narrator voice registrations..."
$oneCorePath = "HKLM:\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens"
try {
    $oneCoreTensions = Get-ChildItem $oneCorePath -ErrorAction SilentlyContinue
    if ($oneCoreTensions) {
        foreach ($token in $oneCoreTensions) {
            Write-Host "  - $($token.PSChildName) (OneCore)"
        }
    } else {
        Write-Host "  (No OneCore voices found)"
    }
} catch {
    Write-Host "  (OneCore registry not accessible)"
}
"""

result = subprocess.run(
    ["powershell", "-NoProfile", "-Command", ps_discover],
    capture_output=True,
    text=True,
    timeout=15
)

print(result.stdout)
if result.stderr:
    print("Notes:", result.stderr[:300])

print()
print("=" * 70)
print("ATTEMPTING TO GENERATE WITH NARRATOR VOICES")
print("=" * 70)
print()

# Try various possible voice names for Narrator-installed Jenny
voice_attempts = [
    "Microsoft Jenny",
    "Microsoft Jenny Narrator",
    "Microsoft Jenny OneCore",
    "Microsoft Jenny Natural",
    "Microsoft.OneCore.Jenny",
    "Microsoft.Narrator.Jenny",
    "Jenny",
    "Microsoft Jenny - English (United States)",
]

def try_generate_with_voice(voice_name, label):
    """Try to generate with a specific voice name."""
    
    output_file = f"Store Support/Projects/AMP/Zorro/output/podcasts/amp_podcast_91202b13_{label}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    
    ps_cmd = f"""
$text = @'
{message_body}
'@

[System.Reflection.Assembly]::LoadWithPartialName("System.Speech") | Out-Null
$tts = New-Object System.Speech.Synthesis.SpeechSynthesizer

try {{
    $tts.SelectVoice("{voice_name}")
    $tts.Rate = -2
    $tts.Volume = 100
    $tts.SetOutputToWaveFile('{output_file}')
    $tts.Speak($text)
    $tts.SetOutputToNull()
    $tts.Dispose()
    
    if (Test-Path '{output_file}') {{
        $size = [math]::Round((Get-Item '{output_file}').Length / 1MB, 2)
        Write-Host "✓ Success with: {voice_name}"
        Write-Host "  File: {output_file}"
        Write-Host "  Size: $size MB"
    }}
}} catch {{
    Write-Host "✗ Failed: {voice_name}"
    Write-Host "  Error: $_"
}}
"""
    
    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", ps_cmd],
        capture_output=True,
        text=True,
        timeout=120
    )
    
    # Parse output
    if "Success with" in result.stdout:
        print(result.stdout)
        return True
    else:
        print(f"Tried: {voice_name}")
        if "Error:" in result.stdout:
            error_line = [l for l in result.stdout.split('\n') if 'Error:' in l][0] if [l for l in result.stdout.split('\n') if 'Error:' in l] else ""
            print(f"  {error_line[:80]}")
        return False

os.makedirs("Store Support/Projects/AMP/Zorro/output/podcasts", exist_ok=True)

success = False
for voice_name in voice_attempts:
    if try_generate_with_voice(voice_name, "jenny_narrator"):
        success = True
        break

if not success:
    print()
    print("=" * 70)
    print("❌ NARRATOR VOICE NOT ACCESSIBLE VIA SAPI5")
    print("=" * 70)
    print()
    print("Reason: Narrator voices in Windows 11 don't always register with SAPI5")
    print()
    print("Solutions:")
    print()
    print("Option 1: Use existing voices")
    print("  Run: python generate_both_voices.py")
    print("  This will generate with David and Zira instead")
    print()
    print("Option 2: Use Aria voice (if available)")
    print("  Aria is another natural voice that may work better")
    print("  Install from Settings > Accessibility > Text-to-speech > Manage voices")
    print()
    print("Option 3: Check Narrator Registration")
    print("  Sometimes Narrator voices need to be copied to the SAPI5 registry")
    print("  Run: python register_narrator_voices.py")
    print()
else:
    print()
    print("🎙️  Listen at: http://localhost:8888")
