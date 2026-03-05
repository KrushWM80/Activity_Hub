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
        "OK" { "[+]" }
        "FAIL" { "[-]" }
        "INFO" { "[*]" }
        "WARN" { "[!]" }
        default { "[?]" }
    }
    Write-Host "$icon $Message" -ForegroundColor $Color
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
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "         ACTIVITY HUB - SERVICE HEALTH CHECK                    " -ForegroundColor Cyan
Write-Host "         $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')                    " -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Port Status
Write-Host "------- PORT STATUS -------" -ForegroundColor Yellow
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
Write-Host "------- AUTHENTICATION -------" -ForegroundColor Yellow
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
Write-Host "------- PYTHON ENVIRONMENTS -------" -ForegroundColor Yellow

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
Write-Host "------- CRITICAL DEPENDENCIES -------" -ForegroundColor Yellow
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

# 5. Key Folders
Write-Host "------- FOLDER STRUCTURE -------" -ForegroundColor Yellow

$keyFolders = @(
    @{Path = "Documentation"; Description = "Documentation files"},
    @{Path = "Infrastructure"; Description = "Infrastructure and deployment"},
    @{Path = "Projects"; Description = "Project-organized scripts"},
    @{Path = "Platform"; Description = "Platform utilities"},
    @{Path = "Automation"; Description = "Automation scripts"}
)

foreach ($folder in $keyFolders) {
    if (Test-Path $folder.Path) {
        $fileCount = (Get-ChildItem -Path $folder.Path -File -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count
        Write-StatusLine "OK" "$($folder.Path) - $fileCount files" "Green"
    } else {
        Write-StatusLine "WARN" "$($folder.Path) - not found" "Yellow"
    }
}
Write-Host ""

# 6. Workspace Config
Write-Host "------- WORKSPACE CONFIGURATION -------" -ForegroundColor Yellow

# Check .venv
$venvActivate = Test-Path ".venv\Scripts\Activate.ps1"
if ($venvActivate) {
    Write-StatusLine "OK" "Virtual Environment (.venv) configured" "Green"
} else {
    Write-StatusLine "WARN" "Virtual Environment (.venv) not found" "Yellow"
    Write-Host "          Run: python -m venv .venv" -ForegroundColor Gray
}

# Check .gitignore
$gitignore = Test-Path ".gitignore"
if ($gitignore) {
    Write-StatusLine "OK" "Git repository initialized" "Green"
} else {
    Write-StatusLine "INFO" "Not a git repository" "Gray"
}
Write-Host ""

# 7. Environment Setup
Write-Host "------- ENVIRONMENT SETUP -------" -ForegroundColor Yellow

if ($env:GOOGLE_APPLICATION_CREDENTIALS) {
    Write-StatusLine "OK" "GOOGLE_APPLICATION_CREDENTIALS set" "Green"
    Write-Host "          Path: $env:GOOGLE_APPLICATION_CREDENTIALS" -ForegroundColor Gray
} else {
    Write-StatusLine "INFO" "GOOGLE_APPLICATION_CREDENTIALS not set (will use gcloud default)" "Gray"
}

# Check timezone
$tz = [System.TimeZone]::CurrentTimeZone.StandardName
Write-StatusLine "INFO" "Timezone: $tz" "Gray"
Write-Host ""

# 8. Documentation
Write-Host "------- AVAILABLE DOCUMENTATION -------" -ForegroundColor Yellow

$docs = Get-ChildItem -Path "Documentation" -Filter "*.md" -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Name
if ($docs) {
    Write-StatusLine "OK" "Documentation available - $($docs.Count) items" "Green"
    if ($Verbose) {
        foreach ($doc in $docs | Select-Object -First 5) {
            Write-Host "          - $doc" -ForegroundColor Gray
        }
        if ($docs.Count -gt 5) {
            Write-Host "          ... and $($docs.Count - 5) more" -ForegroundColor Gray
        }
    }
} else {
    Write-StatusLine "INFO" "Documentation folder empty" "Gray"
}
Write-Host ""

# 9. Summary
Write-Host "------- SUMMARY -------" -ForegroundColor Yellow
Write-Host "Active Services: $activeServices / 2" -ForegroundColor $(if ($activeServices -eq 2) { "Green" } else { "Red" })

if ($activeServices -eq 2) {
    Write-Host "Status: All systems operational [OK]" -ForegroundColor Green
} elseif ($activeServices -eq 1) {
    Write-Host "Status: Partial service outage [WARN]" -ForegroundColor Yellow
} else {
    Write-Host "Status: Service down [ERROR]" -ForegroundColor Red
    if ($Auto) {
        Write-Host "`nAttempting auto-start..." -ForegroundColor Cyan
        # Auto-start logic would go here
    }
}

Write-Host ""
Write-Host "------- QUICK REFERENCE -------" -ForegroundColor Yellow
Write-Host "Documentation Location: Documentation/" -ForegroundColor Gray
Write-Host "Key Scripts: Automation/" -ForegroundColor Gray
Write-Host "Project Files: Projects/" -ForegroundColor Gray
Write-Host "Infrastructure Info: Infrastructure/" -ForegroundColor Gray
Write-Host ""

# Footer
Write-Host "=====================================================================" -ForegroundColor Cyan
