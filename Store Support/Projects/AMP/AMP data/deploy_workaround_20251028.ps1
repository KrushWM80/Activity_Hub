# AMP BigQuery Deployment Script - Network/PATH Workaround
# Date: October 28, 2025
# Purpose: Deploy BigQuery trigger system despite network and PATH restrictions

Write-Host "🚀 AMP BigQuery Deployment - Workaround Mode" -ForegroundColor Green
Write-Host "=============================================="

# Define tool paths
$gcloud = "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"
$bq = "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\bq.cmd"

Write-Host "📋 Current Configuration:"
Write-Host "   Project: wmt-assetprotection-prod"
Write-Host "   Account: kendall.rush@walmart.com"
Write-Host "   gcloud: $gcloud"
Write-Host "   bq: $bq"
Write-Host ""

# Test connectivity
Write-Host "🔍 Testing Google Cloud connectivity..."
try {
    $authResult = & $gcloud auth list 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ gcloud authentication: WORKING" -ForegroundColor Green
    } else {
        Write-Host "❌ gcloud authentication: FAILED" -ForegroundColor Red
        Write-Host $authResult
    }
} catch {
    Write-Host "❌ gcloud not accessible: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎯 DEPLOYMENT OPTIONS AVAILABLE:"
Write-Host ""

Write-Host "Option 1: Deploy SQL via Google Cloud Console" -ForegroundColor Yellow
Write-Host "   1. Open https://console.cloud.google.com/bigquery"
Write-Host "   2. Select project: wmt-assetprotection-prod"
Write-Host "   3. Copy and paste SQL from: amp_bigquery_enhanced_multisource_system_20251028_080418.sql"
Write-Host "   4. Execute the queries one by one"
Write-Host ""

Write-Host "Option 2: Deploy via REST API (if network allows)" -ForegroundColor Yellow
Write-Host "   Use PowerShell Invoke-RestMethod to call BigQuery API directly"
Write-Host ""

Write-Host "Option 3: Copy Files to Cloud Shell" -ForegroundColor Yellow
Write-Host "   1. Open https://console.cloud.google.com"
Write-Host "   2. Click Cloud Shell icon (>_)"
Write-Host "   3. Upload files: amp_bigquery_enhanced_multisource_system_20251028_080418.sql"
Write-Host "   4. Run: bq query --use_legacy_sql=false < amp_bigquery_enhanced_multisource_system_20251028_080418.sql"
Write-Host ""

Write-Host "🔧 MANUAL SETUP COMMANDS:"
Write-Host ""
Write-Host "If you can get network access, run these commands:" -ForegroundColor Cyan
Write-Host ""
Write-Host "# Enable required APIs"
Write-Host "& `$gcloud services enable bigquery.googleapis.com"
Write-Host "& `$gcloud services enable cloudfunctions.googleapis.com"
Write-Host "& `$gcloud services enable cloudscheduler.googleapis.com"
Write-Host ""
Write-Host "# Deploy BigQuery SQL"
Write-Host "& `$bq query --use_legacy_sql=false < amp_bigquery_enhanced_multisource_system_20251028_080418.sql"
Write-Host ""
Write-Host "# Deploy Cloud Function"
Write-Host "& `$gcloud functions deploy enhanced-amp-sync-trigger-http --source=. --entry-point=enhanced_amp_sync_trigger_http --runtime=python39 --trigger=http"
Write-Host ""

Write-Host "📄 SQL FILE TO DEPLOY:"
Write-Host "   File: amp_bigquery_enhanced_multisource_system_20251028_080418.sql"
Write-Host "   Size: $(if (Test-Path 'amp_bigquery_enhanced_multisource_system_20251028_080418.sql') { (Get-Item 'amp_bigquery_enhanced_multisource_system_20251028_080418.sql').Length } else { 'File not found' }) bytes"
Write-Host ""

Write-Host "🎉 READY FOR DEPLOYMENT!" -ForegroundColor Green
Write-Host "Choose the deployment option that works best in your corporate environment."