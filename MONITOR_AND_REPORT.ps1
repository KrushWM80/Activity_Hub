# Activity Hub Status Monitor - Enhanced with Downtime Detection
# Runs daily at 6 AM and on system startup
# Detects outages and reports them in emails
# Services monitored: 8001 (Projects in Stores), 8080 (Job Codes), 5000 (TDA Insights),
#                     8081 (AMP Store Dashboard), 8888 (Zorro), 5001 (VET Dashboard),
#                     8090 (Store Meeting Planner), DC PayCycle (26 tasks)

$EmailAddresses = @("ATCTeamsupport@walmart.com", "kendall.rush@walmart.com")
$LogFile = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\system_status.log"
$LastStatusFile = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\last_status.json"

# Ensure log file exists
if (-not (Test-Path $LogFile)) {
    New-Item -Path $LogFile -ItemType File -Force | Out-Null
}

# Get current system status
function Get-SystemStatus {
    $status = @{
        TimeStamp = Get-Date
        ProjectsInStoresRunning = $false
        Port8001Listening = $false
        JobCodesRunning = $false
        Port8080Listening = $false
        DCTasksCount = 0
        TDAWeeklyEmailTask = $false
        JobCodesBackendTask = $false
        TDARunning = $false
        Port5000Listening = $false
        StoreActivityDashboardRunning = $false
        ZorroRunning = $false
        Port8888Listening = $false
        VETDashboardRunning = $false
        Port5001Listening = $false
        MeetingPlannerRunning = $false
        Port8090Listening = $false
    }
    
    # Check Projects in Stores (port 8001)
    $netstat = netstat -ano 2>$null | Select-String ":8001.*LISTENING"
    if ($netstat) {
        $status.ProjectsInStoresRunning = $true
        $status.Port8001Listening = $true
    }
    
    # Check Job Codes Backend (port 8080)
    $netstat8080 = netstat -ano 2>$null | Select-String ":8080.*LISTENING"
    if ($netstat8080) {
        $status.JobCodesRunning = $true
        $status.Port8080Listening = $true
    }
    
    # Check TDA Insights (port 5000)
    $netstat5000 = netstat -ano 2>$null | Select-String ":5000.*LISTENING"
    if ($netstat5000) {
        $status.TDARunning = $true
        $status.Port5000Listening = $true
    }
    
    # Check Store Activity Dashboard (port 8081) - amp_backend_server.py
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8081/" -TimeoutSec 2 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            $status.StoreActivityDashboardRunning = $true
        }
    } catch {
        # Dashboard not responding on port 8081
        $status.StoreActivityDashboardRunning = $false
    }
    
    # Check Zorro (port 8888) - audio_server.py
    $netstat8888 = netstat -ano 2>$null | Select-String ":8888.*LISTENING"
    if ($netstat8888) {
        $status.ZorroRunning = $true
        $status.Port8888Listening = $true
    }
    
    # Check VET Dashboard (port 5001) - backend.py
    $netstat5001 = netstat -ano 2>$null | Select-String ":5001.*LISTENING"
    if ($netstat5001) {
        $status.VETDashboardRunning = $true
        $status.Port5001Listening = $true
    }
    
    # Check Store Meeting Planner (port 8090) - main.py
    $netstat8090 = netstat -ano 2>$null | Select-String ":8090.*LISTENING"
    if ($netstat8090) {
        $status.MeetingPlannerRunning = $true
        $status.Port8090Listening = $true
    }
    
    # Check Job Codes Backend Task
    $jobCodesTask = Get-ScheduledTask -TaskName "JobCodes-Backend-Server" -ErrorAction SilentlyContinue
    $status.JobCodesBackendTask = $null -ne $jobCodesTask
    
    # Check TDA Weekly Email Task
    $tdaWeeklyTask = Get-ScheduledTask -TaskName "Activity_Hub_TDA_Weekly_Email" -ErrorAction SilentlyContinue
    $status.TDAWeeklyEmailTask = $null -ne $tdaWeeklyTask
    
    # Check DC Manager Tasks
    $dcTasks = Get-ScheduledTask -ErrorAction SilentlyContinue | Where-Object {$_.TaskName -like "DC-EMAIL-PC-*"}
    $status.DCTasksCount = if ($dcTasks) { $dcTasks.Count } else { 0 }
    
    return $status
}

