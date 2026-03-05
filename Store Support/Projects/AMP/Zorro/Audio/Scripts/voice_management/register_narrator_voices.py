"""Register Narrator-installed voices with SAPI5 so they're accessible."""

import subprocess
import os
import winreg

print("=" * 70)
print("REGISTERING NARRATOR VOICES WITH SAPI5")
print("=" * 70)
print()

# First, check what Narrator voices are available
ps_check_narrator = r"""
Write-Host "Narrator Voice Locations:"
Write-Host ""

# Check the Narrator voices directory
$narratorPath = "$env:ProgramFiles\WindowsApps"
Write-Host "Checking: $narratorPath"

$msVoices = Get-ChildItem $narratorPath -Filter "*MicrosoftSpeechLanguagePack*" -Directory -ErrorAction SilentlyContinue
if ($msVoices) {
    Write-Host "  Found voice packages:"
    foreach ($voice in $msVoices) {
        Write-Host "    - $($voice.Name)"
    }
} else {
    Write-Host "  (No WindowsApps speech packs found)"
}

# Try to find OneCore voices
Write-Host ""
Write-Host "OneCore voices in registry:"
$oneCoreRegPath = "HKLM:\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens"
try {
    $oneCore = Get-ChildItem $oneCoreRegPath -ErrorAction SilentlyContinue
    if ($oneCore) {
        foreach ($voice in $oneCore) {
            Write-Host "  - $($voice.PSChildName)"
        }
    }
} catch {
    Write-Host "  (Registry path not accessible)"
}
"""

result = subprocess.run(
    ["powershell", "-NoProfile", "-Command", ps_check_narrator],
    capture_output=True,
    text=True,
    timeout=10
)

print(result.stdout)

print()
print("=" * 70)
print("ATTEMPTING REGISTRATION")
print("=" * 70)
print()

# Try to access OneCore voices directly with System.Speech.Synthesis
ps_register = r"""
[System.Reflection.Assembly]::LoadWithPartialName("System.Speech") | Out-Null

# Try to load OneCore voices by creating synthesizer with OneCore hints
$tts = New-Object System.Speech.Synthesis.SpeechSynthesizer

Write-Host "Current SAPI5 voices: $($tts.GetInstalledVoices().Count)"

# Check if we can access OneCore registry for voice names
$oneCoreRegPath = "HKLM:\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens"
$voices = Get-ChildItem $oneCoreRegPath -ErrorAction SilentlyContinue

if ($voices) {
    Write-Host ""
    Write-Host "Attempting to use OneCore voices:"
    
    foreach ($voiceToken in $voices) {
        $voiceName = $voiceToken.PSChildName
        Write-Host "  Trying: $voiceName"
        
        try {
            $tts.SelectVoice($voiceName)
            Write-Host "    ✓ SUCCESS!"
        } catch {
            Write-Host "    ✗ Not accessible to SAPI5"
        }
    }
}

# Alternative: Try to manually load from Windows.Media APIs if available
Write-Host ""
Write-Host "Checking for Windows.Media.SpeechSynthesis API..."
try {
    [Windows.Media.SpeechSynthesis.SpeechSynthesizer] | Out-Null
    Write-Host "  ✓ Windows.Media.SpeechSynthesis available"
    Write-Host "  This API supports all Windows 11 voices including Narrator voices"
    Write-Host "  A Python library would be needed to use this directly"
} catch {
    Write-Host "  ✗ Windows.Media.SpeechSynthesis not available in this context"
}
"""

result = subprocess.run(
    ["powershell", "-NoProfile", "-Command", ps_register],
    capture_output=True,
    text=True,
    timeout=10
)

print(result.stdout)

print()
print("=" * 70)
print("NEXT STEPS")
print("=" * 70)
print()

print("❌ Challenge: Narrator voices don't align with SAPI5")
print()
print("The Narrator voices (Jenny, Aria, Guy) are installed in Windows 11")
print("but they use Microsoft's newer Windows.Media API, not the older SAPI5.")
print()
print("SOLUTION: Use a different approach:")
print()
print("Option A: Download 'Aria' voice (more likely to register)")
print("  1. Settings > Accessibility > Text-to-speech > Manage voices")
print("  2. Install 'Microsoft Aria'")
print("  3. Run: python find_narrator_jenny.py")
print("     (Updated to also search for Aria)")
print()
print("Option B: Use the High-Quality David or Zira")
print("  • These are the best SAPI5 voices available")
print("  • Run: python generate_both_voices.py")
print()
print("Option C: Use a Python TTS Library")
print("  • Libraries like 'pyttsx3' or 'edge-tts' may have better")
print("    support for Narrator voices")
print("  • These are external packages (not built-in)")
print()
