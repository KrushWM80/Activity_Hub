# Setup Auto-Startup for Projects in Stores Backend Server 24/7
# Run as Administrator to create scheduled task
# This creates the Windows Task Scheduler task that was defined in the documentation

$TaskName = "Projects in Stores Server 24/7"
$TaskPath = "\Activity Hub\"
$ScriptPath = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\start_server_24_7.bat"
$WorkingDirectory = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "SETTING UP 24/7 AUTO-START FOR PROJECTS IN STORES" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Task Name:        $TaskName" -ForegroundColor Yellow
Write-Host "Task Path:        $TaskPath" -ForegroundColor Yellow
Write-Host "Script:           $ScriptPath" -ForegroundColor Yellow
Write-Host "Working Dir:      $WorkingDirectory" -ForegroundColor Yellow
Write-Host ""

# Check for admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Host "❌ ERROR: This script requires Administrator privileges!" -ForegroundColor Red
    Write-Host "   Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

# Check if task already exists
$existingTask = Get-ScheduledTask -TaskName $TaskName -TaskPath $TaskPath -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "✓ Scheduled task '$TaskName' already exists" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Current Status:" -ForegroundColor Cyan
    Write-Host "  Name: $($existingTask.TaskName)"
    Write-Host "  Path: $($existingTask.TaskPath)"
    Write-Host "  State: $($existingTask.State)"
    Write-Host ""
    
    $confirm = Read-Host "Replace existing task? (Y/N)"
    if ($confirm -ne 'Y' -and $confirm -ne 'y') {
        Write-Host "Cancelled." -ForegroundColor Gray
        Write-Host ""
        exit 0
    }
    
    Write-Host "Removing existing task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -TaskPath $TaskPath -Confirm:$false
}

try {
    # Create trigger for system startup
    Write-Host "Creating startup trigger..." -ForegroundColor Cyan
    $trigger = New-ScheduledTaskTrigger -AtStartup
    
    # Create action to run the batch file
    Write-Host "Creating action to start server..." -ForegroundColor Cyan
    $action = New-ScheduledTaskAction `
        -Execute "cmd.exe" `
        -Argument "/c `"$ScriptPath`"" `
        -WorkingDirectory $WorkingDirectory
    
    # Create principal to run with highest privileges
    Write-Host "Setting up permissions..." -ForegroundColor Cyan
    $principal = New-ScheduledTaskPrincipal `
        -UserId "$env:USERDOMAIN\$env:USERNAME" `
        -LogonType ServiceAccount `
        -RunLevel Highest
    
    # Create settings for reliable 24/7 operation
    Write-Host "Configuring 24/7 settings..." -ForegroundColor Cyan
    $settings = New-ScheduledTaskSettingsSet `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -StartWhenAvailable `
        -RunOnlyIfNetworkAvailable:$false `
        -RestartCount 3 `
        -RestartInterval (New-TimeSpan -Minutes 1)
    
    # Register the scheduled task
    Write-Host "Registering task..." -ForegroundColor Cyan
    Register-ScheduledTask `
        -TaskName $TaskName `
        -TaskPath $TaskPath `
        -Trigger $trigger `
        -Action $action `
        -Principal $principal `
        -Settings $settings `
        -Description "Automatically starts the Projects in Stores backend server 24/7 with auto-restart on crash" `
        -Force | Out-Null
    
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host "✅ SUCCESS! Scheduled task created" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Task Details:" -ForegroundColor Cyan
    Write-Host "  Name:            $TaskName"
    Write-Host "  Path:            $TaskPath"
    Write-Host "  Trigger:         System Startup"
    Write-Host "  Privileges:      Administrator (Highest)"
    Write-Host "  Auto-Restart:    Yes (3 attempts, 1 min interval)"
    Write-Host ""
    Write-Host "The backend server will now:" -ForegroundColor Yellow
    Write-Host "  • Automatically start when the computer boots"
    Write-Host "  • Run with administrator privileges"
    Write-Host "  • Restart automatically if it crashes"
    Write-Host "  • Listen on port 8001"
    Write-Host "  • Be accessible at http://localhost:8001"
    Write-Host ""
    Write-Host "Users can access the dashboard immediately after boot." -ForegroundColor Green
    Write-Host ""
}
catch {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host "❌ ERROR: Failed to create scheduled task" -ForegroundColor Red
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Error Details:" -ForegroundColor Yellow
    Write-Host "$_"
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Cyan
    Write-Host "  • Make sure you're running as Administrator"
    Write-Host "  • Verify the script path exists: $ScriptPath"
    Write-Host "  • Check file permissions on the script"
    Write-Host ""
    exit 1
}
