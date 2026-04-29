# Create All PayCycle Tasks: PC-07 through PC-26
# Uses schtasks.exe (bypasses CIM/WMI — works even when Get-ScheduledTask fails)
# Run this in ADMIN PowerShell

$pythonExe = 'c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe'
$scriptPath = 'c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails\send_paycycle_production_email_generic.py'

$tasks = @(
    @{PC=7;  Date="05/01/2026"; Time="06:00"},
    @{PC=8;  Date="05/15/2026"; Time="06:00"},
    @{PC=9;  Date="05/29/2026"; Time="06:00"},
    @{PC=10; Date="06/12/2026"; Time="06:00"},
    @{PC=11; Date="06/26/2026"; Time="06:00"},
    @{PC=12; Date="07/10/2026"; Time="06:00"},
    @{PC=13; Date="07/24/2026"; Time="06:00"},
    @{PC=14; Date="08/07/2026"; Time="06:00"},
    @{PC=15; Date="08/21/2026"; Time="06:00"},
    @{PC=16; Date="09/04/2026"; Time="06:00"},
    @{PC=17; Date="09/18/2026"; Time="06:00"},
    @{PC=18; Date="10/02/2026"; Time="06:00"},
    @{PC=19; Date="10/16/2026"; Time="06:00"},
    @{PC=20; Date="10/30/2026"; Time="06:00"},
    @{PC=21; Date="11/13/2026"; Time="06:00"},
    @{PC=22; Date="11/27/2026"; Time="06:00"},
    @{PC=23; Date="12/11/2026"; Time="06:00"},
    @{PC=24; Date="12/25/2026"; Time="06:00"},
    @{PC=25; Date="01/08/2027"; Time="06:00"},
    @{PC=26; Date="01/22/2027"; Time="06:00"}
)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Creating PayCycle Tasks: PC-07 through PC-26" -ForegroundColor Cyan
Write-Host "Using: schtasks.exe (CIM-free)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

$successCount = 0
$failureCount = 0

foreach ($task in $tasks) {
    $pcNum    = $task.PC
    $pcDate   = $task.Date
    $pcTime   = $task.Time
    $taskName = "DC-EMAIL-PC-{0:D2}-FY27" -f $pcNum
    $args     = "`"$scriptPath`" $pcNum"

    # schtasks /create — no CIM required
    $result = schtasks /create `
        /tn $taskName `
        /tr "`"$pythonExe`" $args" `
        /sc ONCE `
        /sd $pcDate `
        /st $pcTime `
        /rl HIGHEST `
        /f 2>&1

    if ($LASTEXITCODE -eq 0) {
        Write-Host ("[OK] PC-{0:D2}: {1} @ {2} {3}" -f $pcNum, $taskName, $pcDate, $pcTime) -ForegroundColor Green
        $successCount++
    } else {
        Write-Host ("[FAIL] PC-{0:D2}: {1}" -f $pcNum, $taskName) -ForegroundColor Red
        Write-Host "    $result" -ForegroundColor Red
        $failureCount++
    }
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "  Created: $successCount tasks" -ForegroundColor Green
if ($failureCount -gt 0) {
    Write-Host "  Failed:  $failureCount tasks" -ForegroundColor Red
}
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Verify using schtasks /query (also CIM-free)
Write-Host "Verifying registered tasks..." -ForegroundColor Cyan
schtasks /query /fo TABLE /nh | findstr "DC-EMAIL-PC"
