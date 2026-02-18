# Persistent server startup script with auto-restart
# This script will keep the server running even if it crashes

$serverPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $serverPath

Write-Host "Starting Job Codes Dashboard Server..." -ForegroundColor Green
Write-Host "Server will auto-restart if it crashes" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Cyan
Write-Host ""

$restartCount = 0
$maxRestarts = 10

while ($restartCount -lt $maxRestarts) {
    try {
        Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - Starting server (Attempt $($restartCount + 1))" -ForegroundColor Green
        
        # Start the Python server
        python backend\main.py
        
        # If we get here, the server exited normally
        Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - Server stopped normally" -ForegroundColor Yellow
        break
    }
    catch {
        Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - Server crashed: $_" -ForegroundColor Red
        $restartCount++
        
        if ($restartCount -lt $maxRestarts) {
            Write-Host "Restarting in 5 seconds..." -ForegroundColor Yellow
            Start-Sleep -Seconds 5
        }
        else {
            Write-Host "Maximum restart attempts reached. Please check the logs." -ForegroundColor Red
            break
        }
    }
}

Write-Host ""
Write-Host "Server stopped. Press any key to exit..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
