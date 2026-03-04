# TDA Insights Dashboard - BigQuery Setup Guide

## Quick Setup (5 minutes)

### Option 1: Using gcloud CLI (Recommended)

1. Install Google Cloud SDK:
   - Download from: https://cloud.google.com/sdk/docs/install
   - Or run the installer from: Store Support/General Setup/BigQueryProject/02-Authentication/install_gcloud.ps1

2. Authenticate with Google Cloud:
   \\\powershell
   gcloud auth login
   gcloud config set project wmt-assetprotection-prod
   gcloud auth application-default login
   \\\

3. Install Python dependencies:
   \\\powershell
   cd \"Store Support/Projects/TDA Insights\"
   pip install -r requirements.txt
   \\\

4. Create .env file (already created):
   - File: .env
   - Leave GOOGLE_APPLICATION_CREDENTIALS empty (uses gcloud)

5. Run the backend:
   \\\powershell
   python backend_simple.py
   \\\

6. Open dashboard:
   - http://localhost:5000/dashboard.html

---

### Option 2: Using Service Account JSON

1. Get service account JSON file from your GCP admin

2. Save the file to: Store Support/Projects/TDA Insights/service-account-key.json

3. Set environment variable in PowerShell:
   \\\powershell
   \=\"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\TDA Insights\service-account-key.json\"
   \\\

4. Or edit .env file:
   \\\
   GOOGLE_APPLICATION_CREDENTIALS=service-account-key.json
   \\\

5. Install dependencies and run:
   \\\powershell
   pip install -r requirements.txt
   python backend_simple.py
   \\\

---

## Troubleshooting

### \"gcloud: command not found\"
- Install Google Cloud SDK from: https://cloud.google.com/sdk/docs/install
- Restart PowerShell after installation

### \"GOOGLE_APPLICATION_CREDENTIALS not found\"
- Verify file path is correct
- Use absolute path, not relative path
- Check file exists: \Test-Path <path>\

### \"Could not initialize BigQuery client\"
- Run: \gcloud auth application-default login\
- Or set GOOGLE_APPLICATION_CREDENTIALS to valid JSON file

### Still using sample data?
- Check startup message: \"Data Source: Sample Data\" means BigQuery failed
- Review error messages in console
- Check GCP project has BigQuery API enabled

---

## Next Steps

Once authentication is working:
1. Dashboard should show \"Data Source: BigQuery (wmt-assetprotection-prod)\"
2. Should load 50+ projects instead of 5 sample projects
3. Phase filters will work with real data
4. PPT generation will include real project information

---

## Project Details

- **BigQuery Project**: wmt-assetprotection-prod
- **Dataset**: Store_Support_Dev
- **Table**: Output_TDA Report
- **Required Columns**: Initiative - Project Title, Health Status, Phase, # of Stores, Intake & Testing, Dallas POC, Deployment

---
