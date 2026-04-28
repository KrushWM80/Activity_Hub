# Create Windows Task Scheduler job for hierarchy sync
# Run this script as Administrator

$taskName = "Activity Hub - Sync Hierarchy"
$taskPath = "\Activity Hub\"
$batFile = "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\run_hierarchy_sync.bat"

# Remove existing task if present
try {
    Get-ScheduledTask -TaskName $taskName -TaskPath $taskPath -ErrorAction Stop | Unregister-ScheduledTask -Confirm:$false
    Write-Host "Removed existing task"
} catch {
    Write-Host "No existing task found"
}

# Create new trigger for daily at 5:00 AM
$trigger = New-ScheduledTaskTrigger -Daily -At "05:00AM"

# Create action to run batch file
$action = New-ScheduledTaskAction -Execute $batFile

# Create task settings
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Register the task
Register-ScheduledTask -TaskName $taskName `
    -TaskPath $taskPath `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -User "SYSTEM" `
    -RunLevel Highest `
    -Force

Write-Host "✓ Hierarchy sync task scheduled for daily at 5:00 AM"
Write-Host "  Task Name: $taskName"
Write-Host "  Task Path: $taskPath"
Write-Host "  Batch File: $batFile"
