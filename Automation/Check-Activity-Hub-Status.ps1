# Activity Hub - Check Status & Run Health Check
# Right-click in PowerShell and select "Run as Administrator"
# OR: Right-click this file, select "Run with PowerShell"

# Check if running as admin
if (-NOT ([Security.Principal.WindowsIdentity]::GetCurrent()).groups -match "S-1-5-32-544") {
    Write-Host ""
    Write-Host "WARNING: Not running as Administrator" -ForegroundColor Yellow
    Write-Host "Some features may not work properly." -ForegroundColor Yellow
    Write-Host ""
}

$ProjectRoot = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Activity Hub - Status Check & Health Report" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Show scheduled tasks
Write-Host "=== SCHEDULED TASKS STATUS ===" -ForegroundColor Yellow
Write-Host ""
$tasks = Get-ScheduledTask | Where-Object {$_.TaskName -like "Activity_Hub*"} | Select-Object TaskName, State
$tasks | Format-Table

$count = ($tasks | Measure-Object).Count
Write-Host "$count tasks configured" -ForegroundColor Green
Write-Host ""

# Show running services
Write-Host "=== RUNNING PYTHON SERVICES ===" -ForegroundColor Yellow
Write-Host ""
$processes = Get-Process python -ErrorAction SilentlyContinue
if ($processes) {
    Write-Host "$($processes.Count) Python processes running" -ForegroundColor Green
    $processes | Select-Object Name, Id, WorkingSet | Format-Table
} else {
    Write-Host "No Python processes running" -ForegroundColor Gray
}

Write-Host ""
Write-Host "=== RUNNING HEALTH CHECK ===" -ForegroundColor Yellow
Write-Host ""
Write-Host "Checking all services and sending email report..." -ForegroundColor Cyan
Write-Host ""

# Run health check
& "$ProjectRoot\MONITOR_AND_REPORT.ps1"

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "  Health check complete!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to close"
