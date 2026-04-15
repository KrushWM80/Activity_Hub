# Create All PayCycle Tasks: PC-07 through PC-26
# Run this in ADMIN PowerShell
# This will register all remaining email tasks through January 22, 2027

$pythonExe = "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"
$scriptPath = "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails\send_pc06_production_email.py"

# Define all PayCycle tasks
$tasks = @(
    @{PC=7; Date="2026-05-01 06:00:00"},
    @{PC=8; Date="2026-05-15 06:00:00"},
    @{PC=9; Date="2026-05-29 06:00:00"},
    @{PC=10; Date="2026-06-12 06:00:00"},
    @{PC=11; Date="2026-06-26 06:00:00"},
    @{PC=12; Date="2026-07-10 06:00:00"},
    @{PC=13; Date="2026-07-24 06:00:00"},
    @{PC=14; Date="2026-08-07 06:00:00"},
    @{PC=15; Date="2026-08-21 06:00:00"},
    @{PC=16; Date="2026-09-04 06:00:00"},
    @{PC=17; Date="2026-09-18 06:00:00"},
    @{PC=18; Date="2026-10-02 06:00:00"},
    @{PC=19; Date="2026-10-16 06:00:00"},
    @{PC=20; Date="2026-10-30 06:00:00"},
    @{PC=21; Date="2026-11-13 06:00:00"},
    @{PC=22; Date="2026-11-27 06:00:00"},
    @{PC=23; Date="2026-12-11 06:00:00"},
    @{PC=24; Date="2026-12-25 06:00:00"},
    @{PC=25; Date="2027-01-08 06:00:00"},
    @{PC=26; Date="2027-01-22 06:00:00"}
)

Write-Host "=========================================="
Write-Host "Creating PayCycle Tasks: PC-07 through PC-26"
Write-Host "=========================================="
Write-Host ""

$successCount = 0
$failureCount = 0

foreach ($task in $tasks) {
    $pcNum = $task.PC
    $pcDate = $task.Date
    $taskName = "DC-EMAIL-PC-{0:D2}-FY27 PC {0:D2}" -f $pcNum
    
    try {
        $trigger = New-ScheduledTaskTrigger -At $pcDate -Once
        $action = New-ScheduledTaskAction -Execute $pythonExe -Argument "`"$scriptPath`""
        $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
        Register-ScheduledTask -TaskName $taskName -Trigger $trigger -Action $action -Settings $settings -RunLevel Highest -User SYSTEM -Force | Out-Null
        
        Write-Host "[OK] PC-$($pcNum): $taskName" -ForegroundColor Green
        Write-Host "    Scheduled: $pcDate" -ForegroundColor Green
        $successCount++
    }
    catch {
        Write-Host "[FAIL] PC-$($pcNum): Task creation failed" -ForegroundColor Red
        Write-Host "    Error: $_" -ForegroundColor Red
        $failureCount++
    }
}

Write-Host ""
Write-Host "=========================================="
Write-Host "Summary:"
Write-Host "=========================================="
Write-Host "Successfully Created: $successCount tasks" -ForegroundColor Green
if ($failureCount -gt 0) {
    Write-Host "Failed: $failureCount tasks" -ForegroundColor Red
}
Write-Host ""
Write-Host "All PayCycle emails scheduled through January 22, 2027"
Write-Host ""

# Verify all tasks were created
Write-Host "Verifying task creation..."
Write-Host ""
Get-ScheduledTask -TaskName "DC-EMAIL-PC-*" | Select-Object TaskName, State | Sort-Object TaskName | Format-Table -AutoSize
