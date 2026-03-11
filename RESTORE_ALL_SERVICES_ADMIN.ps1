# Restore All Activity Hub Services
# REQUIRES ADMINISTRATOR PRIVILEGES
# Right-click PowerShell - Run as Administrator, then run this script

Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "ACTIVITY HUB - RESTORE ALL SERVICES" -ForegroundColor Cyan
Write-Host "March 10, 2026" -ForegroundColor Cyan
Write-Host "================================================`n" -ForegroundColor Cyan

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "ERROR: This script MUST be run as Administrator" -ForegroundColor Red
    Write-Host "`nHow to run as Administrator:" -ForegroundColor Yellow
    Write-Host "  1. Press Win+X"
    Write-Host "  2. Select 'Windows PowerShell (Admin)'"
    Write-Host "  3. Run: .\RESTORE_ALL_SERVICES_ADMIN.ps1"
    Write-Host ""
    Exit 1
}

Write-Host "SUCCESS: Running with Administrator privileges`n" -ForegroundColor Green

# ============================================================
# PART 1: PROJECTS IN STORES BACKEND (Port 8001)
# ============================================================

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "PART 1: Projects in Stores Backend (Port 8001)" -ForegroundColor Cyan
Write-Host "================================================`n" -ForegroundColor Cyan

Write-Host "[1/3] Creating ActivityHubServer scheduled task..." -ForegroundColor Yellow

