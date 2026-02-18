# Backend Server Startup Script (VPN Access)
# This script starts the FastAPI backend server accessible to anyone on the VPN network

Write-Host "Starting Backend Server for VPN Access..." -ForegroundColor Cyan
Write-Host ""

# Navigate to backend directory
Set-Location $PSScriptRoot

# Display network information
Write-Host "Network Information:" -ForegroundColor Yellow
$ipAddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike "*Loopback*"}).IPAddress
Write-Host "Your IP Address(es):"
foreach ($ip in $ipAddress) {
    Write-Host "- $ip" -ForegroundColor Green
}
Write-Host ""

# Set environment variables
$env:GCP_PROJECT_ID = "wmt-assetprotection-prod"
$env:BIGQUERY_DATASET = "Store_Support_Dev"
$env:BIGQUERY_TABLE = "IH_Intake_Data"

Write-Host "Server Configuration:" -ForegroundColor Yellow
Write-Host "Host: 0.0.0.0 (All network interfaces)" -ForegroundColor Green
Write-Host "Port: 8001" -ForegroundColor Green
Write-Host "BigQuery Project: $env:GCP_PROJECT_ID" -ForegroundColor Green
Write-Host ""

Write-Host "Authentication:" -ForegroundColor Yellow
Write-Host "Checking Google Cloud credentials..." -ForegroundColor White

# Check if GOOGLE_APPLICATION_CREDENTIALS is set
if ($env:GOOGLE_APPLICATION_CREDENTIALS) {
    Write-Host "Service account credentials found" -ForegroundColor Green
} else {
    Write-Host "Using default gcloud credentials" -ForegroundColor Yellow
    Write-Host "Run 'gcloud auth application-default login' if needed" -ForegroundColor White
}
Write-Host ""

Write-Host "Access Instructions:" -ForegroundColor Yellow
Write-Host "For users on VPN to access this server:" -ForegroundColor White
Write-Host "1. Share one of the IP addresses above" -ForegroundColor White
Write-Host "2. Users should update code_puppy_standalone.html:" -ForegroundColor White
Write-Host "   const VPN_SERVER_URL = 'http://YOUR_IP:8001';" -ForegroundColor Cyan
Write-Host "3. Users open the HTML file in their browser" -ForegroundColor White
Write-Host ""

Write-Host "Starting server..." -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor White
Write-Host ""
Write-Host "========================================================================" -ForegroundColor Gray
Write-Host ""

# Start the FastAPI server
python main.py
