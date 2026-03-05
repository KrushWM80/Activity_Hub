"""Deep diagnostic of Narrator voice installation status."""

import subprocess
import os

print("=" * 70)
print("DEEP DIAGNOSTIC - NARRATOR VOICE INSTALLATION")
print("=" * 70)
print()

# Check what voices are claimed to be installed in Settings
ps_diagnostic = r"""
Write-Host "Checking Windows Speech Settings..."
Write-Host ""

# Check Narrator voice files in common locations
$commonPaths = @(
    "$env:ProgramFiles\WindowsApps",
    "$env:LOCALAPPDATA\Microsoft\Speech",
    "$env:APPDATA\Microsoft\Speech",
    "C:\Windows\System32\Speech"
)

foreach ($path in $commonPaths) {
    if (Test-Path $path) {
        Write-Host "Checking: $path"
        $items = Get-ChildItem $path -Filter "*jenny*" -Recurse -ErrorAction SilentlyContinue
        if ($items) {
            Write-Host "  ✓ Found Jenny-related files:"
            foreach ($item in $items) {
                Write-Host "    - $($item.Name)"
            }
        } else {
            Write-Host "  (No Jenny files found)"
        }
    }
}

Write-Host ""
Write-Host "Checking Narrator voice installation via Windows Settings..."
Write-Host ""

# Try to get installed language packs
$speechPacks = Get-AppxPackage -Name "*SpeechSynthesis*" -ErrorAction SilentlyContinue
if ($speechPacks) {
    Write-Host "Speech Synthesis packages found:"
    foreach ($pack in $speechPacks) {
        Write-Host "  - $($pack.Name)"
        Write-Host "    Version: $($pack.Version)"
        Write-Host "    Status: $($pack.Status)"
    }
} else {
    Write-Host "No Speech Synthesis packages found"
}

Write-Host ""
Write-Host "Checking for OneCore language packs..."
$langPacks = Get-WindowsCapability -Online -ErrorAction SilentlyContinue | Where-Object {$_.Name -like "*Speech*"}
if ($langPacks) {
    Write-Host "Language packs with Speech capability:"
    foreach ($pack in $langPacks) {
        Write-Host "  - $($pack.Name)"
        Write-Host "    State: $($pack.State)"
    }
} else {
    Write-Host "No Speech-related language packs installed"
}

Write-Host ""
Write-Host "Registry check - SAPI voices..."
$regPath = "HKLM:\SOFTWARE\Microsoft\Speech\Voices\Tokens"
$sapi = Get-ChildItem $regPath -ErrorAction SilentlyContinue
Write-Host "SAPI5 voices: $($sapi.Count)"
foreach ($v in $sapi) {
    Write-Host "  - $($v.PSChildName)"
}

Write-Host ""
Write-Host "Registry check - OneCore voices..."
$oneCoreRegPath = "HKLM:\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens"
$oneCore = Get-ChildItem $oneCoreRegPath -ErrorAction SilentlyContinue
Write-Host "OneCore voices: $($oneCore.Count)"
foreach ($v in $oneCore) {
    Write-Host "  - $($v.PSChildName)"
}
"""

result = subprocess.run(
    ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_diagnostic],
    capture_output=True,
    text=True,
    timeout=30
)

print(result.stdout)

print()
print("=" * 70)
print("ANALYSIS")
print("=" * 70)
print()

if "Jenny" in result.stdout or "jenny" in result.stdout:
    print("✓ Jenny files/registry entries detected")
    print()
    print("RECOMMENDATION:")
    print("  1. Restart your computer (full restart)")
    print("  2. Run: python list_exact_voices.py")
    print("  3. Try: python generate_with_windows_media_api.py")
else:
    print("✗ NO Jenny files or registry entries found")
    print()
    print("CONCLUSION:")
    print("  Jenny installation did NOT complete successfully")
    print()
    print("TO FIX:")
    print("  1. Open Settings > Apps > Installed apps")
    print("  2. Search for 'Jenny'")
    print("  3. If you see it:")
    print("     • Click the '...' menu")
    print("     • Select 'Repair' or 'Reinstall'")
    print("     • OR: Uninstall and reinstall fresh")
    print()
    print("  4. If you DON'T see it:")
    print("     • Go to Settings > Accessibility > Text-to-speech")
    print("     • Click 'Manage voices'")
    print("     • Click 'Add voices'")
    print("     • Find 'Microsoft Jenny'")
    print("     • Click 'Get' or 'Install'")
    print("     • Wait for installation to complete (should show checkmark)")
    print()
    print("  5. After installation:")
    print("     • Restart your computer")
    print("     • Run: python list_exact_voices.py")
    print()

print("=" * 70)
print("ALTERNATIVE: Use available voices NOW")
print("=" * 70)
print()
print("David and Zira are professional, high-quality voices")
print("Run: python generate_both_voices.py")
print()
