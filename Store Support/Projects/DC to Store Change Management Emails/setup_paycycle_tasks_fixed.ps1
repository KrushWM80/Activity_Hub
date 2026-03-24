# PayCycle Task Setup - FIXED VERSION
# Creates tasks ONLY for future PayCycles (March 24, 2026 onwards)

$WorkingDirectory = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails"
$PythonExe = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"
$ScriptName = "daily_check_smart.py"

# All PayCycles for FY27
$AllPayCycles = @(
    @{ PC = 1; Date = "2026-02-06"; Time = "06:00:00" },
    @{ PC = 2; Date = "2026-02-20"; Time = "06:00:00" },
    @{ PC = 3; Date = "2026-03-06"; Time = "06:00:00" },
    @{ PC = 4; Date = "2026-03-20"; Time = "06:00:00" },
    @{ PC = 5; Date = "2026-04-03"; Time = "06:00:00" },
    @{ PC = 6; Date = "2026-04-17"; Time = "06:00:00" },
    @{ PC = 7; Date = "2026-05-01"; Time = "06:00:00" },
    @{ PC = 8; Date = "2026-05-15"; Time = "06:00:00" },
    @{ PC = 9; Date = "2026-05-29"; Time = "06:00:00" },
    @{ PC = 10; Date = "2026-06-12"; Time = "06:00:00" },
    @{ PC = 11; Date = "2026-06-26"; Time = "06:00:00" },
    @{ PC = 12; Date = "2026-07-10"; Time = "06:00:00" },
    @{ PC = 13; Date = "2026-07-24"; Time = "06:00:00" },
    @{ PC = 14; Date = "2026-08-07"; Time = "06:00:00" },
    @{ PC = 15; Date = "2026-08-21"; Time = "06:00:00" },
    @{ PC = 16; Date = "2026-09-04"; Time = "06:00:00" },
    @{ PC = 17; Date = "2026-09-18"; Time = "06:00:00" },
    @{ PC = 18; Date = "2026-10-02"; Time = "06:00:00" },
    @{ PC = 19; Date = "2026-10-16"; Time = "06:00:00" },
    @{ PC = 20; Date = "2026-10-30"; Time = "06:00:00" },
    @{ PC = 21; Date = "2026-11-13"; Time = "06:00:00" },
    @{ PC = 22; Date = "2026-11-27"; Time = "06:00:00" },
    @{ PC = 23; Date = "2026-12-11"; Time = "06:00:00" },
    @{ PC = 24; Date = "2026-12-25"; Time = "06:00:00" },
    @{ PC = 25; Date = "2027-01-08"; Time = "06:00:00" },
    @{ PC = 26; Date = "2027-01-22"; Time = "06:00:00" }
)

$Today = Get-Date
$FuturePayCycles = @()

# Filter for only future PayCycles
foreach ($Cycle in $AllPayCycles) {
    $CycleDate = [DateTime]::Parse("$($Cycle.Date) $($Cycle.Time)")
    if ($CycleDate -gt $Today) {
        $FuturePayCycles += $Cycle
    }
}

Write-Host "`n$('='*80)"
Write-Host "DC Manager Change Detection - PayCycle Task Setup (FIXED)"
Write-Host "Today: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host "$('='*80)`n"

Write-Host "Creating tasks for FUTURE PayCycles only:`n"
Write-Host "  Total future PayCycles: $($FuturePayCycles.Count)/26"
Write-Host "  Working Directory: $WorkingDirectory"
Write-Host "  Python: $PythonExe`n"

if (-not (Test-Path $WorkingDirectory)) {
    Write-Host "[ERROR] Directory not found: $WorkingDirectory`n" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $PythonExe)) {
    Write-Host "[ERROR] Python not found: $PythonExe`n" -ForegroundColor Red
    exit 1
}

$CreatedCount = 0
$SkippedCount = 0
$FailedCount = 0

foreach ($Cycle in $FuturePayCycles) {
    $PC = $Cycle.PC.ToString("00")
    $Date = $Cycle.Date
    $Time = $Cycle.Time
    $TaskName = "DC-EMAIL-PC-$PC"
    $Description = "PayCycle $PC - $Date @ $Time"
    
    # Check if task already exists
    $ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($ExistingTask) {
        Write-Host "  [SKIP] PC-$PC already exists" -ForegroundColor Yellow
        $SkippedCount++
        continue
    }
    
    try {
        $TriggerDateTime = [DateTime]::Parse("$Date $Time")
        
        # Create trigger for specific date/time
        $Trigger = New-ScheduledTaskTrigger -Once -At $TriggerDateTime
        
        # Create action
        $Action = New-ScheduledTaskAction `
            -Execute $PythonExe `
            -Argument $ScriptName `
            -WorkingDirectory $WorkingDirectory
        
        # Create settings
        $Settings = New-ScheduledTaskSettingsSet `
            -StartWhenAvailable `
            -RunOnlyIfNetworkAvailable `
            -AllowStartIfOnBatteries `
            -DontStopIfGoingOnBatteries
        
        # Register task
        Register-ScheduledTask `
            -TaskName $TaskName `
            -Trigger $Trigger `
            -Action $Action `
            -Settings $Settings `
            -Description $Description `
            -RunLevel Highest `
            -Force -ErrorAction Stop | Out-Null
        
        Write-Host "  [OK] PC-$PC created for $Date @ $Time" -ForegroundColor Green
        $CreatedCount++
        
    } catch {
        Write-Host "  [ERROR] PC-$PC failed: $($_.Exception.Message)" -ForegroundColor Red
        $FailedCount++
    }
}

Write-Host "`n$('='*80)"
Write-Host "Results:"
Write-Host "  Created: $CreatedCount"
Write-Host "  Skipped: $SkippedCount"
Write-Host "  Failed: $FailedCount"
Write-Host "$('='*80)`n"

# Verify
$AllTasks = Get-ScheduledTask -TaskName "DC-EMAIL-PC-*" -ErrorAction SilentlyContinue
Write-Host "Total tasks in scheduler: $($AllTasks.Count)/26`n"

if ($AllTasks.Count -gt 0) {
    Write-Host "Next PayCycle scheduled:"
    $AllTasks | Where-Object {$_.NextRunTime -gt (Get-Date)} | Sort-Object NextRunTime | Select-Object -First 1 | 
        ForEach-Object { Write-Host "  $($_.TaskName) - $($_.NextRunTime)" -ForegroundColor Cyan }
}

Write-Host "`nSetup complete!`n"
