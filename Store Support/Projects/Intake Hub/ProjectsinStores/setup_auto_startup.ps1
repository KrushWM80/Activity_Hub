# Setup Auto-Startup for Backend Server
# Run as Administrator to create scheduled task

$TaskName = "ProjectsInStores-Backend"
$ScriptPath = "C:\Users\krush\Documents\VSCode\Intake Hub\ProjectsinStores\backend\start_server.ps1"
$WorkingDirectory = "C:\Users\krush\Documents\VSCode\Intake Hub\ProjectsinStores\backend"

Write-Host "Setting up automatic startup for Projects in Stores Backend..." -ForegroundColor Cyan
Write-Host ""

# Check if task already exists
$existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "Scheduled task '$TaskName' already exists" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Task Details:" -ForegroundColor Cyan
    Write-Host "  Name: $($existingTask.TaskName)"
    Write-Host "  Status: $($existingTask.State)"
    Write-Host "  Next Run: $($existingTask.Triggers.StartBoundary)"
    Write-Host ""
    Write-Host "The backend will automatically start on system boot." -ForegroundColor Green
    exit
}

try {
    # Create trigger for system startup
    $trigger = New-ScheduledTaskTrigger -AtStartup
    
    # Create action to run PowerShell script
    $action = New-ScheduledTaskAction `
        -Execute "powershell.exe" `
        -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$ScriptPath`"" `
        -WorkingDirectory $WorkingDirectory
    
    # Create task with high privileges
    $principal = New-ScheduledTaskPrincipal `
        -UserId "$env:USERDOMAIN\$env:USERNAME" `
        -LogonType ServiceAccount `
        -RunLevel Highest
    
    # Register the scheduled task
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Trigger $trigger `
        -Action $action `
        -Principal $principal `
        -Description "Automatically starts the Projects in Stores backend server on system startup" `
        -Force
    
    Write-Host "Scheduled task created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Task Details:" -ForegroundColor Cyan
    Write-Host "  Name: $TaskName"
    Write-Host "  Trigger: At System Startup"
    Write-Host "  Script: $ScriptPath"
    Write-Host "  Working Directory: $WorkingDirectory"
    Write-Host ""
    Write-Host "The backend server will now:" -ForegroundColor Yellow
    Write-Host "  - Automatically start when you boot your computer"
    Write-Host "  - Run with administrator privileges"
    Write-Host "  - Listen on port 8001"
    Write-Host "  - Be accessible at http://10.97.105.88:8001"
    Write-Host ""
    Write-Host "Users can access the dashboard immediately after boot." -ForegroundColor Green
}
catch {
    Write-Host "Error creating scheduled task: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Make sure you're running PowerShell as Administrator!" -ForegroundColor Yellow
}
