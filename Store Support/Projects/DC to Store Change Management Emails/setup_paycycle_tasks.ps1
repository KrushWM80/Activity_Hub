# Windows Task Scheduler - PayCycle Email Send Configuration
# This script creates automated tasks for each Walmart PayCycle in 2026
# Tasks will run the email change detection system on each PayCycle end date

# PayCycles Schedule for 2026 (26 cycles, biweekly, Fridays)
$PayCycles = @(
    @{ PC = 1; Date = "02/06/2026"; Time = "06:00"; Description = "FY27 PC 01" },
    @{ PC = 2; Date = "02/20/2026"; Time = "06:00"; Description = "FY27 PC 02" },
    @{ PC = 3; Date = "03/06/2026"; Time = "06:00"; Description = "FY27 PC 03 - FIRST AUTO SEND" },
    @{ PC = 4; Date = "03/20/2026"; Time = "06:00"; Description = "FY27 PC 04" },
    @{ PC = 5; Date = "04/03/2026"; Time = "06:00"; Description = "FY27 PC 05" },
    @{ PC = 6; Date = "04/17/2026"; Time = "06:00"; Description = "FY27 PC 06" },
    @{ PC = 7; Date = "05/01/2026"; Time = "06:00"; Description = "FY27 PC 07" },
    @{ PC = 8; Date = "05/15/2026"; Time = "06:00"; Description = "FY27 PC 08" },
    @{ PC = 9; Date = "05/29/2026"; Time = "06:00"; Description = "FY27 PC 09" },
    @{ PC = 10; Date = "06/12/2026"; Time = "06:00"; Description = "FY27 PC 10" },
    @{ PC = 11; Date = "06/26/2026"; Time = "06:00"; Description = "FY27 PC 11" },
    @{ PC = 12; Date = "07/10/2026"; Time = "06:00"; Description = "FY27 PC 12" },
    @{ PC = 13; Date = "07/24/2026"; Time = "06:00"; Description = "FY27 PC 13" },
    @{ PC = 14; Date = "08/07/2026"; Time = "06:00"; Description = "FY27 PC 14" },
    @{ PC = 15; Date = "08/21/2026"; Time = "06:00"; Description = "FY27 PC 15" },
    @{ PC = 16; Date = "09/04/2026"; Time = "06:00"; Description = "FY27 PC 16" },
    @{ PC = 17; Date = "09/18/2026"; Time = "06:00"; Description = "FY27 PC 17" },
    @{ PC = 18; Date = "10/02/2026"; Time = "06:00"; Description = "FY27 PC 18" },
    @{ PC = 19; Date = "10/16/2026"; Time = "06:00"; Description = "FY27 PC 19" },
    @{ PC = 20; Date = "10/30/2026"; Time = "06:00"; Description = "FY27 PC 20" },
    @{ PC = 21; Date = "11/13/2026"; Time = "06:00"; Description = "FY27 PC 21" },
    @{ PC = 22; Date = "11/27/2026"; Time = "06:00"; Description = "FY27 PC 22" },
    @{ PC = 23; Date = "12/11/2026"; Time = "06:00"; Description = "FY27 PC 23" },
    @{ PC = 24; Date = "12/25/2026"; Time = "06:00"; Description = "FY27 PC 24" },
    @{ PC = 25; Date = "01/08/2027"; Time = "06:00"; Description = "FY27 PC 25 (2027)" },
    @{ PC = 26; Date = "01/22/2027"; Time = "06:00"; Description = "FY27 PC 26 (2027)" }
)

# Configuration
$WorkingDirectory = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails"
$PythonExe = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"
$ScriptName = "daily_check_smart.py"
$TaskFolderPath = "\DC to Store Change Management Emails\"
$TaskNamePrefix = "DC-EMAIL-PC"

Write-Host "`n"
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "WINDOWS TASK SCHEDULER - PayCycle Configuration" -ForegroundColor Cyan
Write-Host "================================================================`n" -ForegroundColor Cyan

