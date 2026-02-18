# Direct BigQuery Connection Script
# Connects directly to wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Prep

Write-Host "🔗 AMP Dashboard - Direct BigQuery Connection" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

# Check if Google Cloud CLI is installed
try {
    $gcloudVersion = gcloud --version 2>$null
    Write-Host "✅ Google Cloud CLI found" -ForegroundColor Green
} catch {
    Write-Host "❌ Google Cloud CLI not found" -ForegroundColor Red
    Write-Host ""
    Write-Host "📋 Install Google Cloud CLI:" -ForegroundColor Yellow
    Write-Host "1. Go to: https://cloud.google.com/sdk/docs/install"
    Write-Host "2. Download and install gcloud CLI"
    Write-Host "3. Run this script again"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "🚀 Starting BigQuery connection..." -ForegroundColor Yellow

# Run the Python connection script
python connect_bigquery.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "🎉 BigQuery connection successful!" -ForegroundColor Green
    Write-Host ""
    
    # Ask if user wants to start dashboard
    $startDashboard = Read-Host "Start dashboard server? (y/n)"
    
    if ($startDashboard -eq "y" -or $startDashboard -eq "Y") {
        Write-Host "🚀 Starting dashboard on http://localhost:8080" -ForegroundColor Cyan
        Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
        Write-Host ""
        
        # Start the dashboard server
        python -m http.server 8080
    } else {
        Write-Host ""
        Write-Host "✅ BigQuery data is ready!" -ForegroundColor Green
        Write-Host "📋 To start dashboard: python -m http.server 8080" -ForegroundColor Yellow
        Write-Host "🌐 Then visit: http://localhost:8080/Store%20Updates%20Dashboard/" -ForegroundColor Yellow
    }
} else {
    Write-Host ""
    Write-Host "❌ BigQuery connection failed" -ForegroundColor Red
    Write-Host "See error messages above for troubleshooting" -ForegroundColor Yellow
}

Read-Host "Press Enter to exit"