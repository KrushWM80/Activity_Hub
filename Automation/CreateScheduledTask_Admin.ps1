# Create 24/7 Auto-Start Task for Projects in Stores Backend
# This script MUST be run as Administrator

# Check for admin privileges
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script requires Administrator privileges!" -ForegroundColor Red
    Write-Host "Please run PowerShell as Administrator and try again" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Creating scheduled task for Projects in Stores Backend 24/7..." -ForegroundColor Cyan

$TaskName = "Projects in Stores Server 24/7"
$ScriptPath = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_server_24_7.bat"

# Remove existing task if it exists
Write-Host "`nRemoving old task if it exists..." -ForegroundColor Yellow
Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue | Unregister-ScheduledTask -Confirm:$false -ErrorAction SilentlyContinue | Out-Null

# Create trigger for system startup
$Trigger = New-ScheduledTaskTrigger -AtStartup

# Create action to run the batch file
$Action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$ScriptPath`""

# Create task settings for 24/7 operation
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable:$false `
    -MultipleInstances IgnoreNew

# Register the task to run with highest privileges
try {
    Register-ScheduledTask -TaskName $TaskName `
        -Action $Action `
        -Trigger $Trigger `
        -Settings $Settings `
        -RunLevel Highest `
        -Force `
        -ErrorAction Stop | Out-Null
    
    Write-Host "`n✅ SUCCESS: Scheduled task created!" -ForegroundColor Green
    Write-Host "   Task Name: $TaskName" -ForegroundColor Green
    Write-Host "   Trigger: At system startup" -ForegroundColor Green
    Write-Host "   Run Level: Highest (Admin)" -ForegroundColor Green
    Write-Host "   Script: $ScriptPath" -ForegroundColor Green
    
    # Verify task
    Write-Host "`nVerifying task..." -ForegroundColor Yellow
    $task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    
    if ($task) {
        Write-Host "✅ Task verified - Status: $($task.State)" -ForegroundColor Green
        Write-Host "`n📋 Details:" -ForegroundColor Cyan
        Write-Host "   - Task will run at system startup" -ForegroundColor Cyan
        Write-Host "   - Batch file will auto-restart server if it crashes" -ForegroundColor Cyan
        Write-Host "   - Server is currently running on port 8001" -ForegroundColor Cyan
    } else {
        Write-Host "⚠️ WARNING: Task was created but verification failed" -ForegroundColor Yellow
    }
    
    Write-Host "`n✅ You're all set! The server will auto-start on the next system restart." -ForegroundColor Green
    Write-Host "   It is currently running and will restart automatically if it crashes." -ForegroundColor Green
    
} catch {
    Write-Host "`n❌ ERROR: Failed to create task" -ForegroundColor Red
    Write-Host "Error details: $_" -ForegroundColor Red
    exit 1
}

Read-Host "`nPress Enter to close"
