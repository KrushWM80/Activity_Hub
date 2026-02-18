# Schedule Daily BigQuery Update
# Run this script ONCE to set up the Windows Task Scheduler

$ErrorActionPreference = "Stop"

# Configuration
$scriptPath = "C:\Users\krush\Documents\VSCode\Spark-Playground\General Setup\Distribution_Lists"
$scriptFile = Join-Path $scriptPath "daily_update_to_bigquery.ps1"
$taskName = "DL_BigQuery_Daily_Update"
$taskDescription = "Extract distribution lists from AD and upload to BigQuery daily at 5:00 AM"
$scheduleTime = "05:00"  # 5:00 AM

Write-Host "=========================================="
Write-Host "Setting up Windows Task Scheduler"
Write-Host "=========================================="

# Check if script exists
if (!(Test-Path $scriptFile)) {
    Write-Host "ERROR: Script not found: $scriptFile" -ForegroundColor Red
    exit 1
}

Write-Host "Script location: $scriptFile"
Write-Host "Schedule time: $scheduleTime daily"
Write-Host ""

# Remove existing task if it exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "Removing existing task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Create scheduled task action
$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptFile`"" `
    -WorkingDirectory $scriptPath

# Create scheduled task trigger (daily at 5:00 AM)
$trigger = New-ScheduledTaskTrigger -Daily -At $scheduleTime

# Create scheduled task settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Hours 2)

# Create scheduled task principal (run as current user)
$principal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType Interactive `
    -RunLevel Highest

# Register the scheduled task
Write-Host "Creating scheduled task..." -ForegroundColor Cyan
Register-ScheduledTask `
    -TaskName $taskName `
    -Description $taskDescription `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal

Write-Host ""
Write-Host "SUCCESS: Scheduled task created!" -ForegroundColor Green
Write-Host ""
Write-Host "Task Details:" -ForegroundColor Cyan
Write-Host "  Name: $taskName"
Write-Host "  Schedule: Daily at $scheduleTime"
Write-Host "  Script: $scriptFile"
Write-Host ""
Write-Host "To verify:" -ForegroundColor Yellow
Write-Host "  1. Open Task Scheduler (taskschd.msc)"
Write-Host "  2. Look for: $taskName"
Write-Host "  3. Right-click > Run to test immediately"
Write-Host ""
Write-Host "To view logs after it runs:"
Write-Host "  Get-Content `"$scriptPath\logs\daily_update_*.log`" | Select-Object -Last 50"
Write-Host ""
Write-Host "To remove the task later:"
Write-Host "  Unregister-ScheduledTask -TaskName `"$taskName`" -Confirm:`$false"
Write-Host ""
Write-Host "=========================================="
Write-Host "Setup Complete!"
Write-Host "=========================================="
