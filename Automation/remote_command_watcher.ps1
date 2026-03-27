# Activity Hub Remote Command Watcher
# Runs on the DESKTOP (WEUS42608431466) continuously
# Polls the remote_commands/ folder for .cmd.json files
# Executes predefined commands and writes .result.json responses
# OneDrive syncs results back to laptop (LEUS62315243171)
#
# Start via: start_remote_watcher_24_7.bat
# Or schedule: SCHTASKS /CREATE /TN "Activity_Hub_Remote_Watcher" /TR "powershell -ExecutionPolicy Bypass -File remote_command_watcher.ps1" /SC ONSTART

$ProjectRoot = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"
$CommandsDir = "$ProjectRoot\Automation\remote_commands"
$LogFile     = "$ProjectRoot\Automation\remote_watcher.log"
$PollSeconds = 30

# Service definitions — matches continuous_monitor.ps1
$Services = @{
    "jobcodes"       = @{ Port = 8080; Bat = "$ProjectRoot\Automation\start_jobcodes_server_24_7.bat" }
    "projects"       = @{ Port = 8001; Bat = "$ProjectRoot\Automation\start_projects_in_stores_24_7.bat" }
    "tda"            = @{ Port = 5000; Bat = "$ProjectRoot\Automation\start_tda_insights_24_7.bat" }
    "storedashboard" = @{ Port = 8081; Bat = "$ProjectRoot\Automation\start_store_dashboard_24_7.bat" }
    "meetingplanner" = @{ Port = 8090; Bat = "$ProjectRoot\Automation\start_meeting_planner_24_7.bat" }
    "vet"            = @{ Port = 5001; Bat = "$ProjectRoot\Automation\start_vet_dashboard_24_7.bat" }
    "zorro"          = @{ Port = 8888; Bat = "$ProjectRoot\Automation\start_zorro_24_7.bat" }
}

# Ensure directories exist
if (-not (Test-Path $CommandsDir)) { New-Item -Path $CommandsDir -ItemType Directory -Force | Out-Null }

function Log {
    param([string]$Message, [string]$Level = "INFO")
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $entry = "[$ts] [$Level] $Message"
    Add-Content -Path $LogFile -Value $entry
    Write-Host $entry -ForegroundColor $(switch($Level) { "ERROR" {"Red"} "WARN" {"Yellow"} "OK" {"Green"} default {"Cyan"} })
}

function Get-AllServiceStatus {
    $results = @{}
    foreach ($name in $Services.Keys) {
        $port = $Services[$name].Port
        $listening = (netstat -ano 2>$null | Select-String ":$port\s+.*LISTENING") -ne $null
        $results[$name] = @{
            Port      = $port
            Running   = $listening
            Status    = if ($listening) { "RUNNING" } else { "OFFLINE" }
        }
    }

    # Process count
    $pythonProcs = @(Get-Process -Name "python*" -ErrorAction SilentlyContinue)

    # DC Paycycle tasks
    $dcTasks = @(Get-ScheduledTask -TaskPath "\Activity_Hub*" -ErrorAction SilentlyContinue |
                 Where-Object { $_.TaskName -like "*PayCycle*" -or $_.TaskName -like "*Paycycle*" })

    return @{
        Services     = $results
        PythonCount  = $pythonProcs.Count
        DCTasksCount = $dcTasks.Count
        Hostname     = $env:COMPUTERNAME
        Timestamp    = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    }
}

function Stop-ServiceByName {
    param([string]$ServiceName)
    if (-not $Services.ContainsKey($ServiceName)) { return "Unknown service: $ServiceName" }
    $port = $Services[$ServiceName].Port

    $pids = netstat -ano 2>$null | Select-String ":$port\s+.*LISTENING" |
            ForEach-Object { ($_ -split '\s+')[-1] } | Sort-Object -Unique

    if ($pids) {
        foreach ($p in $pids) {
            try {
                Stop-Process -Id ([int]$p) -Force -ErrorAction Stop
                Log "Stopped PID $p for $ServiceName (port $port)" "OK"
            } catch {
                Log "Failed to stop PID $p : $_" "ERROR"
            }
        }
        return "Stopped $ServiceName (port $port)"
    }
    return "$ServiceName was not running"
}

function Start-ServiceByName {
    param([string]$ServiceName)
    if (-not $Services.ContainsKey($ServiceName)) { return "Unknown service: $ServiceName" }
    $bat = $Services[$ServiceName].Bat
    $port = $Services[$ServiceName].Port

    # Check if already running
    $already = netstat -ano 2>$null | Select-String ":$port\s+.*LISTENING"
    if ($already) { return "$ServiceName already running on port $port" }

    if (-not (Test-Path $bat)) { return "Batch file not found: $bat" }

    Start-Process -FilePath "cmd.exe" -ArgumentList "/c `"$bat`"" -WindowStyle Hidden
    Start-Sleep -Seconds 5

    $check = netstat -ano 2>$null | Select-String ":$port\s+.*LISTENING"
    if ($check) {
        return "Started $ServiceName on port $port"
    }
    return "Start command sent for $ServiceName - may need more time to initialize"
}

function Restart-ServiceByName {
    param([string]$ServiceName)
    $stopResult  = Stop-ServiceByName -ServiceName $ServiceName
    Start-Sleep -Seconds 3
    $startResult = Start-ServiceByName -ServiceName $ServiceName
    return "$stopResult`n$startResult"
}

