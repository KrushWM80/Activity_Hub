# Store Meeting Planner - Server Startup
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Store Meeting Planner - Starting Server" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Set-Location -Path (Join-Path $PSScriptRoot "backend")

# Check Python
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "[ERROR] Python not found. Install Python 3.10+." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Install dependencies
Write-Host "[Setup] Checking dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet 2>$null

Write-Host ""
Write-Host "[Server] Starting on http://localhost:8090" -ForegroundColor Green
Write-Host "[Server] Press Ctrl+C to stop." -ForegroundColor Gray
Write-Host ""

python main.py
