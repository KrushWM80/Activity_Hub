#!/bin/bash
# REDEPLOY.sh - Quick redeploy to Cloud Run
# Usage: ./REDEPLOY.sh

echo ""
echo "Deploying Distribution List API to Cloud Run..."
echo "Project: wmt-assetprotection-prod"
echo "Region: us-central1"
echo ""

# Check if api directory exists
if [ ! -d "api" ]; then
    echo "Error: 'api' directory not found!"
    echo "Make sure you're in the Distribution_Lists directory"
    exit 1
fi

# Navigate to api directory
cd api

# Deploy to Cloud Run
gcloud run deploy distribution-list-api \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --project wmt-assetprotection-prod

cd ..

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "Deployment successful!"
    echo "========================================"
    echo ""
    echo "API Base URL:"
    echo "https://distribution-list-api-xxxxx.us-central1.run.app"
    echo ""
    echo "Test Endpoints:"
    echo "curl https://distribution-list-api-xxxxx.us-central1.run.app/health"
    echo "curl https://distribution-list-api-xxxxx.us-central1.run.app/status"
    echo "curl 'https://distribution-list-api-xxxxx.us-central1.run.app/api/distribution-lists?limit=5'"
    echo ""
    echo "Next Steps:"
    echo "1. Test the endpoints above"
    echo "2. Update index.html with the actual API URL (if needed)"
    echo "3. Hard refresh Code Puppy Page (Ctrl+Shift+R)"
    echo ""
else
    echo ""
    echo "========================================"
    echo "Deployment failed!"
    echo "========================================"
    echo ""
    echo "Troubleshooting:"
    echo "1. Check gcloud is installed: gcloud --version"
    echo "2. Verify authentication: gcloud auth list"
    echo "3. Check project: gcloud config get-value project"
    echo "4. View logs: gcloud run services logs read distribution-list-api --limit 50"
    echo ""
    exit 1
fi
