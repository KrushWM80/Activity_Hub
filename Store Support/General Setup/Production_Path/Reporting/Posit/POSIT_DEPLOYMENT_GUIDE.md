# Posit Connect - Deployment Guide

**Last Updated:** December 3, 2025

## What is Posit Connect?

Posit Connect (formerly RStudio Connect) is Walmart's enterprise platform for hosting **data science applications** including:
- Python Flask/FastAPI applications
- R Shiny applications  
- Jupyter Notebooks
- Quarto documents
- Dashboards and reports

**Key Difference from Code Puppy:**
- **Posit**: Full applications with backend + frontend (Python/R)
- **Code Puppy**: Single HTML pages only (no backend)

---

## When to Use Posit vs Code Puppy

### Use Posit Connect When You Have:
✅ Python Flask/FastAPI backend application  
✅ R Shiny application  
✅ Need server-side processing  
✅ Multiple files and directories  
✅ Database connections beyond BigQuery  
✅ Complex business logic on backend  
✅ User authentication requirements  
✅ Scheduled reports or jobs  

### Use Code Puppy When You Have:
✅ Single HTML page only  
✅ Client-side JavaScript only  
✅ Direct BigQuery connection  
✅ Simple visualization/dashboard  
✅ No backend server needed  

---

## Posit Connect Requirements

### 1. Project Structure
```
your-app/
├── app.py                  # Flask entry point (REQUIRED)
├── requirements.txt        # Python dependencies (REQUIRED)
├── manifest.json          # Posit config (REQUIRED)
├── .env                   # Environment variables
├── src/                   # Source code modules
│   ├── __init__.py
│   ├── data_ingestion.py
│   ├── feature_engineering.py
│   └── utils.py
├── templates/             # HTML templates (Flask)
│   └── dashboard.html
├── static/                # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── images/
└── tests/                 # Test files (optional)
```

### 2. Core Files

#### app.py (Entry Point)
```python
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy'})

@app.route('/api/data')
def get_data():
    # Your data logic here
    return jsonify({'data': []})

if __name__ == '__main__':
    app.run(debug=False, port=8080)
```

#### requirements.txt
```
Flask>=2.3.0
pandas>=2.1.0
numpy>=1.26.0
google-cloud-bigquery>=3.11.0
google-cloud-storage>=2.10.0
python-dotenv>=1.0.0
gunicorn>=21.0.0
plotly>=5.17.0
```

#### manifest.json (CRITICAL for Posit)
```json
{
  "version": 1,
  "locale": "en_US.UTF-8",
  "metadata": {
    "appmode": "python-flask",
    "entrypoint": "app:app"
  },
  "python": {
    "version": "3.9.0",
    "package_manager": {
      "name": "pip",
      "version": "21.0.0"
    }
  },
  "title": "Your Application Title",
  "description": "Description of your application",
  "access_type": "logged_in",
  "run_as": "visitor",
  "environment": {
    "FLASK_ENV": "production",
    "FLASK_DEBUG": "false",
    "TZ": "America/Chicago"
  },
  "resource_limits": {
    "cpu_request": "0.5",
    "cpu_limit": "2",
    "memory_request": "512Mi",
    "memory_limit": "2Gi"
  },
  "health_check": {
    "enabled": true,
    "path": "/api/health",
    "timeout": 30
  }
}
```

---

## Deployment Steps

### Step 1: Prepare Your Application

1. **Organize Files** - Follow the project structure above
2. **Create manifest.json** - Required for Posit deployment
3. **Test Locally**:
   ```bash
   python app.py
   # Visit http://localhost:8080
   ```
4. **Freeze Dependencies**:
   ```bash
   pip freeze > requirements.txt
   ```

### Step 2: GCP Service Account Setup

Posit applications need GCP credentials to access BigQuery:

1. **Create Service Account** in GCP Console
2. **Grant Permissions**:
   - `roles/bigquery.dataViewer`
   - `roles/bigquery.jobUser`
   - `roles/storage.objectViewer` (if using GCS)
