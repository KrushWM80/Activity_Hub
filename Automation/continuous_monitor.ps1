# continuous_monitor.ps1
# Checks all 8 Activity Hub services every 5 minutes.
# If a service port is down, starts its bat loop in a hidden window.
# Logs all events to continuous_monitor.log.
#
# Registered as scheduled task: Activity_Hub_ContinuousMonitor
# Schedule: Every 5 minutes (all day)
# Run level: Highest (admin)
#
# SAFE PATTERN: Never kills python.exe by name.
# Each bat loop already kills its own stale port process at the top of each loop.
# If a bat loop died, this script restarts it. If the bat loop is alive but Python
# crashed, the bat loop's own restart logic handles it within 5 seconds.

$AutomationDir = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation"
$LogFile       = "$AutomationDir\continuous_monitor.log"
$Timestamp     = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# --- Service Definitions ---
$Services = @(
    @{ Name = "JobCodes Dashboard";         Port = 8080; Bat = "$AutomationDir\start_jobcodes_server_24_7.bat"      },
    @{ Name = "Projects in Stores";         Port = 8001; Bat = "$AutomationDir\start_projects_in_stores_24_7.bat"   },
    @{ Name = "TDA Insights";               Port = 5000; Bat = "$AutomationDir\start_tda_insights_24_7.bat"         },
    @{ Name = "AMP Store Dashboard";        Port = 8081; Bat = "$AutomationDir\start_store_dashboard_24_7.bat"      },
    @{ Name = "Store Meeting Planner";      Port = 8090; Bat = "$AutomationDir\start_meeting_planner_24_7.bat"      },
    @{ Name = "VET Dashboard";              Port = 5001; Bat = "$AutomationDir\start_vet_dashboard_24_7.bat"        },
    @{ Name = "Audio Message Hub (Zorro)";  Port = 8888; Bat = "$AutomationDir\start_zorro_24_7.bat"               },
    @{ Name = "Activity Hub";               Port = 8088; Bat = "$AutomationDir\start_activity_hub_24_7.bat"        }
)

# --- TCP Port Check ---
function Test-Port {
    param([int]$Port)
    try {
        $tcp = New-Object System.Net.Sockets.TcpClient
        $connect = $tcp.BeginConnect("localhost", $Port, $null, $null)
        $wait = $connect.AsyncWaitHandle.WaitOne(2000, $false)   # 2s timeout
        if (-not $wait) { $tcp.Close(); return $false }
        $tcp.EndConnect($connect)
        $tcp.Close()
        return $true
    } catch {
        return $false
    }
}

# --- Log Rotation: Keep last 500 lines ---
if (Test-Path $LogFile) {
    $lines = Get-Content $LogFile
    if ($lines.Count -gt 500) {
        $lines | Select-Object -Last 400 | Set-Content $LogFile
    }
}

# --- Check Each Service ---
$downsFound = @()

foreach ($svc in $Services) {
    if (-not (Test-Port -Port $svc.Port)) {
        "$Timestamp [MONITOR] $($svc.Name) (port $($svc.Port)) DOWN — starting bat loop" | Out-File -Append $LogFile
        Start-Process -FilePath "cmd.exe" -ArgumentList "/c `"$($svc.Bat)`"" -WindowStyle Hidden
        $downsFound += $svc
    }
}

# --- Verify Restarts (if any were down) ---
if ($downsFound.Count -gt 0) {
    Start-Sleep -Seconds 15

    foreach ($svc in $downsFound) {
        if (Test-Port -Port $svc.Port) {
            "$Timestamp [MONITOR] RECOVERED: $($svc.Name) (port $($svc.Port)) is back online" | Out-File -Append $LogFile
        } else {
            "$Timestamp [MONITOR] FAILED:    $($svc.Name) (port $($svc.Port)) still down after restart attempt" | Out-File -Append $LogFile
        }
    }
} else {
    # Quiet success — only log a heartbeat every 30 minutes to keep log manageable
    $minute = (Get-Date).Minute
    if ($minute -lt 5 -or ($minute -ge 30 -and $minute -lt 35)) {
        "$Timestamp [MONITOR] All 8 services UP" | Out-File -Append $LogFile
    }
}
