"""Attempt to register and activate the downloaded Microsoft natural voices."""

import subprocess
import os

print("=" * 70)
print("ACTIVATING MICROSOFT NATURAL VOICES (JENNY, GUY)")
print("=" * 70)
print()

# Try using Windows Package Manager to install voices
print("Attempting to install voices via Windows Package Manager (WinGet)...")
print()

voices_to_install = [
    "Microsoft.OneCore.Jenny.US",
    "Microsoft.OneCore.Guy.US",
]

for voice_pkg in voices_to_install:
    print(f"Installing {voice_pkg}...")
    result = subprocess.run(
        ["winget", "install", "--id", voice_pkg, "-e", "--accept-source-agreements", "--accept-package-agreements"],
        capture_output=True,
        text=True,
        timeout=120
    )
    
    if result.returncode == 0:
        print(f"  ✓ Success!")
    else:
        # Show just first 200 chars of output
        output = (result.stdout + result.stderr)[:200]
        print(f"  Note: {output}")
    print()

print("=" * 70)
print("ALTERNATIVE: Manual Activation")
print("=" * 70)
print()
print("If WinGet didn't work:")
print()
print("1. Open Settings > Apps > Installed apps")
print("2. Search for 'Jenny' or 'Guy'")
print("3. If you see them:")
print("   • Click the three dots (...)")
print("   • Select 'Modify' or 'Install'")
print("   • Follow the prompts")
print()
print("4. Or:")
print("   • Settings > Accessibility > Text-to-speech")
print("   • Click 'Manage voices'")
print("   • Click 'Add voices'")
print("   • Find and click 'Get' on Microsoft Jenny and Microsoft Guy")
print()
print("5. After installation/activation:")
print("   • Restart PowerShell (close all and open new window)")
print("   • Run: python generate_jenny_guy.py")
print()
