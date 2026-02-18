# Projects in Stores Dashboard - Deployment Guide

## 🚀 Quick Deployment to Code Puppy Pages

Your **Projects in Stores Dashboard** is production-ready and can be deployed today!

### Current Status
- ✅ **196 active projects** from BigQuery
- ✅ **4,576 unique stores** with project assignments
- ✅ **Sparky AI** with intelligent project search
- ✅ **Hierarchical navigation** (Division → Region → Market → Store)
- ✅ **Real-time filtering** with instant count updates
- ✅ **CSV export** at any navigation level
- ✅ **No build process** required (vanilla HTML/CSS/JS)

### Prerequisites
- Python 3.10+ server for backend
- gcloud CLI for BigQuery authentication
- Access to `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data` table

### Step 1: Install Dependencies

```powershell
cd backend
pip install fastapi uvicorn google-cloud-bigquery
```

### Step 2: Authenticate with BigQuery

```powershell
gcloud auth application-default login
```

### Step 3: Start Backend Server

**Option A: Using start.ps1** (Recommended)
```powershell
cd "c:\Users\krush\Documents\VSCode\Intake Hub\ProjectsinStores"
.\start.ps1
```

**Option B: Manual Start**
```powershell
# Terminal 1 - Backend
cd backend
python main.py

# Terminal 2 - Frontend (new PowerShell window)
cd frontend
python -m http.server 8082
```

The API will be at: `http://localhost:8000`
The dashboard will be at: `http://localhost:8082/simple.html`

### Step 4: Verify Dashboard

Open `http://localhost:8082/simple.html` and verify:
- ✅ Summary shows 196 projects, 4,576 stores
- ✅ Project table displays data
- ✅ Filters work (Division, Phase, etc.)
- ✅ Sparky AI responds to "help" command
- ✅ Hierarchical navigation buttons appear
- ✅ CSV export works

## 📊 Dashboard Features

### 1. **Live BigQuery Data**
- 196 active operational projects
- 4,576 stores with project assignments
- Real-time connection to BigQuery
- Project_Source = 'Operations' (all current data)

### 2. **Sparky AI Assistant**
- **Project search**: "Sidekick", "GMD", "DSD"
- **Data analysis**: "How many stores?", "divisions", "phases"
- **Auto-filtering**: When exactly 1 project matches
- **Multi-match handling**: Shows list when multiple projects found
- **Help command**: Type "help" for capabilities
- **Minimize/maximize**: − and + buttons

### 3. **Hierarchical Navigation**
- Division → Region → Market → Store drill-down
- Breadcrumb trail for easy backtracking
- Multi-level buttons (up to 3 per level)
- Store counts at each level
- CSV export at any level

### 4. **Advanced Filtering**
- Project Source (Operations)
- Phase (Roll/Deploy, Test, Mkt Scale, etc.)
- Division (EAST, WEST, NORTH, SOUTH, CENTRAL, NATIONAL)
- Region (1-22)
- Market (1-8 per region)
- Tribe (1-21)
- Store (individual store numbers)
- WM Week (Walmart calendar weeks)

**Real-time count updates**: Summary stats update instantly as you filter!

## 🔧 API Endpoints

### Health Check
```
GET /api/health
```
Returns backend health and BigQuery connection status.

### Get Projects
```
GET /api/projects?division=EAST&phase=Roll/Deploy
```
Returns all projects matching filter criteria (no status parameter needed).

### Get Summary Statistics
```
GET /api/summary
```
Returns: 196 projects, 4,576 stores, project distribution by division and phase.

### Get Filter Options
```
GET /api/filters
```
Returns all available: divisions, regions, markets, phases, tribes, stores, WM weeks, project sources.

### Get Store Counts
```
GET /api/store-counts?dimension=region&division=EAST
```
For hierarchical navigation: get counts by dimension (region, market, store).

### Sparky AI Query
```
POST /api/ai/query
Body: {
  "query": "Sidekick",
  "context": {}
}
```
Returns intelligent response with project search, auto-apply if 1 match, or list if multiple.

## 📦 Code Puppy Pages Deployment

### Recommended: Single Backend + Static Frontend

**Backend Deployment:**
1. Deploy `backend/` folder to a Python 3.10+ server
2. Install dependencies: `pip install fastapi uvicorn google-cloud-bigquery`
3. Authenticate: `gcloud auth application-default login`
4. Start server: `python main.py` (runs on port 8000)
5. Update CORS in `main.py` if needed:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://codepuppy.walmart.com"],  # Update this
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

