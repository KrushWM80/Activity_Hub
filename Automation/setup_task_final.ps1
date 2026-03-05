$TaskName = "Projects in Stores Server 24/7"
$TaskPath = "\Activity Hub\"
$ScriptPath = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\start_server_24_7.bat"
$WorkingDirectory = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"

# Check for admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Host "ERROR: This script requires Administrator privileges!" -ForegroundColor Red
    exit 1
}

# Remove existing task first
Get-ScheduledTask -TaskName $TaskName -TaskPath $TaskPath -ErrorAction SilentlyContinue | Unregister-ScheduledTask -Confirm:$false -ErrorAction SilentlyContinue | Out-Null

try {
    # Create trigger for system startup
    $trigger = New-ScheduledTaskTrigger -AtStartup
    
    # Create action to run the batch file
    $action = New-ScheduledTaskAction `
        -Execute "cmd.exe" `
        -Argument "/c `"$ScriptPath`"" `
        -WorkingDirectory $WorkingDirectory
    
    # Create principal to run with highest privileges
    $principal = New-ScheduledTaskPrincipal `
        -UserId "$env:USERDOMAIN\$env:USERNAME" `
        -LogonType ServiceAccount `
        -RunLevel Highest
    
    # Create settings for reliable 24/7 operation
    $settings = New-ScheduledTaskSettingsSet `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -StartWhenAvailable `
        -RunOnlyIfNetworkAvailable:$false `
        -RestartCount 3 `
        -RestartInterval (New-TimeSpan -Minutes 1)
    
    # Register the scheduled task
    Register-ScheduledTask `
        -TaskName $TaskName `
        -TaskPath $TaskPath `
        -Trigger $trigger `
        -Action $action `
        -Principal $principal `
        -Settings $settings `
        -Description "Automatically starts the Projects in Stores backend server 24/7 with auto-restart on crash" `
        -Force | Out-Null
    
    Write-Host "SUCCESS: Task created - Projects in Stores Server 24/7" -ForegroundColor Green
    $task = Get-ScheduledTask -TaskName $TaskName -TaskPath $TaskPath
    Write-Host "Task State: $($task.State)"
    Write-Host "Task Path: $($task.TaskPath)"
}
catch {
    Write-Host "ERROR: Failed to create scheduled task" -ForegroundColor Red
    Write-Host "$_"
    exit 1
}
