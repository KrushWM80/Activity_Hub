# 🚀 Quick Start - Projects in Stores Dashboard

## 📊 What You're Building

A **live BigQuery dashboard** showing:
- **196 active operational projects** across **4,576 stores**
- **Hierarchical drill-down:** Division → Region → Market → Store
- **Sparky AI:** Search projects by name, get instant insights
- **Real-time filtering** with live count updates
- **CSV export** at any level

## ✅ Step 1: Install Dependencies (30 seconds)

```powershell
cd "c:\Users\krush\Documents\VSCode\Intake Hub\ProjectsinStores\backend"
python -m pip install fastapi uvicorn google-cloud-bigquery python-dotenv
```

## ✅ Step 2: Connect to BigQuery (1 minute)

### Option A: gcloud CLI (Recommended ✨)

```powershell
# Authenticate with Google Cloud
gcloud auth application-default login

# Set project
gcloud config set project wmt-assetprotection-prod

# Done! Dashboard will connect automatically
```

### Option B: Service Account Key

```powershell
# Set environment variable
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\service-account-key.json"
```



### **Easy Method:** Use the start script
```powershell
cd "c:\Users\krush\Documents\VSCode\Intake Hub\ProjectsinStores"
.\start.ps1
```

### **Manual Method:**
```powershell
# Option 1: Use the Batch File (Recommended)
.\START_DASHBOARD.bat

# Option 2: Manual Start
cd "c:\Users\krush\Documents\VSCode\Intake Hub\ProjectsinStores\backend"
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

Browser opens automatically to:
- **http://localhost:8001/** - Main Dashboard (Dev)
- **http://127.0.0.1:8001/** - Main Dashboard (Production/Live)
- **http://localhost:8001/admin.html** - Admin Panel

---

## 🎯 You're Live!

Your dashboard now shows:
- ✅ **196 active projects** from BigQuery
- ✅ **4,576 stores** with project assignments
- ✅ **Sparky AI** for intelligent search
- ✅ **Hierarchical navigation** with drill-down
- ✅ **Live filtering** with count updates
- ✅ **CSV export** at any level

---

## 💬 Using Sparky AI

Click the 💬 button (bottom right) and try:
- **"Sidekick"** - Find all Sidekick projects
- **"GMD"** - Show all GMD projects
- **"How many projects?"** - Get statistics
- **"What divisions?"** - See division breakdown
- **"Help"** - See all Sparky capabilities

---

## 🔧 Quick Troubleshooting

### Backend won't start?
```powershell
python --version  # Need 3.10+
python -m pip install fastapi uvicorn google-cloud-bigquery
```

### Can't connect to BigQuery?
```powershell
# Re-authenticate
gcloud auth application-default login
gcloud config set project wmt-assetprotection-prod
```

### Frontend showing errors?
- Make sure server is running on port 8001
- Open **http://localhost:8001/** (FastAPI serves the frontend)
- Check browser console (F12) for errors

### Can't connect to BigQuery?
```powershell
# Test authentication
gcloud auth list

# Re-authenticate
gcloud auth application-default login
```

### Dashboard shows "Failed to load data"?
- Check server is running: http://localhost:8001/api/health
- Backend auto-uses mock data if BigQuery not connected

---

## 📚 More Help

- **BigQuery Setup:** [BIGQUERY_SETUP.md](BIGQUERY_SETUP.md)
- **Full Guide:** [DEPLOYMENT.md](DEPLOYMENT.md)
- **Architecture:** [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 🎉 Success!

Your Projects in Stores Dashboard is running!

**API Documentation:** http://localhost:8000/docs  
**Dashboard:** Open `frontend/index.html`
