# Job Code Teaming Dashboard - Start Script
# Run this to start your dashboard

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Job Code Teaming Dashboard" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get Python path
$pythonPath = "C:\Users\krush\.code-puppy-venv\Scripts\python.exe"

# Check if Python exists
if (-not (Test-Path $pythonPath)) {
    Write-Host "X Python not found at $pythonPath" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Python found" -ForegroundColor Green

# Navigate to dashboard directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Check if data files exist
$teamingFile = Join-Path $scriptPath "..\TMS Data (3).xlsx"
$polarisFile = Join-Path $scriptPath "..\polaris_job_codes.csv"

if (Test-Path $teamingFile) {
    Write-Host "[OK] Teaming data file found" -ForegroundColor Green
} else {
    Write-Host "[!] Teaming data file not found: $teamingFile" -ForegroundColor Yellow
}

if (Test-Path $polarisFile) {
    Write-Host "[OK] Polaris data file found" -ForegroundColor Green
} else {
    Write-Host "[!] Polaris data file not found: $polarisFile" -ForegroundColor Yellow
}

# Get hostname and IP addresses
$fqdn = [System.Net.Dns]::GetHostEntry($env:COMPUTERNAME).HostName
$ipAddresses = Get-NetIPAddress -AddressFamily IPv4 | Where-Object { 
    $_.IPAddress -notlike "127.*" -and $_.IPAddress -notlike "169.254.*" 
}
$vpnIP = ($ipAddresses | Where-Object { $_.IPAddress -like "10.*" } | Select-Object -First 1).IPAddress

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting Server..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Dashboard will be available at:" -ForegroundColor Green
Write-Host ""
Write-Host "  Local:     http://localhost:8080" -ForegroundColor White
Write-Host ""
Write-Host "  PERMANENT: http://${fqdn}:8080" -ForegroundColor Green
Write-Host "             (Use this URL - it never changes!)" -ForegroundColor Green
Write-Host ""
Write-Host "  IP:        http://${vpnIP}:8080" -ForegroundColor DarkGray
Write-Host ""
Write-Host "Share the PERMANENT URL with your team!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Default Login: admin / admin123" -ForegroundColor Yellow
Write-Host "(Change password immediately!)" -ForegroundColor Red
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor DarkGray
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start the server
& $pythonPath backend\main.py
