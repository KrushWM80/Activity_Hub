# DC Manager Change Detection PayCycle Task Verification
# Purpose: Verify all 26 PayCycle tasks are registered; recreate if missing after system restart
# Run after system restart to ensure PayCycle tasks are active

Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "PayCycle Task Verification" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Time: $(Get-Date)" -ForegroundColor Gray
Write-Host ""

$PayCycleDir = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails"
$SetupScript = "$PayCycleDir\setup_tasks_revised.ps1"

# Check if PayCycle directory exists
if (!(Test-Path $PayCycleDir)) {
    Write-Host "[✗] PayCycle directory not found: $PayCycleDir" -ForegroundColor Red
    Write-Host "    Cannot verify or recreate tasks." -ForegroundColor Red
    Exit 1
}

# Check how many tasks currently exist
$ExistingTasks = Get-ScheduledTask -ErrorAction SilentlyContinue | Where-Object {$_.TaskName -like "DC-EMAIL-PC-*"}
$TaskCount = if ($ExistingTasks) { $ExistingTasks.Count } else { 0 }

Write-Host "Current PayCycle tasks: $TaskCount/26" -ForegroundColor Yellow

if ($TaskCount -eq 26) {
    Write-Host "[✓] All 26 PayCycle tasks verified and active" -ForegroundColor Green
    
    # Show next scheduled execution
    $NextPaycycle = $ExistingTasks | Where-Object {$_.NextRunTime -gt (Get-Date)} | Sort-Object NextRunTime | Select-Object -First 1
    if ($NextPaycycle) {
        Write-Host ""
        Write-Host "Next PayCycle Execution:" -ForegroundColor Cyan
        Write-Host "  Task: $($NextPaycycle.TaskName)" -ForegroundColor Green
        Write-Host "  Time: $($NextPaycycle.NextRunTime)" -ForegroundColor Green
        Write-Host ""
    }
    
    # Show all upcoming PayCycles for the next 30 days
    $Upcoming = $ExistingTasks | 
        Where-Object {$_.NextRunTime -gt (Get-Date) -and $_.NextRunTime -lt (Get-Date).AddDays(30)} | 
        Sort-Object NextRunTime
    
    if ($Upcoming.Count -gt 0) {
        Write-Host "Upcoming PayCycles (Next 30 days):" -ForegroundColor Cyan
        foreach ($task in $Upcoming) {
            $pcNum = $task.TaskName -replace "DC-EMAIL-PC-", ""
            Write-Host "  PC $pcNum : $($task.NextRunTime)" -ForegroundColor Gray
        }
    }
} else {
    Write-Host "[WARNING] Missing PayCycle tasks detected!" -ForegroundColor Yellow
    Write-Host "Found: $TaskCount, Expected: 26" -ForegroundColor Yellow
    Write-Host ""
    
    # Check if setup script exists
    if (!(Test-Path $SetupScript)) {
        Write-Host "[✗] Setup script not found: $SetupScript" -ForegroundColor Red
        Write-Host "    Cannot recreate tasks automatically." -ForegroundColor Red
        Exit 1
    }
    
    # Prompt user to fix
    Write-Host "To recreate missing tasks:" -ForegroundColor Cyan
    Write-Host "1. Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Gray
    Write-Host "2. Run: cd '$PayCycleDir'" -ForegroundColor Gray
    Write-Host "3. Run: .\setup_tasks_revised.ps1" -ForegroundColor Gray
    Write-Host ""
    
    # Ask if user wants to recreate now
    if ((Get-Process -Name powershell -ErrorAction SilentlyContinue | Where-Object {$_.Description -eq "Administrator"} | Measure-Object).Count -gt 0) {
        $response = Read-Host "Try to recreate tasks now? (y/n)"
        if ($response -eq 'y' -or $response -eq 'Y') {
            Write-Host "Launching setup script in admin window..." -ForegroundColor Yellow
            Start-Process powershell -ArgumentList "-NoExit -Command `\"cd '$PayCycleDir'; .\\setup_tasks_revised.ps1`\"" -Verb RunAs
            Write-Host "Setup launched. Check new window for results." -ForegroundColor Cyan
        }
    }
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Verification Complete" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
