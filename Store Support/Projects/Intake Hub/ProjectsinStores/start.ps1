# Projects in Stores Dashboard - Start Script
# Run this to start your dashboard

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Projects in Stores Dashboard" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.10+" -ForegroundColor Red
    exit 1
}

# Navigate to backend directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location "$scriptPath\backend"

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  No .env file found - using mock data" -ForegroundColor Yellow
    Write-Host "   To use real data: copy .env.example to .env and configure" -ForegroundColor Yellow
    Write-Host ""
}

# Check if dependencies are installed
Write-Host "Checking dependencies..." -ForegroundColor Cyan
$pipList = pip list 2>&1
if ($pipList -match "fastapi" -and $pipList -match "uvicorn") {
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "⚠️  Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Backend Server..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Server will be available at:" -ForegroundColor Green
Write-Host "  🔗 API: http://localhost:8000" -ForegroundColor White
Write-Host "  📚 Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Frontend: Open ../frontend/index.html in browser" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start the server
python main.py
