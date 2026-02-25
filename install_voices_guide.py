"""
Guide for downloading Windows 11 natural voices.

Method 1: Manual Installation (Recommended - Easy)
=================================================
1. Press Windows + I to open Settings
2. Go to: Accessibility > Text-to-speech
3. Under "Voice", click "Manage voices"
4. Click "Add voices" button
5. Select and download:
   - Microsoft Aria Desktop (Female, US)
   - Microsoft Jenny Desktop (Female, US)  
   - Microsoft Guy Desktop (Male, US)
6. Wait for download to complete
7. Restart your application or run the voice comparison again

These natural voices will then appear in your SAPI5 voice list and 
have much more natural, human-like pronunciation than the desktop voices.

Method 2: Automated Installation (Via WinGet - if available)
===========================================================
"""

import subprocess
import os

def check_if_voices_installed():
    """Check if new voices are available."""
    ps_script = r"""
[System.Reflection.Assembly]::LoadWithPartialName("System.Speech") | Out-Null
$tts = New-Object System.Speech.Synthesis.SpeechSynthesizer
$voices = $tts.GetInstalledVoices()

Write-Host "Current SAPI5 Voices:"
foreach ($v in $voices) {
    Write-Host "  - $($v.VoiceInfo.Name)"
}
"""
    
    result = subprocess.run(
        ["powershell", "-Command", ps_script],
        capture_output=True,
        text=True
    )
    
    return result.stdout

print("=" * 70)
print("WINDOWS 11 NATURAL VOICE INSTALLATION GUIDE")
print("=" * 70)
print()
print("Your system: Windows 11 Build 26100")
print()
print("CURRENTLY INSTALLED VOICES:")
print(check_if_voices_installed())
print()
print("=" * 70)
print("TO INSTALL NEW VOICES:")
print("=" * 70)
print()
print("STEP 1: Open Windows Settings")
print("  • Press Windows + I")
print()
print("STEP 2: Navigate to Text-to-Speech settings")
print("  • Click: Accessibility (left menu)")
print("  • Click: Text-to-speech")
print()
print("STEP 3: Download natural voices")
print("  • Find 'Voice' section")
print("  • Click 'Manage voices'")
print("  • Click 'Add voices'")
print("  • Select and download:")
print("     ✓ Microsoft Aria (Female, US)")
print("     ✓ Microsoft Jenny (Female, US)")
print("     ✓ Microsoft Guy (Female, US)")
print()
print("STEP 4: After installation")
print("  • Come back here and run: python check_voices.py")
print("  • Then: python generate_both_voices.py")
print("  • Your new voices will be available for comparison!")
print()
print("=" * 70)
print("WHY THESE VOICES?")
print("=" * 70)
print()
print("Microsoft Aria:")
print("  • Female voice")
print("  • Professional quality")
print("  • Best for business/store communications")
print()
print("Microsoft Jenny:")
print("  • Female voice")
print("  • Friendly, engaging tone")
print("  • Good for announcements")
print()
print("Microsoft Guy:")
print("  • Male voice")
print("  • Professional quality")
print("  • Alternative to David Desktop")
print()
print("These are Azure-quality voices that sound much more natural than")
print("the legacy desktop voices (David, Zira).")
print()
