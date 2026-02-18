# AMP BigQuery Trigger System - Installation Guide

**Generated:** 2025-10-28 10:09:15  
**System:** win32

## 🚨 Required Actions

### Essential Software Missing:

#### Google Cloud CLI (gcloud)
- **Status**: ❌ Not Installed
- **Description**: Essential for BigQuery operations and Cloud Function deployment
- **Install From**: https://cloud.google.com/sdk/docs/install
- **Action Required**: Download and install before proceeding

#### Git
- **Status**: ❌ Not Installed
- **Description**: Version control and includes Git Bash terminal
- **Install From**: https://git-scm.com/download/windows
- **Action Required**: Download and install before proceeding

### Python Packages Missing:
```bash
pip install google-cloud-bigquery google-cloud-functions-framework google-auth pandas requests
```

## 🔧 Environment Setup Steps

### 1. Google Cloud CLI Setup
```bash
# After installing gcloud, authenticate
gcloud auth login

# Set your project
gcloud config set project wmt-assetprotection-prod

# Enable required APIs
gcloud services enable bigquery.googleapis.com
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudscheduler.googleapis.com
gcloud services enable pubsub.googleapis.com
```

### 2. BigQuery Authentication
```bash
# Create and download service account key
gcloud iam service-accounts create bigquery-data-sync --display-name="BigQuery Data Sync"

# Grant necessary permissions
gcloud projects add-iam-policy-binding wmt-assetprotection-prod     --member="serviceAccount:bigquery-data-sync@wmt-assetprotection-prod.iam.gserviceaccount.com"     --role="roles/bigquery.dataEditor"

gcloud projects add-iam-policy-binding wmt-assetprotection-prod     --member="serviceAccount:bigquery-data-sync@wmt-assetprotection-prod.iam.gserviceaccount.com"     --role="roles/bigquery.jobUser"

# Download key
gcloud iam service-accounts keys create key.json     --iam-account=bigquery-data-sync@wmt-assetprotection-prod.iam.gserviceaccount.com

# Set environment variable
set GOOGLE_APPLICATION_CREDENTIALS=key.json
```

### 3. Test Your Setup
```bash
# Test BigQuery access
bq ls wmt-assetprotection-prod:Store_Support

# Test Cloud Functions access  
gcloud functions list --project=wmt-assetprotection-prod
```

## 📥 Download Links

### Essential Downloads:
- **Google Cloud CLI (gcloud)**: https://cloud.google.com/sdk/docs/install
- **Git**: https://git-scm.com/download/windows

### Recommended Downloads:
- **Git for Windows**: https://git-scm.com/download/windows (includes Git Bash)
- **Google Cloud CLI**: https://cloud.google.com/sdk/docs/install-sdk

## 🚀 Deployment Checklist

After installing missing software:

1. ✅ Run BigQuery SQL to create tables and procedures
2. ✅ Set up Google Cloud authentication  
3. ✅ Deploy Cloud Functions using the deployment script
4. ✅ Test the trigger system
5. ✅ Set up monitoring

## 🆘 Troubleshooting

### Common Issues:
- **"gcloud not found"**: Add Google Cloud CLI to your PATH
- **Authentication errors**: Run `gcloud auth login` 
- **Permission denied**: Check service account permissions
- **BigQuery access denied**: Verify project and dataset permissions

### Get Help:
- Google Cloud Documentation: https://cloud.google.com/docs
- BigQuery Documentation: https://cloud.google.com/bigquery/docs
