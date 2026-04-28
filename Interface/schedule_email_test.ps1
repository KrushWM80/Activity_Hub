<# 
  Schedule Activity Hub email test â€” runs daily at 7:00 AM starting Wednesday April 29
  Day-of-week logic in the Python script decides what to send:
    Monday    â†’ Kendall Rush owner email (all projects)
    Wednesday â†’ Kendall Rush owner email (not-updated projects)
    Thursday  â†’ Matt Farnworth + Kristine Torres leadership emails
  
  All emails go to kendall.rush@walmart.com (TEST_MODE = True).
  Run this script as Administrator.
#>

$ErrorActionPreference = "Stop"
$VenvPython = "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"
$Script     = "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Interface\run_scheduled_emails.py"
$LogDir     = "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\logs"
$TaskName   = "ActivityHub_Email_Test"

# Ensure log directory exists
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir -Force | Out-Null }

$LogFile = Join-Path $LogDir "email_scheduler.log"

# Build the action â€” run python script, append output to log
$ArgString = "`"$Script`" >> `"$LogFile`" 2>&1"
$Action  = New-ScheduledTaskAction -Execute $VenvPython -Argument $ArgString `
           -WorkingDirectory "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Interface"

# Trigger: daily at 7:00 AM starting tomorrow (Wednesday April 29)
$StartDate = (Get-Date).AddDays(1).Date.AddHours(7)
$Trigger   = New-ScheduledTaskTrigger -Daily -At $StartDate

# Settings
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopOnIdleEnd `
            -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
            -ExecutionTimeLimit (New-TimeSpan -Minutes 10)

# Remove existing task if present
if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host "Removed existing task: $TaskName" -ForegroundColor Yellow
}

# Register task
Register-ScheduledTask -TaskName $TaskName `
    -Action $Action -Trigger $Trigger -Settings $Settings `
    -Description "Activity Hub Email Test - Kendall Rush + Matt Farnworth + Kristine Torres (daily 7 AM)" `
    -RunLevel Highest | Out-Null

Write-Host ""
Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host " [OK] Scheduled Task Created: $TaskName" -ForegroundColor Green
Write-Host "   Runs: Daily at 7:00 AM starting $($StartDate.ToString('dddd, MMMM dd yyyy'))" -ForegroundColor White
Write-Host "   Script: $Script" -ForegroundColor Gray
Write-Host "   Log: $LogFile" -ForegroundColor Gray
Write-Host "   Recipients: Real addresses (test scope only)" -ForegroundColor Gray
Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Upcoming emails:" -ForegroundColor White
Write-Host "  Wed Apr 29 - Kendall Rush owner email (not-updated) -> kendall.rush@walmart.com" -ForegroundColor Yellow
Write-Host "  Thu Apr 30 - Matt Farnworth leadership -> matthew.farnworth@walmart.com" -ForegroundColor Yellow
Write-Host "  Thu Apr 30 - Kristine Torres leadership -> kristine.torres@walmart.com" -ForegroundColor Yellow
Write-Host "  Mon May  4 - Kendall Rush owner email (all projects) -> kendall.rush@walmart.com" -ForegroundColor Yellow
Write-Host ""
Write-Host "Each person receives their email at their own address." -ForegroundColor Cyan
