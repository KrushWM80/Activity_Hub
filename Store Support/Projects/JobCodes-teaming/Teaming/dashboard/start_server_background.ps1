# Start server as a background process
# This allows you to close the terminal without stopping the server

$serverPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$logFile = Join-Path $serverPath "server.log"
$pidFile = Join-Path $serverPath "server.pid"

Write-Host "Starting Job Codes Dashboard Server in background..." -ForegroundColor Green

# Check if server is already running
if (Test-Path $pidFile) {
    $serverPid = Get-Content $pidFile
    $process = Get-Process -Id $serverPid -ErrorAction SilentlyContinue
    if ($process) {
        Write-Host "Server is already running (PID: $serverPid)" -ForegroundColor Yellow
        Write-Host "Use stop_server.ps1 to stop it first" -ForegroundColor Cyan
        exit
    }
}

# Start server in background
$errorLogFile = Join-Path $serverPath "server_error.log"
$process = Start-Process -FilePath "python" -ArgumentList "backend\main.py" `
    -WorkingDirectory $serverPath `
    -RedirectStandardOutput $logFile `
    -RedirectStandardError $errorLogFile `
    -WindowStyle Hidden `
    -PassThru

# Save PID
$process.Id | Out-File $pidFile

Write-Host "Server started successfully!" -ForegroundColor Green
Write-Host "  PID: $($process.Id)" -ForegroundColor Cyan
Write-Host "  Log file: $logFile" -ForegroundColor Cyan
Write-Host "  URL: http://localhost:8080" -ForegroundColor Cyan
Write-Host ""
Write-Host "Use stop_server.ps1 to stop the server" -ForegroundColor Yellow
