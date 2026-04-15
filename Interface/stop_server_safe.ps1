# Safe Activity Hub Server Shutdown - Only kills saved PID
# Usage: .\stop_server_safe.ps1
# Location: Activity Hub\Interface\

$RootDir = Split-Path -Parent $PSScriptRoot
$PidFile = Join-Path $RootDir "PIDS\activity_hub_server.pid"
$Port = 8088

Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Activity Hub Server - Safe Stop" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan

if (-not (Test-Path $PidFile)) {
    Write-Host "✓ Server is not running (no PID file found)" -ForegroundColor Yellow
    return
}

$Pid = Get-Content $PidFile -Raw

try {
    $proc = Get-Process -Id $Pid -ErrorAction SilentlyContinue
    
    if (-not $proc) {
        Write-Host "✓ Process (PID $Pid) is already stopped" -ForegroundColor Yellow
        Remove-Item $PidFile -Force -ErrorAction SilentlyContinue
        return
    }
    
    Write-Host "▶ Stopping Activity Hub (PID $Pid) on port $Port..." -ForegroundColor Cyan
    Stop-Process -Id $Pid -Force -ErrorAction Stop
    Start-Sleep -Milliseconds 500
    
    # Verify it's dead
    $check = Get-Process -Id $Pid -ErrorAction SilentlyContinue
    if (-not $check) {
        Remove-Item $PidFile -Force -ErrorAction SilentlyContinue
        Write-Host "✓ Process stopped successfully" -ForegroundColor Green
        Write-Host "✓ PID file removed" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to stop process" -ForegroundColor Red
    }
    
} catch {
    Write-Host "✗ Error: $_" -ForegroundColor Red
}

Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
