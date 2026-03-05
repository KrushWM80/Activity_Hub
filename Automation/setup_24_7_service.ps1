$TaskName = "Activity Hub Server 24/7"
$TaskPath = "\Activity Hub\"
$ScriptPath = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\start_server_24_7.bat"

# Remove existing task if it exists
Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue | Unregister-ScheduledTask -Confirm:$false -ErrorAction SilentlyContinue

# Create trigger for system startup
$Trigger = New-ScheduledTaskTrigger -AtStartup

# Create action to run the batch file
$Action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$ScriptPath`""

# Create task settings for 24/7 operation
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable:$false

# Register the task to run with highest privileges
Register-ScheduledTask -TaskName $TaskName `
    -TaskPath $TaskPath `
    -Trigger $Trigger `
    -Action $Action `
    -Settings $Settings `
    -RunLevel Highest `
    -Force

Write-Host "✅ Scheduled task created: Activity Hub Server 24/7"
Write-Host "The server will start at system startup and auto-restart if it crashes"
