#!/usr/bin/env powershell
# Register PayCycle Tasks - Using schtasks.exe
# Run in any PowerShell (no admin needed for creation, only for viewing)

$pythonExe = "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"
$scriptPath = "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails\send_paycycle_production_email_generic.py"

$tasks = @(
    @{PC=7; Date="05/01/2026"; Time="06:00:00"},
    @{PC=8; Date="05/15/2026"; Time="06:00:00"},
    @{PC=9; Date="05/29/2026"; Time="06:00:00"},
    @{PC=10; Date="06/12/2026"; Time="06:00:00"},
    @{PC=11; Date="06/26/2026"; Time="06:00:00"},
    @{PC=12; Date="07/10/2026"; Time="06:00:00"},
    @{PC=13; Date="07/24/2026"; Time="06:00:00"},
    @{PC=14; Date="08/07/2026"; Time="06:00:00"},
    @{PC=15; Date="08/21/2026"; Time="06:00:00"},
    @{PC=16; Date="09/04/2026"; Time="06:00:00"},
    @{PC=17; Date="09/18/2026"; Time="06:00:00"},
    @{PC=18; Date="10/02/2026"; Time="06:00:00"},
    @{PC=19; Date="10/16/2026"; Time="06:00:00"},
    @{PC=20; Date="10/30/2026"; Time="06:00:00"},
    @{PC=21; Date="11/13/2026"; Time="06:00:00"},
    @{PC=22; Date="11/27/2026"; Time="06:00:00"},
    @{PC=23; Date="12/11/2026"; Time="06:00:00"},
    @{PC=24; Date="12/25/2026"; Time="06:00:00"},
    @{PC=25; Date="01/08/2027"; Time="06:00:00"},
    @{PC=26; Date="01/22/2027"; Time="06:00:00"}
)

Write-Host "=========================================="
Write-Host "Registering PayCycle Tasks (PC-07-26)"
Write-Host "=========================================="
Write-Host ""

$successCount = 0
$failureCount = 0

foreach ($task in $tasks) {
    $pcNum = $task.PC
    $taskName = "DC-EMAIL-PC-{0:D2}-FY27" -f $pcNum
    $command = "`"$pythonExe`" `"$scriptPath`" $pcNum"
    
    Write-Host "Creating: PC-$pcNum ... " -NoNewline
    
    $output = & schtasks /create /tn "$taskName" /tr "$command" /sc once /st "$($task.Time)" /sd "$($task.Date)" /f 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "OK" -ForegroundColor Green
        $successCount++
    } else {
        Write-Host "FAIL (exit $LASTEXITCODE)" -ForegroundColor Red
        $failureCount++
    }
}

Write-Host ""
Write-Host "=========================================="
Write-Host "Results:"
Write-Host "  Success: $successCount"
Write-Host "  Failed:  $failureCount"
Write-Host "=========================================="
Write-Host ""

# Verify
Write-Host "Verifying registered tasks..."
Write-Host ""

$count = 0
for ($i = 7; $i -le 26; $i++) {
    $taskName = "DC-EMAIL-PC-{0:D2}-FY27" -f $i
    $check = & schtasks /query /tn "$taskName" /fo list 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "OK - PC-$i" -ForegroundColor Green
        $count++
    }
}

Write-Host ""
Write-Host "Registered: $count / 20 tasks"
Write-Host ""
