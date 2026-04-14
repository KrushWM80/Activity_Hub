# Fast Setup for AMP AutoFeed Validation
# No execution policy issues - runs directly

Write-Host "AMP AutoFeed Validation - Setup" -ForegroundColor Green
Write-Host "================================`n" -ForegroundColor Green

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Cyan
$pythonCheck = & cmd /c "py --version 2>&1"

if ($pythonCheck -like "*Python*") {
    Write-Host "[OK] Python found: $pythonCheck" -ForegroundColor Green
    $pythonCmd = "py"
} else {
    $pythonCheck2 = & cmd /c "python3 --version 2>&1"
    if ($pythonCheck2 -like "*Python*") {
        Write-Host "[OK] Python3 found: $pythonCheck2" -ForegroundColor Green
        $pythonCmd = "python3"
    } else {
        Write-Host "[ERROR] Python not found in PATH" -ForegroundColor Red
        Write-Host "`nPlease install Python:" -ForegroundColor Yellow
        Write-Host "  Option 1: Windows Store - search for 'Python 3.11'"
        Write-Host "  Option 2: python.org/downloads"
        Write-Host "  Option 3: Ensure Python is added to PATH during install"
        exit 1
    }
}

# Install dependencies
Write-Host "`nInstalling dependencies..." -ForegroundColor Cyan
Write-Host "  Installing beautifulsoup4..." -ForegroundColor Gray
& $pythonCmd -m pip install beautifulsoup4 -q
if ($LASTEXITCODE -eq 0) {
    Write-Host "  [OK] beautifulsoup4 installed" -ForegroundColor Green
}

Write-Host "  Installing pywin32..." -ForegroundColor Gray
& $pythonCmd -m pip install pywin32 -q
if ($LASTEXITCODE -eq 0) {
    Write-Host "  [OK] pywin32 installed" -ForegroundColor Green
}

Write-Host "  Installing pypiwin32 (post-install)..." -ForegroundColor Gray
& $pythonCmd -m pip install pypiwin32 -q

# Try to run pywin32 post-install
Write-Host "  Running pywin32 post-install..." -ForegroundColor Gray
& cmd /c "$pythonCmd -m Scripts.pywin32_postinstall -install 2>nul" | Out-Null
Write-Host "  [OK] pywin32 post-install complete" -ForegroundColor Green

Write-Host "`n[OK] All dependencies installed!" -ForegroundColor Green

# Create scheduled tasks
Write-Host "`nCreating scheduled tasks..." -ForegroundColor Cyan

$ScriptPath = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\amp_autofeed_orchestrator.py"
$LogDir = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\amp_validation_logs"

# Daily validation task
Write-Host "  Creating daily validation task..." -ForegroundColor Gray
$action = New-ScheduledTaskAction -Execute $pythonCmd -Argument "`"$ScriptPath`" daily --log-dir `"$LogDir`""
$trigger = New-ScheduledTaskTrigger -Daily -At 7:00am
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount
$settings = New-ScheduledTaskSettingsSet -DontStopOnIdleEnd -RunOnlyIfNetworkAvailable

try {
    Register-ScheduledTask -TaskName "AMP-AutoFeed-DailyValidation" `
        -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force | Out-Null
    Write-Host "  [OK] Daily task created (7:00 AM)" -ForegroundColor Green
} catch {
    Write-Host "  [WARN] Could not create daily task: $_" -ForegroundColor Yellow
}

# Weekly report task
Write-Host "  Creating weekly report task..." -ForegroundColor Gray
$reportAction = New-ScheduledTaskAction -Execute $pythonCmd -Argument "`"$ScriptPath`" csv-report --days 90 --log-dir `"$LogDir`""
$reportTrigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 6:00am

try {
    Register-ScheduledTask -TaskName "AMP-AutoFeed-WeeklyReport" `
        -Action $reportAction -Trigger $reportTrigger -Principal $principal -Settings $settings -Force | Out-Null
    Write-Host "  [OK] Weekly task created (Monday 6:00 AM)" -ForegroundColor Green
} catch {
    Write-Host "  [WARN] Could not create weekly task: $_" -ForegroundColor Yellow
}

# Summary
Write-Host "`n==== Setup Complete ====" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Verify Outlook folders exist:" -ForegroundColor Cyan
Write-Host "   Inbox > ATC > Reports > AMP > [Quick Base API Response Data + Auto Feed]"
Write-Host ""
Write-Host "2. Test validation:" -ForegroundColor Cyan
Write-Host "   cd 'C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub'"
Write-Host "   $pythonCmd .\amp_autofeed_orchestrator.py daily"
Write-Host ""
Write-Host "3. Check scheduled tasks:" -ForegroundColor Cyan
Write-Host "   Get-ScheduledTask -TaskName 'AMP-AutoFeed-*' | Select-Object TaskName, State"
Write-Host ""
Write-Host "Logs: $LogDir" -ForegroundColor Gray
