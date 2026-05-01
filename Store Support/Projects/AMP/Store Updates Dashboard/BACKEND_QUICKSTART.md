# AMP Dashboard with Backend Server - Quick Start

## Overview
The AMP Dashboard now uses a **Python backend server** to securely access BigQuery using your existing `gcloud` credentials. No OAuth2 setup needed!

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies (2 min)

```powershell
cd "Store Support\Projects\AMP\Store Updates Dashboard"
pip install -r requirements.txt
```

### Step 2: Start Backend Server (Terminal 1)

```powershell
cd "Store Support\Projects\AMP\Store Updates Dashboard"
python amp_backend_server.py
```

You should see:
```
🚀 Starting AMP Dashboard Backend on http://localhost:5000
📊 BigQuery: wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2
🔐 Using gcloud application default credentials
📖 API docs: http://localhost:5000/
```

### Step 3: Start Dashboard Server (Terminal 2)

```powershell
cd "Store Support\Projects\AMP\Store Updates Dashboard"
python -m http.server 8080
```

### Step 4: Open Dashboard

Open browser: **http://localhost:8081**

You should see:
- ✅ Green "✅ Connected to BigQuery" status
- 📊 Dashboard with live AMP data (past 90 days)
- 🎯 Working filters
- 📈 Real metrics and data

---

## 🔄 How It Works

```
Browser Dashboard (Port 8080)
    ↓
    ├─ Calls backend API endpoints
    │  (fetch API with CORS enabled)
    ↓
Backend Server (Port 5000)
    ├─ Receives request with filters
    ├─ Uses gcloud credentials
    ├─ Queries BigQuery
    ├─ Returns JSON response
    ↓
Dashboard displays live data
```

---

## 📡 Backend API Endpoints

All endpoints return JSON responses.

### GET /health
Check backend and BigQuery connection status.

**Response:**
```json
{
  "status": "ok",
  "service": "AMP Dashboard Backend",
  "project": "wmt-assetprotection-prod",
  "bigquery_connected": true,
  "timestamp": "2026-02-20T12:00:00"
}
```

### GET /api/amp-data
Fetch AMP data with optional filters.

**Parameters:**
- `division` - Filter by division
- `region` - Filter by region
- `market` - Filter by market
- `facility` - Filter by facility
- `week` - Filter by WM week number
- `activity_type` - Filter by activity type
- `store_area` - Filter by store area
- `keyword` - Search in title/type/area
- `days` - Number of days back (default: 90)
- `limit` - Max results (default: 1000)

**Example:**
```
http://localhost:5000/api/amp-data?division=WEST&days=90&limit=100
```

**Response:**
```json
{
  "success": true,
  "count": 15,
  "data": [
    {
      "week_number": 8,
      "activity_title": "Action Required...",
      "status": "complete",
      "total_count": 4500,
      ...
    }
  ],
  "filters_applied": {...},
  "timestamp": "2026-02-20T12:00:00"
}
```

### GET /api/amp-metrics
Get summary metrics for the data.

**Response:**
```json
{
  "success": true,
  "metrics": {
    "total_activities": 150,
    "completed_activities": 125,
    "in_progress_activities": 15,
    "inform_only_activities": 10,
    "total_store_impact": 45000,
    "completion_rate": 83.33
  }
}
```

### GET /api/amp-filters
Get distinct filter options.

**Response:**
```json
{
  "success": true,
  "filters": {
    "divisions": ["WEST", "NORTH", "NHM", ...],
    "regions": ["1", "2", "3", ...],
    "markets": ["Market 1", "Market 2", ...],
    "facilities": [...],
    "weeks": [8, 7, 6, ...],
    "activity_types": ["Verification", "Inform"],
    "store_areas": ["Pharmacy", "Auto", ...]
  }
}
```

---

## 🆘 Troubleshooting

### "Backend not running" status in dashboard

**Solution:**
1. Make sure backend server is running on Terminal 1
2. Check for error messages in backend terminal
3. Verify no other process is using port 5000

### "Backend running but BigQuery not connected"

**Solution:**
1. Check gcloud credentials are configured:
   ```powershell
   gcloud auth list
   gcloud config list
   ```
2. If not configured, run:
   ```powershell
   gcloud auth login
   gcloud config set project wmt-assetprotection-prod
   gcloud auth application-default login
   ```

### Dashboard shows "Sample Data" instead of live data

**Solutions:**
1. Check backend status indicator (should be green ✅)
2. Check dashboard browser console (F12) for errors
3. Verify backend can reach BigQuery:
   ```powershell
   # In backend terminal, check logs for error messages
   ```

### Port 5000 already in use

**Solution:**
Either:
- Kill process using port 5000: `netstat -ano | findstr :5000`
- Change backend port in `amp_backend_server.py` line ~150

### Certificate/SSL errors

**Solution:**
These are normal in development. The browser sandboxing prevents CORS errors with `CORS` enabled in Flask.

---

## 📊 Testing the API Directly

Use browser or curl to test endpoints:

```powershell
# Health check
Invoke-WebRequest http://localhost:5000/health | ConvertFrom-Json

# Get data
Invoke-WebRequest "http://localhost:5000/api/amp-data?days=90&limit=10" | ConvertFrom-Json

# Get metrics
Invoke-WebRequest http://localhost:5000/api/amp-metrics | ConvertFrom-Json

# Get filters
Invoke-WebRequest http://localhost:5000/api/amp-filters | ConvertFrom-Json
```

---

## 🔐 Security Notes

✅ **What's secure:**
- Credentials stored locally in gcloud (application_default_credentials.json)
- Backend server runs on localhost only (not exposed to internet)
- No API keys in frontend code
- BigQuery requests go through authenticated backend
- CORS restricted to localhost (currently)

⚠️ **For production:**
- Run backend on private network only
- Add authentication between dashboard and backend
- Use HTTPS if exposing to network
- Restrict CORS origins to specific domains
- Implement rate limiting

---

## 📝 Files

- `amp_backend_server.py` - Python Flask backend server
- `amp-data-connector.js` - Updated to call backend instead of BigQuery REST
- `backend-status-checker.js` - Monitors backend connection status
- `requirements.txt` - Python dependencies
- `amp_analysis_dashboard.html` - Updated to remove OAuth2 UI

---

## ✨ Next Steps

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Start backend: `python amp_backend_server.py`
3. ✅ Start dashboard: `python -m http.server 8080`
4. ✅ Open browser: `http://localhost:8081`
5. ✅ Verify data loads and is live
6. ✅ Test filters and metrics
7. ✅ Check console for any errors

---

**Backend implementation complete! Ready to use with your existing gcloud credentials. 🚀**
