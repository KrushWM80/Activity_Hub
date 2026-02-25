"""Check if Jenny is a Windows Capability feature that needs enabling."""

import subprocess

print("=" * 70)
print("CHECKING JENNY AS WINDOWS CAPABILITY")
print("=" * 70)
print()

ps_capability = r"""
Write-Host "Checking Windows Capabilities for speech/voice features..."
Write-Host ""

# Get all capabilities
$capabilities = Get-WindowsCapability -Online | Where-Object {$_.Name -like "*speech*" -or $_.Name -like "*voice*" -or $_.Name -like "*narrator*"}

if ($capabilities) {
    Write-Host "Found speech-related capabilities:"
    foreach ($cap in $capabilities) {
        Write-Host "  Name: $($cap.Name)"
        Write-Host "  State: $($cap.State)"
        Write-Host ""
    }
    
    # Check for disabled ones
    $disabled = $capabilities | Where-Object {$_.State -eq "Disabled"}
    if ($disabled) {
        Write-Host "Attempting to enable disabled capabilities..."
        foreach ($cap in $disabled) {
            Write-Host "  Enabling: $($cap.Name)"
            try {
                Add-WindowsCapability -Online -Name $cap.Name -ErrorAction SilentlyContinue
                Write-Host "    ✓ Enabled"
            } catch {
                Write-Host "    ✗ Could not enable"
            }
        }
    }
} else {
    Write-Host "No speech-related capabilities found"
}

Write-Host ""
Write-Host "Checking provisioned language packs..."
$langPacks = Get-WindowsCapability -Online | Where-Object {$_.Name -like "*Language*en-US*"}
Write-Host "US English packs: $($langPacks.Count)"
foreach ($pack in $langPacks | Select-Object -First 5) {
    Write-Host "  - $($pack.Name) [$($pack.State)]"
}
"""

result = subprocess.run(
    ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_capability],
    capture_output=True,
    text=True,
    timeout=60
)

print(result.stdout)

print()
print("=" * 70)
print("CHECKING WMI/CIM FOR VOICE INFO")
print("=" * 70)
print()

ps_wmi = r"""
# Try WMI/CIM to find speech synthesizers
try {
    $voices = Get-CimInstance -Class "Win32_PnPEntity" | Where-Object {$_.Name -like "*speech*" -or $_.Name -like "*narrator*"}
    if ($voices) {
        Write-Host "Found speech devices via WMI:"
        foreach ($v in $voices) {
            Write-Host "  - $($v.Name)"
        }
    } else {
        Write-Host "No speech devices found in WMI"
    }
} catch {
    Write-Host "Could not query WMI"
}

Write-Host ""
Write-Host "Checking if Advanced Options reveals anything..."
$jennyApp = Get-AppxPackage -AllUsers | Where-Object {$_.PublisherID -like "*8wekyb3d8bbwe*"}
if ($jennyApp) {
    Write-Host "Microsoft Store apps found:"
    foreach ($app in $jennyApp) {
        if ($app.Name -like "*speech*" -or $app.Name -like "*voice*" -or $app.Name -like "*narrator*") {
            Write-Host "  - $($app.Name)"
        }
    }
}
"""

result = subprocess.run(
    ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_wmi],
    capture_output=True,
    text=True,
    timeout=30
)

print(result.stdout)

print()
print("=" * 70)
print("RECOMMENDATION")
print("=" * 70)
print()
print("Since Jenny shows in Settings but isn't accessible to applications:")
print()
print("✅ BEST SOLUTION: Cleanly uninstall and reinstall")
print()
print("Steps:")
print("  1. Settings > Apps > Installed apps")
print("  2. Search 'Jenny'")
print("  3. Click the three dots (...)")
print("  4. Select 'Uninstall'")
print("  5. Wait for complete uninstall")
print("  6. Empty Recycle Bin")
print()
print("  7. Then reinstall fresh:")
print("     • Settings > Accessibility > Text-to-speech")
print("     • Click 'Manage voices'")
print("     • Click 'Add voices'")
print("     • Search 'Microsoft Jenny'")
print("     • Click 'Get' button")
print("     • Wait for 100% installation")
print("     • Restart computer")
print()
print("  8. After restart, run: python list_exact_voices.py")
print()
print("🚀 OR use David/Zira RIGHT NOW:")
print("  python generate_both_voices.py")
print()
