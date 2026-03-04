# TDA Insights Dashboard - Quick Start Guide

Get the TDA Insights Dashboard running in 5 minutes.

## 🚀 Quick Start

### Step 1: Verify Prerequisites (2 mins)

```powershell
# Check Python version (should be 3.8+)
python --version

# Check Google Cloud auth
gcloud auth list
```

If no auth, run:
```powershell
gcloud auth application-default login
```

### Step 2: Install Dependencies (1 min)

```powershell
cd "Store Support\Projects\TDA Insights"
pip install -r requirements.txt
```

### Step 3: Start Backend (1 min)

**Terminal 1:**
```powershell
cd "Store Support\Projects\TDA Insights"
python backend.py
```

Expected output:
```
INFO:__main__:BigQuery client initialized for project: wmt-assetprotection-prod
INFO:__main__:Starting TDA Insights backend on port 5000
 * Running on http://0.0.0.0:5000
```

### Step 4: Open Dashboard (1 min)

**Terminal 2:**
```powershell
cd "Store Support\Projects\TDA Insights"
start dashboard.html
```

Or manually navigate to: `http://localhost:5000/dashboard.html`

✅ **Done!** Your dashboard is running.

## 📊 Using the Dashboard

### Load Data
1. Dashboard loads automatically when you open it
2. Filters populate from BigQuery
3. Initial data loads in seconds

### Filter Data
1. Select a **Phase** from dropdown (Test, Production, etc.)
2. Select a **Health Status** (On Track, At Risk, Off Track)
3. Click **Apply Filters**

### Export Data
- Click **📥 Export CSV** to download filtered data

### Generate Report
- Click **📊 Generate PPT** to create a PowerPoint (coming soon)

## 🐛 Troubleshooting

| Problem | Solution |
|---|---|
| "Connection error" | Is `python backend.py` running? |
| No data in dashboard | Check BigQuery permissions |
| Button doesn't work | Open browser console (F12) for errors |
| Slow loading | Try refreshing page or restarting backend |

## 📈 Generate PowerPoint Reports

### Option 1: From Python Script
```powershell
cd "Store Support\Projects\TDA Insights"
python generate_ppt.py
```

### Option 2: From Python Code
```python
from generate_ppt import TDAPowerPointGenerator

gen = TDAPowerPointGenerator()
gen.fetch_data()
gen.generate_report("MyReport.pptx")
```

The generated PowerPoint will have:
- Title slide
- One slide per Phase
- Summary statistics
- Top initiatives per phase
- Professional Walmart branding

## 🎨 Customizing the Dashboard

### Change Colors
Edit `dashboard.html`, modify the CSS `:root` variables:
```css
:root {
    --walmart-blue: #0071CE;
    --walmart-yellow: #FFCC00;
    --success: #107C10;
    /* ... */
}
```

### Change API URL
If backend runs on different server, edit in `dashboard.html`:
```javascript
const API_BASE = 'http://your-server:5000/api';
```

### Add Filters
Edit `backend.py` in `filter_data()` method:
```python
def filter_data(self, phase: str = None, health_status: str = None, custom_field: str = None):
    # Add your filter logic here
```

Then add HTML select element in `dashboard.html`.

## 📝 Common Tasks

### View API Documentation
Visit: `http://localhost:5000/api/health`

### Query Raw Data
Get all data as JSON:
```bash
curl http://localhost:5000/api/data
```

Get filtered data:
```bash
curl "http://localhost:5000/api/data?phase=Test&health_status=On%20Track"
```

Get summary:
```bash
curl http://localhost:5000/api/summary
```

### Verify BigQuery Connection
```python
from google.cloud import bigquery
client = bigquery.Client()
print(client.list_datasets())
```

### Check Table Schema
```python
from google.cloud import bigquery
client = bigquery.Client()
table = client.get_table("wmt-assetprotection-prod.Store_Support_Dev.`Output_TDA Report`")
print([field.name for field in table.schema])
```

## 📋 Configuration

### Backend Config
Set environment before running `backend.py`:
```powershell
$env:PORT=5000
$env:FLASK_DEBUG=True
python backend.py
```

### Frontend Config
Edit `dashboard.html`:
```javascript
// Change API endpoint
const API_BASE = 'http://localhost:5000/api';

// Customize refresh interval
const REFRESH_INTERVAL = 300000; // 5 minutes
```

## 🔄 Restarting & Stopping

### Stop Backend
Press `Ctrl+C` in the terminal running `python backend.py`

### Clear Cache
Edit `backend.py`:
```python
data_manager._data_cache = None
data_manager._cache_timestamp = None
```

Then restart backend.

### Force Refresh Data
Add `?refresh=true` to API call:
```javascript
fetch(`${API_BASE}/data?refresh=true`)
```

## 📚 Learn More

- See [README.md](README.md) for full documentation
- Check [design guidelines](../../General%20Setup/Design/DESIGN_SYSTEM.md) for branding
- Review [BigQuery docs](https://cloud.google.com/bigquery/docs)

## ❓ FAQ

**Q: Where is my data coming from?**  
A: BigQuery table `wmt-assetprotection-prod.Store_Support_Dev.Output_TDA Report`

**Q: Can I change the dashboard colors?**  
A: Yes! Edit CSS variables in `dashboard.html` `:root` section

**Q: How do I add more filters?**  
A: Add select element in HTML, update `backend.py` filter logic, and add API endpoint

**Q: Is this secure for production?**  
A: This is a local dashboard for internal use. For production, add authentication (OAuth2), HTTPS, and proper access controls.

**Q: Can I schedule automatic reports?**  
A: Not yet, but you can schedule `python generate_ppt.py` with a task scheduler (Windows Task Scheduler, cron, etc.)

---

**Happy Dashboard-ing! 📊**

For issues or questions, see the README.md or contact the Activity Hub team.
