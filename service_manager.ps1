# Activity Hub Service PID Manager
# Unified script to safely start/stop all services with PID tracking
# Usage: 
#   .\service_manager.ps1 -Action start -Service activity_hub
#   .\service_manager.ps1 -Action stop -Service all
#   .\service_manager.ps1 -Action status

param(
    [ValidateSet('start', 'stop', 'status', 'restart')]
    [string]$Action = 'status',
    
    [ValidateSet('activity_hub', 'projects_in_stores', 'job_codes', 'amp_dashboard', 'meeting_planner', 'vet_dashboard', 'tda_insights', 'zorro', 'scheduler_logic', 'all')]
    [string]$Service = 'all'
)

$RootDir = $PSScriptRoot

# Service definitions — matches register_tasks_cmd.bat and continuous_monitor.ps1
$Services = @{
    'activity_hub' = @{
        Name = 'Activity Hub'
        Port = 8088
        Script = 'Interface\activity_hub_server.py'
        WorkDir = $RootDir
        Bat    = 'Automation\start_activity_hub_24_7.bat'
    }
    'projects_in_stores' = @{
        Name = 'Projects in Stores'
        Port = 8001
        Script = 'Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend\main.py'
        WorkDir = $RootDir
        Bat    = 'Automation\start_projects_in_stores_24_7.bat'
    }
    'job_codes' = @{
        Name = 'Job Codes Dashboard'
        Port = 8080
        Script = 'Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend\main.py'
        WorkDir = $RootDir
        Bat    = 'Automation\start_jobcodes_server_24_7.bat'
    }
    'amp_dashboard' = @{
        Name = 'AMP Store Dashboard'
        Port = 8081
        Script = 'Store Support\Projects\AMP\Store Updates Dashboard\amp_backend_server.py'
        WorkDir = $RootDir
        Bat    = 'Automation\start_store_dashboard_24_7.bat'
    }
    'meeting_planner' = @{
        Name = 'Store Meeting Planner'
        Port = 8090
        Script = 'Store Support\Projects\AMP\Store Meeting Planners\backend\main.py'
        WorkDir = $RootDir
        Bat    = 'Automation\start_meeting_planner_24_7.bat'
    }
    'vet_dashboard' = @{
        Name = 'V.E.T. Dashboard'
        Port = 5001
        Script = 'Store Support\Projects\VET_Dashboard\backend.py'
        WorkDir = $RootDir
        Bat    = 'Automation\start_vet_dashboard_24_7.bat'
    }
    'tda_insights' = @{
        Name = 'TDA Insights'
        Port = 5000
        Script = 'Store Support\Projects\TDA Insights\backend_simple.py'
        WorkDir = 'Store Support\Projects\TDA Insights'
        Bat    = 'Automation\start_tda_insights_24_7.bat'
    }
    'zorro' = @{
        Name = 'Audio Message Hub (Zorro)'
        Port = 8888
        Script = 'Store Support\Projects\AMP\Zorro\audio_server.py'
        WorkDir = 'Store Support\Projects\AMP\Zorro'
        Bat    = 'Automation\start_zorro_24_7.bat'
    }
    'scheduler_logic' = @{
        Name = 'Logic Scheduler Service'
        Port = 5011
        Script = 'Interface\Admin\Logic\Scheduler\main.py'
        WorkDir = $RootDir
        Bat    = 'Automation\start_logic_scheduler_24_7.bat'
    }
}

# Helper: get the PID currently listening on a port via netstat
function Get-PortPid {
    param([int]$Port)
    $match = netstat -ano 2>$null | Select-String ":$Port\s.*LISTENING"
    if ($match) {
        return ($match.Line -split '\s+')[-1].Trim()
    }
    return $null
}

function Get-ServiceStatus {
    param([string]$ServiceKey)

    $svc = $Services[$ServiceKey]
    $livePid = Get-PortPid -Port $svc.Port

    if ($livePid) {
        $proc = Get-Process -Id $livePid -ErrorAction SilentlyContinue
        $mem  = if ($proc) { "$([math]::Round($proc.WorkingSet/1MB, 1)) MB" } else { '-' }
        $uptime = if ($proc -and $proc.StartTime) {
            $span = (Get-Date) - $proc.StartTime
            if ($span.TotalHours -ge 1) { "$([math]::Floor($span.TotalHours))h $($span.Minutes)m" }
            else { "$($span.Minutes)m $($span.Seconds)s" }
        } else { '-' }
        return [PSCustomObject]@{
            Service = $svc.Name
            Port    = $svc.Port
            Status  = 'Running'
            PID     = $livePid
            Memory  = $mem
            Uptime  = $uptime
        }
    } else {
        return [PSCustomObject]@{
            Service = $svc.Name
            Port    = $svc.Port
            Status  = 'DOWN'
            PID     = '-'
            Memory  = '-'
            Uptime  = '-'
        }
    }
}

