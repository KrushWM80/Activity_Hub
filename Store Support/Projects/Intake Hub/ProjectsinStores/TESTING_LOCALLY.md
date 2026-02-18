# Testing with Real Data Locally

## Quick Start

### 1. Start the Backend Server

Open a terminal and run:

```powershell
cd "c:\Users\krush\Documents\VSCode\Intake Hub\ProjectsinStores\backend"
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

**Keep this terminal window open!** The server needs to stay running.

You should see:
```
✅ BigQuery client initialized successfully
   Project: wmt-assetprotection-prod
   Dataset: Store_Support_Dev
   Table: IH_Intake_Data
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### 2. Open the Dashboard

Open your web browser and go to:
```
file:///c:/Users/krush/Documents/VSCode/Intake Hub/ProjectsinStores/frontend/index.html
```

Or simply open the file `frontend/index.html` in your browser.

### 3. Test the API

While the server is running, you can test the API endpoints:

#### Test Health Endpoint
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/health" | Select-Object -ExpandProperty Content
```

Expected response:
```json
{"status":"healthy","timestamp":"2026-01-06T10:49:28.830803","database":"connected"}
```

#### Test Summary Endpoint
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/summary?status=Active" | Select-Object -ExpandProperty Content
```

#### Test Projects Endpoint
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/projects?status=Active" | Select-Object -ExpandProperty Content
```

### 4. View API Documentation

Open this URL in your browser while the server is running:
```
http://127.0.0.1:8000/docs
```

This will show the interactive Swagger UI documentation where you can test all API endpoints.

## What to Verify

### ✅ Backend Checklist
- [ ] Server starts without errors
- [ ] BigQuery connection shows "✅ connected"
- [ ] Health endpoint returns status "healthy"
- [ ] Summary endpoint returns real data (not mock data)
- [ ] Projects endpoint returns actual projects from BigQuery

### ✅ Frontend Checklist
- [ ] Dashboard loads without errors
- [ ] Summary statistics show real numbers (207 active projects)
- [ ] Filters populate with real options from BigQuery
- [ ] Charts display real data
- [ ] Project table shows actual projects
- [ ] AI assistant responds to queries

## Troubleshooting

### Server Won't Start
If you get authentication errors:
```powershell
gcloud auth application-default login
```

### Can't Connect to BigQuery
Check your `.env` file has:
```
GCP_PROJECT_ID=wmt-assetprotection-prod
BIGQUERY_DATASET=Store_Support_Dev
BIGQUERY_TABLE=IH_Intake_Data
```

### Dashboard Shows Mock Data
Make sure:
1. Backend server is running (check http://127.0.0.1:8000/api/health)
2. Frontend API_BASE_URL points to http://127.0.0.1:8000

## Current Status

### ✅ Completed
- BigQuery connection working
- API endpoints functional
- Real data mapping complete
- Dashboard UI ready

### 📊 Real Data Stats
- **Total Rows**: 4,535,103
- **Active Projects**: 207
- **Table**: wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data

## Next Steps

Once local testing confirms everything works:
1. Review CODE_PUPPY_CHECKLIST.md
2. Follow DEPLOYMENT.md for Code Puppy Pages deployment
3. Configure production environment variables
