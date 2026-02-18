# AMP Dashboard Live Data Setup Script
# Sets up BigQuery connection and fetches live data

Write-Host "🚀 AMP Dashboard Live Data Setup" -ForegroundColor Green
Write-Host "=" * 50

# Check Python installation
Write-Host "`n🐍 Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python 3.7+" -ForegroundColor Red
    exit 1
}

# Install BigQuery library
Write-Host "`n📦 Installing Google Cloud BigQuery library..." -ForegroundColor Yellow
try {
    pip install google-cloud-bigquery --quiet
    Write-Host "✅ BigQuery library installed" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Error installing BigQuery library" -ForegroundColor Yellow
    Write-Host "   Continuing anyway..." -ForegroundColor Gray
}

# Authentication setup instructions
Write-Host "`n🔑 AUTHENTICATION SETUP" -ForegroundColor Cyan
Write-Host "Choose one authentication method:" -ForegroundColor White

Write-Host "`n1️⃣ SERVICE ACCOUNT (Recommended)" -ForegroundColor Yellow
Write-Host "   • Download service account JSON from Google Cloud Console" -ForegroundColor Gray
Write-Host "   • Save as 'service-account.json' in current directory" -ForegroundColor Gray
Write-Host "   • File path: $(Get-Location)\service-account.json" -ForegroundColor Gray

Write-Host "`n2️⃣ GCLOUD CLI" -ForegroundColor Yellow
Write-Host "   • Install gcloud CLI: https://cloud.google.com/sdk/docs/install" -ForegroundColor Gray
Write-Host "   • Run: gcloud auth application-default login" -ForegroundColor Gray

Write-Host "`n3️⃣ ENVIRONMENT VARIABLE" -ForegroundColor Yellow
Write-Host "   • Set GOOGLE_APPLICATION_CREDENTIALS to your JSON file path" -ForegroundColor Gray

# Check for existing credentials
$serviceAccountFile = "service-account.json"
$hasServiceAccount = Test-Path $serviceAccountFile

if ($hasServiceAccount) {
    Write-Host "`n✅ Found service account file: $serviceAccountFile" -ForegroundColor Green
} else {
    Write-Host "`n⚠️  No service account file found" -ForegroundColor Yellow
}

# Check for gcloud auth
try {
    $gcloudAuth = gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>$null
    if ($gcloudAuth) {
        Write-Host "✅ Found gcloud authentication: $gcloudAuth" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  Gcloud CLI not found or not authenticated" -ForegroundColor Yellow
}

# Prompt to continue
Write-Host "`n🤔 Ready to fetch live data?" -ForegroundColor White
$continue = Read-Host "Continue? (y/N)"

if ($continue -ne 'y' -and $continue -ne 'Y') {
    Write-Host "👋 Exiting. Run this script again when authentication is set up." -ForegroundColor Gray
    exit 0
}

# Run the data fetcher
Write-Host "`n📊 Fetching live BigQuery data..." -ForegroundColor Green
Write-Host "Table: wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Prep" -ForegroundColor Gray

try {
    python fetch_live_data.py
    
    if (Test-Path "live_amp_data.json") {
        Write-Host "`n🎉 SUCCESS! Live data fetched." -ForegroundColor Green
        Write-Host "📁 File: live_amp_data.json" -ForegroundColor White
        
        # Get file info
        $fileInfo = Get-Item "live_amp_data.json"
        $fileSize = [math]::Round($fileInfo.Length / 1KB, 2)
        Write-Host "📏 Size: $fileSize KB" -ForegroundColor Gray
        Write-Host "📅 Created: $($fileInfo.CreationTime)" -ForegroundColor Gray
        
        Write-Host "`n🌐 Starting dashboard server..." -ForegroundColor Yellow
        
        # Start the server in background
        Start-Process python -ArgumentList "-m http.server 8080" -WindowStyle Hidden
        Start-Sleep 2
        
        Write-Host "✅ Dashboard server started on http://localhost:8080" -ForegroundColor Green
        Write-Host "`n🎯 NEXT STEPS:" -ForegroundColor Cyan
        Write-Host "1. Open: http://localhost:8080" -ForegroundColor White
        Write-Host "2. Click Connect to BigQuery button" -ForegroundColor White
        Write-Host "3. Select the live_amp_data.json file" -ForegroundColor White
        Write-Host "4. Test the preview links!" -ForegroundColor White
        
        # Open browser
        Start-Process "http://localhost:8080"
        
    } else {
        Write-Host "`n❌ Live data fetch failed. Check error messages above." -ForegroundColor Red
        Write-Host "`n🔧 TROUBLESHOOTING:" -ForegroundColor Yellow
        Write-Host "• Verify BigQuery table access permissions" -ForegroundColor Gray
        Write-Host "• Check authentication setup" -ForegroundColor Gray
        Write-Host "• Ensure table exists: wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Prep" -ForegroundColor Gray
    }
    
} catch {
    Write-Host "`n❌ Error running data fetcher: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nPress any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")