# PayCycle Task Scheduler Setup - CORRECTED for Future Dates Only
# Only creates tasks for PayCycles with future dates (TODAY is March 24, 2026)
# This version creates recurring tasks that will execute every 2 weeks starting from first future date

Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "PayCycle Task Setup - Future Only" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Current Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm')`n" -ForegroundColor Yellow

$WorkingDirectory = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails"
$PythonExe = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"
$ScriptName = "daily_check_smart.py"

# ALL PayCycles for reference
$AllPayCycles = @(
    @{ PC = 1; Date = "2026-02-06" },
    @{ PC = 2; Date = "2026-02-20" },
    @{ PC = 3; Date = "2026-03-06" },
    @{ PC = 4; Date = "2026-03-20" },
    @{ PC = 5; Date = "2026-04-03" },
    @{ PC = 6; Date = "2026-04-17" },
    @{ PC = 7; Date = "2026-05-01" },
    @{ PC = 8; Date = "2026-05-15" },
    @{ PC = 9; Date = "2026-05-29" },
    @{ PC = 10; Date = "2026-06-12" },
    @{ PC = 11; Date = "2026-06-26" },
    @{ PC = 12; Date = "2026-07-10" },
    @{ PC = 13; Date = "2026-07-24" },
    @{ PC = 14; Date = "2026-08-07" },
    @{ PC = 15; Date = "2026-08-21" },
    @{ PC = 16; Date = "2026-09-04" },
    @{ PC = 17; Date = "2026-09-18" },
    @{ PC = 18; Date = "2026-10-02" },
    @{ PC = 19; Date = "2026-10-16" },
    @{ PC = 20; Date = "2026-10-30" },
    @{ PC = 21; Date = "2026-11-13" },
    @{ PC = 22; Date = "2026-11-27" },
    @{ PC = 23; Date = "2026-12-11" },
    @{ PC = 24; Date = "2026-12-25" },
    @{ PC = 25; Date = "2027-01-08" },
    @{ PC = 26; Date = "2027-01-22" }
)

# Filter to ONLY future PayCycles
$Today = Get-Date
$FuturePayCycles = $AllPayCycles | Where-Object {[DateTime]::Parse($_.Date) -gt $Today}

Write-Host "Status:`n"
Write-Host "  Past PayCycles: $($AllPayCycles.Count - $FuturePayCycles.Count)"
Write-Host "  Future PayCycles: $($FuturePayCycles.Count)`n"

if ($FuturePayCycles.Count -eq 0) {
    Write-Host "ERROR: No future PayCycles found!" -ForegroundColor Red
    exit 1
}

Write-Host "Configuration:`n"
Write-Host "  Working Directory: $WorkingDirectory"
Write-Host "  Python: $PythonExe"
Write-Host "  Script: $ScriptName"
Write-Host "  Total to Create: $($FuturePayCycles.Count)`n"

# Verify directories/files exist
if (-not (Test-Path $WorkingDirectory)) {
    Write-Host "[✗] Working directory not found" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $PythonExe)) {
    Write-Host "[✗] Python executable not found" -ForegroundColor Red
    exit 1
}

Write-Host "Creating scheduled tasks...`n" -ForegroundColor Cyan

$CreatedCount = 0
$FailedCount = 0

foreach ($Cycle in $FuturePayCycles) {
    $PC = $Cycle.PC.ToString("00")
    $Date = $Cycle.Date
    $TaskName = "DC-EMAIL-PC-$PC"
    $Description = "DC Manager Change Detection - PayCycle $PC ($Date @ 06:00)"
    
    try {
        # Parse the date and time
        $TriggerDateTime = [DateTime]::Parse("$Date 06:00:00")
        
        # Create trigger for this specific date at 6:00 AM
        $Trigger = New-ScheduledTaskTrigger -Once -At $TriggerDateTime
        
        # Create action
        $Action = New-ScheduledTaskAction `
            -Execute $PythonExe `
            -Argument "`"$WorkingDirectory\$ScriptName`"" `
            -WorkingDirectory $WorkingDirectory
        
        # Create principal (run with highest privilege)
        $Principal = New-ScheduledTaskPrincipal `
            -UserId "SYSTEM" `
            -LogonType ServiceAccount `
            -RunLevel Highest
        
        # Create/register the task
        Register-ScheduledTask `
            -TaskName $TaskName `
            -Action $Action `
            -Trigger $Trigger `
            -Principal $Principal `
            -Description $Description `
            -Force `
            -ErrorAction Stop | Out-Null
        
        Write-Host "[✓] PC $PC : $Date @ 06:00 AM" -ForegroundColor Green
        $CreatedCount++
    }
    catch {
        Write-Host "[✗] PC $PC : FAILED - $($_.Exception.Message)" -ForegroundColor Red
        $FailedCount++
    }
}

Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "Setup Complete" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Created: $CreatedCount tasks" -ForegroundColor Green
Write-Host "Failed:  $FailedCount tasks" -ForegroundColor $(if ($FailedCount -gt 0) { "Red" } else { "Green" })

# Verify
Write-Host "`nVerifying tasks in Task Scheduler...`n" -ForegroundColor Yellow
$VerifyCount = (Get-ScheduledTask | Where-Object {$_.TaskName -like "DC-EMAIL-PC-*"} | Measure-Object).Count
Write-Host "Tasks found in Task Scheduler: $VerifyCount`n" -ForegroundColor Cyan

if ($VerifyCount -gt 0) {
    Write-Host "Next 5 scheduled PayCycles:`n" -ForegroundColor Cyan
    Get-ScheduledTask | Where-Object {$_.TaskName -like "DC-EMAIL-PC-*"} | 
        Select-Object TaskName, State, NextRunTime | 
        Sort-Object NextRunTime | 
        Select-Object -First 5 | 
        ForEach-Object { Write-Host "  $($_.TaskName) -> $($_.NextRunTime)" -ForegroundColor Green }
}

Write-Host ""
