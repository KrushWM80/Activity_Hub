# Activity Hub Continuous Monitoring & Auto-Recovery
# Runs every 5 minutes (24/7)
# Checks all 6 services and restarts any that are down
# Can be scheduled via: SCHTASKS /CREATE /TN Activity_Hub_Continuous_Monitor /TR "powershell -ExecutionPolicy Bypass -File monitor.ps1" /SC minute /MO 5

$LogFile = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\continuous_monitor.log"
$ConfigFile = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\ACTIVITY_HUB_CONFIGURATION.txt"

# Ensure log exists
if (-not (Test-Path $LogFile)) {
    New-Item -Path $LogFile -ItemType File -Force | Out-Null
}

function Log {
    param([string]$Message, [string]$Level = "INFO")
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogEntry = "[$Timestamp] [$Level] $Message"
    Add-Content -Path $LogFile -Value $LogEntry
    Write-Host $LogEntry -ForegroundColor $(if($Level -eq "ERROR") {"Red"} elseif($Level -eq "WARN") {"Yellow"} else {"Green"})
}

# Service definitions
$Services = @(
    @{Name="JobCodes"; Port=8080; HealthURL="http://10.97.114.181:8080"; RestartScript="C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_jobcodes_server_24_7.bat"},
    @{Name="ProjectsInStores"; Port=8001; HealthURL="http://localhost:8001"; RestartScript="C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_projects_in_stores_24_7.bat"},
    @{Name="TDAInsights"; Port=5000; HealthURL="http://localhost:5000"; RestartScript="C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_tda_insights_24_7.bat"},
    @{Name="VETDashboard"; Port=5001; HealthURL="http://localhost:5001"; RestartScript="C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_vet_dashboard_24_7.bat"},
    @{Name="StoreDashboard"; Port=8081; HealthURL="http://localhost:8081"; RestartScript="C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_store_dashboard_24_7.bat"},
    @{Name="MeetingPlanner"; Port=8090; HealthURL="http://localhost:8090"; RestartScript="C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_meeting_planner_24_7.bat"},
    @{Name="Zorro"; Port=8888; HealthURL="http://localhost:8888"; RestartScript="C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_zorro_24_7.bat"},
    @{Name="ActivityHub"; Port=8088; HealthURL="http://localhost:8088/activity-hub/"; RestartScript="C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_activity_hub_24_7.bat"}
)

Log "===== CONTINUOUS MONITORING CYCLE ====="

# Check each service
$DownServices = @()

foreach ($service in $Services) {
    $portListening = netstat -ano 2>$null | Select-String ":$($service.Port).*LISTENING" | Measure-Object
    
    if ($portListening.Count -gt 0) {
        Log "$($service.Name) (port $($service.Port)): ✓ RUNNING" "INFO"
    } else {
        Log "$($service.Name) (port $($service.Port)): ✗ DOWN - Checking bat process..." "WARN"
        $DownServices += $service

        # Check if the bat's restart loop is already running — if so, do NOT launch another copy.
        # Launching a second bat instance causes the port-kill block to kill the first instance,
        # creating a death-loop where both instances kill each other indefinitely.
        $batName = [System.IO.Path]::GetFileName($service.RestartScript)
        $batAlreadyRunning = @(Get-WmiObject Win32_Process -Filter "Name='cmd.exe'" -ErrorAction SilentlyContinue |
            Where-Object { $_.CommandLine -like "*$batName*" })

        if ($batAlreadyRunning.Count -gt 0) {
            Log "$($service.Name): Bat loop already running (PID $($batAlreadyRunning.ProcessId -join ' ')) - port is between restarts, no action needed." "INFO"
        } else {
            Log "$($service.Name): Bat not running — launching restart..." "WARN"
            try {
                $process = Start-Process -FilePath "cmd.exe" -ArgumentList "/c `"$($service.RestartScript)`"" -PassThru -WindowStyle Hidden -ErrorAction SilentlyContinue
                Log "$($service.Name): Restart command executed (PID: $($process.Id))" "INFO"

                Start-Sleep -Seconds 5

                $checkAgain = netstat -ano 2>$null | Select-String ":$($service.Port).*LISTENING" | Measure-Object
                if ($checkAgain.Count -gt 0) {
                    Log "$($service.Name): Recovery successful, port now listening" "INFO"
                } else {
                    Log "$($service.Name): Recovery pending, may take additional time to start" "WARN"
                }
            }
            catch {
                Log "$($service.Name): Failed to restart - $_" "ERROR"
            }
        }
    }
}

# Summary
Log "Monitoring cycle complete. Down services: $($DownServices.Count)/7" "INFO"

if ($DownServices.Count -gt 0) {
    Log "Services requiring attention: $($DownServices.Name -join ', ')" "WARN"
    
    # Send alert email (optional - requires email setup)
    # Send-MailMessage -From "activity-hub@walmart.com" -To "admin@walmart.com" -SmtpServer "localhost" `
    #     -Subject "Activity Hub - Service Outage Detected" `
    #     -Body "The following services are down: $($DownServices.Name -join ', ')`nCheck logs for details."
}

Log "===== CYCLE COMPLETE ====="
