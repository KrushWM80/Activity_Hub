# Check server status

$serverPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$pidFile = Join-Path $serverPath "server.pid"

Write-Host "=== Job Codes Dashboard Server Status ===" -ForegroundColor Cyan
Write-Host ""

# Check PID file
if (Test-Path $pidFile) {
    $serverPid = Get-Content $pidFile
    $process = Get-Process -Id $serverPid -ErrorAction SilentlyContinue
    
    if ($process) {
        Write-Host "Process Status: RUNNING" -ForegroundColor Green
        Write-Host "  PID: $serverPid" -ForegroundColor Cyan
        Write-Host "  CPU: $([math]::Round($process.CPU, 2))s" -ForegroundColor Cyan
        Write-Host "  Memory: $([math]::Round($process.WorkingSet64 / 1MB, 2)) MB" -ForegroundColor Cyan
        Write-Host "  Start Time: $($process.StartTime)" -ForegroundColor Cyan
    }
    else {
        Write-Host "Process Status: NOT RUNNING (stale PID file)" -ForegroundColor Red
    }
}
else {
    Write-Host "Process Status: NOT RUNNING" -ForegroundColor Red
}

Write-Host ""

# Check port
$portOpen = Test-NetConnection -ComputerName localhost -Port 8080 -InformationLevel Quiet -WarningAction SilentlyContinue

if ($portOpen) {
    Write-Host "Port 8080: OPEN" -ForegroundColor Green
    Write-Host "  URL: http://localhost:8080" -ForegroundColor Cyan
}
else {
    Write-Host "Port 8080: CLOSED" -ForegroundColor Red
}

Write-Host ""
Write-Host "=======================================" -ForegroundColor Cyan
