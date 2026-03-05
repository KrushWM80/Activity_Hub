# Create scheduled task for Projects in Stores auto-start
# This must run as Administrator

param([switch]$RunAsAdmin)

# Check if running as Admin
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "Not running as Administrator. Requesting elevation..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`" -RunAsAdmin" -Verb RunAs -Wait
    exit
}

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "Projects in Stores Server - Auto-Start Setup" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

$TaskName = "Projects in Stores Server 24/7"
$BatchScript = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_server_24_7.bat"

# Verify batch script exists
if (-not (Test-Path $BatchScript)) {
    Write-Host "ERROR: Batch script not found: $BatchScript" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Batch Script: $BatchScript" -ForegroundColor Green
Write-Host "Task Name: $TaskName" -ForegroundColor Green

# Remove existing task if present
Write-Host "`nRemoving old task (if exists)..." -ForegroundColor Yellow
Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue | Unregister-ScheduledTask -Confirm:$false -ErrorAction SilentlyContinue | Out-Null

# Create task trigger (At Startup)
$Trigger = New-ScheduledTaskTrigger -AtStartup

# Create task action
$Action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$BatchScript`""

# Create task settings
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable:$false `
    -MultipleInstances IgnoreNew

# Register the task
try {
    Write-Host "`nCreating scheduled task..." -ForegroundColor Cyan
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Action $Action `
        -Trigger $Trigger `
        -Settings $Settings `
        -RunLevel Highest `
        -Force `
        -ErrorAction Stop | Out-Null
    
    Write-Host "✅ Task created successfully!" -ForegroundColor Green
    
    # Verify
    $task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($task) {
        Write-Host "✅ Task verified - Status: $($task.State)" -ForegroundColor Green
        Write-Host "`n📋 Task Details:" -ForegroundColor Cyan
        Write-Host "   Name: $TaskName" -ForegroundColor Cyan
        Write-Host "   State: $($task.State)" -ForegroundColor Cyan
        Write-Host "   Trigger: At System Startup" -ForegroundColor Cyan
        Write-Host "   Run Level: Highest (Admin)" -ForegroundColor Cyan
        Write-Host "`n✅ Server will auto-start on next system reboot!" -ForegroundColor Green
        Write-Host "✅ Server will auto-restart if it crashes!" -ForegroundColor Green
    } else {
        Write-Host "⚠️ WARNING: Task created but verification failed" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "❌ ERROR: Failed to create task" -ForegroundColor Red
    Write-Host "Details: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "`n============================================" -ForegroundColor Green
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "============================================`n" -ForegroundColor Green

Read-Host "Press Enter to close"
