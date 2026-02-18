# Setup automatic startup for Job Codes Dashboard Server
# Creates a Windows Task Scheduler task to start server on login

$taskName = "JobCodesDashboardServer"
$scriptPath = Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) "start_server_background.ps1"
$workingDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=== Job Codes Dashboard - Auto-Start Setup ===" -ForegroundColor Cyan
Write-Host ""

# Check if task already exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "Auto-start task already exists!" -ForegroundColor Yellow
    $response = Read-Host "Do you want to remove and recreate it? (y/n)"
    if ($response -ne 'y') {
        Write-Host "Setup cancelled." -ForegroundColor Yellow
        exit
    }
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "Removed existing task" -ForegroundColor Green
}

# Create the scheduled task action
$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-ExecutionPolicy Bypass -WindowStyle Hidden -File `"$scriptPath`"" `
    -WorkingDirectory $workingDir

# Create the trigger (at logon)
$trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME

# Create settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1)

# Create the principal (run as current user)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive

# Register the task
Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Description "Automatically starts the Job Codes Dashboard server at login" `
    -ErrorAction Stop

Write-Host ""
Write-Host "Auto-start setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Configuration:" -ForegroundColor Cyan
Write-Host "  Task Name: $taskName" -ForegroundColor White
Write-Host "  Trigger: At login for user $env:USERNAME" -ForegroundColor White
Write-Host "  Script: $scriptPath" -ForegroundColor White
Write-Host "  Auto-restart: Yes (3 attempts, 1 minute intervals)" -ForegroundColor White
Write-Host ""
Write-Host "The server will now start automatically when you log in to Windows!" -ForegroundColor Green
Write-Host ""
Write-Host "Management Commands:" -ForegroundColor Yellow
Write-Host "  - Disable auto-start: .\disable_auto_start.ps1" -ForegroundColor White
Write-Host "  - Check server status: .\check_server.ps1" -ForegroundColor White
Write-Host "  - Stop server: .\stop_server.ps1" -ForegroundColor White
Write-Host ""
Write-Host "Would you like to start the server now? (y/n)" -ForegroundColor Cyan
$startNow = Read-Host

if ($startNow -eq 'y') {
    Write-Host "Starting server..." -ForegroundColor Yellow
    & $scriptPath
}