function Start-Service-Safe {
    param([string]$ServiceKey)

    if (-not $Services.ContainsKey($ServiceKey)) {
        Write-Host "x Unknown service: $ServiceKey" -ForegroundColor Red
        return $false
    }

    $svc = $Services[$ServiceKey]

    # Check if already running
    $livePid = Get-PortPid -Port $svc.Port
    if ($livePid) {
        Write-Host "! $($svc.Name) already running (PID $livePid, Port $($svc.Port))" -ForegroundColor Yellow
        return $true
    }

    # Start via bat loop (consistent with AutoStart / continuous_monitor pattern)
    $batPath = Join-Path $RootDir $svc.Bat
    if (-not (Test-Path $batPath)) {
        Write-Host "x Bat not found: $batPath" -ForegroundColor Red
        return $false
    }

    Write-Host "Starting $($svc.Name) via bat loop..." -ForegroundColor Cyan
    Start-Process -FilePath 'cmd.exe' -ArgumentList "/c `"$batPath`"" -WindowStyle Hidden
    Start-Sleep -Seconds 8

    $newPid = Get-PortPid -Port $svc.Port
    if ($newPid) {
        Write-Host "OK Started (PID $newPid, Port $($svc.Port))" -ForegroundColor Green
        return $true
    } else {
        Write-Host "FAIL $($svc.Name) did not bind to port $($svc.Port) within 8 seconds" -ForegroundColor Red
        return $false
    }
}

function Stop-Service-Safe {
    param([string]$ServiceKey)
    
    if (-not $Services.ContainsKey($ServiceKey)) {
        Write-Host "✗ Unknown service: $ServiceKey" -ForegroundColor Red
        return $true
    }
    
    $svc = $Services[$ServiceKey]

    # Use netstat to find live PID — no .pid files needed
    $livePid = Get-PortPid -Port $svc.Port

    if (-not $livePid) {
        Write-Host "$($svc.Name) not running" -ForegroundColor Gray
        return $true
    }

    Write-Host "Stopping $($svc.Name) (PID $livePid, Port $($svc.Port))..." -ForegroundColor Cyan

    try {
        # taskkill with /T kills the bat loop parent and its Python child together
        $result = taskkill /F /PID $livePid /T 2>&1
        Start-Sleep -Milliseconds 800
        Write-Host "Stopped" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "Failed to stop: $_" -ForegroundColor Red
        return $false
    }
}

# Main logic
Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host "  Activity Hub Service Manager (PID Tracking)" -ForegroundColor Cyan
Write-Host "===========================================================" -ForegroundColor Cyan

$servicesToProcess = if ($Service -eq 'all') { $Services.Keys } else { @($Service) }

switch ($Action) {
    "status" {
        Write-Host "`n[SERVICE STATUS]`n" -ForegroundColor Cyan
        $servicesToProcess | ForEach-Object { Get-ServiceStatus $_ } | Format-Table -AutoSize
        Write-Host ""

        # --- Scheduled Task Verification ---
        Write-Host "[SCHEDULED TASKS]`n" -ForegroundColor Cyan

        # AutoStart + infrastructure tasks (registered with admin — query all tasks)
        $expectedTasks = @(
            "Activity_Hub_JobCodes_AutoStart",
            "Activity_Hub_ProjectsInStores_AutoStart",
            "Activity_Hub_TDA_AutoStart",
            "Activity_Hub_Store_Dashboard_AutoStart",
            "Activity_Hub_StoreMeetingPlanner_AutoStart",
            "Activity_Hub_VETDashboard_AutoStart",
            "Activity_Hub_Zorro_AutoStart",
            "Activity_Hub_ActivityHub_AutoStart",
            "Activity_Hub_Daily_HealthCheck",
            "Activity_Hub_ContinuousMonitor"
        )

        $allTasks = schtasks /query /fo CSV /v 2>$null | ConvertFrom-Csv
        $taskResults = foreach ($name in $expectedTasks) {
            $t = $allTasks | Where-Object { $_.TaskName -like "*$name*" } | Select-Object -First 1
            [PSCustomObject]@{
                Task   = $name -replace "Activity_Hub_", ""
                Status = if ($t) { $t.Status } else { "MISSING" }
                Color  = if ($t -and $t.Status -ne "Disabled") { "Green" } else { "Red" }
            }
        }
        foreach ($r in $taskResults) {
            $color = if ($r.Status -eq "MISSING") { "Red" } elseif ($r.Status -eq "Disabled") { "Yellow" } else { "Green" }
            Write-Host ("  {0,-45} {1}" -f $r.Task, $r.Status) -ForegroundColor $color
        }

        # DC PayCycle tasks (registered as SYSTEM — only visible from admin context)
        $dcTasks = $allTasks | Where-Object { $_.TaskName -like "*DC-EMAIL-PC*" }
        $dcCount = if ($dcTasks) { @($dcTasks).Count } else { 0 }
        if ($dcCount -gt 0) {
            $dcColor = if ($dcCount -ge 20) { "Green" } else { "Yellow" }
            Write-Host ("  {0,-45} {1}" -f "DC-EMAIL PayCycle Tasks", "$dcCount registered") -ForegroundColor $dcColor
        } else {
            Write-Host ("  {0,-45} {1}" -f "DC-EMAIL PayCycle Tasks", "Not visible (requires admin) or MISSING") -ForegroundColor Yellow
            Write-Host "    To verify: run this script from an admin terminal" -ForegroundColor Gray
            Write-Host "    To recreate: run CREATE_ALL_PAYCYCLE_TASKS.ps1 as admin" -ForegroundColor Gray
        }
        Write-Host ""
    }
    
    "start" {
        Write-Host ""
        $servicesToProcess | ForEach-Object { 
            Start-Service-Safe $_
            Start-Sleep -Milliseconds 300
        }
        Write-Host ""
    }
    
    "stop" {
        Write-Host ""
        $servicesToProcess | ForEach-Object { 
            Stop-Service-Safe $_
            Start-Sleep -Milliseconds 300
        }
        Write-Host ""
    }
    
    "restart" {
        Write-Host ""
        $servicesToProcess | ForEach-Object { 
            Stop-Service-Safe $_
            Start-Sleep -Seconds 1
            Start-Service-Safe $_
            Start-Sleep -Milliseconds 300
        }
        Write-Host ""
    }
}

Write-Host "-----------------------------------------------------------" -ForegroundColor Cyan
