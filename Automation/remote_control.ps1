# Activity Hub Remote Control - Laptop Side
# Sends commands to the desktop via OneDrive-synced command files
# Called by remote_control.bat or directly from PowerShell
#
# Usage:
#   .\remote_control.ps1 status
#   .\remote_control.ps1 start jobcodes
#   .\remote_control.ps1 stop meetingplanner
#   .\remote_control.ps1 restart all
#   .\remote_control.ps1 processes
#   .\remote_control.ps1 ping

param(
    [Parameter(Position=0)]
    [string]$Action = "status",

    [Parameter(Position=1)]
    [string]$Target = "all"
)

$ProjectRoot = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"
$CommandsDir = "$ProjectRoot\Automation\remote_commands"
$MaxWaitSec  = 120  # Max time to wait for result (OneDrive sync ~30-60s)
$PollSec     = 5

$ValidActions = @("status", "start", "stop", "restart", "processes", "ping")
$ValidTargets = @("all", "jobcodes", "projects", "tda", "storedashboard", "meetingplanner", "vet", "zorro")

# Validate inputs
$Action = $Action.ToLower().Trim()
$Target = $Target.ToLower().Trim()

if ($Action -notin $ValidActions) {
    Write-Host ""
    Write-Host "  Invalid action: $Action" -ForegroundColor Red
    Write-Host "  Valid actions: $($ValidActions -join ', ')" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

if ($Target -notin $ValidTargets) {
    Write-Host ""
    Write-Host "  Invalid target: $Target" -ForegroundColor Red
    Write-Host "  Valid targets: $($ValidTargets -join ', ')" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

# Generate a unique command ID
$cmdId = "cmd_$(Get-Date -Format 'yyyyMMdd_HHmmss')_$([System.IO.Path]::GetRandomFileName().Split('.')[0])"
$cmdFile    = Join-Path $CommandsDir "$cmdId.cmd.json"
$resultFile = Join-Path $CommandsDir "$cmdId.result.json"

# Write command file
$command = @{
    id        = $cmdId
    action    = $Action
    target    = $Target
    timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    from      = $env:COMPUTERNAME
} | ConvertTo-Json

Write-Host ""
Write-Host "  ============================================" -ForegroundColor Cyan
Write-Host "   Activity Hub Remote Control" -ForegroundColor Cyan
Write-Host "  ============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Command:  " -NoNewline; Write-Host "$Action $Target" -ForegroundColor Yellow
Write-Host "  From:     " -NoNewline; Write-Host "$env:COMPUTERNAME" -ForegroundColor Gray
Write-Host "  Sent at:  " -NoNewline; Write-Host "$(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Gray
Write-Host ""

# Check if we're on the desktop — run locally instead of waiting for sync
$desktopHostname = "WEUS42608431466"
if ($env:COMPUTERNAME -eq $desktopHostname) {
    Write-Host "  Running locally on desktop..." -ForegroundColor Green
    Set-Content -Path $cmdFile -Value $command -Encoding UTF8
    # The watcher will pick it up, but give it a nudge — just wait a bit
    Write-Host "  Command file written. Watcher will process shortly." -ForegroundColor Gray
} else {
    Set-Content -Path $cmdFile -Value $command -Encoding UTF8
    Write-Host "  Command file written to OneDrive." -ForegroundColor Gray
    Write-Host "  Waiting for desktop to execute (OneDrive sync ~30-60s)..." -ForegroundColor Gray
}

Write-Host ""

# Wait for result
$elapsed = 0
$spinner = @('|', '/', '-', '\')
$spinIdx = 0

while ($elapsed -lt $MaxWaitSec) {
    if (Test-Path $resultFile) {
        # Result arrived
        Write-Host "`r  " -NoNewline
        Write-Host "  Result received!" -ForegroundColor Green
        Write-Host ""

        try {
            $result = Get-Content -Path $resultFile -Raw | ConvertFrom-Json

            Write-Host "  Executed on:  " -NoNewline; Write-Host "$($result.executedOn)" -ForegroundColor Cyan
            Write-Host "  Executed at:  " -NoNewline; Write-Host "$($result.executedAt)" -ForegroundColor Gray
            Write-Host ""

            if ($result.result.success) {
                $data = $result.result.data
                if ($Action -eq "status" -and $data.Services) {
                    Write-Host "  SERVICE STATUS" -ForegroundColor White
                    Write-Host "  -------------------------------------------" -ForegroundColor Gray
                    foreach ($svc in $data.Services.PSObject.Properties) {
                        $name   = $svc.Name.PadRight(18)
                        $port   = $svc.Value.Port
                        $status = $svc.Value.Status
                        $color  = if ($status -eq "RUNNING") { "Green" } else { "Red" }
                        Write-Host "  $name  :$port  " -NoNewline
                        Write-Host "$status" -ForegroundColor $color
                    }
                    Write-Host "  -------------------------------------------" -ForegroundColor Gray
                    Write-Host "  Python processes: $($data.PythonCount)" -ForegroundColor Gray
                    Write-Host "  DC Paycycle tasks: $($data.DCTasksCount)" -ForegroundColor Gray
                    Write-Host "  Desktop hostname:  $($data.Hostname)" -ForegroundColor Gray
                } else {
                    # Generic output
                    $dataStr = if ($data -is [string]) { $data } else { $data | ConvertTo-Json -Depth 3 }
                    Write-Host $dataStr
                }
            } else {
                Write-Host "  ERROR: $($result.result.error)" -ForegroundColor Red
            }
        } catch {
            Write-Host "  Error reading result: $_" -ForegroundColor Red
            Write-Host "  Raw content:" -ForegroundColor Yellow
            Get-Content -Path $resultFile -Raw | Write-Host
        }

        # Clean up result file
        Remove-Item -Path $resultFile -Force -ErrorAction SilentlyContinue
        Write-Host ""
        exit 0
    }

    # Spinner animation
    $char = $spinner[$spinIdx % $spinner.Count]
    Write-Host "`r  $char Waiting... ${elapsed}s / ${MaxWaitSec}s " -NoNewline -ForegroundColor DarkGray
    $spinIdx++

    Start-Sleep -Seconds $PollSec
    $elapsed += $PollSec
}

# Timeout
Write-Host ""
Write-Host ""
Write-Host "  TIMEOUT after ${MaxWaitSec}s - no response from desktop." -ForegroundColor Red
Write-Host "  Possible causes:" -ForegroundColor Yellow
Write-Host "    - Desktop is offline or sleeping" -ForegroundColor Yellow
Write-Host "    - Remote watcher is not running on desktop" -ForegroundColor Yellow
Write-Host "    - OneDrive sync is paused or slow" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Command file left in place: $cmdFile" -ForegroundColor Gray
Write-Host "  It will be processed when the desktop comes online." -ForegroundColor Gray
Write-Host ""
exit 1
