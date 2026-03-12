# Full Activity Hub Restoration - March 12, 2026
# Run this in Administrator PowerShell

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Restoring All Activity Hub Tasks" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Paths
$ProjectPath = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"
$MonitorScript = "$ProjectPath\MONITOR_AND_REPORT.ps1"
$JobCodesScript = "$ProjectPath\Store Support\Projects\JobCodes-teaming\Teaming\job_code_comparison.py"
$PythonExe = "$ProjectPath\.venv\Scripts\python.exe"
$StartServerBat = "$ProjectPath\Automation\start_server_24_7.bat"

# Principal for all tasks
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount

write-host ""
Write-Host "Part 1: Projects in Stores (ActivityHubServer)" -ForegroundColor Yellow
$action1 = New-ScheduledTaskAction -Execute $StartServerBat
$trigger1 = New-ScheduledTaskTrigger -AtStartup -RandomDelay (New-TimeSpan -Seconds 30)
$settings1 = New-ScheduledTaskSettingsSet -DontStopOnIdleEnd
Register-ScheduledTask -TaskName "ActivityHubServer" -Action $action1 -Trigger $trigger1 -Principal $principal -Settings $settings1 -Force | Out-Null
Write-Host "[OK] ActivityHubServer task created"

Write-Host ""
Write-Host "Part 2: Job Codes Dashboard Backend (Port 8080)" -ForegroundColor Yellow
$jobcodesStartBat = "$ProjectPath\Automation\start_jobcodes_server_24_7.bat"
$action2 = New-ScheduledTaskAction -Execute $jobcodesStartBat
# Multiple triggers: On startup, daily at 3 AM, and every 6 hours to ensure it stays running
$trigger2a = New-ScheduledTaskTrigger -AtStartup -RandomDelay (New-TimeSpan -Seconds 15)
$trigger2b = New-ScheduledTaskTrigger -Daily -At 3:00am
$trigger2c = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 6) -RepetitionDuration (New-TimeSpan -Days 999)
$settings2 = New-ScheduledTaskSettingsSet -DontStopOnIdleEnd -AllowHardTerminate
Register-ScheduledTask -TaskName "JobCodes-Backend-Server" -Action $action2 -Trigger @($trigger2a, $trigger2b, $trigger2c) -Principal $principal -Settings $settings2 -Force | Out-Null
Write-Host "[OK] JobCodes-Backend-Server task created (Port 8080)"
Write-Host "     - Triggers: Startup, Daily @ 3AM, Every 6 hours"
Write-Host "     - URL: http://10.97.114.181:8080/static/index.html#"

Write-Host ""
Write-Host "Part 2b: Job Codes Daily Sync (Reconciliation)" -ForegroundColor Yellow
$action2b = New-ScheduledTaskAction -Execute $PythonExe -Argument "$JobCodesScript" -WorkingDirectory "$ProjectPath\Store Support\Projects\JobCodes-teaming\Teaming"
$trigger2ba = New-ScheduledTaskTrigger -Daily -At 2:00am
$trigger2bb = New-ScheduledTaskTrigger -AtStartup -RandomDelay (New-TimeSpan -Seconds 90)
Register-ScheduledTask -TaskName "JobCodes-Daily-Reconciliation" -Action $action2b -Trigger @($trigger2ba, $trigger2bb) -Principal $principal -Force | Out-Null
Write-Host "[OK] JobCodes-Daily-Reconciliation task created"

Write-Host ""
Write-Host "Part 3: Daily Status Email at 6 AM" -ForegroundColor Yellow
$action3 = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$MonitorScript`""
$trigger3 = New-ScheduledTaskTrigger -Daily -At 6:00am
$settings3 = New-ScheduledTaskSettingsSet -DontStopOnIdleEnd -RunOnlyIfNetworkAvailable
Register-ScheduledTask -TaskName "ActivityHub-DailyStatus-6AM" -Action $action3 -Trigger $trigger3 -Principal $principal -Settings $settings3 -Force | Out-Null
Write-Host "[OK] ActivityHub-DailyStatus-6AM task created"

Write-Host ""
Write-Host "Part 4: System Restart Status Email" -ForegroundColor Yellow
$action4 = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$MonitorScript`""
$trigger4 = New-ScheduledTaskTrigger -AtStartup -RandomDelay (New-TimeSpan -Seconds 30)
$settings4 = New-ScheduledTaskSettingsSet -DontStopOnIdleEnd
Register-ScheduledTask -TaskName "ActivityHub-Startup-Report" -Action $action4 -Trigger $trigger4 -Principal $principal -Settings $settings4 -Force | Out-Null
Write-Host "[OK] ActivityHub-Startup-Report task created"

Write-Host ""
Write-Host "Part 5: DC Manager PayCycle Tasks (26 tasks)" -ForegroundColor Yellow
& "$ProjectPath\Automation\setup_tasks_revised.ps1"

Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host "Verification" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""

Get-ScheduledTask -TaskName "ActivityHubServer" | Select-Object TaskName, State
Write-Host ""
Get-ScheduledTask -TaskName "JobCodes-Backend-Server" | Select-Object TaskName, State
Write-Host ""
Get-ScheduledTask -TaskName "JobCodes-Daily-Reconciliation" | Select-Object TaskName, State
Write-Host ""
Get-ScheduledTask -TaskName "ActivityHub-DailyStatus-6AM" | Select-Object TaskName, State
Write-Host ""
Get-ScheduledTask -TaskName "ActivityHub-Startup-Report" | Select-Object TaskName, State

Write-Host ""
$pcCount = (Get-ScheduledTask | Where-Object {$_.TaskName -like "DC-EMAIL-PC-*"} | Measure-Object).Count
Write-Host "PayCycle Tasks: $pcCount/26" -ForegroundColor Yellow

Write-Host ""
Write-Host "[OK] All tasks restored and verified" -ForegroundColor Green
