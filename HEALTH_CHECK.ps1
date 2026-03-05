#!/usr/bin/env powershell
# Activity Hub - Service Health Check
# Run this script to verify all services are running correctly
# Usage: .\HEALTH_CHECK.ps1

param(
    [switch]$Verbose = $false,
    [switch]$Auto = $false  # Auto-start missing services
)

$ErrorActionPreference = "SilentlyContinue"
$WarningPreference = "SilentlyContinue"

function Write-StatusLine {
    param([string]$Status, [string]$Message, [string]$Color = "Gray")
    $icon = switch($Status) {
        "OK" { "✓" }
        "FAIL" { "✗" }
        "INFO" { "ℹ" }
        "WARN" { "⚠" }
        default { "?" }
    }
    Write-Host "[$icon] $Message" -ForegroundColor $Color
}

function Test-Port {
    param([int]$Port)
    try {
        $conn = [System.Net.Sockets.TcpClient]::new()
        $conn.ConnectAsync("127.0.0.1", $Port).Wait(1000)
        $result = $conn.Connected
        $conn.Dispose()
        return $result
    } catch {
        return $false
    }
}

function Get-ProcessOnPort {
    param([int]$Port)
    try {
        $connection = netstat -ano | Select-String ":$Port.*LISTENING"
        if ($connection) {
            $pid = $connection -split '\s+' | Select-Object -Last 1
            return [int]$pid
        }
        return $null
    } catch {
        return $null
    }
}

# Header
Clear-Host
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║         ACTIVITY HUB - SERVICE HEALTH CHECK                    ║" -ForegroundColor Cyan
Write-Host "║         $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')                    ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# 1. Port Status
Write-Host "━━━ PORT STATUS ━━━" -ForegroundColor Yellow
$ports = @(
    @{Port = 5000; Service = "TDA Insights Backend"; Color = "Green"}
    @{Port = 8001; Service = "Projects in Stores Backend"; Color = "Green"}
)

$activeServices = 0
foreach ($p in $ports) {
    if (Test-Port -Port $p.Port) {
        Write-StatusLine "OK" "Port $($p.Port) - $($p.Service)" $p.Color
        $activeServices++
        
        $pid = Get-ProcessOnPort -Port $p.Port
        if ($pid) {
            $proc = Get-Process -Id $pid -ErrorAction SilentlyContinue
            if ($proc) {
                Write-Host "          PID: $($proc.Id) | Started: $($proc.StartTime)" -ForegroundColor Gray
            }
        }
    } else {
        Write-StatusLine "FAIL" "Port $($p.Port) - $($p.Service)" "Red"
    }
}
Write-Host ""

# 2. Authentication
Write-Host "━━━ AUTHENTICATION ━━━" -ForegroundColor Yellow
$gcloudAuth = Test-Path "C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json" -PathType Leaf
if ($gcloudAuth) {
    Write-StatusLine "OK" "Google Cloud Credentials Found" "Green"
} else {
    Write-StatusLine "FAIL" "Google Cloud Credentials Missing" "Red"
    Write-Host "          Run: gcloud auth application-default login" -ForegroundColor Gray
}

# Verify gcloud is installed
$gcloud = Get-Command gcloud -ErrorAction SilentlyContinue
if ($gcloud) {
    $gcVersion = & gcloud --version 2>$null | Select-Object -First 1
    Write-StatusLine "OK" "gcloud CLI Installed: $gcVersion" "Green"
} else {
    Write-StatusLine "WARN" "gcloud CLI Not Found" "Yellow"
}
Write-Host ""

# 3. Python Environments
Write-Host "━━━ PYTHON ENVIRONMENTS ━━━" -ForegroundColor Yellow

# System Python
$sysPython = Get-Command python -ErrorAction SilentlyContinue
if ($sysPython) {
    $version = & python --version 2>&1
    Write-StatusLine "OK" "System Python: $version" "Green"
} else {
    Write-StatusLine "WARN" "System Python Not Found" "Yellow"
}

# .venv Python
$venvPython = Test-Path "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"
if ($venvPython) {
    Write-StatusLine "OK" ".venv Python Found" "Green"
} else {
    Write-StatusLine "FAIL" ".venv Python Not Found" "Red"
}

# AppData Python
$appPython = Test-Path "C:\Users\krush\AppData\Local\Python\bin\python.exe"
if ($appPython) {
    Write-StatusLine "OK" "AppData Python Found" "Green"
} else {
    Write-StatusLine "WARN" "AppData Python Not Found" "Yellow"
}
Write-Host ""

# 4. Critical Dependencies
Write-Host "━━━ CRITICAL DEPENDENCIES ━━━" -ForegroundColor Yellow
$pythonExe = "C:\Users\krush\AppData\Local\Python\bin\python.exe"

if (Test-Path $pythonExe) {
    $packages = @("flask", "google-cloud-bigquery", "python-pptx", "requests")
    foreach ($pkg in $packages) {
        $check = & $pythonExe -m pip list 2>$null | Select-String $pkg
        if ($check) {
            Write-StatusLine "OK" "Package: $pkg" "Green"
        } else {
            Write-StatusLine "FAIL" "Package: $pkg (MISSING)" "Red"
        }
    }
}
Write-Host ""