# Function to create a task
function Create-PayCycleTask {
    param(
        [int]$PCNumber,
        [string]$PCDate,
        [string]$PCTime,
        [string]$PCDescription
    )
    
    $TaskName = "$TaskNamePrefix-$($PCNumber.ToString('00'))-$PCDescription"
    $FullTaskPath = "$TaskFolderPath$TaskName"
    
    Write-Host "Creating Task: PC $($PCNumber.ToString('00')) | $PCDate at $PCTime | $PCDescription"
    
    try {
        # Create action
        $Action = New-ScheduledTaskAction `
            -Execute $PythonExe `
            -Argument $ScriptName `
            -WorkingDirectory $WorkingDirectory
        
        # Create trigger (one time at specific date/time)
        $Trigger = New-ScheduledTaskTrigger `
            -Once `
            -At ([datetime]"$PCDate $PCTime")
        
        # Create settings (allow task to run for longer if needed)
        $Settings = New-ScheduledTaskSettingsSet `
            -AllowStartIfOnBatteries `
            -DontStopIfGoingOnBatteries `
            -StartWhenAvailable `
            -RunOnlyIfNetworkAvailable
        
        # Create or update task
        if (Get-ScheduledTask -TaskName $TaskName -TaskPath $TaskFolderPath -ErrorAction SilentlyContinue) {
            $Task = Get-ScheduledTask -TaskName $TaskName -TaskPath $TaskFolderPath
            $Task | Set-ScheduledTask -Action $Action -Trigger $Trigger -Settings $Settings
            Write-Host "  ✓ Updated existing task`n"
        } else {
            Register-ScheduledTask `
                -TaskName $TaskName `
                -TaskPath $TaskFolderPath `
                -Action $Action `
                -Trigger $Trigger `
                -Settings $Settings `
                -RunLevel Highest `
                -Description "DC to Store Manager Change Detection - PayCycle $PCNumber"
            Write-Host "  ✓ Created new task`n"
        }
    }
    catch {
        Write-Host "  ✗ Error: $_`n" -ForegroundColor Red
    }
}

# Main Process
Write-Host "Status: Creating/Updating PayCycle Tasks for 2026`n"
Write-Host "Total Tasks: $($PayCycles.Count)`n"
Write-Host "Working Directory: $WorkingDirectory"
Write-Host "Python Executable: $PythonExe"
Write-Host "Script: $ScriptName`n"
Write-Host "================================================================`n"

$CreatedCount = 0
$UpdatedCount = 0

foreach ($Cycle in $PayCycles) {
    Create-PayCycleTask -PCNumber $Cycle.PC -PCDate $Cycle.Date -PCTime $Cycle.Time -PCDescription $Cycle.Description
    $CreatedCount++
}

Write-Host "================================================================"
Write-Host "TASK CREATION COMPLETE" -ForegroundColor Green
Write-Host "================================================================`n"

# Verify tasks
Write-Host "Verifying Created Tasks:`n"
$Tasks = Get-ScheduledTask -TaskPath $TaskFolderPath -ErrorAction SilentlyContinue
if ($Tasks) {
    Write-Host "Found $($Tasks.Count) PayCycle tasks in Task Scheduler`n"
    Write-Host "First 5 Tasks:"
    $Tasks | Select-Object -First 5 | ForEach-Object {
        Write-Host "  • $($_.TaskName)"
    }
    if ($Tasks.Count -gt 5) {
        Write-Host "  ... and $($Tasks.Count - 5) more"
    }
    Write-Host ""
}

Write-Host "Next Steps:"
Write-Host "  1. Verify tasks in Task Scheduler GUI"
Write-Host "  2. Test with: PC 03 on 03/06/2026 (9 days away)"
Write-Host "  3. Monitor execution logs for email sends"
Write-Host "  4. After 2-3 cycles, move to production"
Write-Host ""

Write-Host "To View Tasks:"
Write-Host "  1. Open Task Scheduler"
Write-Host "  2. Navigate to: Task Scheduler Library > DC to Store Change Management Emails"
Write-Host "  3. Review all 26 PayCycle tasks"
Write-Host ""

Write-Host "To Run Task Manually:"
Write-Host "  Start-ScheduledTask -TaskPath '\DC to Store Change Management Emails\' -TaskName 'DC-EMAIL-PC-03-FY27 PC 03 - FIRST AUTO SEND'"
Write-Host ""