3. **Download Key** - Save as `gcp_key.json`
4. **Never commit key to git** - Add to `.gitignore`

### Step 3: Environment Variables

Create `.env` file (DO NOT commit to git):
```bash
GOOGLE_CLOUD_PROJECT=your-project-id
GCS_BUCKET_NAME=your-bucket-name
GOOGLE_APPLICATION_CREDENTIALS=/path/to/gcp_key.json
FLASK_ENV=production
FLASK_DEBUG=false
PORT=8080
```

### Step 4: Deploy to Posit Connect

**Option A: Via Git (Recommended)**
1. Push code to Walmart GitHub (gecgithub01.walmart.com)
2. In Posit Connect web interface:
   - Click "Publish"
   - Select "Git"
   - Connect to your repository
   - Select branch
   - Posit will auto-detect manifest.json and deploy

**Option B: Direct Upload**
1. Package your application directory
2. In Posit Connect:
   - Click "Publish"
   - Upload directory
   - Configure settings
   - Deploy

**Option C: Using rsconnect-python CLI**
```bash
pip install rsconnect-python

rsconnect deploy \
  --server https://posit.walmart.com \
  --api-key YOUR_API_KEY \
  .
```

---

## BigQuery Integration in Posit

### Using google-cloud-bigquery

```python
from google.cloud import bigquery
from google.oauth2 import service_account
import os

# Load credentials
credentials = service_account.Credentials.from_service_account_file(
    os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
)

# Create client
client = bigquery.Client(
    credentials=credentials,
    project=os.getenv('GOOGLE_CLOUD_PROJECT')
)

# Query data
def get_data_from_bigquery():
    query = """
        SELECT *
        FROM `project.dataset.table`
        WHERE condition = true
        LIMIT 1000
    """
    
    query_job = client.query(query)
    results = query_job.result()
    
    # Convert to pandas DataFrame
    df = results.to_dataframe()
    return df
```

### Error Handling & Fallback

```python
def load_dashboard_data():
    """Load data with fallback to mock data"""
    try:
        # Try live BigQuery data
        df = get_data_from_bigquery()
        return {'data': df, 'source': 'bigquery', 'success': True}
    except Exception as e:
        logger.error(f"BigQuery error: {e}")
        
        # Fallback to mock data
        df_mock = create_mock_data()
        return {'data': df_mock, 'source': 'mock', 'success': False, 'error': str(e)}

def create_mock_data():
    """Create sample data for development/fallback"""
    return pd.DataFrame({
        'id': range(1, 101),
        'name': [f'Item_{i}' for i in range(1, 101)],
        'value': [100 + i for i in range(100)]
    })
```

---

## Converting Your React App to Posit

If you have a **React + Node.js** app (like Refresh Guide), you need to convert it:

### Option 1: Keep React, Add Flask Backend

**Structure:**
```
your-app/
├── app.py                 # Flask backend
├── client/                # React frontend
│   ├── src/
│   ├── public/
│   └── package.json
├── requirements.txt
└── manifest.json
```

**Build Process:**
1. Build React app: `npm run build`
2. Flask serves built files:
```python
from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='client/build')

@app.route('/')
def index():
    return send_from_directory('client/build', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('client/build', path)
```

### Option 2: Pure Flask with Jinja Templates (Simpler)

Convert React components to Jinja templates:

**Before (React):**
```jsx
function Dashboard() {
  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      {items.map(item => <ItemCard key={item.id} item={item} />)}
    </div>
  );
}
```

**After (Jinja):**
```html
<div class="dashboard">
  <h1>Dashboard</h1>
  {% for item in items %}
    <div class="item-card">
      <h3>{{ item.name }}</h3>
      <p>{{ item.description }}</p>
    </div>
  {% endfor %}
</div>
```

**Flask Route:**
```python
@app.route('/dashboard')
def dashboard():
    items = get_items_from_bigquery()
    return render_template('dashboard.html', items=items)
```

---

## Common Issues & Solutions

### Issue: "Module Not Found" Error
**Problem:** Python can't find your modules

