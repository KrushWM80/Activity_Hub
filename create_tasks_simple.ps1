# DC PayCycle Task Creator - Simple Direct Approach
# Run as admin to create tasks

$BasePath = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails"
$PyExe = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"
$Script = "daily_check_smart.py"

# Create individual tasks
$tasks = @(
    @{pc=5; d="2026-04-03"},
    @{pc=6; d="2026-04-17"},
    @{pc=7; d="2026-05-01"},
    @{pc=8; d="2026-05-15"},
    @{pc=9; d="2026-05-29"},
    @{pc=10; d="2026-06-12"},
    @{pc=11; d="2026-06-26"},
    @{pc=12; d="2026-07-10"},
    @{pc=13; d="2026-07-24"},
    @{pc=14; d="2026-08-07"},
    @{pc=15; d="2026-08-21"},
    @{pc=16; d="2026-09-04"},
    @{pc=17; d="2026-09-18"},
    @{pc=18; d="2026-10-02"},
    @{pc=19; d="2026-10-16"},
    @{pc=20; d="2026-10-30"},
    @{pc=21; d="2026-11-13"},
    @{pc=22; d="2026-11-27"},
    @{pc=23; d="2026-12-11"},
    @{pc=24; d="2026-12-25"},
    @{pc=25; d="2027-01-08"},
    @{pc=26; d="2027-01-22"}
)

Write-Host "Creating 22 PayCycle tasks...`n"

$ok = 0
foreach ($t in $tasks) {
    $tn = "DC-EMAIL-PC-$($t.pc.ToString('00'))"
    $dt = [datetime]"$($t.d) 06:00:00"
    
    try {
        $tr = New-ScheduledTaskTrigger -Once -At $dt
        $ac = New-ScheduledTaskAction -Execute $PyExe -Argument $Script -WorkingDirectory $BasePath
        $se = New-ScheduledTaskSettingsSet -StartWhenAvailable
        $pr = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
        
        Register-ScheduledTask -TaskName $tn -Trigger $tr -Action $ac -Settings $se -Principal $pr -Force | Out-Null
        Write-Host "OK: $tn" -ForegroundColor Green
        $ok++
    } catch {
        Write-Host "ERROR: $tn - $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n=== Created: $ok/22 ===" -ForegroundColor Cyan
$all = (Get-ScheduledTask -TaskName "DC-EMAIL-PC-*" -ErrorAction SilentlyContinue).Count
Write-Host "Total in scheduler: $all/26`n"
