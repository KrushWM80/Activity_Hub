"""Unstick Narrator voices - force SAPI5 registration."""

import subprocess
import os
import time

print("=" * 70)
print("UNSTICKING NARRATOR VOICES FOR SAPI5")
print("=" * 70)
print()

# Method 1: Restart Speech service
print("METHOD 1: Restart Windows Speech Service")
print("-" * 70)

ps_restart_service = r"""
Write-Host "Stopping Speech service..."
Stop-Service -Name "Speech" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

Write-Host "Starting Speech service..."
Start-Service -Name "Speech" -ErrorAction SilentlyContinue
Start-Sleep -Seconds 3

Write-Host "Checking service status..."
$service = Get-Service -Name "Speech" -ErrorAction SilentlyContinue
if ($service.Status -eq "Running") {
    Write-Host "✓ Speech service restarted"
} else {
    Write-Host "✗ Could not restart Speech service"
}
"""

result = subprocess.run(
    ["powershell", "-NoProfile", "-Command", ps_restart_service],
    capture_output=True,
    text=True,
    timeout=15
)
print(result.stdout)
print()

# Method 2: Clear SAPI5 voice cache
print("METHOD 2: Clear Voice Cache and Re-scan")
print("-" * 70)

ps_clear_cache = r"""
# Narrator voice cache locations
$cachePaths = @(
    "$env:LOCALAPPDATA\Microsoft\Speech",
    "$env:APPDATA\Microsoft\Speech"
)

foreach ($path in $cachePaths) {
    if (Test-Path $path) {
        Write-Host "Clearing: $path"
        Get-ChildItem $path -Recurse -Filter "*.dat" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
    }
}

Write-Host "✓ Cache cleared"
"""

result = subprocess.run(
    ["powershell", "-NoProfile", "-Command", ps_clear_cache],
    capture_output=True,
    text=True,
    timeout=10
)
print(result.stdout)
print()

# Method 3: Force re-enumerate voices
print("METHOD 3: Force Voice Re-enumeration")
print("-" * 70)

ps_reenumerate = r"""
[System.Reflection.Assembly]::LoadWithPartialName("System.Speech") | Out-Null

# Create fresh synthesizer instances to force re-scan
Write-Host "Creating fresh TTS instances..."

$tts1 = New-Object System.Speech.Synthesis.SpeechSynthesizer
$count1 = $tts1.GetInstalledVoices().Count
Write-Host "  Attempt 1: Found $count1 voices"

Start-Sleep -Seconds 1

$tts2 = New-Object System.Speech.Synthesis.SpeechSynthesizer
$count2 = $tts2.GetInstalledVoices().Count
Write-Host "  Attempt 2: Found $count2 voices"

if ($count2 -gt $count1) {
    Write-Host "✓ Additional voices detected on second scan"
} else {
    Write-Host "  (Same number of voices)"
}
"""

result = subprocess.run(
    ["powershell", "-NoProfile", "-Command", ps_reenumerate],
    capture_output=True,
    text=True,
    timeout=10
)
print(result.stdout)
print()

# Method 4: Check Narrator voice registry paths
print("METHOD 4: Verify Narrator Voice Registry Paths")
print("-" * 70)

ps_check_registry = r"""
Write-Host "Checking SAPI5 voice registry..."
$regPath = "HKLM:\SOFTWARE\Microsoft\Speech\Voices\Tokens"
$voices = Get-ChildItem $regPath -ErrorAction SilentlyContinue

Write-Host "SAPI5 registered voices:"
foreach ($voice in $voices) {
    Write-Host "  - $($voice.PSChildName)"
}

Write-Host ""
Write-Host "Checking OneCore voice registry..."
$oneCoreRegPath = "HKLM:\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens"
$oneCore = Get-ChildItem $oneCoreRegPath -ErrorAction SilentlyContinue

if ($oneCore) {
    Write-Host "OneCore registered voices:"
    foreach ($voice in $oneCore) {
        Write-Host "  - $($voice.PSChildName)"
    }
} else {
    Write-Host "(No OneCore voices in registry)"
}

Write-Host ""
Write-Host "Looking for Narrator voice installation..."
$appDataVoices = Get-ChildItem "$env:LOCALAPPDATA\MicrosoftEdge\User Data" -Filter "*voice*" -ErrorAction SilentlyContinue
if ($appDataVoices) {
    Write-Host "Found voice-related items in AppData"
}
"""

result = subprocess.run(
    ["powershell", "-NoProfile", "-Command", ps_check_registry],
    capture_output=True,
    text=True,
    timeout=10
)
print(result.stdout)
print()

# Method 5: Final check
print("METHOD 5: Final Voice Availability Check")
print("-" * 70)

ps_final_check = r"""
[System.Reflection.Assembly]::LoadWithPartialName("System.Speech") | Out-Null
$tts = New-Object System.Speech.Synthesis.SpeechSynthesizer
$voices = $tts.GetInstalledVoices()

Write-Host "Voices now available:"
foreach ($v in $voices) {
    Write-Host "  ✓ $($v.VoiceInfo.Name)"
}

if ($voices.Count -gt 2) {
    Write-Host ""
    Write-Host "✓ NEW VOICES DETECTED!"
} else {
    Write-Host ""
    Write-Host "⚠ Still only $($voices.Count) voices available"
}
"""

result = subprocess.run(
    ["powershell", "-NoProfile", "-Command", ps_final_check],
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

# Check result and advise
if "NEW VOICES DETECTED" in result.stdout:
    print("✅ SUCCESS! New voices are now available.")
    print()
    print("Run: python generate_jenny_guy.py")
else:
    print("⚠️  Unsticking didn't fully work. Try these fallback options:")
    print()
    print("Option A: Restart Your Computer")
    print("  • Close everything, restart Windows")
    print("  • Sometimes Windows needs a full restart to process voice changes")
    print()
    print("Option B: Use Aria instead of Jenny")
    print("  1. Settings > Accessibility > Text-to-speech > Manage voices")
    print("  2. Uninstall Jenny")
    print("  3. Install Microsoft Aria")
    print("  4. Restart computer")
    print("  5. Run: python list_exact_voices.py")
    print()
    print("Option C: Use David or Zira (Works Now)")
    print("  • Both are available and high-quality")
    print("  • Run: python generate_both_voices.py")
    print()
    print("Option D: Use Edge-TTS (Online, Supports All Voices)")
    print("  • Install: pip install edge-tts")
    print("  • Run: edge-tts --voice en-US-JennyNeural --output-file output.mp3")
    print()