**Solution:** 
```python
# Add at top of app.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
```

### Issue: BigQuery Permission Denied
**Problem:** Service account lacks permissions

**Solution:**
1. Check GCP IAM roles
2. Verify key file path is correct
3. Test locally first:
```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
python app.py
```

### Issue: App Crashes on Startup
**Problem:** Missing dependencies or configuration

**Solution:**
1. Check Posit logs
2. Verify all required files present
3. Test health endpoint: `curl https://your-app.posit.com/api/health`

### Issue: Static Files Not Loading
**Problem:** CSS/JS not found

**Solution:**
```python
# Correct static file configuration
app = Flask(__name__, 
            static_folder='static',
            static_url_path='/static')
```

---

## Best Practices

### 1. Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info("Application started")
```

### 2. Health Checks
```python
@app.route('/api/health')
def health_check():
    try:
        # Test BigQuery connection
        client.query("SELECT 1").result()
        return jsonify({'status': 'healthy', 'bigquery': 'connected'})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500
```

### 3. Caching
```python
from functools import lru_cache
from datetime import datetime, timedelta

@lru_cache(maxsize=1)
def get_cached_data(cache_key):
    """Cache expensive BigQuery queries"""
    return query_bigquery()

# Invalidate cache after 1 hour
def get_data_with_cache():
    cache_key = datetime.now().strftime('%Y%m%d%H')  # Hour-based key
    return get_cached_data(cache_key)
```

### 4. Error Pages
```python
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {error}")
    return render_template('500.html'), 500
```

---

## Security Considerations

### 1. Never Commit Secrets
```bash
# .gitignore
.env
gcp_key.json
*.key
secrets/
```

### 2. Use Environment Variables
```python
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
```

### 3. Input Validation
```python
from flask import request, abort

@app.route('/api/data/<item_id>')
def get_item(item_id):
    # Validate input
    if not item_id.isdigit():
        abort(400, 'Invalid item ID')
    
    # Sanitize for SQL
    item_id = int(item_id)
    # Use parameterized queries
```

### 4. CORS Configuration
```python
from flask_cors import CORS

# Only allow specific origins
CORS(app, origins=['https://walmart.com'])
```

---

## Performance Optimization

### 1. Query Optimization
```python
# Bad: Load entire table
query = "SELECT * FROM large_table"

# Good: Select only needed columns and limit rows
query = """
    SELECT id, name, status
    FROM large_table
    WHERE created_date >= CURRENT_DATE() - 7
    LIMIT 1000
"""
```

### 2. Pagination
```python
@app.route('/api/items')
def get_items():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    offset = (page - 1) * per_page
    
    query = f"""
        SELECT * FROM items
        LIMIT {per_page}
        OFFSET {offset}
    """
    # Execute query...
```

### 3. Async Processing
```python
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

@app.route('/api/reports')
def generate_report():
    # Start background task
    future = executor.submit(long_running_task)
    return jsonify({'task_id': id(future), 'status': 'processing'})
```

---

## Resources

### Internal Walmart Resources
- **Posit Connect URL:** [Add internal URL]
- **GCP Console:** [Add internal URL]
- **Documentation:** [Add internal URL]

### External Learning
- **Flask Documentation:** https://flask.palletsprojects.com/
- **BigQuery Python Client:** https://cloud.google.com/bigquery/docs/reference/libraries
- **Posit Connect Guide:** https://docs.posit.co/connect/

---

## Deployment Checklist

Before deploying to Posit:

- [ ] `app.py` exists with Flask app
- [ ] `requirements.txt` includes all dependencies
- [ ] `manifest.json` configured correctly
- [ ] GCP service account created with permissions
- [ ] `.env` file created (not committed)
- [ ] `.gitignore` includes secrets
- [ ] Health check endpoint works
- [ ] Tested locally successfully
- [ ] All API endpoints return proper JSON
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Static files load correctly
- [ ] BigQuery queries optimized
- [ ] Documentation updated

---

**Created by:** Kendall Rush  
**Last Updated:** December 3, 2025
