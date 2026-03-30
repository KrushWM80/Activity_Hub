@echo off
echo ================================================================
echo  Activity Hub - Register Daily Health Check Task
echo  Requires: Run as Administrator
echo ================================================================
echo.
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$action = New-ScheduledTaskAction ^
        -Execute 'powershell.exe' ^
        -Argument '-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File \"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\MONITOR_AND_REPORT.ps1\"' ^
        -WorkingDirectory 'C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub'; ^
    $trigger = New-ScheduledTaskTrigger -Daily -At '06:00AM'; ^
    $settings = New-ScheduledTaskSettingsSet ^
        -StartWhenAvailable ^
        -WakeToRun ^
        -ExecutionTimeLimit (New-TimeSpan -Minutes 30) ^
        -MultipleInstances IgnoreNew ^
        -DisallowStartIfOnBatteries:$false ^
        -StopIfGoingOnBatteries:$false; ^
    $principal = New-ScheduledTaskPrincipal -UserId 'krush' -LogonType Interactive -RunLevel Limited; ^
    Register-ScheduledTask ^
        -TaskName 'Activity_Hub_Daily_HealthCheck' ^
        -Action $action ^
        -Trigger $trigger ^
        -Settings $settings ^
        -Principal $principal ^
        -Force; ^
    Write-Host 'SUCCESS: Task registered! Next run: tomorrow at 6:00 AM' -ForegroundColor Green; ^
    Write-Host 'StartWhenAvailable=true: Will run on login if machine was off at 6am' -ForegroundColor Cyan; ^
    Write-Host 'WakeToRun=true: Will wake machine from sleep at 6am' -ForegroundColor Cyan; ^
    Get-ScheduledTask -TaskName 'Activity_Hub_Daily_HealthCheck' | Select-Object TaskName, State"
echo.
echo Done. Press any key to close...
pause