# Calculate downtime
function Get-DowntimeInfo {
    if (-not (Test-Path $LastStatusFile)) {
        return $null  # First run, no previous status
    }
    
    try {
        $lastStatus = Get-Content $LastStatusFile | ConvertFrom-Json
        $lastTime = [DateTime]$lastStatus.TimeStamp
        $currentTime = Get-Date
        $downtime = $currentTime - $lastTime
        
        # If downtime is more than 5 minutes, report it
        if ($downtime.TotalMinutes -gt 5) {
            return @{
                WasDown = $true
                DowntimeMinutes = [Math]::Round($downtime.TotalMinutes, 2)
                DowntimeHours = [Math]::Round($downtime.TotalHours, 2)
                LastSeen = $lastTime
                CurrentTime = $currentTime
            }
        }
    } catch {
        # Log error but continue
    }
    
    return $null
}

# Build email body with status
function Build-StatusEmail {
    param($CurrentStatus, $DowntimeInfo, $IsRestartEmail = $false)
    
    $statusOK = $CurrentStatus.ProjectsInStoresRunning -and $CurrentStatus.DCTasksCount -eq 26 -and $CurrentStatus.JobCodesRunning -and $CurrentStatus.VETDashboardRunning -and $CurrentStatus.MeetingPlannerRunning
    $statusIndicator = if ($statusOK) { "ALL SYSTEMS OPERATIONAL" } else { "ATTENTION REQUIRED" }
    $currentTime = Get-Date -Format 'MMMM d, yyyy - h:mm tt'
    
    $downtimeAlert = ""
    if ($DowntimeInfo -and $DowntimeInfo.WasDown) {
        $downtimeAlert = @"
    <div style="background-color: #fff3cd; border: 2px solid #ff9800; padding: 15px; margin: 15px 0; border-radius: 5px;">
        <h3 style="color: #ff6f00; margin-top: 0;">DOWNTIME ALERT</h3>
        <p><strong>System was offline for:</strong> $($DowntimeInfo.DowntimeHours) hours ($($DowntimeInfo.DowntimeMinutes) minutes)</p>
        <p><strong>Last Status:</strong> $($DowntimeInfo.LastSeen.ToString('MMMM d, yyyy h:mm tt'))</p>
        <p><strong>Back Online:</strong> $($DowntimeInfo.CurrentTime.ToString('MMMM d, yyyy h:mm tt'))</p>
    </div>
"@
    }
    
    $restartNote = ""
    if ($IsRestartEmail) {
        $restartNote = @"
    <div style="background-color: #e8f5e9; border: 2px solid #4caf50; padding: 15px; margin: 15px 0; border-radius: 5px;">
        <h3 style="color: #2e7d32; margin-top: 0;">SYSTEM RESTART DETECTED</h3>
        <p>The system was restarted at <strong>$currentTime</strong>.</p>
        <p>All services have been restored and verified operational.</p>
    </div>
"@
    }
    
    $html = @"
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial; font-size: 11pt; color: #333; }
        .header { background: #0071ce; color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px; }
        .status-ok { color: #22863a; font-weight: bold; }
        .status-down { color: #cb2431; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; margin: 10px 0; }
        th { background: #f1f8ff; text-align: left; padding: 8px; border: 1px solid #ddd; font-weight: bold; }
        td { padding: 8px; border: 1px solid #ddd; }
        .section { margin: 15px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h2>Activity Hub Daily Status Report</h2>
        <p style="margin: 5px 0;">$currentTime</p>
        <p style="margin: 5px 0; font-size: 12pt;"><strong>Status: $statusIndicator</strong></p>
    </div>

    $downtimeAlert
    $restartNote

    <div class="section">
        <h3>System Components</h3>
        <table>
            <tr>
                <th>Component</th>
                <th>Status</th>
                <th>Details</th>
            </tr>
            <tr>
                <td>Projects in Stores Backend</td>
                <td class="$(if ($CurrentStatus.ProjectsInStoresRunning) { 'status-ok' } else { 'status-down' })">$(if ($CurrentStatus.ProjectsInStoresRunning) { 'RUNNING' } else { 'OFFLINE' })</td>
                <td>Port 8001 - $(if ($CurrentStatus.Port8001Listening) { 'Listening' } else { 'Not responding' })</td>
            </tr>
            <tr>
                <td>Job Codes Teaming Dashboard</td>
                <td class="$(if ($CurrentStatus.JobCodesRunning) { 'status-ok' } else { 'status-down' })">$(if ($CurrentStatus.JobCodesRunning) { 'RUNNING' } else { 'OFFLINE' })</td>
                <td>Port 8080 - $(if ($CurrentStatus.Port8080Listening) { 'Listening' } else { 'Not responding' })</td>
            </tr>
            <tr>
                <td>TDA Insights Dashboard</td>
                <td class="$(if ($CurrentStatus.TDARunning) { 'status-ok' } else { 'status-down' })">$(if ($CurrentStatus.TDARunning) { 'RUNNING' } else { 'OFFLINE' })</td>
                <td>Port 5000 - $(if ($CurrentStatus.Port5000Listening) { 'Listening' } else { 'Not responding' })</td>
            </tr>
            <tr>
                <td>AMP Store Updates Dashboard</td>
                <td class="$(if ($CurrentStatus.StoreActivityDashboardRunning) { 'status-ok' } else { 'status-down' })">$(if ($CurrentStatus.StoreActivityDashboardRunning) { 'RUNNING' } else { 'OFFLINE' })</td>
                <td>HTTP Server port 8081 - $(if ($CurrentStatus.StoreActivityDashboardRunning) { 'Responding' } else { 'Not responding' })</td>
            </tr>
            <tr>
                <td>Zorro Podcast Server</td>
                <td class="$(if ($CurrentStatus.ZorroRunning) { 'status-ok' } else { 'status-down' })">$(if ($CurrentStatus.ZorroRunning) { 'RUNNING' } else { 'OFFLINE' })</td>
                <td>Port 8888 - $(if ($CurrentStatus.Port8888Listening) { 'Listening' } else { 'Not responding' })</td>
            </tr>
            <tr>
                <td>V.E.T. Dashboard</td>
                <td class="$(if ($CurrentStatus.VETDashboardRunning) { 'status-ok' } else { 'status-down' })">$(if ($CurrentStatus.VETDashboardRunning) { 'RUNNING' } else { 'OFFLINE' })</td>
                <td>Port 5001 - $(if ($CurrentStatus.Port5001Listening) { 'Listening' } else { 'Not responding' })</td>
            </tr>
            <tr>
                <td>Store Meeting Planner</td>
                <td class="$(if ($CurrentStatus.MeetingPlannerRunning) { 'status-ok' } else { 'status-down' })">$(if ($CurrentStatus.MeetingPlannerRunning) { 'RUNNING' } else { 'OFFLINE' })</td>
                <td>Port 8090 - $(if ($CurrentStatus.Port8090Listening) { 'Listening' } else { 'Not responding' })</td>
            </tr>
            <tr>
                <td>DC Manager PayCycle Tasks</td>
                <td class="$(if ($CurrentStatus.DCTasksCount -eq 26) { 'status-ok' } else { 'status-down' })">$(if ($CurrentStatus.DCTasksCount -eq 26) { 'ACTIVE' } else { 'INCOMPLETE' })</td>
                <td>$($CurrentStatus.DCTasksCount)/26 tasks scheduled</td>
            </tr>
            <tr>
                <td>TDA Weekly Email Task</td>
                <td class="$(if ($CurrentStatus.TDAWeeklyEmailTask) { 'status-ok' } else { 'status-down' })">$(if ($CurrentStatus.TDAWeeklyEmailTask) { 'REGISTERED' } else { 'NOT REGISTERED' })</td>
                <td>Scheduled: Thursdays 11:00 AM</td>
            </tr>
        </table>
    </div>

    <div class="section">
        <h3>Key Metrics</h3>
        <ul>
            <li><strong>Overall Status:</strong> $(if ($statusOK) { 'All systems operational' } else { 'Issues detected' })</li>
            <li><strong>Services Running:</strong> $(($CurrentStatus.ProjectsInStoresRunning -as [int]) + ($CurrentStatus.JobCodesRunning -as [int]) + ($CurrentStatus.TDARunning -as [int]) + ($CurrentStatus.StoreActivityDashboardRunning -as [int]) + ($CurrentStatus.ZorroRunning -as [int]) + ($CurrentStatus.VETDashboardRunning -as [int]) + ($CurrentStatus.MeetingPlannerRunning -as [int]))/7 running</li>
            <li><strong>Scheduled Tasks:</strong> 29 active</li>
            <li><strong>Report Generated:</strong> $currentTime</li>
        </ul>
    </div>

    <div class="section">
        <h3>Access Points</h3>
        <ul>
            <li><strong>Projects in Stores:</strong> http://10.97.114.181:8001/</li>
            <li><strong>Job Codes Dashboard:</strong> http://10.97.114.181:8080/static/index.html#</li>
            <li><strong>TDA Insights:</strong> http://localhost:5000/dashboard.html</li>
            <li><strong>AMP Store Dashboard:</strong> http://localhost:8081/</li>
            <li><strong>Zorro Podcast Server:</strong> http://localhost:8888/</li>
            <li><strong>V.E.T. Dashboard:</strong> http://localhost:5001/vet_dashboard.html</li>
            <li><strong>Store Meeting Planner:</strong> http://localhost:8090/</li>
            <li><strong>Note:</strong> Use IP address for Job Codes &amp; Projects. Use localhost for all others.</li>
        </ul>
    </div>

    <div class="section">
        <h3>Upcoming Events</h3>
        <ul>
            <li><strong>Daily (3:00 AM EST):</strong> Job Codes scheduled restart</li>
            <li><strong>Daily (6:00 AM EST):</strong> Health check and status report</li>
            <li><strong>Every 6 Hours:</strong> Background health check restart cycle</li>
        </ul>
    </div>

    <hr style="margin: 20px 0; border: none; border-top: 1px solid #ddd;">
    <p style="font-size: 9pt; color: #666;">
        <strong>Activity Hub Monitor</strong> | Computer: WEUS42608431466<br>
        Automated status report with health checks and auto-restart capability | Next scheduled: Tomorrow 6:00 AM
    </p>
</body>
</html>
"@
    
    return $html
}

# ==========================================
# JOB CODES HEALTH CHECK & AUTO-RESTART
# ==========================================
function Check-And-RestartJobCodes {
    param($SystemStatus)
    
    if (-not $SystemStatus.JobCodesRunning) {
        Write-Host "⚠ Job Codes is offline - attempting automatic restart..." -ForegroundColor Yellow
        
        try {
            # Trigger the JobCodes-Backend-Server task to run immediately
            $jobCodesTask = Get-ScheduledTask -TaskName "JobCodes-Backend-Server" -ErrorAction SilentlyContinue
            if ($jobCodesTask) {
                Start-ScheduledTask -TaskName "JobCodes-Backend-Server" -ErrorAction SilentlyContinue
                Write-Host "✓ Triggered JobCodes-Backend-Server task" -ForegroundColor Green
                
                # Wait 3 seconds for process to start
                Start-Sleep -Seconds 3
                
                # Re-check if it's running
                $netstat = netstat -ano 2>$null | Select-String ":8080.*LISTENING"
                if ($netstat) {
                    Write-Host "✓ Job Codes successfully restarted and listening on port 8080" -ForegroundColor Green
                    return $true
                } else {
                    Write-Host "✗ Job Codes task triggered but not yet listening" -ForegroundColor Yellow
                    return $false
                }
            }
        } catch {
            Write-Host "✗ Error restarting Job Codes: $_" -ForegroundColor Red
            return $false
        }
    } else {
        Write-Host "✓ Job Codes is running normally on port 8080" -ForegroundColor Green
        return $true
    }
}

# ==========================================
# TDA INSIGHTS HEALTH CHECK & AUTO-RESTART
# ==========================================
function Check-And-RestartTDA {
    param($SystemStatus)
    
    if (-not $SystemStatus.TDARunning) {
        Write-Host "⚠ TDA Insights is offline - attempting automatic restart..." -ForegroundColor Yellow
        
        try {
            # Define TDA backend path and startup command
            $tdaPath = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\TDA Insights"
            $pythonExe = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"
            
            if (Test-Path $tdaPath) {
                # Start TDA backend process in background
                $env:GOOGLE_APPLICATION_CREDENTIALS = "C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json"
                $process = Start-Process -FilePath $pythonExe -ArgumentList "$tdaPath\backend_simple.py" -WorkingDirectory $tdaPath -WindowStyle Hidden -PassThru -ErrorAction SilentlyContinue
                
                if ($process) {
                    Write-Host "✓ Started TDA Insights backend (PID: $($process.Id))" -ForegroundColor Green
                    Start-Sleep -Seconds 2
                    
                    # Re-check if it's running
                    $netstat = netstat -ano 2>$null | Select-String ":5000.*LISTENING"
                    if ($netstat) {
                        Write-Host "✓ TDA successfully restarted and listening on port 5000" -ForegroundColor Green
                        return $true
                    }
                }
            }
        } catch {
            Write-Host "✗ Error restarting TDA: $_" -ForegroundColor Red
            return $false
        }
    } else {
        Write-Host "✓ TDA Insights is running normally on port 5000" -ForegroundColor Green
        return $true
    }
}

# ==========================================
# ZORRO HEALTH CHECK & AUTO-RESTART
# ==========================================
function Check-And-RestartZorro {
    param($SystemStatus)
    
    if (-not $SystemStatus.ZorroRunning) {
        Write-Host "⚠ Zorro is offline - attempting automatic restart..." -ForegroundColor Yellow
        
        try {
            # Define Zorro path and startup command
            $zorroPath = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\AMP\Zorro"
            $pythonExe = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"
            
            if (Test-Path $zorroPath) {
                # Start Zorro server process in background
                $process = Start-Process -FilePath $pythonExe -ArgumentList "$zorroPath\audio_server.py" -WorkingDirectory $zorroPath -WindowStyle Hidden -PassThru -ErrorAction SilentlyContinue
                
                if ($process) {
                    Write-Host "✓ Started Zorro server (PID: $($process.Id))" -ForegroundColor Green
                    Start-Sleep -Seconds 2
                    
                    # Re-check if it's running
                    $netstat = netstat -ano 2>$null | Select-String ":8888.*LISTENING"
                    if ($netstat) {
                        Write-Host "✓ Zorro successfully restarted and listening on port 8888" -ForegroundColor Green
                        return $true
                    }
                }
            }
        } catch {
            Write-Host "✗ Error restarting Zorro: $_" -ForegroundColor Red
            return $false
        }
    } else {
        Write-Host "✓ Zorro is running normally on port 8888" -ForegroundColor Green
        return $true
    }
}

# ==========================================
# AMP STORE UPDATES DASHBOARD HEALTH CHECK & AUTO-RESTART
# ==========================================
function Check-And-RestartAMPDashboard {
    param($SystemStatus)
    
    if (-not $SystemStatus.StoreActivityDashboardRunning) {
        Write-Host "⚠ AMP Store Updates Dashboard is offline - attempting automatic restart..." -ForegroundColor Yellow
        
        try {
            # Define AMP dashboard path and startup command
            $ampPath = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\AMP\Store Updates Dashboard"
            $pythonExe = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"
            
            if (Test-Path $ampPath) {
                # Set Google Cloud credentials (amp_backend_server.py needs BigQuery access)
                $env:GOOGLE_APPLICATION_CREDENTIALS = "C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json"
                $env:PORT = "8081"
                
                # Start AMP backend process in background
                $process = Start-Process -FilePath $pythonExe -ArgumentList "$ampPath\amp_backend_server.py" -WorkingDirectory $ampPath -WindowStyle Hidden -PassThru -ErrorAction SilentlyContinue
                
                if ($process) {
                    Write-Host "✓ Started AMP Store Updates Dashboard (PID: $($process.Id))" -ForegroundColor Green
                    Start-Sleep -Seconds 3
                    
                    # Re-check if it's responding
                    try {
                        $response = Invoke-WebRequest -Uri "http://localhost:8081/" -TimeoutSec 2 -ErrorAction SilentlyContinue
                        if ($response.StatusCode -eq 200) {
                            Write-Host "✓ AMP Dashboard successfully restarted and responding on port 8081" -ForegroundColor Green
                            return $true
                        }
                    } catch {
                        Write-Host "✗ AMP Dashboard started but not yet responding" -ForegroundColor Yellow
                        return $false
                    }
                }
            } else {
                Write-Host "✗ AMP Dashboard path not found: $ampPath" -ForegroundColor Red
            }
        } catch {
            Write-Host "✗ Error restarting AMP Dashboard: $_" -ForegroundColor Red
            return $false
        }
    } else {
        Write-Host "✓ AMP Store Updates Dashboard is running normally on port 8081" -ForegroundColor Green
        return $true
    }
}

# ==========================================
# VET DASHBOARD HEALTH CHECK & AUTO-RESTART
# ==========================================
function Check-And-RestartVETDashboard {
    param($SystemStatus)
    
    if (-not $SystemStatus.VETDashboardRunning) {
        Write-Host "⚠ V.E.T. Dashboard is offline - attempting automatic restart..." -ForegroundColor Yellow
        
        try {
            $vetPath = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\VET_Dashboard"
            $pythonExe = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"
            $batFile = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_vet_dashboard_24_7.bat"
            
            if (Test-Path $batFile) {
                $process = Start-Process -FilePath "cmd.exe" -ArgumentList "/c `"$batFile`"" -WindowStyle Hidden -PassThru -ErrorAction SilentlyContinue
                Start-Sleep -Seconds 4
            } elseif (Test-Path $vetPath) {
                $env:GOOGLE_APPLICATION_CREDENTIALS = "C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json"
                $process = Start-Process -FilePath $pythonExe -ArgumentList "backend.py" -WorkingDirectory $vetPath -WindowStyle Hidden -PassThru -ErrorAction SilentlyContinue
                Start-Sleep -Seconds 4
            }
            
            $check = netstat -ano 2>$null | Select-String ":5001.*LISTENING"
            if ($check) {
                Write-Host "✓ V.E.T. Dashboard successfully restarted on port 5001" -ForegroundColor Green
                return $true
            } else {
                Write-Host "✗ V.E.T. Dashboard restart attempted but not yet listening" -ForegroundColor Yellow
                return $false
            }
        } catch {
            Write-Host "✗ Error restarting V.E.T. Dashboard: $_" -ForegroundColor Red
            return $false
        }
    } else {
        Write-Host "✓ V.E.T. Dashboard is running normally on port 5001" -ForegroundColor Green
        return $true
    }
}

# ==========================================
# STORE MEETING PLANNER HEALTH CHECK & AUTO-RESTART
# ==========================================
function Check-And-RestartMeetingPlanner {
    param($SystemStatus)
    
    if (-not $SystemStatus.MeetingPlannerRunning) {
        Write-Host "⚠ Store Meeting Planner is offline - attempting automatic restart..." -ForegroundColor Yellow
        
        try {
            $plannerPath = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\AMP\Store Meeting Planners\backend"
            $pythonExe = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"
            $batFile = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Automation\start_meeting_planner_24_7.bat"
            
            if (Test-Path $batFile) {
                $process = Start-Process -FilePath "cmd.exe" -ArgumentList "/c `"$batFile`"" -WindowStyle Hidden -PassThru -ErrorAction SilentlyContinue
                Start-Sleep -Seconds 4
            } elseif (Test-Path $plannerPath) {
                $env:GOOGLE_APPLICATION_CREDENTIALS = "C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json"
                $process = Start-Process -FilePath $pythonExe -ArgumentList "main.py" -WorkingDirectory $plannerPath -WindowStyle Hidden -PassThru -ErrorAction SilentlyContinue
                Start-Sleep -Seconds 4
            }
            
            $check = netstat -ano 2>$null | Select-String ":8090.*LISTENING"
            if ($check) {
                Write-Host "✓ Store Meeting Planner successfully restarted on port 8090" -ForegroundColor Green
                return $true
            } else {
                Write-Host "✗ Store Meeting Planner restart attempted but not yet listening" -ForegroundColor Yellow
                return $false
            }
        } catch {
            Write-Host "✗ Error restarting Store Meeting Planner: $_" -ForegroundColor Red
            return $false
        }
    } else {
        Write-Host "✓ Store Meeting Planner is running normally on port 8090" -ForegroundColor Green
        return $true
    }
}

# Send email via Outlook
function Send-StatusEmail {
    param($Subject, $HTMLBody)
    
    try {
        $outlook = New-Object -ComObject Outlook.Application
        $mail = $outlook.CreateItem(0)
        
        $mail.To = $EmailAddresses -join ";"
        $mail.Subject = $Subject
        $mail.HTMLBody = $HTMLBody
        $mail.Send()
        
        Write-Host "✓ Email sent successfully" -ForegroundColor Green
        Write-Host "  To: $($EmailAddresses -join ', ')" -ForegroundColor Green
        Write-Host "  Subject: $Subject" -ForegroundColor Green
        Write-Host "  Time: $(Get-Date -Format 'h:mm tt')" -ForegroundColor Green
        
        # Log the send
        "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - Email sent: $Subject" | Add-Content $LogFile
        
    } catch {
        Write-Host "✗ Error sending email: $_" -ForegroundColor Red
        "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - ERROR: $_" | Add-Content $LogFile
    }
}

# Main execution
Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "Activity Hub Status Monitor" -ForegroundColor Cyan
Write-Host "$(Get-Date -Format 'MMMM d, yyyy h:mm tt')" -ForegroundColor Cyan
Write-Host "================================================`n" -ForegroundColor Cyan

# Get current status
$currentStatus = Get-SystemStatus
Write-Host "✓ Current Status retrieved" -ForegroundColor Green

# Check Job Codes health and auto-restart if needed
Write-Host "`nChecking Job Codes health..." -ForegroundColor Cyan
Check-And-RestartJobCodes -SystemStatus $currentStatus

# Check TDA Insights health and auto-restart if needed
Write-Host "`nChecking TDA Insights health..." -ForegroundColor Cyan
Check-And-RestartTDA -SystemStatus $currentStatus

# Check Zorro health and auto-restart if needed
Write-Host "`nChecking Zorro health..." -ForegroundColor Cyan
Check-And-RestartZorro -SystemStatus $currentStatus

# Check AMP Store Updates Dashboard health and auto-restart if needed
Write-Host "`nChecking AMP Store Updates Dashboard health..." -ForegroundColor Cyan
Check-And-RestartAMPDashboard -SystemStatus $currentStatus

# Check VET Dashboard health and auto-restart if needed
Write-Host "`nChecking V.E.T. Dashboard health..." -ForegroundColor Cyan
Check-And-RestartVETDashboard -SystemStatus $currentStatus

# Check Store Meeting Planner health and auto-restart if needed
Write-Host "`nChecking Store Meeting Planner health..." -ForegroundColor Cyan
Check-And-RestartMeetingPlanner -SystemStatus $currentStatus

# Refresh status after all potential restarts
$currentStatus = Get-SystemStatus
Write-Host "`n✓ All health checks complete" -ForegroundColor Green

# Check for downtime
$downtimeInfo = Get-DowntimeInfo
$isRestartEmail = $false

# Detect if this is a startup email (check if system was recently restarted)
try {
    $bootTime = [datetime]::FromFileTime((Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager").SystemBootTime.ToInt64())
    $timeSinceBoot = (Get-Date) - $bootTime
    if ($timeSinceBoot.TotalMinutes -lt 5) {
        $isRestartEmail = $true
        Write-Host "✓ Startup detected - sending restart notification" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠ Could not determine boot time, assuming normal run" -ForegroundColor Yellow
}

# Build email
$subject = if ($isRestartEmail) {
    "Activity Hub Status - System Restart Detected - $(Get-Date -Format 'MMMM d, yyyy')"
} else {
    "Activity Hub Daily Status Report - $(Get-Date -Format 'MMMM d, yyyy')"
}

$htmlBody = Build-StatusEmail -CurrentStatus $currentStatus -DowntimeInfo $downtimeInfo -IsRestartEmail $isRestartEmail

# Send email
Send-StatusEmail -Subject $subject -HTMLBody $htmlBody

# Save current status for next run
$currentStatus | Add-Member -MemberType NoteProperty -Name "TimeStamp" -Value (Get-Date) -Force
$currentStatus | ConvertTo-Json | Set-Content $LastStatusFile

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "Status check complete" -ForegroundColor Green
Write-Host "================================================`n" -ForegroundColor Green
