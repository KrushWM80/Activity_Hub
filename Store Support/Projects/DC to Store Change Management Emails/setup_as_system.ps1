# PayCycle Task Setup - Using SYSTEM User
# This should have proper permissions to create tasks

$WorkingDirectory = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails"
$PythonExe = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"
$ScriptName = "daily_check_smart.py"

$FuturePayCycles = @(
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

Write-Host "`nCreating PayCycle tasks (22 future cycles)...`n" -ForegroundColor Cyan

$CreatedCount = 0
$FailedCount = 0

foreach ($Cycle in $FuturePayCycles) {
    $PC = $Cycle.PC.ToString("00")
    $TaskName = "DC-EMAIL-PC-$PC"
    $TriggerDateTime = [DateTime]::Parse("$($Cycle.Date) $($Cycle.Time)")
    
    try {
        # Create PowerShell script that will be executed
        $TaskScript = @"
Set-Location "$WorkingDirectory"
& "$PythonExe" $ScriptName
"@
        
        $PSEncoded = [Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes($TaskScript))
        
        # Create trigger
        $Trigger = New-ScheduledTaskTrigger -Once -At $TriggerDateTime
        
        # Create action using powershell encoded command
        $Action = New-ScheduledTaskAction `
            -Execute "powershell.exe" `
            -Argument "-NoProfile -EncodedCommand $PSEncoded"
        
        # Create settings
        $Settings = New-ScheduledTaskSettingsSet `
            -StartWhenAvailable `
            -RunOnlyIfNetworkAvailable `
            -AllowStartIfOnBatteries
        
        # Create principal that runs as SYSTEM
        $Principal = New-ScheduledTaskPrincipal `
            -UserId "NT AUTHORITY\SYSTEM" `
            -LogonType ServiceAccount `
            -RunLevel Highest
        
        # Register task
        Register-ScheduledTask `
            -TaskName $TaskName `
            -Trigger $Trigger `
            -Action $Action `
            -Settings $Settings `
            -Principal $Principal `
            -Force -ErrorAction Stop | Out-Null
        
        Write-Host "  [OK] PC-$PC @ $($Cycle.Date)" -ForegroundColor Green
        $CreatedCount++
        
    } catch {
        Write-Host "  [ERROR] PC-$PC: $($_.Exception.Message)" -ForegroundColor Red
        $FailedCount++
    }
}

Write-Host "`nResults: Created=$CreatedCount, Failed=$FailedCount`n" -ForegroundColor Yellow

# Verify
$AllTasks = Get-ScheduledTask -TaskName "DC-EMAIL-PC-*" -ErrorAction SilentlyContinue
Write-Host "Total tasks registered: $($AllTasks.Count)/26`n" -ForegroundColor Cyan

if ($AllTasks.Count -gt 0) {
    Write-Host "Next scheduled PayCycle:"
    $AllTasks | Where-Object {$_.NextRunTime -gt (Get-Date)} | Sort-Object NextRunTime | Select-Object -First 1 |
        ForEach-Object { Write-Host "  $($_.TaskName) - $($_.NextRunTime)" -ForegroundColor Green }
}
