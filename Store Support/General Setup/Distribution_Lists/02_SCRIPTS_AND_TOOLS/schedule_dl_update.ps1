# Schedule DL Catalog Update - Run Daily at 5 AM
# This script sets up Windows Task Scheduler to refresh the DL catalog every morning

$taskName = "DL_Catalog_Daily_Update"
$scriptPath = "$PSScriptRoot\extract_all_dls_optimized.py"
$pythonPath = "python"  # Or full path like "C:\Python311\python.exe"
$logPath = "$PSScriptRoot\logs"

# Create logs directory if it doesn't exist
if (-not (Test-Path $logPath)) {
    New-Item -ItemType Directory -Path $logPath | Out-Null
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host "  DL Catalog Daily Update Scheduler Setup" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

# Check if task already exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "`nTask already exists. Removing old task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Create scheduled task action
$action = New-ScheduledTaskAction `
    -Execute $pythonPath `
    -Argument "$scriptPath" `
    -WorkingDirectory $PSScriptRoot

# Create trigger for 5 AM daily
$trigger = New-ScheduledTaskTrigger -Daily -At 5:00AM

# Task settings
$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable `
    -DontStopIfGoingOnBatteries `
    -AllowStartIfOnBatteries

# Create principal (run as current user)
$principal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType Interactive `
    -RunLevel Limited

# Register the task
try {
    Register-ScheduledTask `
        -TaskName $taskName `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Principal $principal `
        -Description "Daily update of distribution list catalog at 5 AM" `
        -ErrorAction Stop
    
    Write-Host "`n✓ Successfully created scheduled task!" -ForegroundColor Green
    Write-Host "`nTask Details:" -ForegroundColor White
    Write-Host "  Name: $taskName" -ForegroundColor White
    Write-Host "  Schedule: Daily at 5:00 AM" -ForegroundColor White
    Write-Host "  Script: $scriptPath" -ForegroundColor White
    Write-Host "  Working Directory: $PSScriptRoot" -ForegroundColor White
    
    Write-Host "`n==========================================================" -ForegroundColor Cyan
    Write-Host "  Task Actions" -ForegroundColor Yellow
    Write-Host "==========================================================" -ForegroundColor Cyan
    
    Write-Host "`nView task:"
    Write-Host "  taskschd.msc (Task Scheduler GUI)" -ForegroundColor White
    Write-Host "  Or: Get-ScheduledTask -TaskName '$taskName'" -ForegroundColor White
    
    Write-Host "`nTest task now:"
    Write-Host "  Start-ScheduledTask -TaskName '$taskName'" -ForegroundColor White
    
    Write-Host "`nDisable task:"
    Write-Host "  Disable-ScheduledTask -TaskName '$taskName'" -ForegroundColor White
    
    Write-Host "`nRemove task:"
    Write-Host "  Unregister-ScheduledTask -TaskName '$taskName'" -ForegroundColor White
    
    Write-Host "`n==========================================================" -ForegroundColor Cyan
    
}
catch {
    Write-Host "`nX Error creating scheduled task: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "`nNote: You may need to run PowerShell as Administrator" -ForegroundColor Yellow
    exit 1
}

# Offer to test now
Write-Host "`nWould you like to test the task now? (Y/N): " -NoNewline -ForegroundColor Yellow
$response = Read-Host

if ($response -eq 'Y' -or $response -eq 'y') {
    Write-Host "`nStarting task..." -ForegroundColor Green
    Start-ScheduledTask -TaskName $taskName
    Write-Host "✓ Task started. Check the logs folder for progress." -ForegroundColor Green
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
