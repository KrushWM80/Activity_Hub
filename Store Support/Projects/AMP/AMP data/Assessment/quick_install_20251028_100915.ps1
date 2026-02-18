# AMP BigQuery Trigger System - Quick Install Script (PowerShell)
# Run this script as Administrator to install missing software

Write-Host "🚀 AMP BigQuery Trigger System - Quick Install" -ForegroundColor Green
Write-Host "=" * 50

# Function to check if software is installed
function Test-SoftwareInstalled {
    param([string]$Command)
    try {
        & $Command --version 2>$null
        return $true
    } catch {
        return $false
    }
}

# Install Chocolatey if not present (package manager for Windows)
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "📦 Installing Chocolatey package manager..." -ForegroundColor Yellow
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

# Install Git (includes Git Bash)
if (!(Test-SoftwareInstalled "git")) {
    Write-Host "📥 Installing Git for Windows..." -ForegroundColor Yellow
    choco install git -y
} else {
    Write-Host "✅ Git already installed" -ForegroundColor Green
}

# Install Google Cloud CLI
if (!(Test-SoftwareInstalled "gcloud")) {
    Write-Host "☁️ Installing Google Cloud CLI..." -ForegroundColor Yellow
    choco install gcloudsdk -y
} else {
    Write-Host "✅ Google Cloud CLI already installed" -ForegroundColor Green
}

# Install curl (usually pre-installed on Windows 10+)
if (!(Test-SoftwareInstalled "curl")) {
    Write-Host "🌐 Installing curl..." -ForegroundColor Yellow
    choco install curl -y
} else {
    Write-Host "✅ curl already installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎯 Installation Complete!" -ForegroundColor Green
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Restart your terminal/PowerShell" -ForegroundColor White
Write-Host "2. Run: gcloud auth login" -ForegroundColor White
Write-Host "3. Run: gcloud config set project wmt-assetprotection-prod" -ForegroundColor White
Write-Host "4. Execute the BigQuery SQL scripts" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
