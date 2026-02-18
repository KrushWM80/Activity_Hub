# Start Server in Isolated Process
# This script starts the Python server launcher in a completely isolated PowerShell process

param(
    [switch]$NoWindow = $false
)

$scriptPath = Join-Path $PSScriptRoot "server_launcher.py"
$launcherPath = Join-Path $PSScriptRoot "server_launcher.py"

Write-Host "[*] Starting server in isolated process..."
Write-Host "[*] Launcher: $launcherPath"

$argumentList = @("-NoExit", "-Command", "python '$launcherPath'")

if ($NoWindow) {
    # Start with no visible window
    $null = Start-Process powershell -ArgumentList $argumentList -WindowStyle Hidden
    Write-Host "[OK] Server started in background (hidden window)"
} else {
    # Start with visible window (recommended for monitoring)
    Start-Process powershell -ArgumentList $argumentList
    Write-Host "[OK] Server started in isolated window"
}

Write-Host "[*] Server is now running independently"
Write-Host "[*] Access the API at: http://localhost:8001"
Write-Host "[*] Health check: http://localhost:8001/api/health"
