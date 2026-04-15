# Safe Activity Hub Server Startup with PID Tracking
# Usage: .\start_server_safe.ps1
# Location: Activity Hub\Interface\

param(
    [switch]$ForceRestart = $false
)

$RootDir = Split-Path -Parent $PSScriptRoot
$ServerScript = "Interface\activity_hub_server.py"
$ServerPath = Join-Path $RootDir $ServerScript
$PidFile = Join-Path $RootDir "PIDS\activity_hub_server.pid"
$PidDir = Split-Path -Parent $PidFile
$Port = 8088

Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Activity Hub Server - Safe Start" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan

# Create PID directory if it doesn't exist
if (-not (Test-Path $PidDir)) {
    New-Item -ItemType Directory -Path $PidDir -Force | Out-Null
    Write-Host "✓ Created PID tracking directory" -ForegroundColor Green
}

# Check if already running
if ($ForceRestart -eq $false -and (Test-Path $PidFile)) {
    $OldPid = Get-Content $PidFile -Raw
    $ProcessCheck = Get-Process -Id $OldPid -ErrorAction SilentlyContinue
    
    if ($ProcessCheck) {
        Write-Host "⚠ Activity Hub already running on PID $OldPid (Port $Port)" -ForegroundColor Yellow
        Write-Host "✓ Listening on http://localhost:$Port/activity-hub" -ForegroundColor Green
        return
    }
}

# Kill any old processes with this PID
if (Test-Path $PidFile) {
    $OldPid = Get-Content $PidFile -Raw
    try {
        Stop-Process -Id $OldPid -Force -ErrorAction SilentlyContinue
        Start-Sleep -Milliseconds 500
        Write-Host "✓ Cleaned up old process (PID $OldPid)" -ForegroundColor Green
    } catch { }
}

# Start the server
Write-Host "`n▶ Starting Activity Hub Server..." -ForegroundColor Cyan
$env:GOOGLE_APPLICATION_CREDENTIALS = "$env:APPDATA\gcloud\application_default_credentials.json"

$proc = Start-Process `
    -FilePath "$(Join-Path $RootDir '.venv\Scripts\python.exe')" `
    -ArgumentList "`"$ServerPath`"" `
    -WorkingDirectory (Join-Path $RootDir "Interface") `
    -PassThru `
    -NoNewWindow

# Save PID
$proc.Id | Out-File -FilePath $PidFile -Force
Write-Host "✓ Process started: PID $($proc.Id)" -ForegroundColor Green
Write-Host "✓ Saved to: $PidFile" -ForegroundColor Green

# Wait for port to be available
Write-Host "`n⏳ Waiting for server to start (checking port $Port)..." -ForegroundColor Yellow
$maxWait = 30
$elapsed = 0
while ($elapsed -lt $maxWait) {
    try {
        $connection = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
        if ($connection) {
            Write-Host "✓ Server is listening on port $Port" -ForegroundColor Green
            Write-Host "✓ Access at: http://localhost:$Port/activity-hub" -ForegroundColor Green
            break
        }
    } catch { }
    
    # Check if process crashed
    $proc = Get-Process -Id $proc.Id -ErrorAction SilentlyContinue
    if (-not $proc) {
        Write-Host "✗ Process crashed before port became available" -ForegroundColor Red
        Remove-Item $PidFile -Force -ErrorAction SilentlyContinue
        return
    }
    
    Start-Sleep -Seconds 1
    $elapsed++
}

Write-Host "`n═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Server Ready! [PID: $($proc.Id)]" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
