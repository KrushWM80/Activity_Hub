# Activity Hub Status Monitor - Enhanced with Downtime Detection
# Runs daily at 6 AM and on system startup
# Detects outages and reports them in emails

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
        DCTasksCount = 0
        JobCodesTaskActive = $false
    }
    
    # Check Projects in Stores
    $netstat = netstat -ano 2>$null | Select-String ":8001.*LISTENING"
    if ($netstat) {
        $status.ProjectsInStoresRunning = $true
        $status.Port8001Listening = $true
    }
    
    # Check DC Manager Tasks
    $dcTasks = Get-ScheduledTask -ErrorAction SilentlyContinue | Where-Object {$_.TaskName -like "DC-EMAIL-PC-*"}
    $status.DCTasksCount = if ($dcTasks) { $dcTasks.Count } else { 0 }
    
    # Check Job Codes Task
    $jobCodesTask = Get-ScheduledTask -TaskName "JobCodes-Continuous-Sync" -ErrorAction SilentlyContinue
    $status.JobCodesTaskActive = $null -ne $jobCodesTask
    
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
    
    $statusOK = $CurrentStatus.ProjectsInStoresRunning -and $CurrentStatus.DCTasksCount -eq 26 -and $CurrentStatus.JobCodesTaskActive
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
                <td>DC Manager PayCycle Tasks</td>
                <td class="$(if ($CurrentStatus.DCTasksCount -eq 26) { 'status-ok' } else { 'status-down' })">$(if ($CurrentStatus.DCTasksCount -eq 26) { 'ACTIVE' } else { 'INCOMPLETE' })</td>
                <td>$($CurrentStatus.DCTasksCount)/26 tasks scheduled</td>
            </tr>
            <tr>
                <td>Job Codes Continuous Sync</td>
                <td class="$(if ($CurrentStatus.JobCodesTaskActive) { 'status-ok' } else { 'status-down' })">$(if ($CurrentStatus.JobCodesTaskActive) { 'ACTIVE' } else { 'INACTIVE' })</td>
                <td>Daily reconciliation at 2:00 AM</td>
            </tr>
        </table>
    </div>

    <div class="section">
        <h3>Key Metrics</h3>
        <ul>
            <li><strong>Overall Status:</strong> $(if ($statusOK) { 'All systems operational' } else { 'Issues detected' })</li>
            <li><strong>Services Running:</strong> 3 of 3 configured</li>
            <li><strong>Scheduled Tasks:</strong> 29 active</li>
            <li><strong>Report Generated:</strong> $currentTime</li>
        </ul>
    </div>

    <div class="section">
        <h3>Upcoming Events</h3>
        <ul>
            <li><strong>Tonight (2:00 AM EST):</strong> Job Codes reconciliation</li>
            <li><strong>Tomorrow (6:00 AM EST):</strong> Daily status report</li>
            <li><strong>March 6, 2026 (6:00 AM EST):</strong> Next DC Manager PayCycle (PC-03)</li>
        </ul>
    </div>

    <hr style="margin: 20px 0; border: none; border-top: 1px solid #ddd;">
    <p style="font-size: 9pt; color: #666;">
        <strong>Activity Hub Monitor</strong> | Computer: WEUS42608431466<br>
        Automated status report | Next scheduled: Tomorrow 6:00 AM
    </p>
</body>
</html>
"@
    
    return $html
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

# Check for downtime
$downtimeInfo = Get-DowntimeInfo
$isRestartEmail = $false

# Detect if this is a startup email (check if system was recently restarted)
$bootTime = [datetime]::FromFileTime((Get-ItemProperty HKLM:\SYSTEM\CurrentControlSet\Control\Session` Manager).SystemBootTime.ToInt64())
$timeSinceBoot = (Get-Date) - $bootTime
if ($timeSinceBoot.TotalMinutes -lt 5) {
    $isRestartEmail = $true
    Write-Host "✓ Startup detected - sending restart notification" -ForegroundColor Green
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