# 5. Database Files
Write-Host "━━━ DATABASE & CACHE FILES ━━━" -ForegroundColor Yellow

$cacheDb = Test-Path "Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend\projects_cache.db"
if ($cacheDb) {
    Write-StatusLine "OK" "Projects Cache DB Exists" "Green"
    $dbSize = (Get-Item "Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend\projects_cache.db").Length / 1MB
    Write-Host "          Size: $([math]::Round($dbSize, 2)) MB" -ForegroundColor Gray
} else {
    Write-StatusLine "WARN" "Projects Cache DB Not Found (will be created)" "Yellow"
}

$usersDb = "Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend\active_users.json"
if (Test-Path $usersDb) {
    Write-StatusLine "OK" "Active Users Log Exists" "Green"
}
Write-Host ""

# 6. Log Files
Write-Host "━━━ LOG FILES ━━━" -ForegroundColor Yellow

$tdaLog = "Store Support\Projects\TDA Insights\tda_insights.log"
if (Test-Path $tdaLog) {
    $logSize = (Get-Item $tdaLog).Length / 1KB
    $lastWrite = (Get-Item $tdaLog).LastWriteTime
    Write-StatusLine "OK" "TDA Insights Log ($(([math]::Round($logSize, 2))) KB, last: $lastWrite)" "Green"
    
    if ($Verbose) {
        Write-Host "          Last 10 lines:" -ForegroundColor Gray
        Get-Content $tdaLog -Tail 10 | ForEach-Object { Write-Host "            $_" -ForegroundColor Gray }
    }
} else {
    Write-StatusLine "INFO" "TDA Insights Log Not Created Yet" "Gray"
}
Write-Host ""

# 7. Scheduled Tasks
Write-Host "━━━ SCHEDULED TASKS ━━━" -ForegroundColor Yellow

$taskName1 = "Activity Hub - Projects in Stores Server"
$task1 = Get-ScheduledTask -TaskName $taskName1 -ErrorAction SilentlyContinue
if ($task1) {
    $status = if ($task1.State -eq "Ready") { "Enabled"; "Green" } else { "$($task1.State)"; "Yellow" }
    Write-StatusLine "OK" "Scheduled Task: '$taskName1'" $status[1]
    Write-Host "          State: $($task1.State) | Last Run: $($task1 | Get-ScheduledTaskInfo | Select-Object -ExpandProperty LastRunTime)" -ForegroundColor Gray
} else {
    Write-StatusLine "WARN" "Scheduled Task Not Configured: '$taskName1'" "Yellow"
}

$taskName2 = "Activity Hub - TDA Insights Server"
$task2 = Get-ScheduledTask -TaskName $taskName2 -ErrorAction SilentlyContinue
if ($task2) {
    Write-StatusLine "OK" "Scheduled Task: '$taskName2'" "Green"
} else {
    Write-StatusLine "INFO" "Scheduled Task Not Configured: '$taskName2'" "Gray"
}
Write-Host ""

# 8. File Organization
Write-Host "━━━ FILE ORGANIZATION ━━━" -ForegroundColor Yellow

$rootPyFiles = Get-ChildItem -Path "." -File -Filter "*.py" | Measure-Object | Select-Object -ExpandProperty Count
if ($rootPyFiles -gt 10) {
    Write-StatusLine "WARN" "Root folder contains $rootPyFiles .py files (should be reorganized)" "Yellow"
    Write-Host "          See FILE_ORGANIZATION_PLAN.md for details" -ForegroundColor Gray
} else {
    Write-StatusLine "OK" "Root folder is organized" "Green"
}
Write-Host ""

# 9. Summary
Write-Host "━━━ SUMMARY ━━━" -ForegroundColor Yellow
Write-Host "Active Services: $activeServices / 2" -ForegroundColor $(if ($activeServices -eq 2) { "Green" } else { "Red" })

if ($activeServices -eq 2) {
    Write-Host "Status: All systems operational ✓" -ForegroundColor Green
} elseif ($activeServices -eq 1) {
    Write-Host "Status: Partial service outage ⚠" -ForegroundColor Yellow
} else {
    Write-Host "Status: Service down ✗" -ForegroundColor Red
    if ($Auto) {
        Write-Host "`nAttempting auto-start..." -ForegroundColor Cyan
        # Auto-start logic would go here
    }
}

Write-Host ""
Write-Host "━━━ NEXT STEPS ━━━" -ForegroundColor Yellow
if ($activeServices -lt 2) {
    Write-Host "1. Run OPERATIONS_DASHBOARD.md - Startup Guide section" -ForegroundColor Gray
    Write-Host "2. Check error logs for details" -ForegroundColor Gray
    Write-Host "3. Verify authentication is configured" -ForegroundColor Gray
}
Write-Host "4. Review OPERATIONS_DASHBOARD.md for full service info" -ForegroundColor Gray
Write-Host ""

# Footer
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
