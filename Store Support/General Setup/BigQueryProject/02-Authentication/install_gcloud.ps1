# Google Cloud CLI Installation and Setup Script

Write-Host "🔗 Google Cloud CLI Setup for BigQuery Access" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

# Check if gcloud is already installed
Write-Host "📋 Checking for existing Google Cloud CLI installation..." -ForegroundColor Yellow

try {
    $gcloudVersion = gcloud --version 2>$null
    if ($gcloudVersion) {
        Write-Host "✅ Google Cloud CLI is already installed!" -ForegroundColor Green
        Write-Host $gcloudVersion -ForegroundColor Gray
        
        $skipInstall = Read-Host "Skip installation and proceed to setup? (y/n)"
        if ($skipInstall -eq "y" -or $skipInstall -eq "Y") {
            # Jump to setup
            & "$PSScriptRoot\setup_gcloud_auth.ps1"
            exit 0
        }
    }
} catch {
    Write-Host "❌ Google Cloud CLI not found" -ForegroundColor Red
}

Write-Host ""
Write-Host "📥 Installing Google Cloud CLI..." -ForegroundColor Yellow
Write-Host ""

# Check if installer already exists
$installerPath = "GoogleCloudSDKInstaller.exe"

if (-not (Test-Path $installerPath)) {
    Write-Host "⬇️ Downloading Google Cloud CLI installer..." -ForegroundColor Yellow
    
    try {
        $downloadUrl = "https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe"
        Invoke-WebRequest -Uri $downloadUrl -OutFile $installerPath -UseBasicParsing
        Write-Host "✅ Download completed!" -ForegroundColor Green
    } catch {
        Write-Host "❌ Download failed. Please download manually from:" -ForegroundColor Red
        Write-Host "   https://cloud.google.com/sdk/docs/install-sdk" -ForegroundColor Yellow
        Write-Host "   Save as: GoogleCloudSDKInstaller.exe" -ForegroundColor Yellow
        Read-Host "Press Enter when you have downloaded the installer"
        
        if (-not (Test-Path $installerPath)) {
            Write-Host "❌ Installer not found. Exiting." -ForegroundColor Red
            exit 1
        }
    }
}

Write-Host ""
Write-Host "🚀 Running Google Cloud CLI installer..." -ForegroundColor Yellow
Write-Host "   Please follow the installer prompts" -ForegroundColor Gray
Write-Host "   Choose 'Install for all users' if prompted" -ForegroundColor Gray

try {
    Start-Process -FilePath $installerPath -Wait
    Write-Host "✅ Installation completed!" -ForegroundColor Green
} catch {
    Write-Host "❌ Installation failed" -ForegroundColor Red
    Write-Host "Please run GoogleCloudSDKInstaller.exe manually" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "🔄 Please close and reopen PowerShell to refresh PATH" -ForegroundColor Yellow
Write-Host "Then run: .\setup_gcloud_auth.ps1" -ForegroundColor Cyan

Read-Host "Press Enter to exit"