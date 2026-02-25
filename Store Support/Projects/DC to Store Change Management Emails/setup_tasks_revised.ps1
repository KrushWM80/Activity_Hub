# PayCycle Task Scheduler Setup - Revised Version
# This creates 26 individual tasks for each PayCycle in 2026-2027

$WorkingDirectory = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails"
$PythonExe = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"
$ScriptName = "daily_check_smart.py"

# PayCycles with dates and times
$PayCycles = @(
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

Write-Host "`n$('='*80)"
Write-Host "PayCycle Task Scheduler Setup - Creating 26 Automated Tasks"
Write-Host "$('='*80)`n"

Write-Host "Configuration:`n"
Write-Host "  Working Directory: $WorkingDirectory"
Write-Host "  Python Executable: $PythonExe"
Write-Host "  Script: $ScriptName"
Write-Host "  Total Tasks: $($PayCycles.Count)`n"

# Create folder if needed
if (-not (Test-Path $WorkingDirectory)) {
    Write-Host "ERROR: Working directory not found: $WorkingDirectory`n"
    exit 1
}

# Test Python is accessible
if (-not (Test-Path $PythonExe)) {
    Write-Host "ERROR: Python executable not found: $PythonExe`n"
    exit 1
}

Write-Host "Creating tasks...`n"

$CreatedCount = 0
$FailedCount = 0

foreach ($Cycle in $PayCycles) {
    $PC = $Cycle.PC.ToString("00")
    $Date = $Cycle.Date
    $Time = $Cycle.Time
    $TaskName = "DC-EMAIL-PC-$PC"
    $Description = "DC Manager Change Detection - PayCycle $PC ($Date)"
    
    try {
        # Create trigger for specific date/time
        $TriggerTime = [DateTime]::Parse("$Date $Time")
        
        # Verify date is in future or can be scheduled
        $Trigger = New-ScheduledTaskTrigger -Once -At $TriggerTime
        
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
        
        Write-Host "[OK] PC $PC ($Date at $Time)"
        $CreatedCount++
    }
    catch {
        Write-Host "[FAILED] PC $PC - Error: $($_.Exception.Message)" -ForegroundColor Red
        $FailedCount++
    }
}

Write-Host "`n$('='*80)"
Write-Host "TASK CREATION COMPLETE"
Write-Host "$('='*80)"
Write-Host "`nResults:`n"
Write-Host "  Created: $CreatedCount tasks"
Write-Host "  Failed: $FailedCount tasks"
Write-Host "  Total: $($CreatedCount + $FailedCount) tasks`n"

# Verify creation
$Tasks = Get-ScheduledTask | Where-Object {$_.TaskName -like "DC-EMAIL-PC-*"}
Write-Host "Verification: Found $($Tasks.Count) DC-EMAIL tasks in Task Scheduler`n"

if ($Tasks.Count -gt 0) {
    Write-Host "Sample tasks created:`n"
    $Tasks | Select-Object -First 5 | ForEach-Object {
        Write-Host "  • $($_.TaskName)"
    }
    if ($Tasks.Count -gt 5) {
        Write-Host "  ... and $($Tasks.Count - 5) more`n"
    }
}

Write-Host "Next Steps:"
Write-Host "  1. Open Task Scheduler to view all tasks"
Write-Host "  2. Monitor execution before first send (3/6/2026)"
Write-Host "  3. Check emails_sent folder for generated emails"
