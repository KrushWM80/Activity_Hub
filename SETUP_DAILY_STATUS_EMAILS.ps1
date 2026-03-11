# Schedule Activity Hub Daily Status Reports
# Run this in Administrator PowerShell

$ScriptPath = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\MONITOR_AND_REPORT.ps1"

# Create 6 AM daily email task
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$ScriptPath`""
$trigger = New-ScheduledTaskTrigger -Daily -At 6:00am
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount
$settings = New-ScheduledTaskSettingsSet -DontStopOnIdleEnd -RunOnlyIfNetworkAvailable

Register-ScheduledTask -TaskName "ActivityHub-DailyStatus-6AM" -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force

Write-Host "[OK] Daily 6 AM status email task created" -ForegroundColor Green

# Create system startup email task (30 second delay to let services start)
$actionStartup = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$ScriptPath`""
$triggerStartup = New-ScheduledTaskTrigger -AtStartup -RandomDelay (New-TimeSpan -Seconds 30)
$settingsStartup = New-ScheduledTaskSettingsSet -DontStopOnIdleEnd

Register-ScheduledTask -TaskName "ActivityHub-Startup-Report" -Action $actionStartup -Trigger $triggerStartup -Principal $principal -Settings $settingsStartup -Force

Write-Host "[OK] System startup notification task created" -ForegroundColor Green

# Verify both tasks
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Scheduled Tasks Created:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$dailyTask = Get-ScheduledTask -TaskName "ActivityHub-DailyStatus-6AM"
Write-Host ""
Write-Host "1. Daily Status Email at 6:00 AM" -ForegroundColor Yellow
Write-Host "   Task Name: ActivityHub-DailyStatus-6AM"
Write-Host "   Trigger: Daily at 6:00 AM"
Write-Host "   Status: $($dailyTask.State)"
Write-Host "   Run As: SYSTEM"

$startupTask = Get-ScheduledTask -TaskName "ActivityHub-Startup-Report"
Write-Host ""
Write-Host "2. On System Startup" -ForegroundColor Yellow
Write-Host "   Task Name: ActivityHub-Startup-Report"
Write-Host "   Trigger: System startup (30 second delay)"
Write-Host "   Status: $($startupTask.State)"
Write-Host "   Run As: SYSTEM"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Email Features:" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "[OK] Daily report at 6:00 AM every day"
Write-Host "[OK] Automatic email on system restart"
Write-Host "[OK] Downtime detection (alerts if system was offline >5 minutes)"
Write-Host "[OK] Recipients: ATCTeamsupport@walmart.com, kendall.rush@walmart.com"
Write-Host "[OK] Automatic system status checking (3 services)"
Write-Host ""
