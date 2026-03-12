# DC Manager PayCycle Task Creator
# Creates all 26 biweekly PayCycle automation tasks
# Run in Administrator PowerShell

$DCPath = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Platform"
$PythonExe = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount

# PayCycle dates (2026-2027) - every 2 weeks starting March 6
$PayCycleDates = @(
    @{Name="PC-03"; Date="03/06/2026"; Time="06:00:00"},
    @{Name="PC-04"; Date="03/20/2026"; Time="06:00:00"},
    @{Name="PC-05"; Date="04/03/2026"; Time="06:00:00"},
    @{Name="PC-06"; Date="04/17/2026"; Time="06:00:00"},
    @{Name="PC-07"; Date="05/01/2026"; Time="06:00:00"},
    @{Name="PC-08"; Date="05/15/2026"; Time="06:00:00"},
    @{Name="PC-09"; Date="05/29/2026"; Time="06:00:00"},
    @{Name="PC-10"; Date="06/12/2026"; Time="06:00:00"},
    @{Name="PC-11"; Date="06/26/2026"; Time="06:00:00"},
    @{Name="PC-12"; Date="07/10/2026"; Time="06:00:00"},
    @{Name="PC-13"; Date="07/24/2026"; Time="06:00:00"},
    @{Name="PC-14"; Date="08/07/2026"; Time="06:00:00"},
    @{Name="PC-15"; Date="08/21/2026"; Time="06:00:00"},
    @{Name="PC-16"; Date="09/04/2026"; Time="06:00:00"},
    @{Name="PC-17"; Date="09/18/2026"; Time="06:00:00"},
    @{Name="PC-18"; Date="10/02/2026"; Time="06:00:00"},
    @{Name="PC-19"; Date="10/16/2026"; Time="06:00:00"},
    @{Name="PC-20"; Date="10/30/2026"; Time="06:00:00"},
    @{Name="PC-21"; Date="11/13/2026"; Time="06:00:00"},
    @{Name="PC-22"; Date="11/27/2026"; Time="06:00:00"},
    @{Name="PC-23"; Date="12/11/2026"; Time="06:00:00"},
    @{Name="PC-24"; Date="12/25/2026"; Time="06:00:00"},
    @{Name="PC-25"; Date="01/08/2027"; Time="06:00:00"},
    @{Name="PC-26"; Date="01/22/2027"; Time="06:00:00"}
)

Write-Host "Creating 26 DC Manager PayCycle Tasks..." -ForegroundColor Yellow
Write-Host ""

$successCount = 0
$failCount = 0

foreach ($pc in $PayCycleDates) {
    try {
        $taskName = "DC-EMAIL-$($pc.Name)"
        $dateTime = [DateTime]"$($pc.Date) $($pc.Time)"
        
        $action = New-ScheduledTaskAction -Execute $PythonExe -Argument "daily_check_smart.py" -WorkingDirectory $DCPath
        $trigger = New-ScheduledTaskTrigger -Once -At $dateTime
        
        Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Force | Out-Null
        
        Write-Host "[OK] $taskName - $($pc.Date) at $($pc.Time)"
        $successCount++
    } catch {
        Write-Host "[FAIL] $($pc.Name): $_" -ForegroundColor Red
        $failCount++
    }
}

Write-Host ""
Write-Host "Results: Created: $successCount, Failed: $failCount" -ForegroundColor Green
