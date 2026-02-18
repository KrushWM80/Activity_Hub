# Code Puppy Pages Deployment Checklist

## ✅ Pre-Deployment Status (COMPLETED!)

### Code Complete
- [x] Backend API fully implemented (6 endpoints)
- [x] Frontend dashboard complete (simple.html - 925 lines)
- [x] BigQuery integration working (196 projects, 4,576 stores)
- [x] Sparky AI with intelligent search
- [x] Hierarchical navigation (Division → Region → Market → Store)
- [x] CSV export functionality
- [x] Documentation created and updated
- [x] Local testing successful

### ⚙️ Configuration
- [x] BigQuery authentication configured (gcloud CLI)
- [x] Environment defaults work out of the box
- [x] No `.env` file required (defaults are correct)
- [x] All endpoints tested and functional
- [x] Real data from BigQuery verified

### 🧪 Testing Completed
- [x] Summary stats: 196 projects, 4,576 stores ✅
- [x] All 8 filters work (Division, Phase, Region, Market, Tribe, Store, WM Week, Project Source)
- [x] Sparky AI responds correctly:
  - "Sidekick" → Auto-applies filter (1 match)
  - "GMD" → Shows 5 matching projects
  - "help" → Lists all capabilities
- [x] Hierarchical navigation with breadcrumbs
- [x] CSV export downloads correct data
- [x] Real-time count updates work
- [x] Minimize/maximize Sparky chat works (− and + buttons)

### 🔐 Security Review
- [x] No hardcoded credentials (uses gcloud auth)
- [x] CORS settings configured for localhost
- [ ] **TODO**: Update CORS for production domain
- [x] No `.env` file in repository
- [x] BigQuery read-only access
- [x] No sensitive data logged

---

## 🚀 Deployment Steps for Code Puppy Pages

### Step 1: Deploy Backend to Server

**Requirements:**
- Windows/Linux server with Python 3.10+
- Network access to Google BigQuery
- gcloud CLI installed

**Installation:**
```powershell
# On production server

# 1. Copy backend folder to server
cd "C:\inetpub\projects-in-stores\backend"

# 2. Install dependencies
pip install fastapi uvicorn google-cloud-bigquery

# 3. Authenticate with BigQuery
gcloud auth application-default login

# 4. Update CORS in main.py (line 24) for your domain:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://codepuppy.walmart.com"],  # Update this!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. Start backend (keep running in background)
python main.py

# Backend will run on: http://your-server:8000
```

**Verification:**
```powershell
# Test health endpoint
curl http://your-server:8000/api/health
# Expected: {"status": "healthy", "database": "connected", ...}

# Test summary endpoint
curl http://your-server:8000/api/summary
# Expected: {"total_projects": 196, "total_stores": 4576, ...}
```

---

### Step 2: Configure Frontend for Production

**Update API endpoint in simple.html:**
```javascript
// Line 11 in frontend/simple.html
const API_BASE_URL = 'http://your-backend-server:8000';
// Replace with actual production backend URL
```

**File to upload:** `frontend/simple.html`

---

### Step 3: Deploy to Code Puppy Pages

**Option A: Standalone Page** (Recommended)
1. Upload `frontend/simple.html` to Code Puppy Pages
2. Set page title: **"Projects in Stores"**
3. Access at: `https://codepuppy.walmart.com/your-path/simple.html`

**Option B: Embedded iFrame**
```html
<!-- Add to existing Code Puppy page -->
<iframe 
  src="https://codepuppy.walmart.com/your-path/simple.html" 
  width="100%" 
  height="1200px" 
  frameborder="0"
  style="border: none;">
</iframe>
```

---

### Step 4: Post-Deployment Verification

**Checklist:**
- [ ] Dashboard URL loads correctly
- [ ] Summary shows: **196 projects, 4,576 stores**
- [ ] Project table displays data
- [ ] Sparky AI responds to these queries:
  - [ ] "help" → Shows capabilities list
  - [ ] "Sidekick" → Auto-applies filter (1 project)
  - [ ] "GMD" → Shows 5 matching projects
  - [ ] "How many stores?" → Explains data structure
