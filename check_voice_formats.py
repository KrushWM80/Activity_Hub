"""Try alternative voice name formats and check registry."""

import subprocess
import os
import winreg

print("=" * 70)
print("CHECKING FOR JENNY & GUY IN ALL LOCATIONS")
print("=" * 70)
print()

# Check registry for all speech-related keys
print("Checking Windows Registry...")
try:
    reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Speech\Voices\Tokens")
    idx = 0
    print("Found voices in registry:")
    while True:
        try:
            voice_name = winreg.EnumKey(reg_key, idx)
            if "jenny" in voice_name.lower() or "guy" in voice_name.lower():
                print(f"  ⭐ {voice_name}")
            else:
                print(f"  • {voice_name}")
            idx += 1
        except:
            break
except Exception as e:
    print(f"  Error reading registry: {e}")

print()
print("=" * 70)
print("TRYING ALTERNATIVE VOICE NAMES")
print("=" * 70)
print()

# Try various voice name formats
voice_patterns = [
    "Microsoft Jenny",
    "Microsoft Guy",
    "Microsoft Jenny Desktop",
    "Microsoft Guy Desktop",
    "Microsoft Jenny Natural",
    "Microsoft Guy Natural",
    "Microsoft Jenny OneCore", 
    "Microsoft Guy OneCore",
    "Microsoft OneCore Jenny",
    "Microsoft OneCore Guy",
    "Jenny",
    "Guy",
]

ps_test_voices = """
[System.Reflection.Assembly]::LoadWithPartialName("System.Speech") | Out-Null
$tts = New-Object System.Speech.Synthesis.SpeechSynthesizer

foreach ($voiceName in @({voice_list})) {{
    try {{
        $tts.SelectVoice($voiceName)
        Write-Host "✓ FOUND: $voiceName"
    }} catch {{
        # Voice not found, skip
    }}
}}
"""

voice_list_str = ",".join([f'"{v}"' for v in voice_patterns])
ps_script = ps_test_voices.format(voice_list=voice_list_str)

result = subprocess.run(
    ["powershell", "-Command", ps_script],
    capture_output=True,
    text=True,
    timeout=10
)

if result.stdout.strip():
    print(result.stdout)
else:
    print("No alternative voice names found.")

print()
print("=" * 70)
print("REQUIRED ACTION")
print("=" * 70)
print()
print("⚠️  The new voices (Jenny & Guy) haven't fully registered yet.")
print()
print("Option 1: Wait and Retry (30 seconds)")
print("  • Sometimes Windows needs time to process new voice installations")
print("  • Wait 30 seconds, then run: python list_exact_voices.py")
print()
print("Option 2: Verify in Settings")
print("  • Open Settings > Accessibility > Text-to-speech")
print("  • Scroll to 'Voice' section")
print("  • Click 'Manage voices'")
print("  • Check if Jenny and Guy show as 'Installed' (not just 'Available')")
print("  • If they say 'Install', click to install them")
print("  • If they say 'Installed', they may need a restart to activate")
print()
print("Option 3: Restart Windows")
print("  • New voice installations sometimes require a full system restart")
print("  • Restart your computer and try again")
print()
print("Option 4: Fresh Install")
print("  • Remove Jenny & Guy from Settings")
print("  • Reinstall them fresh from Settings > Accessibility > Text-to-speech")
print()
