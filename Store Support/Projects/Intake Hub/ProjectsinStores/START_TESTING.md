# 🎯 Ready to Test with Real Data!

## Current Status: ✅ All Systems Ready

### What We've Accomplished
- ✅ Complete dashboard built (backend + frontend)
- ✅ BigQuery connection configured and working
- ✅ Authentication successful (gcloud CLI)
- ✅ Schema mapping updated for real table structure
- ✅ API endpoints tested and functional

### Real Data Connection
- **Project**: wmt-assetprotection-prod
- **Dataset**: Store_Support_Dev
- **Table**: IH_Intake_Data
- **Total Rows**: 4,535,103
- **Active Projects**: 207

---

## 🚀 How to Test Locally (2 Simple Steps)

### Step 1: Start the Backend
Open a **new PowerShell terminal** and run:

```powershell
cd "c:\Users\krush\Documents\VSCode\Intake Hub\ProjectsinStores\backend"
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

**Important**: Keep this terminal open! The server must stay running.

You should see:
```
✅ BigQuery client initialized successfully
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### Step 2: Open the Test Page
Double-click this file:
```
c:\Users\krush\Documents\VSCode\Intake Hub\ProjectsinStores\test_dashboard.html
```

This page will:
- ✅ Test your backend connection
- ✅ Show you real data from BigQuery  
- ✅ Provide links to the dashboard and API docs

---

## 📊 What to Verify

### Backend Tests
1. **Health Check**: Should show "healthy" status with "connected" database
2. **Summary Data**: Should show 207 active projects (real data, not mock!)
3. **Projects List**: Should return actual projects from BigQuery
4. **Filter Options**: Should show real divisions, regions, markets from data

### Frontend Dashboard
Open `frontend/index.html` in your browser and verify:
- Summary cards show real numbers
- Filters populate with actual data
- Charts display real project information
- Project table shows current projects
- No "mock data" indicators

---

## 🔧 Quick Commands

### Test API Endpoints
```powershell
# Health check
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/health" | Select-Object -ExpandProperty Content

# Get summary
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/summary?status=Active" | Select-Object -ExpandProperty Content

# Get projects
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/projects?status=Active" | Select-Object -ExpandProperty Content
```

### View API Documentation
Open in browser while server is running:
```
http://127.0.0.1:8000/docs
```

---

## 🎨 Files Ready for Testing

### Core Application
- `backend/main.py` - FastAPI server with 6 REST endpoints
- `backend/database.py` - BigQuery integration (updated for real schema)
- `frontend/index.html` - Complete React dashboard (single file)

### Configuration
- `backend/.env` - BigQuery credentials configured
- Schema mapping updated:
  - `Intake_Card` → project_id
  - `Project_Source` → project_source
  - `Title` → title
  - `Division`, `Region`, `Market`, `Phase` → filters
  - `Facility` → store number

### Testing Tools
- `test_dashboard.html` - Interactive test page
- `backend/test_bigquery.py` - Direct BigQuery test
- `backend/check_schema.py` - Schema inspection tool

### Documentation
- `TESTING_LOCALLY.md` - Detailed local testing guide
- `README.md` - Project overview
- `QUICKSTART.md` - Quick start guide
- `DEPLOYMENT.md` - Code Puppy deployment instructions
- `CODE_PUPPY_CHECKLIST.md` - Deployment checklist

---

## ⚠️ Troubleshooting

### "Cannot connect to backend"
- Make sure you started the backend server (Step 1)
- Check that the terminal window is still open
- Verify you see "Uvicorn running on http://127.0.0.1:8000"

### "Authentication error"
Run this command and follow the browser login:
```powershell
gcloud auth application-default login
```

### "No data showing" or "Mock data"
1. Check backend terminal for errors
2. Test the health endpoint (should show "connected")
3. Verify `.env` file has correct BigQuery settings

---

## 📍 Where You Are Now

You're at the **local testing phase**. Here's what's next:

### Current Phase: Local Testing 🧪
- [ ] Start backend server
- [ ] Test API endpoints
- [ ] Verify real data is loading
- [ ] Check dashboard displays correctly
- [ ] Test all filters and charts

### Next Phase: Code Puppy Deployment 🚀
Once local testing confirms everything works:
1. Review `CODE_PUPPY_CHECKLIST.md`
2. Follow `DEPLOYMENT.md` instructions
3. Deploy to Code Puppy Pages
4. Configure production environment

---

## 💡 Pro Tips

1. **Keep the terminal open**: The backend must run continuously while testing

2. **Use test_dashboard.html**: This is the easiest way to verify everything works

3. **Check the logs**: The backend terminal shows all requests and any errors

4. **Use Swagger UI**: http://127.0.0.1:8000/docs lets you test endpoints interactively

5. **Browser console**: Press F12 to see any frontend errors

---

## 📞 Need Help?

### Common Issues Solved
- **Port 8000 in use**: Change to 8001 in the uvicorn command and frontend API_BASE_URL
- **Slow queries**: Normal for large BigQuery tables, first query may take 5-10 seconds
- **Schema errors**: We've mapped the actual schema (Project_Source, Intake_Card, etc.)

### Files to Check
- `backend/.env` - BigQuery configuration
- `frontend/index.html` line 583 - API_BASE_URL setting
- `backend/database.py` - Schema mapping and queries

---

## ✅ Success Criteria

You'll know it's working when:
- ✅ Backend starts with "✅ BigQuery client initialized successfully"
- ✅ test_dashboard.html shows green "✅ Backend is running!"
- ✅ Summary shows "207 active projects" (real data)
- ✅ Dashboard displays real project information
- ✅ Filters populate with actual divisions, regions, markets
- ✅ No errors in browser console or backend logs

---

## 🎉 Ready to Go!

Everything is configured and ready. Just follow Steps 1 and 2 above to start testing with your real BigQuery data!

**Questions?** Check TESTING_LOCALLY.md for more detailed instructions.

**Ready to deploy?** See CODE_PUPPY_CHECKLIST.md when testing is complete.