- [ ] Filters work:
  - [ ] Division (select EAST)
  - [ ] Phase (select Roll/Deploy)
  - [ ] Region, Market, Tribe, Store
- [ ] Hierarchical Navigation:
  - [ ] Click Division button → Shows regions
  - [ ] Click Region button → Shows markets
  - [ ] Click Market button → Shows stores
  - [ ] Breadcrumbs work for navigation back
- [ ] CSV Export:
  - [ ] "Export to CSV" downloads file
  - [ ] CSV contains correct columns
  - [ ] Filtered data exports correctly
- [ ] No console errors (check browser DevTools)
- [ ] Backend stays running (no crashes)

**API Health Checks:**
```powershell
# From production server
curl http://localhost:8000/api/health
curl http://localhost:8000/api/summary
curl http://localhost:8000/api/filters
```

---

## 📊 Current Features in Production

### ✅ Sparky AI Assistant
| Query | Expected Behavior |
|-------|-------------------|
| "Sidekick" | Auto-applies filter (1 unique project) |
| "GMD" | Shows 5 matching projects, asks for clarification |
| "DSD" | Shows all DSD-related projects |
| "How many stores?" | Explains hierarchical navigation |
| "divisions" | Lists all 6 divisions with drill-down instructions |
| "phases" | Shows all phase types with descriptions |
| "help" | Lists all Sparky capabilities |

### ✅ Hierarchical Navigation
- **Division → Region → Market → Store** drill-down
- **Breadcrumb trail** (e.g., EAST / Region 1 / Market 2)
- **Multi-level buttons** (up to 3 per level, sorted by store count)
- **Store counts** at each level
- **CSV export** at any level

### ✅ Advanced Filtering
- **8 filter types**: Project Source, Phase, Division, Region, Market, Tribe, Store, WM Week
- **Real-time updates**: Summary stats update instantly
- **Filter persistence**: Filters stay active during Sparky searches
- **Clear filters**: Reset button available

### ✅ Data Export
- **CSV format**: Project Title, Division, Region, Market, Store, Phase, Tribe
- **Filtered export**: Only exports visible data
- **Navigation export**: Works at any navigation level

---

## 🔧 Troubleshooting

### Dashboard shows "Error loading data"
```powershell
# Check backend health
curl http://your-server:8000/api/health

# If error, check BigQuery authentication
gcloud auth application-default login

# Restart backend
cd backend
python main.py
```

### Sparky AI not responding
- Check browser console for errors
- Verify `/api/ai/query` endpoint: `curl -X POST http://your-server:8000/api/ai/query -H "Content-Type: application/json" -d '{"query":"help","context":{}}'`
- Check backend logs for errors

### Filters not working
- Check browser console for JavaScript errors
- Verify data loaded: Check "Total Projects" shows 196
- Clear browser cache and reload

### CORS errors in browser console
```python
# Update main.py line 24:
allow_origins=["https://codepuppy.walmart.com"]  # Match your domain!
```

### BigQuery connection fails
```powershell
# Re-authenticate
gcloud auth application-default login

# Verify project access
gcloud projects list | grep wmt-assetprotection-prod

# Test query manually
cd backend
python check_status.py
```

---

## 📞 Support

### Documentation Files
- **[README.md](README.md)** - Project overview
- **[QUICKSTART.md](QUICKSTART.md)** - 30-second start guide
- **[START_HERE.md](START_HERE.md)** - Detailed setup
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment instructions
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Complete project summary

### Useful Commands
```powershell
# Check backend status
curl http://localhost:8000/api/health

# View backend logs
# (Check terminal where python main.py is running)

# Restart backend
cd backend
python main.py

# Test BigQuery connection
cd backend
python check_status.py

# Local testing
.\start.ps1
# Open: http://localhost:8082/simple.html
```

---

## ✅ Deployment Complete!

Once all checkboxes above are marked:
1. ✅ Backend deployed and running
2. ✅ Frontend uploaded to Code Puppy Pages
3. ✅ All verification tests pass
4. ✅ No console errors

**Your dashboard is LIVE! 🎉**

Share the URL with your team and enjoy the **196 projects** and **4,576 stores** at your fingertips!