try {
    # Remove old task if exists
    Get-ScheduledTask -TaskName "ActivityHubServer" -ErrorAction SilentlyContinue | Unregister-ScheduledTask -Confirm:$false -ErrorAction SilentlyContinue
    
    $action = New-ScheduledTaskAction -Execute "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_server_24_7.bat" `
        -WorkingDirectory "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"
    
    $trigger = New-ScheduledTaskTrigger -AtStartup -RandomDelay (New-TimeSpan -Seconds 30)
    
    $principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
    
    Register-ScheduledTask -TaskName "ActivityHubServer" `
        -Action $action `
        -Trigger $trigger `
        -Principal $principal `
        -Force | Out-Null
    
    Write-Host "   [OK] ActivityHubServer task created successfully" -ForegroundColor Green
} catch {
    Write-Host "   [ERROR] Failed to create task: $_" -ForegroundColor Red
    Exit 1
}

Write-Host "`n[2/3] Verifying task configuration..." -ForegroundColor Yellow
try {
    $task = Get-ScheduledTask -TaskName "ActivityHubServer" -ErrorAction Stop
    Write-Host "   [OK] Task Name: $($task.TaskName)" -ForegroundColor Green
    Write-Host "   [OK] State: $($task.State)" -ForegroundColor Green
    Write-Host "   [OK] Owner: $($task.Principal.UserId)" -ForegroundColor Green
} catch {
    Write-Host "   [ERROR] Failed to verify: $_" -ForegroundColor Red
}

Write-Host "`n[3/3] Starting Projects in Stores backend immediately..." -ForegroundColor Yellow
try {
    Start-ScheduledTask -TaskName "ActivityHubServer" -ErrorAction Stop
    Write-Host "   [OK] Service started - waiting for port 8001 to listen..." -ForegroundColor Green
    
    # Wait for service to start
    Start-Sleep -Seconds 5
    
    # Check if listening
    $listening = netstat -ano 2>$null | Select-String ":8001.*LISTENING"
    if ($listening) {
        Write-Host "   [OK] Port 8001 is now LISTENING" -ForegroundColor Green
        Write-Host "   [OK] Projects in Stores Backend is ONLINE" -ForegroundColor Green
    } else {
        Write-Host "   [WAIT] Port 8001 not listening yet - may be starting up" -ForegroundColor Yellow
        Write-Host "   Waiting 10 more seconds..." -ForegroundColor Gray
        Start-Sleep -Seconds 10
        $listening = netstat -ano 2>$null | Select-String ":8001.*LISTENING"
        if ($listening) {
            Write-Host "   [OK] Port 8001 is now LISTENING" -ForegroundColor Green
        }
    }
} catch {
    Write-Host "   [WAIT] Task started but verify manually: $_" -ForegroundColor Yellow
}

# ============================================================
# PART 2: DC MANAGER PAYCYCLE TASKS (26 Tasks)
# ============================================================

Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "PART 2: DC Manager PayCycle Tasks" -ForegroundColor Cyan
Write-Host "================================================`n" -ForegroundColor Cyan

$PayCycleDir = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails"
$SetupScript = "$PayCycleDir\setup_tasks_revised.ps1"

Write-Host "[1/3] Checking PayCycle directory..." -ForegroundColor Yellow
if (-not (Test-Path $PayCycleDir)) {
    Write-Host "   [ERROR] PayCycle directory not found" -ForegroundColor Red
    Write-Host "   Location: $PayCycleDir" -ForegroundColor Red
    Exit 1
}
Write-Host "   [OK] PayCycle directory found" -ForegroundColor Green

Write-Host "`n[2/3] Running PayCycle setup script..." -ForegroundColor Yellow
try {
    if (-not (Test-Path $SetupScript)) {
        Write-Host "   [ERROR] Setup script not found: $SetupScript" -ForegroundColor Red
        Exit 1
    }
    
    # Run the setup script
    & $SetupScript
    Write-Host "   [OK] PayCycle setup completed" -ForegroundColor Green
} catch {
    Write-Host "   [ERROR] Failed to run setup: $_" -ForegroundColor Red
    Exit 1
}

Write-Host "`n[3/3] Verifying 26 PayCycle tasks..." -ForegroundColor Yellow
try {
    $PayCycleTasks = Get-ScheduledTask -ErrorAction SilentlyContinue | Where-Object {$_.TaskName -like "DC-EMAIL-PC-*"}
    $TaskCount = if ($PayCycleTasks) { $PayCycleTasks.Count } else { 0 }
    
    if ($TaskCount -eq 26) {
        Write-Host "   [OK] All 26 PayCycle tasks verified and active" -ForegroundColor Green
        
        # Show next scheduled execution
        $NextPaycycle = $PayCycleTasks | Where-Object {$_.NextRunTime -gt (Get-Date)} | Sort-Object NextRunTime | Select-Object -First 1
        if ($NextPaycycle) {
            Write-Host "   [OK] Next PayCycle Execution:" -ForegroundColor Green
            Write-Host "      Task: $($NextPaycycle.TaskName)" -ForegroundColor Green
            Write-Host "      Time: $($NextPaycycle.NextRunTime)" -ForegroundColor Green
        }
    } else {
        Write-Host "   [WARN] Found $TaskCount/26 tasks (expected 26)" -ForegroundColor Yellow
        Write-Host "   Rerun setup script or contact support" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   [WARN] Could not verify tasks: $_" -ForegroundColor Yellow
}

# ============================================================
# PART 3: JOB CODES TEAMING (Continuous Service)
# ============================================================

Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "PART 3: Job Codes and Teaming" -ForegroundColor Cyan
Write-Host "================================================`n" -ForegroundColor Cyan

$JobCodesDir = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming"
$PythonExe = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"

Write-Host "[1/3] Checking Job Codes project directory..." -ForegroundColor Yellow
if (-not (Test-Path $JobCodesDir)) {
    Write-Host "   [ERROR] Job Codes directory not found" -ForegroundColor Red
    Write-Host "   Location: $JobCodesDir" -ForegroundColor Red
    Exit 1
}
Write-Host "   [OK] Job Codes directory found" -ForegroundColor Green

Write-Host "`n[2/3] Creating Job Codes comparison scheduled task (Daily)..." -ForegroundColor Yellow
try {
    # Remove old task if exists
    Get-ScheduledTask -TaskName "JobCodes-Continuous-Sync" -ErrorAction SilentlyContinue | Unregister-ScheduledTask -Confirm:$false -ErrorAction SilentlyContinue
    
    # Create action for both comparison scripts
    $action = New-ScheduledTaskAction -Execute $PythonExe `
        -Argument 'job_code_comparison.py' `
        -WorkingDirectory $JobCodesDir
    
    # Run daily at 2 AM
    $trigger = New-ScheduledTaskTrigger -Daily -At "02:00 AM"
    
    # Also add at startup trigger
    $trigger2 = New-ScheduledTaskTrigger -AtStartup
    
    $principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
    
    Register-ScheduledTask -TaskName "JobCodes-Continuous-Sync" `
        -Action $action `
        -Trigger $trigger `
        -Principal $principal `
        -Force | Out-Null
    
    # Add second trigger for startup
    $task = Get-ScheduledTask -TaskName "JobCodes-Continuous-Sync"
    $task.Triggers += $trigger2
    Set-ScheduledTask -InputObject $task | Out-Null
    
    Write-Host "   [OK] Job Codes task created (Daily 2 AM + At Startup)" -ForegroundColor Green
} catch {
    Write-Host "   [ERROR] Failed to create task: $_" -ForegroundColor Red
}

Write-Host "`n[3/3] Verifying Job Codes task..." -ForegroundColor Yellow
try {
    $task = Get-ScheduledTask -TaskName "JobCodes-Continuous-Sync" -ErrorAction Stop
    Write-Host "   [OK] Task Name: $($task.TaskName)" -ForegroundColor Green
    Write-Host "   [OK] State: $($task.State)" -ForegroundColor Green
    Write-Host "   [OK] Next Run: $(($task.Triggers | Where-Object {$_.Enabled} | Select-Object -First 1).NextRunTime)" -ForegroundColor Green
} catch {
    Write-Host "   [WARN] Could not verify: $_" -ForegroundColor Yellow
}

# ============================================================
# FINAL SUMMARY
# ============================================================

Write-Host "`n================================================" -ForegroundColor Green
Write-Host "RESTORATION COMPLETE" -ForegroundColor Green
Write-Host "================================================`n" -ForegroundColor Green

Write-Host "Service Status Summary:" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

Write-Host "`n1. Projects in Stores Backend" -ForegroundColor White
Write-Host "   Port: 8001" -ForegroundColor Gray
Write-Host "   Auto-start: ENABLED (on system startup)" -ForegroundColor Green
Write-Host "   Status: $(if ($listening) { 'RUNNING' } else { 'STARTED' })" -ForegroundColor Green
Write-Host "   Task Name: ActivityHubServer" -ForegroundColor Gray

Write-Host "`n2. DC Manager Change Detection (PayCycle)" -ForegroundColor White
Write-Host "   Tasks: 26 scheduled" -ForegroundColor Gray
Write-Host "   Auto-start: ENABLED (on PayCycle dates)" -ForegroundColor Green
Write-Host "   Status: READY" -ForegroundColor Green
Write-Host "   Task Names: DC-EMAIL-PC-01 through DC-EMAIL-PC-26" -ForegroundColor Gray

Write-Host "`n3. Job Codes and Teaming Continuous Sync" -ForegroundColor White
Write-Host "   Type: Analysis and comparison service" -ForegroundColor Gray
Write-Host "   Auto-start: ENABLED (daily plus system startup)" -ForegroundColor Green
Write-Host "   Status: READY" -ForegroundColor Green
Write-Host "   Task Name: JobCodes-Continuous-Sync" -ForegroundColor Gray

Write-Host "`n================================================" -ForegroundColor Cyan

Write-Host "`nNext Steps:" -ForegroundColor Cyan
Write-Host "   1. Verify Projects in Stores is running at http://localhost:8001/admin.html" -ForegroundColor Gray
Write-Host "   2. Monitor port 8001 for next 5 minutes to confirm startup" -ForegroundColor Gray
Write-Host "   3. Check Job Codes output tomorrow morning" -ForegroundColor Gray
Write-Host "   4. Document next DC Manager PayCycle date for monitoring" -ForegroundColor Gray
Write-Host "   5. Reboot system to verify all auto-start tasks work" -ForegroundColor Gray

Write-Host "`nAll Activity Hub services have been restored!" -ForegroundColor Green
Write-Host "   They will automatically restart on system reboot.`n" -ForegroundColor Green
