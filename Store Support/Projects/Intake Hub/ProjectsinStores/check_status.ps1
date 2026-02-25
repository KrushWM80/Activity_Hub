# =========================================================
# Projects in Stores - Status Check Script
# Run this to verify all services are running
# =========================================================

Write-Host "`n" -ForegroundColor Cyan
Write-Host "╔═══════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  PROJECTS IN STORES - SYSTEM STATUS CHECK        ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check 1: Keep-Awake Service
Write-Host "Checking Keep-Awake Service..." -ForegroundColor Yellow
$keepAwakeTask = Get-ScheduledTask -TaskName "Keep Computer Awake 24/7" -TaskPath "\Activity Hub\" -ErrorAction SilentlyContinue

if ($keepAwakeTask) {
    $taskState = $keepAwakeTask.State
    if ($taskState -eq "Running") {
        Write-Host "  ✅ Keep-Awake: RUNNING (Task Scheduler)" -ForegroundColor Green
    } elseif ($taskState -eq "Ready") {
        Write-Host "  ⚠️  Keep-Awake: Ready but not currently running" -ForegroundColor Yellow
        Write-Host "     → Run: Start-ScheduledTask -TaskName 'Keep Computer Awake 24/7'" -ForegroundColor Gray
    } else {
        Write-Host "  ❌ Keep-Awake: $taskState" -ForegroundColor Red
    }
} else {
    Write-Host "  ❌ Keep-Awake: Task not found" -ForegroundColor Red
    Write-Host "     → Please run the Keep-Awake setup script first" -ForegroundColor Gray
}

Write-Host ""

# Check 2: Projects in Stores Backend (Port 8001)
Write-Host "Checking Projects in Stores Backend..." -ForegroundColor Yellow
$port8001 = Get-NetTCPConnection -LocalPort 8001 -ErrorAction SilentlyContinue

if ($port8001) {
    Write-Host "  ✅ Backend: RUNNING on port 8001" -ForegroundColor Green
    Write-Host "     Process ID: $($port8001.OwningProcess)" -ForegroundColor Gray
    Write-Host "     Access: http://localhost:8001" -ForegroundColor Cyan
} else {
    Write-Host "  ❌ Backend: NOT RUNNING on port 8001" -ForegroundColor Red
    Write-Host "     → Run: .\restart_everything.bat" -ForegroundColor Yellow
}

Write-Host ""

# Check 3: Backend Task Scheduler
Write-Host "Checking Backend Scheduled Task..." -ForegroundColor Yellow
$backendTask = Get-ScheduledTask -TaskName "Projects in Stores Server 24/7" -TaskPath "\Activity Hub\" -ErrorAction SilentlyContinue

if ($backendTask) {
    $taskState = $backendTask.State
    if ($taskState -eq "Running") {
        Write-Host "  ✅ Backend Task: RUNNING (Task Scheduler)" -ForegroundColor Green
    } elseif ($taskState -eq "Ready") {
        Write-Host "  ✅ Backend Task: Ready (will auto-start on reboot)" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  Backend Task: $taskState" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ❌ Backend Task: Not found" -ForegroundColor Red
}

Write-Host ""

# Summary
Write-Host "╔═══════════════════════════════════════════════════╗" -ForegroundColor Cyan
$allRunning = ($port8001) -and ($keepAwakeTask)
if ($allRunning) {
    Write-Host "║  ✅ ALL SYSTEMS OPERATIONAL                     ║" -ForegroundColor Green
} else {
    Write-Host "║  ⚠️  SOME SYSTEMS NOT RUNNING - SEE ABOVE      ║" -ForegroundColor Yellow
}
Write-Host "╚═══════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Additional Info
Write-Host "Quick Commands:" -ForegroundColor Cyan
Write-Host "  • Restart Everything:   .\restart_everything.bat" -ForegroundColor White
Write-Host "  • Restart Backend Only: Restart-ScheduledTask -TaskName 'Projects in Stores Server 24/7'" -ForegroundColor White
Write-Host "  • View Startup Guide:   .\STARTUP_GUIDE.md" -ForegroundColor White
Write-Host ""
