$base = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation"

$tasks = @(
    @{ Name = "Activity_Hub_JobCodes_AutoStart";           Bat = "start_jobcodes_server_24_7.bat" },
    @{ Name = "Activity_Hub_ProjectsInStores_AutoStart";   Bat = "start_projects_in_stores_24_7.bat" },
    @{ Name = "Activity_Hub_TDA_AutoStart";                Bat = "start_tda_insights_24_7.bat" },
    @{ Name = "Activity_Hub_Store_Dashboard_AutoStart";    Bat = "start_store_dashboard_24_7.bat" },
    @{ Name = "Activity_Hub_StoreMeetingPlanner_AutoStart"; Bat = "start_meeting_planner_24_7.bat" },
    @{ Name = "Activity_Hub_VETDashboard_AutoStart";       Bat = "start_vet_dashboard_24_7.bat" },
    @{ Name = "Activity_Hub_Zorro_AutoStart";              Bat = "start_zorro_24_7.bat" }
)

foreach ($t in $tasks) {
    $action  = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$base\$($t.Bat)`""
    $trigger = New-ScheduledTaskTrigger -AtLogOn -User "HOMEOFFICE\krush"
    $settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 0)
    $principal = New-ScheduledTaskPrincipal -UserId "krush" -LogonType Interactive -RunLevel Limited

    Register-ScheduledTask -TaskName $t.Name -Action $action -Trigger $trigger `
        -Settings $settings -Principal $principal -Force | Out-Null

    if ($?) { Write-Host "  Created: $($t.Name)" -ForegroundColor Green }
    else     { Write-Host "  FAILED:  $($t.Name)" -ForegroundColor Red }
}

# Daily Health Check at 6 AM
$ps1 = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\MONITOR_AND_REPORT.ps1"
$action  = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$ps1`""
$trigger = New-ScheduledTaskTrigger -Daily -At "06:00"
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -WakeToRun
$principal = New-ScheduledTaskPrincipal -UserId "krush" -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName "Activity_Hub_Daily_HealthCheck" -Action $action -Trigger $trigger `
    -Settings $settings -Principal $principal -Force | Out-Null

if ($?) { Write-Host "  Created: Activity_Hub_Daily_HealthCheck" -ForegroundColor Green }
else     { Write-Host "  FAILED:  Activity_Hub_Daily_HealthCheck" -ForegroundColor Red }

Write-Host "`nDone. Verifying..." -ForegroundColor Cyan
schtasks /query /fo TABLE 2>&1 | Select-String "Activity_Hub"
