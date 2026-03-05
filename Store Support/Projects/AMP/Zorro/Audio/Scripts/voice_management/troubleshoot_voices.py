"""Troubleshoot and re-enable the newly installed voices."""

import os
import subprocess

print("=" * 70)
print("VOICE INSTALLATION TROUBLESHOOTING")
print("=" * 70)
print()

# Step 1: Check current voices
print("STEP 1: Checking currently registered voices...")
ps_check = r"""
[System.Reflection.Assembly]::LoadWithPartialName("System.Speech") | Out-Null
$tts = New-Object System.Speech.Synthesis.SpeechSynthesizer
Write-Host "System voices loaded: $($tts.GetInstalledVoices().Count)"
$tts.GetInstalledVoices() | ForEach-Object { Write-Host "  - $($_.VoiceInfo.Name)" }
"""

result = subprocess.run(
    ["powershell", "-Command", ps_check],
    capture_output=True,
    text=True
)
print(result.stdout)

# Step 2: Suggest enabling voices
print()
print("STEP 2: To properly enable the new voices:")
print()
print("Option A: Restart PowerShell")
print("  • Sometimes new voices don't load until PowerShell is restarted")
print("  • Close all PowerShell windows and open a new one")
print()
print("Option B: Verify voices in Settings")
print("  • Open Settings > Accessibility > Text-to-speech")
print("  • Ensure voices are marked as 'Installed'")
print("  • Check that they're not disabled")
print()
print("Option C: Reinstall voices")
print("  • Settings > Accessibility > Text-to-speech > Manage voices")
print("  • Remove and reinstall Microsoft Jenny and Microsoft Guy")
print()

# Step 3: Check if voices are in registry
print("STEP 3: Checking Windows Registry for voices...")
ps_registry = r"""
$regPath = "HKLM:\SOFTWARE\Microsoft\Speech\Voices\Tokens"
$voices = Get-ChildItem $regPath -ErrorAction SilentlyContinue | Select-Object PSChildName

if ($voices) {
    Write-Host "Voices found in registry:"
    $voices | ForEach-Object { Write-Host "  - $($_.PSChildName)" }
} else {
    Write-Host "No voices found in registry - may need reinstall"
}
"""

result = subprocess.run(
    ["powershell", "-Command", ps_registry],
    capture_output=True,
    text=True
)
print(result.stdout)

print()
print("=" * 70)
print("NEXT STEPS")
print("=" * 70)
print()
print("1. Try one of the options above (restart PowerShell is quickest)")
print("2. Run this script again to verify voices are registered")
print("3. Once registered, run: python generate_jenny_guy.py")
print()