**Frontend Deployment:**
1. Upload `frontend/simple.html` to Code Puppy Pages
2. Update `API_BASE_URL` in simple.html (line ~11):
   ```javascript
   const API_BASE_URL = 'http://your-backend-server:8000';
   ```
3. Access dashboard at: `https://codepuppy.walmart.com/your-path/simple.html`

### Alternative: Embedded Dashboard

For embedding in existing Code Puppy pages:

```html
<iframe 
  src="https://your-dashboard-url/simple.html" 
  width="100%" 
  height="1200px" 
  frameborder="0"
  style="border: none;">
</iframe>
```

## 🔐 Production Configuration

### Environment Variables (Optional)
Create `backend/.env` if you need to override defaults:
```env
GCP_PROJECT_ID=wmt-assetprotection-prod
BIGQUERY_TABLE=wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data
```

### Security Checklist
- ✅ Update CORS origins in `main.py` to match your domain
- ✅ Use HTTPS for all API calls in production
- ✅ Secure BigQuery service account credentials
- ✅ Use read-only BigQuery permissions
- ✅ Enable API rate limiting if needed
- ✅ Add authentication layer if deploying publicly

## 🧪 Testing Before Deployment

### 1. Local Testing
```powershell
.\start.ps1
# Open: http://localhost:8082/simple.html
```

### 2. Verify All Features
- ✅ Summary shows 196 projects, 4,576 stores
- ✅ Sparky AI responds to "Sidekick", "GMD", "help"
- ✅ Filters update counts in real-time
- ✅ Hierarchical navigation works (Division → Region → Market → Store)
- ✅ CSV export downloads correct data
- ✅ Breadcrumbs allow navigation back up levels

### 3. API Health Check
```powershell
curl http://localhost:8000/api/health
# Should return: {"status": "healthy", "database": "connected", ...}

curl http://localhost:8000/api/summary
# Should return: {"total_projects": 196, "total_stores": 4576, ...}
```
3. All features will work with sample data

## 🔐 Security Notes

### For Production Deployment:

1. **Never commit `.env` files** - Always use environment variables
2. **Use service accounts** with minimal required permissions
3. **Enable CORS properly** - Update `allow_origins` in `main.py` to specific domains
4. **Use HTTPS** - Ensure all API calls use HTTPS in production
5. **Secure API keys** - Store OpenAI keys in secure vault/secret manager

### Update CORS Settings:

In `backend/main.py`, update:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-codepuppy-domain.com"],  # Update this!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📱 Browser Compatibility

- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support
- Mobile browsers: ✅ Responsive design

## 🐛 Troubleshooting

### Backend won't start
- Check Python version: `python --version` (need 3.10+)
- Verify all dependencies: `pip list`
- Check `.env` file exists and has correct values

### Frontend shows "Failed to load data"
- Verify backend is running: `http://localhost:8000/api/health`
- Check browser console for CORS errors
- Verify `API_BASE_URL` in `index.html` is correct

### Database connection fails
- Verify service account credentials are valid
- Check BigQuery permissions
- Try with mock data first (remove credentials)

### AI agent not responding
- Verify `OPENAI_API_KEY` is set
- Check API key has quota remaining
- Review backend logs for error messages

## 📈 Performance Tips

1. **Limit project queries** - Use filters to reduce data size
2. **Cache filter options** - Frontend caches for 5 minutes
3. **Paginate results** - Table shows first 50 projects
4. **Optimize queries** - Add indexes on commonly filtered columns

## 🔄 Updating the Dashboard

### To add new filters:
1. Add to `FilterCriteria` in `models.py`
2. Update `_build_where_clause()` in `database.py`
3. Add filter UI in `frontend/index.html`

### To add new visualizations:
1. Create new API endpoint in `main.py`
2. Query data in `database.py`
3. Add chart component in `frontend/index.html`

## 📞 Support

For issues or questions:
1. Check this documentation
2. Review backend logs
3. Test with mock data
4. Check API health endpoint

## ✅ Deployment Checklist

- [ ] Python dependencies installed
- [ ] `.env` file configured
- [ ] Database credentials valid
- [ ] OpenAI API key set (optional)
- [ ] Backend starts successfully
- [ ] API health check passes
- [ ] Frontend loads without errors
- [ ] Filters work correctly
- [ ] Charts render properly
- [ ] AI assistant responds (if configured)
- [ ] CORS settings updated for production
- [ ] Security review completed

## 🎉 You're Ready!

Your dashboard is now ready to deploy to Code Puppy Pages. Start the backend, open the frontend, and you'll have a fully functional Projects in Stores Dashboard!
