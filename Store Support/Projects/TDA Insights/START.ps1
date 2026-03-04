# TDA Insights Dashboard - Quick Start Script (PowerShell)
# Run: .\START.ps1

Write-Host ""
Write-Host "======================================" -ForegroundColor Blue
Write-Host "TDA Insights Dashboard - Starting Up" -ForegroundColor Blue
Write-Host "======================================" -ForegroundColor Blue
Write-Host ""

# Get the script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check if we're in the right place
if (!(Test-Path "$ScriptDir\backend.py")) {
    Write-Host "ERROR: backend.py not found in current directory" -ForegroundColor Red
    Write-Host "Please run this script from the TDA Insights folder" -ForegroundColor Red
    exit 1
}

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://www.python.org/" -ForegroundColor Red
    exit 1
}

# Check and install dependencies
Write-Host "Checking dependencies..." -ForegroundColor Yellow
try {
    & python -c "import flask" 2>&1 | Out-Null
} catch {
    Write-Host "Installing required packages..." -ForegroundColor Yellow
    & pip install -r "$ScriptDir\requirements.txt"
    if (!$?) {
        Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
}

# Start backend
Write-Host "Starting TDA Insights Backend..." -ForegroundColor Yellow
$backendProcess = Start-Process powershell -ArgumentList "-NoExit -Command `"cd '$ScriptDir'; python backend.py`"" -PassThru

Write-Host "Waiting for backend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Open dashboard
Write-Host "Opening TDA Insights Dashboard..." -ForegroundColor Yellow
Start-Process "http://localhost:5000/dashboard.html"

# Wait and show status
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "✅ TDA Insights Dashboard Started!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend URL: http://localhost:5000" -ForegroundColor Cyan
Write-Host "Dashboard: http://localhost:5000/dashboard.html" -ForegroundColor Cyan
Write-Host ""
Write-Host "API Endpoints:" -ForegroundColor Cyan
Write-Host "  GET  http://localhost:5000/api/health          - Health check"
Write-Host "  GET  http://localhost:5000/api/data            - Get TDA data"
Write-Host "  GET  http://localhost:5000/api/phases          - Get phases"
Write-Host "  GET  http://localhost:5000/api/health-statuses - Get statuses"
Write-Host "  POST http://localhost:5000/api/ppt/generate    - Generate PPT"
Write-Host ""
Write-Host "To stop the backend:" -ForegroundColor Yellow
Write-Host "  - Close the backend console window"
Write-Host "  - Or press Ctrl+C in the backend window"
Write-Host ""
Write-Host "Backend Process ID: $($backendProcess.Id)" -ForegroundColor Gray
Write-Host ""
