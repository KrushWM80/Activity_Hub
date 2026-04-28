# Schedule Daily Batch Update Task
# Run as Administrator

$taskName = "Activity Hub - Batch Update Projects"
$taskPath = "\Activity Hub\"
$batFile = "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\run_batch_update_daily.bat"

Write-Host "Scheduling daily batch update for projects hierarchy synchronization..."

# Remove existing task if present
try {
    Get-ScheduledTask -TaskName $taskName -TaskPath $taskPath -ErrorAction Stop | Unregister-ScheduledTask -Confirm:$false
    Write-Host "Removed existing task"
} catch {
    Write-Host "No existing task found"
}

# Create new trigger for daily at 5:05 AM (5 minutes after hierarchy sync)
$trigger = New-ScheduledTaskTrigger -Daily -At "05:05AM"

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

Write-Host ""
Write-Host "✓ Task scheduled successfully"
Write-Host "  Task Name: $taskName"
Write-Host "  Schedule: Daily at 5:05 AM"
Write-Host "  Task Path: $taskPath"
Write-Host "  Batch File: $batFile"
Write-Host "  Log Files: logs\batch_update_*.log"
Write-Host ""
Write-Host "Execution Flow:"
Write-Host "  1. 5:00 AM - Hierarchy Sync runs (sync_hierarchy_simple.py)"
Write-Host "  2. 5:05 AM - Batch Update runs (batch_update_daily.py)"
Write-Host "  3. Projects with known owners get director/sr_director populated"
