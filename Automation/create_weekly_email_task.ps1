# TDA Weekly Email - Create Scheduled Task (must run as Admin)
$action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument '/c "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\send_tda_weekly_email.bat"'
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Thursday -At "11:00AM"
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName "Activity_Hub_TDA_Weekly_Email" -Action $action -Trigger $trigger -Settings $settings -Description "TDA weekly email Thursdays 11AM" -Force
Write-Host "Task created successfully!" -ForegroundColor Green
Get-ScheduledTaskInfo -TaskName "Activity_Hub_TDA_Weekly_Email" | Select-Object NextRunTime
Start-Sleep 5
