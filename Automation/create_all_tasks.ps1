$ProjectRoot = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"

# Check if running as admin
if (-NOT ([Security.Principal.WindowsIdentity]::GetCurrent()).groups -match "S-1-5-32-544") {
    Write-Host "❌ ERROR: This script requires Administrator privileges" -ForegroundColor Red
    Write-Host "Please right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "✓ Running as Administrator - Creating scheduled tasks..." -ForegroundColor Green
Write-Host ""

# Task 1: Job Codes
Write-Host "Creating Task 1: Job Codes Auto-Start..."
$action1 = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$ProjectRoot\Automation\start_jobcodes_server_24_7.bat`""
$trigger1 = New-ScheduledTaskTrigger -AtStartup
$settings1 = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
$principal1 = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
Register-ScheduledTask -TaskName "Activity_Hub_JobCodes_AutoStart" -Action $action1 -Trigger $trigger1 -Settings $settings1 -Principal $principal1 -Force | Out-Null
Write-Host "   ✓ Activity_Hub_JobCodes_AutoStart" -ForegroundColor Green

# Task 2: Projects in Stores
Write-Host "Creating Task 2: Projects in Stores Auto-Start..."
$action2 = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$ProjectRoot\Store Support\Projects\Intake Hub\ProjectsinStores\START_BACKEND.bat`""
$trigger2 = New-ScheduledTaskTrigger -AtStartup
$settings2 = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
$principal2 = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
Register-ScheduledTask -TaskName "Activity_Hub_ProjectsInStores_AutoStart" -Action $action2 -Trigger $trigger2 -Settings $settings2 -Principal $principal2 -Force | Out-Null
Write-Host "   ✓ Activity_Hub_ProjectsInStores_AutoStart" -ForegroundColor Green

# Task 3: TDA Insights
Write-Host "Creating Task 3: TDA Insights Auto-Start..."
$action3 = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$ProjectRoot\Automation\start_tda_insights_24_7.bat`""
$trigger3 = New-ScheduledTaskTrigger -AtStartup
$settings3 = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
$principal3 = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
Register-ScheduledTask -TaskName "Activity_Hub_TDA_AutoStart" -Action $action3 -Trigger $trigger3 -Settings $settings3 -Principal $principal3 -Force | Out-Null
Write-Host "   ✓ Activity_Hub_TDA_AutoStart" -ForegroundColor Green

# Task 4: Store Dashboard
Write-Host "Creating Task 4: Store Dashboard Auto-Start..."
$action4 = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$ProjectRoot\Automation\start_store_dashboard_24_7.bat`""
$trigger4 = New-ScheduledTaskTrigger -AtStartup
$settings4 = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
$principal4 = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
Register-ScheduledTask -TaskName "Activity_Hub_Store_Dashboard_AutoStart" -Action $action4 -Trigger $trigger4 -Settings $settings4 -Principal $principal4 -Force | Out-Null
Write-Host "   ✓ Activity_Hub_Store_Dashboard_AutoStart" -ForegroundColor Green

# Task 5: Store Meeting Planner
Write-Host "Creating Task 5: Store Meeting Planner Auto-Start..."
$action5 = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$ProjectRoot\Automation\start_meeting_planner_24_7.bat`""
$trigger5 = New-ScheduledTaskTrigger -AtLogon
$settings5 = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
$principal5 = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -RunLevel Highest
Register-ScheduledTask -TaskName "Activity_Hub_StoreMeetingPlanner_AutoStart" -Action $action5 -Trigger $trigger5 -Settings $settings5 -Principal $principal5 -Force | Out-Null
Write-Host "   ✓ Activity_Hub_StoreMeetingPlanner_AutoStart" -ForegroundColor Green

# Task 6: Zorro
Write-Host "Creating Task 6: Zorro Auto-Start..."
$action6 = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$ProjectRoot\Automation\start_zorro_24_7.bat`""
$trigger6 = New-ScheduledTaskTrigger -AtStartup
$settings6 = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
$principal6 = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
Register-ScheduledTask -TaskName "Activity_Hub_Zorro_AutoStart" -Action $action6 -Trigger $trigger6 -Settings $settings6 -Principal $principal6 -Force | Out-Null
Write-Host "   ✓ Activity_Hub_Zorro_AutoStart" -ForegroundColor Green

# Task 7: Daily Health Check
Write-Host "Creating Task 7: Daily Health Check at 6:00 AM..."
$action7 = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File `"$ProjectRoot\MONITOR_AND_REPORT.ps1`""
$trigger7 = New-ScheduledTaskTrigger -Daily -At 06:00:00
$settings7 = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
$principal7 = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
Register-ScheduledTask -TaskName "Activity_Hub_Daily_HealthCheck" -Action $action7 -Trigger $trigger7 -Settings $settings7 -Principal $principal7 -Force | Out-Null
Write-Host "   ✓ Activity_Hub_Daily_HealthCheck" -ForegroundColor Green

# Task 8: Activity Hub Server
Write-Host "Creating Task 8: Activity Hub Server Auto-Start..."
$action8 = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$ProjectRoot\Automation\start_activity_hub_24_7.bat`""
$trigger8 = New-ScheduledTaskTrigger -AtStartup
$settings8 = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
$principal8 = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
Register-ScheduledTask -TaskName "Activity_Hub_Server_AutoStart" -Action $action8 -Trigger $trigger8 -Settings $settings8 -Principal $principal8 -Force | Out-Null
Write-Host "   ✓ Activity_Hub_Server_AutoStart" -ForegroundColor Green

# Task 9: Logic Scheduler Service
Write-Host "Creating Task 9: Logic Scheduler Service Auto-Start..."
$action9 = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$ProjectRoot\Automation\start_logic_scheduler_24_7.bat`""
$trigger9 = New-ScheduledTaskTrigger -AtStartup
$settings9 = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
$principal9 = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
Register-ScheduledTask -TaskName "Activity_Hub_LogicScheduler_AutoStart" -Action $action9 -Trigger $trigger9 -Settings $settings9 -Principal $principal9 -Force | Out-Null
Write-Host "   ✓ Activity_Hub_LogicScheduler_AutoStart" -ForegroundColor Green

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "✓ ALL SCHEDULED TASKS CREATED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

# Verify tasks were created
Write-Host "Verifying tasks..."
$tasks = Get-ScheduledTask | Where-Object {$_.TaskName -like "Activity_Hub*"} 
Write-Host "Found $($tasks.Count) tasks:" -ForegroundColor Cyan
$tasks | Select-Object TaskName, State | Format-Table -AutoSize

Write-Host ""
Write-Host "Your services will now auto-start on system reboot." -ForegroundColor Green