function Get-ProcessList {
    $procs = Get-Process -Name "python*" -ErrorAction SilentlyContinue |
             Select-Object Id, ProcessName, StartTime,
                 @{N='CPU_Sec';E={[math]::Round($_.CPU,1)}},
                 @{N='Mem_MB';E={[math]::Round($_.WorkingSet64/1MB,1)}} |
             Sort-Object Id
    return ($procs | Format-Table -AutoSize | Out-String)
}

# ============================================================
#  ALLOWED COMMANDS — only these are accepted (security)
# ============================================================
$AllowedCommands = @("status", "start", "stop", "restart", "processes", "ping")

function Invoke-RemoteCommand {
    param($CmdObj)

    $action  = if ($CmdObj.action) { $CmdObj.action.ToLower().Trim() } else { "" }
    $target  = if ($CmdObj.target) { $CmdObj.target.ToLower().Trim() } else { "all" }

    if ($action -notin $AllowedCommands) {
        return @{ success = $false; error = "Command '$action' not allowed. Valid: $($AllowedCommands -join ', ')" }
    }

    switch ($action) {
        "status" {
            return @{ success = $true; data = (Get-AllServiceStatus) }
        }
        "ping" {
            return @{ success = $true; data = @{
                pong      = $true
                hostname  = $env:COMPUTERNAME
                timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
                uptime    = ((Get-Date) - (Get-CimInstance Win32_OperatingSystem).LastBootUpTime).ToString()
            }}
        }
        "processes" {
            return @{ success = $true; data = (Get-ProcessList) }
        }
        "start" {
            if ($target -eq "all") {
                $msgs = foreach ($svc in $Services.Keys) { Start-ServiceByName -ServiceName $svc }
                return @{ success = $true; data = ($msgs -join "`n") }
            }
            return @{ success = $true; data = (Start-ServiceByName -ServiceName $target) }
        }
        "stop" {
            if ($target -eq "all") {
                $msgs = foreach ($svc in $Services.Keys) { Stop-ServiceByName -ServiceName $svc }
                return @{ success = $true; data = ($msgs -join "`n") }
            }
            return @{ success = $true; data = (Stop-ServiceByName -ServiceName $target) }
        }
        "restart" {
            if ($target -eq "all") {
                $msgs = foreach ($svc in $Services.Keys) { Restart-ServiceByName -ServiceName $svc }
                return @{ success = $true; data = ($msgs -join "`n") }
            }
            return @{ success = $true; data = (Restart-ServiceByName -ServiceName $target) }
        }
    }
}

# ============================================================
#  MAIN LOOP — poll for command files
# ============================================================
Log "===== REMOTE COMMAND WATCHER STARTED on $env:COMPUTERNAME ====="
Log "Watching: $CommandsDir"
Log "Poll interval: ${PollSeconds}s"
Log "Allowed commands: $($AllowedCommands -join ', ')"

while ($true) {
    try {
        $cmdFiles = Get-ChildItem -Path $CommandsDir -Filter "*.cmd.json" -ErrorAction SilentlyContinue

        foreach ($file in $cmdFiles) {
            Log "Processing command file: $($file.Name)"

            try {
                $cmdObj = Get-Content -Path $file.FullName -Raw | ConvertFrom-Json

                # Validate it has required fields
                if (-not $cmdObj.action) {
                    Log "Invalid command file (no action): $($file.Name)" "WARN"
                    Remove-Item -Path $file.FullName -Force
                    continue
                }

                # Execute the command
                $result = Invoke-RemoteCommand -CmdObj $cmdObj

                # Write result file (same name but .result.json)
                $resultFileName = $file.Name -replace '\.cmd\.json$', '.result.json'
                $resultPath = Join-Path $CommandsDir $resultFileName

                $resultPayload = @{
                    command    = $cmdObj.action
                    target     = $(if ($cmdObj.target) { $cmdObj.target } else { "all" })
                    requestedAt = $(if ($cmdObj.timestamp) { $cmdObj.timestamp } else { "unknown" })
                    executedAt  = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
                    executedOn  = $env:COMPUTERNAME
                    result     = $result
                } | ConvertTo-Json -Depth 5

                Set-Content -Path $resultPath -Value $resultPayload -Encoding UTF8
                Log "Result written: $resultFileName" "OK"

                # Remove the command file (processed)
                Remove-Item -Path $file.FullName -Force
                Log "Command file removed: $($file.Name)" "OK"

            } catch {
                Log "Error processing $($file.Name): $_" "ERROR"
                # Remove bad command file to avoid reprocessing
                Remove-Item -Path $file.FullName -Force -ErrorAction SilentlyContinue
            }
        }
    } catch {
        Log "Watcher loop error: $_" "ERROR"
    }

    Start-Sleep -Seconds $PollSeconds
}
