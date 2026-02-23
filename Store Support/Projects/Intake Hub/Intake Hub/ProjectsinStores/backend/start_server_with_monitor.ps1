# ==========================================
# Intake Hub Server - Persistent Monitor
# ==========================================
# Features:
# - Auto-restarts server if it crashes
# - Logs all restarts and errors
# - Prevents crash loops with cooldown
# - Monitors every 5 seconds
# ==========================================

param(
    [switch]$NoWindow = $false
)

$backendDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$logFile = Join-Path $backendDir "server_monitor.log"
$pidFile = Join-Path $backendDir "server.pid"
$pythonExe = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe"
$maxConsecutiveCrashes = 5
$crashCooldownSeconds = 30

# Initialize logging
function Log-Message {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] [$Level] $Message"
    Write-Host $logEntry -ForegroundColor $(if($Level -eq "ERROR") { "Red" } elseif($Level -eq "WARN") { "Yellow" } else { "Green" })
    Add-Content -Path $logFile -Value $logEntry
}

# Stop existing server if running
function Stop-ExistingServer {
    if (Test-Path $pidFile) {
        $pid = Get-Content $pidFile -ErrorAction SilentlyContinue
        $process = Get-Process -Id $pid -ErrorAction SilentlyContinue
        if ($process) {
            Log-Message "Stopping existing server process (PID: $pid)..." "WARN"
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
            Start-Sleep -Seconds 2
        }
    }
}

# Run server with monitoring
function Start-ServerMonitor {
    Set-Location $backendDir
    
    Log-Message "========================================" "INFO"
    Log-Message "Intake Hub Server Monitor STARTED" "INFO"
    Log-Message "========================================" "INFO"
    Log-Message "Python: $pythonExe" "INFO"
    Log-Message "Backend Dir: $backendDir" "INFO"
    Log-Message "Monitor will auto-restart on crash" "INFO"
    Log-Message "========================================" "INFO"
    Write-Host ""
    
    $consecutiveCrashes = 0
    
    while ($true) {
        try {
            # Start server process
            $process = Start-Process -FilePath $pythonExe `
                -ArgumentList "main.py" `
                -WorkingDirectory $backendDir `
                -PassThru `
                -WindowStyle $(if($NoWindow) { "Hidden" } else { "Normal" })
            
            $process.Id | Out-File $pidFile
            
            Log-Message "Server started (PID: $($process.Id))" "INFO"
            $consecutiveCrashes = 0
            
            # Monitor process
            while (!$process.HasExited) {
                Start-Sleep -Seconds 5
            }
            
            # Process exited - log it
            $exitCode = $process.ExitCode
            Log-Message "Server process exited with code: $exitCode" "WARN"
            $consecutiveCrashes++
            
            # Check if we're in a crash loop
            if ($consecutiveCrashes -ge $maxConsecutiveCrashes) {
                Log-Message "CRASH LOOP DETECTED! ($consecutiveCrashes consecutive crashes)" "ERROR"
                Log-Message "Waiting $crashCooldownSeconds seconds before retry..." "WARN"
                Start-Sleep -Seconds $crashCooldownSeconds
                $consecutiveCrashes = 0  # Reset counter
            }
            
            Log-Message "Restarting server in 3 seconds..." "WARN"
            Start-Sleep -Seconds 3
        }
        catch {
            Log-Message "Exception: $_" "ERROR"
            $consecutiveCrashes++
            Start-Sleep -Seconds 5
        }
    }
}

# Main
try {
    Stop-ExistingServer
    Start-ServerMonitor
}
catch {
    Log-Message "Fatal Error: $_" "ERROR"
    exit 1
}
