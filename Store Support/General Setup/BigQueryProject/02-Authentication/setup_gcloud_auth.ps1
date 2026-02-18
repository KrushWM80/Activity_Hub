# Google Cloud Authentication Setup Script

Write-Host "🔐 Google Cloud Authentication Setup" -ForegroundColor Cyan
Write-Host "=" * 40 -ForegroundColor Cyan

# Verify gcloud is installed
Write-Host "📋 Verifying Google Cloud CLI installation..." -ForegroundColor Yellow

try {
    $gcloudVersion = gcloud --version 2>$null
    Write-Host "✅ Google Cloud CLI found!" -ForegroundColor Green
    Write-Host $gcloudVersion[0] -ForegroundColor Gray
} catch {
    Write-Host "❌ Google Cloud CLI not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install first:" -ForegroundColor Yellow
    Write-Host "1. Run: .\install_gcloud.ps1" -ForegroundColor Yellow
    Write-Host "2. OR download from: https://cloud.google.com/sdk/docs/install-sdk" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "🔐 Step 1: Authenticate with Google Cloud" -ForegroundColor Yellow
Write-Host "This will open your browser for authentication..." -ForegroundColor Gray

try {
    gcloud auth login
    Write-Host "✅ Authentication successful!" -ForegroundColor Green
} catch {
    Write-Host "❌ Authentication failed" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "🎯 Step 2: Set project to wmt-assetprotection-prod" -ForegroundColor Yellow

try {
    gcloud config set project wmt-assetprotection-prod
    Write-Host "✅ Project set successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to set project" -ForegroundColor Red
    Write-Host "You may not have access to wmt-assetprotection-prod" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📊 Step 3: Test BigQuery access" -ForegroundColor Yellow

try {
    Write-Host "Testing BigQuery access..." -ForegroundColor Gray
    $datasets = bq ls 2>$null
    
    if ($datasets) {
        Write-Host "✅ BigQuery access confirmed!" -ForegroundColor Green
        Write-Host "Available datasets:" -ForegroundColor Gray
        Write-Host $datasets -ForegroundColor Gray
    } else {
        Write-Host "⚠️ BigQuery access limited or no datasets visible" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ BigQuery access test failed" -ForegroundColor Red
    Write-Host "You may need BigQuery permissions" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🚀 Step 4: Fetch BigQuery data" -ForegroundColor Yellow

$fetchData = Read-Host "Ready to fetch data from BigQuery? (y/n)"

if ($fetchData -eq "y" -or $fetchData -eq "Y") {
    Write-Host "📊 Fetching data from BigQuery..." -ForegroundColor Yellow
    
    try {
        python connect_bigquery.py
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "🎉 SUCCESS! BigQuery data fetched!" -ForegroundColor Green
            Write-Host ""
            Write-Host "📋 Next steps:" -ForegroundColor Cyan
            Write-Host "1. Start your dashboard server: python -m http.server 8080" -ForegroundColor Yellow
            Write-Host "2. Open: http://localhost:8080/Store%20Updates%20Dashboard/" -ForegroundColor Yellow
            Write-Host "3. Look for 'REAL BigQuery Data Connected!' status" -ForegroundColor Yellow
            Write-Host "4. Test the preview links - they should all work!" -ForegroundColor Yellow
            
            $startServer = Read-Host "Start dashboard server now? (y/n)"
            if ($startServer -eq "y" -or $startServer -eq "Y") {
                Write-Host "🚀 Starting dashboard server..." -ForegroundColor Cyan
                python -m http.server 8080
            }
        } else {
            Write-Host "❌ Failed to fetch BigQuery data" -ForegroundColor Red
            Write-Host "Check the error messages above" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "❌ Error running connect_bigquery.py" -ForegroundColor Red
    }
} else {
    Write-Host ""
    Write-Host "✅ Setup complete!" -ForegroundColor Green
    Write-Host "Run 'python connect_bigquery.py' when ready to fetch data" -ForegroundColor Yellow
}

Read-Host "Press Enter to exit"