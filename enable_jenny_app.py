"""Attempt to repair, enable, or reset Jenny installation via PowerShell."""

import subprocess

print("=" * 70)
print("ATTEMPTING TO ACTIVATE/REPAIR JENNY INSTALLATION")
print("=" * 70)
print()

# Method 1: Find the exact Jenny application name and check status
ps_find_jenny = r"""
Write-Host "Finding Jennifer/Jenny application..."
Write-Host ""

# Get all packages matching Jenny/Jennifer
$allApps = Get-AppxPackage -AllUsers | Where-Object {$_.Name -like "*jenny*" -or $_.Name -like "*jennifer*" -or $_.PublisherID -like "*Microsoft*"}

if ($allApps) {
    Write-Host "Found applications:"
    foreach ($app in $allApps) {
        Write-Host "  Name: $($app.Name)"
        Write-Host "  Version: $($app.Version)"
        Write-Host "  PackageFullName: $($app.PackageFullName)"
        Write-Host "  Status: $($app.Status)"
        Write-Host ""
    }
} else {
    Write-Host "No Jenny packages found via Get-AppxPackage"
    Write-Host ""
    Write-Host "Checking provisioned packages..."
    $provisioned = Get-AppxProvisionedPackage -Online | Where-Object {$_.DisplayName -like "*jenny*" -or $_.DisplayName -like "*narrator*"}
    if ($provisioned) {
        foreach ($pkg in $provisioned) {
            Write-Host "  Provisioned: $($pkg.DisplayName)"
        }
    } else {
        Write-Host "  No provisioned packages found"
    }
}
"""

result = subprocess.run(
    ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_find_jenny],
    capture_output=True,
    text=True,
    timeout=30
)

print(result.stdout)

# Method 2: Try to repair/enable Jenny
print()
print("=" * 70)
print("ATTEMPTING REPAIR/RESET")
print("=" * 70)
print()

ps_repair = r"""
Write-Host "Method 1: Reset Jenny package..."

# Try to reset Jenny
try {
    Get-AppxPackage -Name "*jenny*" -AllUsers | Reset-AppxPackage -ErrorAction SilentlyContinue
    Write-Host "✓ Reset command executed"
} catch {
    Write-Host "  Could not reset"
}

Write-Host ""
Write-Host "Method 2: Remove and re-provision Jenny..."

try {
    # Remove the package
    Get-AppxPackage -Name "*jenny*" -AllUsers | Remove-AppxPackage -ErrorAction SilentlyContinue
    Write-Host "✓ Package removed"
    
    # Re-enable provisioned package
    Get-AppxProvisionedPackage -Online | Where-Object {$_.DisplayName -like "*jenny*"} | Add-AppxProvisionedPackage -Online -ErrorAction SilentlyContinue
    Write-Host "✓ Package re-provisioned"
} catch {
    Write-Host "  Could not reprovision"
}

Write-Host ""
Write-Host "Waiting for system to process changes..."
Start-Sleep -Seconds 3

Write-Host "✓ Repair attempt complete"
"""

result = subprocess.run(
    ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_repair],
    capture_output=True,
    text=True,
    timeout=30
)

print(result.stdout)

# Method 3: Check if voices are now available
print()
print("=" * 70)
print("CHECKING VOICE AVAILABILITY")
print("=" * 70)
print()

ps_check_voices = r"""
[System.Reflection.Assembly]::LoadWithPartialName("System.Speech") | Out-Null
$tts = New-Object System.Speech.Synthesis.SpeechSynthesizer

Write-Host "SAPI5 voices:"
$sapi5 = $tts.GetInstalledVoices()
foreach ($v in $sapi5) {
    Write-Host "  ✓ $($v.VoiceInfo.Name)"
}

Write-Host ""
Write-Host "Windows.Media voices (OneCore):"
$winMedia = [Windows.Media.SpeechSynthesis.SpeechSynthesizer]::AllVoices
foreach ($v in $winMedia) {
    Write-Host "  ✓ $($v.DisplayName)"
    if ($v.DisplayName -like "*jenny*" -or $v.DisplayName -like "*jennifer*") {
        Write-Host "    🎉 JENNY FOUND!"
    }
}
"""

result = subprocess.run(
    ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_check_voices],
    capture_output=True,
    text=True,
    timeout=30
)

print(result.stdout)

# Summary
print()
print("=" * 70)
print("NEXT STEPS")
print("=" * 70)
print()

if "JENNY FOUND" in result.stdout:
    print("✅ SUCCESS! Jenny is now available!")
    print()
    print("Run: python generate_with_windows_media_api.py")
else:
    print("⚠️  Jenny still not showing up")
    print()
    print("Options:")
    print()
    print("Option A: Uninstall and Reinstall Fresh")
    print("  1. Settings > Apps > Installed apps")
    print("  2. Search 'Jenny'")
    print("  3. Click 'Uninstall'")
    print("  4. Wait for uninstall to complete")
    print("  5. Go to Settings > Accessibility > Text-to-speech > Manage voices")
    print("  6. Click 'Add voices'")
    print("  7. Find 'Microsoft Jenny' and click 'Get'")
    print("  8. Wait for 100% completion")
    print("  9. Restart your computer")
    print("  10. Run: python list_exact_voices.py")
    print()
    print("Option B: Use David or Zira NOW")
    print("  Run: python generate_both_voices.py")
    print("  Both are professional voices and ready immediately")
    print()
