# REDEPLOY.ps1 - Quick redeploy to Cloud Run
# Usage: .\REDEPLOY.ps1

Write-Host "`nDeploying Distribution List API to Cloud Run..." -ForegroundColor Cyan
Write-Host "Project: wmt-assetprotection-prod" -ForegroundColor Gray
Write-Host "Region: us-central1`n" -ForegroundColor Gray

# Check if api directory exists
if (-not (Test-Path "api")) {
    Write-Host "Error: 'api' directory not found!" -ForegroundColor Red
    Write-Host "Make sure you're in the Distribution_Lists directory" -ForegroundColor Yellow
    exit 1
}

# Navigate to api directory
Push-Location api

# Deploy to Cloud Run
gcloud run deploy distribution-list-api `
  --source . `
  --region us-central1 `
  --allow-unauthenticated `
  --project wmt-assetprotection-prod

Pop-Location

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "Deployment successful!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "`nAPI Base URL:" -ForegroundColor Yellow
    Write-Host "https://distribution-list-api-xxxxx.us-central1.run.app" -ForegroundColor Cyan
    Write-Host "`nTest Endpoints:" -ForegroundColor Yellow
    Write-Host "curl https://distribution-list-api-xxxxx.us-central1.run.app/health" -ForegroundColor Cyan
    Write-Host "curl https://distribution-list-api-xxxxx.us-central1.run.app/status" -ForegroundColor Cyan
    Write-Host "curl 'https://distribution-list-api-xxxxx.us-central1.run.app/api/distribution-lists?limit=5'" -ForegroundColor Cyan
    Write-Host "`nNext Steps:" -ForegroundColor Yellow
    Write-Host "1. Test the endpoints above" -ForegroundColor White
    Write-Host "2. Update index.html with the actual API URL (if needed)" -ForegroundColor White
    Write-Host "3. Hard refresh Code Puppy Page (Ctrl+Shift+R)" -ForegroundColor White
    Write-Host "`n"
} else {
    Write-Host "`n========================================" -ForegroundColor Red
    Write-Host "Deployment failed!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "`nTroubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Check gcloud is installed: gcloud --version" -ForegroundColor White
    Write-Host "2. Verify authentication: gcloud auth list" -ForegroundColor White
    Write-Host "3. Check project: gcloud config get-value project" -ForegroundColor White
    Write-Host "4. View logs: gcloud run services logs read distribution-list-api --limit 50" -ForegroundColor White
    Write-Host "`n"
    exit 1
}
