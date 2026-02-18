# Email Reporting Installation Script
# Run this to install all required dependencies for the email reporting system

Write-Host "================================================" -ForegroundColor Cyan
Write-Host " Email Reporting System - Installation" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the correct directory
if (-not (Test-Path "backend\requirements.txt")) {
    Write-Host "Error: Please run this script from the ProjectsinStores root directory" -ForegroundColor Red
    exit 1
}

Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
Write-Host ""

# Navigate to backend directory
Push-Location backend

# Install dependencies
Write-Host "Installing core dependencies from requirements.txt..." -ForegroundColor Green
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Error: Failed to install dependencies" -ForegroundColor Red
    Pop-Location
    exit 1
}

Write-Host ""
Write-Host "✓ Core dependencies installed" -ForegroundColor Green

# Verify critical packages for email reporting
Write-Host ""
Write-Host "Verifying email reporting packages..." -ForegroundColor Yellow

$packages = @("apscheduler", "reportlab", "email-validator")
$allInstalled = $true

foreach ($package in $packages) {
    $check = pip show $package 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ $package installed" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $package NOT installed" -ForegroundColor Red
        $allInstalled = $false
    }
}

Pop-Location

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan

if ($allInstalled) {
    Write-Host " Installation Complete! " -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Next Steps:" -ForegroundColor Yellow
    Write-Host "  1. Configure SMTP settings in backend\.env (optional)" -ForegroundColor White
    Write-Host "  2. Start the backend: cd backend && python main.py" -ForegroundColor White
    Write-Host "  3. Open reports interface: http://localhost:8001/reports.html" -ForegroundColor White
    Write-Host ""
    Write-Host "Documentation:" -ForegroundColor Yellow
    Write-Host "  - Quick Start: EMAIL_REPORTING_QUICKSTART.md" -ForegroundColor White
    Write-Host "  - Full Guide: EMAIL_REPORTING_GUIDE.md" -ForegroundColor White
    Write-Host "  - Implementation: IMPLEMENTATION_SUMMARY.md" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host " Installation Issues Detected " -ForegroundColor Red
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Some packages failed to install. Try:" -ForegroundColor Yellow
    Write-Host "  1. Upgrade pip: python -m pip install --upgrade pip" -ForegroundColor White
    Write-Host "  2. Install manually: pip install apscheduler reportlab email-validator" -ForegroundColor White
    Write-Host "  3. Check Python version (3.8+ required)" -ForegroundColor White
    Write-Host ""
}

Write-Host "For support, check the documentation or contact the development team." -ForegroundColor Cyan
Write-Host ""
