# MANUAL: Copy and paste THIS ENTIRE BLOCK into an ADMINISTRATOR PowerShell window

# Run these lines one by one in Administrator PowerShell:

$BasePath = "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails"
$PyExe = "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"

# PC-05 through PC-26 (22 tasks for future PayCycles)
$TaskDates = @{
    "05" = "2026-04-03"
    "06" = "2026-04-17"
    "07" = "2026-05-01"
    "08" = "2026-05-15"
    "09" = "2026-05-29"
    "10" = "2026-06-12"
    "11" = "2026-06-26"
    "12" = "2026-07-10"
    "13" = "2026-07-24"
    "14" = "2026-08-07"
    "15" = "2026-08-21"
    "16" = "2026-09-04"
    "17" = "2026-09-18"
    "18" = "2026-10-02"
    "19" = "2026-10-16"
    "20" = "2026-10-30"
    "21" = "2026-11-13"
    "22" = "2026-11-27"
    "23" = "2026-12-11"
    "24" = "2026-12-25"
    "25" = "2027-01-08"
    "26" = "2027-01-22"
}

foreach ($pc in $TaskDates.Keys) {
    $tn = "DC-EMAIL-PC-$pc"
    $dt = [datetime]::Parse("$($TaskDates[$pc]) 06:00:00")
    $tr = New-ScheduledTaskTrigger -Once -At $dt
    $ac = New-ScheduledTaskAction -Execute $PyExe -Argument "daily_check_smart.py" -WorkingDirectory $BasePath
    $st = New-ScheduledTaskSettingsSet -StartWhenAvailable
    Register-ScheduledTask -TaskName $tn -Trigger $tr -Action $ac -Settings $st -RunLevel Highest -Force | Out-Null
    Write-Host "Created: $tn" -ForegroundColor Green
}

# Verify
Write-Host "`nVerifying..." -ForegroundColor Cyan
$all = Get-ScheduledTask -TaskName "DC-EMAIL-PC-*"
Write-Host "Total tasks: $($all.Count)/26`n"

if ($all.Count -gt 0) {
    Write-Host "Next PayCycle:" -ForegroundColor Yellow
    $all | Where-Object {$_.NextRunTime -gt (Get-Date)} | Sort-Object NextRunTime | Select-Object -First 1 | 
        ForEach-Object { Write-Host "  $($_.TaskName) - $($_.NextRunTime)" -ForegroundColor Green }
}
