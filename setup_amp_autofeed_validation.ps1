# Setup script for AMP AutoFeed Validation
# Run this in admin PowerShell to install dependencies and create scheduled task

Write-Host "Installing Python dependencies for AMP AutoFeed Validation..." -ForegroundColor Green

$pythonPath = python -c "import sys; print(sys.executable)" 2>$null
if (-not $pythonPath) {
    Write-Host "ERROR: Python not found. Make sure Python is installed and in PATH" -ForegroundColor Red
    exit 1
}

Write-Host "Python found: $pythonPath" -ForegroundColor Green

# Install required packages
Write-Host "`nInstalling beautifulsoup4..." -ForegroundColor Cyan
& python -m pip install beautifulsoup4 -q
if ($LASTEXITCODE -eq 0) { 
    Write-Host "[OK] beautifulsoup4 installed" -ForegroundColor Green 
}

Write-Host "Installing pywin32 (for Outlook access)..." -ForegroundColor Cyan
& python -m pip install pywin32 -q

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] pywin32 installed" -ForegroundColor Green
    Write-Host "`nRunning pywin32 post-install (required for Outlook COM access)..." -ForegroundColor Cyan
    & python -m pip install pypiwin32
    $pythonScripts = "$($pythonPath -replace 'python.exe', '')\Scripts"
    & "$pythonScripts\pywin32_postinstall.py" -install
    Write-Host "[OK] pywin32 post-install complete" -ForegroundColor Green
}

Write-Host "`n[OK] All dependencies installed" -ForegroundColor Green

# Create scheduled task for daily validation
Write-Host "`nCreating scheduled task for daily validation..." -ForegroundColor Cyan

$ScriptPath = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\amp_autofeed_validation.py"
$LogDir = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\amp_validation_logs"

$action = New-ScheduledTaskAction `
    -Execute "python.exe" `
    -Argument "-u `"$ScriptPath`" --action daily --log-dir `"$LogDir`""

$trigger = New-ScheduledTaskTrigger -Daily -At 7:00am

$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount

$settings = New-ScheduledTaskSettingsSet `
    -DontStopOnIdleEnd `
    -RunOnlyIfNetworkAvailable `
    -RestartCount 2 `
    -RestartInterval (New-TimeSpan -Minutes 5)

$taskName = "AMP-AutoFeed-DailyValidation"

try {
    Register-ScheduledTask `
        -TaskName $taskName `
        -Action $action `
        -Trigger $trigger `
        -Principal $principal `
        -Settings $settings `
        -Force
    
    Write-Host "[OK] Scheduled task created: $taskName" -ForegroundColor Green
    Write-Host "  Schedule: Daily at 7:00 AM" -ForegroundColor Green
    Write-Host "  Log directory: $LogDir" -ForegroundColor Green
} catch {
    Write-Host "ERROR creating scheduled task: $_" -ForegroundColor Red
    exit 1
}

# Create weekly historical report task
Write-Host "`nCreating scheduled task for weekly historical reports..." -ForegroundColor Cyan

$reportAction = New-ScheduledTaskAction `
    -Execute "python.exe" `
    -Argument "-u `"$ScriptPath`" --action both --log-dir `"$LogDir`" --days 90"

$reportTrigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 6:00am

$reportTaskName = "AMP-AutoFeed-WeeklyReport"

try {
    Register-ScheduledTask `
        -TaskName $reportTaskName `
        -Action $reportAction `
        -Trigger $reportTrigger `
        -Principal $principal `
        -Settings $settings `
        -Force
    
    Write-Host "[OK] Scheduled task created: $reportTaskName" -ForegroundColor Green
    Write-Host "  Schedule: Weekly on Monday at 6:00 AM" -ForegroundColor Green
} catch {
    Write-Host "ERROR creating weekly report task: $_" -ForegroundColor Red
}

Write-Host "`n=== Setup Complete ===" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Verify Outlook is configured with the correct email folder"
Write-Host "2. Run manually first: python `"$ScriptPath`" --action daily"
Write-Host "3. Check logs: $LogDir"
Write-Host "4. Scheduled tasks:" -ForegroundColor Cyan
Get-ScheduledTask -TaskName $taskName, $reportTaskName -ErrorAction SilentlyContinue | Select-Object TaskName, State
