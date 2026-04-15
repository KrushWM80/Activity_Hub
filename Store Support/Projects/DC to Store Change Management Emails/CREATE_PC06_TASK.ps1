# Create PC-06 Task for April 17, 2026 @ 6:00 AM
# Run this in ADMIN PowerShell

$pythonExe = "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"
$scriptPath = "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails\send_pc06_production_email.py"

# PC-06 Task (April 17, 2026 @ 6:00 AM)
$trigger = New-ScheduledTaskTrigger -At "2026-04-17 06:00:00" -Once
$action = New-ScheduledTaskAction -Execute $pythonExe -Argument "`"$scriptPath`""
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName "DC-EMAIL-PC-06-FY27 PC 06" -Trigger $trigger -Action $action -Settings $settings -RunLevel Highest -User SYSTEM -Force

Write-Host "[OK] PC-06 task created for April 17, 2026 @ 6:00 AM"
Write-Host "Task Name: DC-EMAIL-PC-06-FY27 PC 06"
Write-Host "Scheduled: 2026-04-17 06:00:00"

# Verify task was created
Get-ScheduledTask -TaskName "DC-EMAIL-PC-06*" | Select-Object TaskName, State
