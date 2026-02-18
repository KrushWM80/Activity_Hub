# Stop the background server

$serverPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$pidFile = Join-Path $serverPath "server.pid"

if (-not (Test-Path $pidFile)) {
    Write-Host "No server PID file found. Server may not be running." -ForegroundColor Yellow
    exit
}

$serverPid = Get-Content $pidFile
$process = Get-Process -Id $serverPid -ErrorAction SilentlyContinue

if ($process) {
    Write-Host "Stopping server (PID: $serverPid)..." -ForegroundColor Yellow
    Stop-Process -Id $serverPid -Force
    Write-Host "Server stopped successfully!" -ForegroundColor Green
}
else {
    Write-Host "Server process not found (PID: $serverPid)" -ForegroundColor Yellow
}

# Clean up PID file
Remove-Item $pidFile -ErrorAction SilentlyContinue
