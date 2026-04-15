param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("start", "stop", "status", "clean")]
    [string]$Action,
    
    [Parameter(Mandatory=$false)]
    [ValidateSet("activity-hub", "job-codes", "amp", "projects-stores", "vet", "all")]
    [string]$Service = "activity-hub"
)

$RootDir = "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"
$PidDir = "$RootDir\.pid_tracker"

if (!(Test-Path $PidDir)) {
    New-Item -ItemType Directory -Path $PidDir -Force | Out-Null
}

function Get-PidFile {
    param([string]$Service)
    return "$PidDir\$Service.pid"
}

function Start-ServiceProc {
    param([string]$Service)
    
    Write-Host "[*] Starting $Service..." -ForegroundColor Green
    
    $pidFile = Get-PidFile -Service $Service
    
    if (Test-Path $pidFile) {
        $oldPid = Get-Content $pidFile -Raw
        $proc = Get-Process -PID $oldPid -ErrorAction SilentlyContinue
        if ($proc) {
            Write-Host "[!] $Service already running (PID: $oldPid). Stopping first..." -ForegroundColor Yellow
            Stop-ServiceProc -Service $Service
            Start-Sleep -Seconds 1
        } else {
            Remove-Item $pidFile -Force
        }
    }
    
    switch ($Service) {
        "activity-hub" {
            Push-Location "$RootDir\Interface"
            $proc = Start-Process -FilePath "$RootDir\.venv\Scripts\python.exe" `
                -ArgumentList "activity_hub_server.py" `
                -PassThru -NoNewWindow
            Pop-Location
        }
        "job-codes" {
            Push-Location "$RootDir\Store Support\Projects\JobCodes-teaming\Teaming\dashboard"
            $proc = Start-Process -FilePath "$RootDir\.venv\Scripts\python.exe" `
                -ArgumentList "backend\main.py" `
                -PassThru -NoNewWindow
            Pop-Location
        }
        "amp" {
            Push-Location "$RootDir\Store Support\Projects\AMP"
            $proc = Start-Process -FilePath "$RootDir\.venv\Scripts\python.exe" `
                -ArgumentList "backend\main.py" `
                -PassThru -NoNewWindow
            Pop-Location
        }
        "projects-stores" {
            Push-Location "$RootDir\Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores"
            $proc = Start-Process -FilePath "$RootDir\.venv\Scripts\python.exe" `
                -ArgumentList "backend\main.py" `
                -PassThru -NoNewWindow
            Pop-Location
        }
        "vet" {
            Push-Location "$RootDir\Store Support\Projects\VET_Dashboard"
            $proc = Start-Process -FilePath "$RootDir\.venv\Scripts\python.exe" `
                -ArgumentList "backend.py" `
                -PassThru -NoNewWindow
            Pop-Location
        }
    }
    
    if ($proc) {
        $proc.Id | Out-File -FilePath $pidFile -NoNewline
        Write-Host "[+] $Service started (PID: $($proc.Id))" -ForegroundColor Green
        return $proc.Id
    } else {
        Write-Host "[-] Failed to start $Service" -ForegroundColor Red
        return $null
    }
}

function Stop-ServiceProc {
    param([string]$Service)
    
    Write-Host "[*] Stopping $Service..." -ForegroundColor Yellow
    
    $pidFile = Get-PidFile -Service $Service
    
    if (!(Test-Path $pidFile)) {
        Write-Host "[!] No PID file for $Service (not running?)" -ForegroundColor Yellow
        return
    }
    
    $procId = Get-Content $pidFile -Raw
    $proc = Get-Process -PID $procId -ErrorAction SilentlyContinue
    
    if ($proc) {
        Stop-Process -ID $procId -Force -ErrorAction SilentlyContinue
        Start-Sleep -Milliseconds 500
        Write-Host "[+] Stopped $Service (PID: $procId)" -ForegroundColor Green
    } else {
        Write-Host "[!] Process $procId not found (already stopped?)" -ForegroundColor Yellow
    }
    
    Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
}

function Get-ServiceStatus {
    param([string]$Service)
    
    $pidFile = Get-PidFile -Service $Service
    
    if (!(Test-Path $pidFile)) {
        Write-Host "[-] $Service -- NOT RUNNING (no PID file)" -ForegroundColor Gray
        return
    }
    
    $procId = Get-Content $pidFile -Raw
    $proc = Get-Process -PID $procId -ErrorAction SilentlyContinue
    
    if ($proc) {
        $mem = [math]::Round($proc.WorkingSet/1MB)
        Write-Host "[+] $Service -- RUNNING (PID: $procId, Memory: ${mem}MB)" -ForegroundColor Green
    } else {
        Write-Host "[-] $Service -- DEAD (PID file exists but process gone: $procId)" -ForegroundColor Red
        Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
    }
}

function Clean-StaleFiles {
    Write-Host "[*] Cleaning stale PID files..." -ForegroundColor Cyan
    
    $count = 0
    Get-ChildItem $PidDir -Filter "*.pid" -ErrorAction SilentlyContinue | ForEach-Object {
        $procId = Get-Content $_.FullName -Raw
        $proc = Get-Process -PID $procId -ErrorAction SilentlyContinue
        
        if (!$proc) {
            Remove-Item $_.FullName -Force
            Write-Host "    Removed: $($_.Name)" -ForegroundColor Gray
            $count++
        }
    }
    
    Write-Host "[+] Cleaned $count stale file(s)" -ForegroundColor Green
}

# MAIN EXECUTION
switch ($Action) {
    start {
        if ($Service -eq "all") {
            Start-ServiceProc -Service "activity-hub"
            Start-Sleep -Seconds 1
            Start-ServiceProc -Service "job-codes"
            Start-Sleep -Seconds 1
            Start-ServiceProc -Service "amp"
            Start-Sleep -Seconds 1
            Start-ServiceProc -Service "projects-stores"
            Start-Sleep -Seconds 1
            Start-ServiceProc -Service "vet"
        } else {
            Start-ServiceProc -Service $Service
        }
    }
    stop {
        if ($Service -eq "all") {
            Stop-ServiceProc -Service "activity-hub"
            Stop-ServiceProc -Service "job-codes"
            Stop-ServiceProc -Service "amp"
            Stop-ServiceProc -Service "projects-stores"
            Stop-ServiceProc -Service "vet"
        } else {
            Stop-ServiceProc -Service $Service
        }
    }
    status {
        Write-Host ""
        Write-Host "[*] Service Status Report" -ForegroundColor Cyan
        Write-Host "=========================" -ForegroundColor Cyan
        Write-Host ""
        
        if ($Service -eq "all") {
            Get-ServiceStatus -Service "activity-hub"
            Get-ServiceStatus -Service "job-codes"
            Get-ServiceStatus -Service "amp"
            Get-ServiceStatus -Service "projects-stores"
            Get-ServiceStatus -Service "vet"
        } else {
            Get-ServiceStatus -Service $Service
        }
        
        Write-Host ""
    }
    clean {
        Clean-StaleFiles
    }
}
