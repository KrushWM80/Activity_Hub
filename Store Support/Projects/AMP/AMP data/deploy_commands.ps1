# AMP BigQuery Deployment - Simple Commands
# Date: October 28, 2025
# Now that PATH is working, here are the deployment commands

Write-Host "🚀 AMP BigQuery Deployment Commands" -ForegroundColor Green
Write-Host "===================================="
Write-Host ""

Write-Host "✅ PATH Setup Complete - All tools working!" -ForegroundColor Green
Write-Host "   Git: $(git --version)"
Write-Host "   Google Cloud SDK: $(gcloud version --format='value(Google Cloud SDK)')"
Write-Host "   BigQuery CLI: $(bq version)"
Write-Host "   Account: $(gcloud config get-value account)"
Write-Host "   Project: $(gcloud config get-value project)"
Write-Host ""

Write-Host "📋 Available Datasets:" -ForegroundColor Yellow
bq ls
Write-Host ""

Write-Host "🎯 DEPLOYMENT COMMANDS:" -ForegroundColor Cyan
Write-Host ""

Write-Host "1. Enable Required APIs:" -ForegroundColor White
Write-Host "   gcloud services enable bigquery.googleapis.com"
Write-Host "   gcloud services enable cloudfunctions.googleapis.com" 
Write-Host "   gcloud services enable cloudscheduler.googleapis.com"
Write-Host ""

Write-Host "2. Deploy BigQuery SQL System:" -ForegroundColor White
Write-Host "   bq query --use_legacy_sql=false < amp_bigquery_enhanced_multisource_system_20251028_080418.sql"
Write-Host ""

Write-Host "3. Test the System:" -ForegroundColor White
Write-Host "   bq query --use_legacy_sql=false 'SELECT * FROM wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Update_Log ORDER BY update_timestamp DESC LIMIT 5'"
Write-Host ""

Write-Host "4. Manual Triggers (after deployment):" -ForegroundColor White
Write-Host "   bq query --use_legacy_sql=false 'CALL wmt-assetprotection-prod.Store_Support_Dev.enhanced_amp_sync_proc()'"
Write-Host ""

Write-Host "🚀 Ready to deploy! Run the commands above in order." -ForegroundColor Green