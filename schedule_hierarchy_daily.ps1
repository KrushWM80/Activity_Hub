# Activity Hub - Hierarchy Sync Task Setup
# Run this script as Administrator to schedule daily hierarchy updates

$taskName = "AH-SyncHierarchy"
$taskPath = "\Activity Hub\"
$batFile = "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\run_hierarchy_sync.bat"
$taskTime = "05:00AM"

Write-Host "=========================================="
Write-Host "Activity Hub - Hierarchy Sync Task Setup"
Write-Host "=========================================="

# 1. Remove existing task if present
Write-Host "`n[1/3] Checking for existing task..."
try {
    $existing = Get-ScheduledTask -TaskName $taskName -TaskPath $taskPath -ErrorAction Stop
    Unregister-ScheduledTask -TaskName $taskName -TaskPath $taskPath -Confirm:$false
    Write-Host "  ✓ Removed existing task"
} catch {
    Write-Host "  ○ No existing task found"
}

# 2. Create new task
Write-Host "`n[2/3] Creating new scheduled task..."
try {
    $trigger = New-ScheduledTaskTrigger -Daily -At $taskTime
    $action = New-ScheduledTaskAction -Execute $batFile
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
    
    $task = Register-ScheduledTask -TaskName $taskName `
        -TaskPath $taskPath `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -User "SYSTEM" `
        -RunLevel Highest `
        -Force
    
    Write-Host "  ✓ Task created successfully"
} catch {
    Write-Host "  ✗ Error creating task: $_"
    exit 1
}

# 3. Verify task
Write-Host "`n[3/3] Verifying task..."
try {
    $task = Get-ScheduledTask -TaskName $taskName -TaskPath $taskPath
    Write-Host "  ✓ Task verified"
    Write-Host ""
    Write-Host "=========================================="
    Write-Host "Task Details"
    Write-Host "=========================================="
    Write-Host "Name:     $($task.TaskName)"
    Write-Host "Path:     $($task.TaskPath)"
    Write-Host "Status:   $($task.State)"
    Write-Host "Trigger:  Daily at $taskTime"
    Write-Host "Batch:    $batFile"
    Write-Host ""
    Write-Host "This task will:"
    Write-Host "  • Extract 172 unique people from Intake Hub"
    Write-Host "  • Populate director/sr_director relationships"
    Write-Host "  • Update AH_Hierarchy table automatically"
    Write-Host "  • Ensure projects stay current with org hierarchy"
    Write-Host ""
} catch {
    Write-Host "  ✗ Error verifying task: $_"
    exit 1
}

Write-Host "=========================================="
Write-Host "Setup Complete!"
Write-Host "=========================================="
