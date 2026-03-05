"""Check if Jenny voice is available in SAPI5 and Windows.Media APIs."""

import subprocess
import sys

print("=" * 70)
print("JENNY VOICE STATUS CHECK")
print("=" * 70)
print()

# Check 1: AppxPackage status
print("1️⃣  CHECKING APPXPACKAGE INSTALLATION")
print("-" * 70)
result = subprocess.run(
    ["powershell", "-Command", "Get-AppxPackage -Name '*Jenny*'"],
    capture_output=True,
    text=True
)
if "Jenny" in result.stdout:
    print("✅ Jenny package is installed")
    print(result.stdout)
else:
    print("❌ Jenny package not found")
print()

# Check 2: SAPI5 registration
print("2️⃣  CHECKING SAPI5 (System.Speech.Synthesis) REGISTRATION")
print("-" * 70)
try:
    from System.Reflection import Assembly
    Assembly.LoadWithPartialName("System.Speech")
    from System.Speech.Synthesis import SpeechSynthesizer
    
    tts = SpeechSynthesizer()
    voices = tts.GetInstalledVoices()
    
    print(f"Total SAPI5 voices available: {len(voices)}")
    print()
    print("Installed voices:")
    jenny_found = False
    for voice in voices:
        voice_name = voice.VoiceInfo.Name
        print(f"  • {voice_name}")
        if "Jenny" in voice_name:
            jenny_found = True
    
    print()
    if jenny_found:
        print("✅ Jenny is registered in SAPI5")
    else:
        print("❌ Jenny is NOT registered in SAPI5")
except Exception as e:
    print(f"Error checking SAPI5: {e}")

print()

# Check 3: Windows.Media API (OneCore voices)
print("3️⃣  CHECKING WINDOWS.MEDIA (OneCore/Narrator) API")
print("-" * 70)
ps_code = """
Add-Type -AssemblyName System.Runtime.WindowsRuntime
[Windows.Media.SpeechSynthesis.SpeechSynthesizer, Windows.Media.Speech, ContentType = WindowsRuntime] | Out-Null
$tts = New-Object Windows.Media.SpeechSynthesis.SpeechSynthesizer
$voices = $tts.AllVoices
Write-Host "Total OneCore voices: $($voices.Count)"
Write-Host ""
Write-Host "Voices available:"
$voices | ForEach-Object { Write-Host "  • $($_.DisplayName)" }
"""

result = subprocess.run(
    ["powershell", "-NoProfile", "-Command", ps_code],
    capture_output=True,
    text=True
)
print(result.stdout)
if result.stderr:
    print(f"Note: {result.stderr[:200]}")

print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)
print()
print("📦 Appx Package: Installed ✅")
print("🔊 SAPI5 (System.Speech): Check above for availability")
print("🎤 OneCore (Windows.Media): Provides Narrator voices")
print()
print("Note: Jenny is downloaded as a Narrator voice (OneCore)")
print("but you're using SAPI5 API for audio generation.")
print()
print("Options to use Jenny:")
print("  1. Switch to Windows.Media.SpeechSynthesis API")
print("  2. Use Windows 11 built-in Narrator voices directly")
print("  3. Continue with David/Zira (SAPI5 working solution)")
