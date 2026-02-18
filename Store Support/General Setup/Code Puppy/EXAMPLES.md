# Code Puppy Examples - Production Use Cases

> **⚠️ Common Pitfall**: Always use relative paths (`/api`) not `http://localhost:5000/api` in your code. See [COMMON_MISTAKES.md](COMMON_MISTAKES.md) for details.

## Example 1: Distribution List Selector

**Project**: Walmart Distribution Lists (134,681 lists)

**Architecture**:
- Frontend: `index.html` with search, filter, autocomplete
- Backend: `api_distribution_lists.py` Flask API
- Data Source: BigQuery `wmt-assetprotection-prod.Store_Support_Dev.dl_catalog`
- Update: Daily at 5 AM via Windows Task Scheduler

**Key Features**:
- Type-ahead autocomplete
- Multi-select with visual tags
- One-click email composition
- Category and size filters
- 134,681+ records, < 2 second load time

**Files**:
```
index.html                      # Frontend UI
api_distribution_lists.py       # BigQuery API
extract_all_dls_optimized.py   # AD extraction
upload_to_bigquery_simple.ps1  # Upload to BigQuery
daily_update_to_bigquery.ps1   # Complete workflow
setup_daily_schedule.ps1        # Scheduler setup
```

**Lessons Learned**:
- BigQuery is faster than CSV for large datasets
- Type-ahead search improves UX significantly
- Daily automated updates keep data fresh
- AD authentication via Code Puppy eliminates manual security

---

## Example 2: Simple Dashboard (Template)

**Use Case**: Team metrics and KPIs

**Architecture**:
- Frontend: `index.html` with charts
- Backend: `api_metrics.py` Flask API
- Data Source: BigQuery aggregated tables

**Features**:
- Real-time metrics
- Visual charts (Chart.js)
- Responsive design
- Auto-refresh every 5 minutes

**Code Sample** (`api_metrics.py`):
```python
from flask import Flask, jsonify
from google.cloud import bigquery

app = Flask(__name__)
client = bigquery.Client(project='your-project')

@app.route('/api/metrics')
def get_metrics():
    query = """
        SELECT 
            metric_name,
            metric_value,
            DATE(timestamp) as date
        FROM `project.dataset.metrics`
        WHERE DATE(timestamp) = CURRENT_DATE()
    """
    
    results = client.query(query).result()
    metrics = [dict(row) for row in results]
    return jsonify(metrics)
```

---

## Example 3: Data Search Tool (Template)

**Use Case**: Search across large datasets

**Architecture**:
- Frontend: Search box with results table
- Backend: Parameterized BigQuery search
- Features: Keyword search, filters, export

**Code Sample** (`api_search.py`):
```python
from flask import Flask, jsonify, request
from google.cloud import bigquery

app = Flask(__name__)
client = bigquery.Client(project='your-project')

@app.route('/api/search')
def search():
    search_term = request.args.get('q', '')
    
    query = """
        SELECT *
        FROM `project.dataset.table`
        WHERE LOWER(column) LIKE @search_term
        LIMIT 100
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("search_term", "STRING", f"%{search_term.lower()}%")
        ]
    )
    
    results = client.query(query, job_config=job_config).result()
    rows = [dict(row) for row in results]
    return jsonify(rows)
```

---

## Example 4: Report Generator (Template)

**Use Case**: Custom reports with parameters

**Architecture**:
- Frontend: Form for report parameters
- Backend: Generate report based on filters
- Output: JSON data, CSV download, or charts

**Code Sample** (`api_reports.py`):
```python
from flask import Flask, jsonify, request
from google.cloud import bigquery
import csv
from io import StringIO

app = Flask(__name__)
client = bigquery.Client(project='your-project')

@app.route('/api/report')
def generate_report():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    category = request.args.get('category')
    
    query = """
        SELECT *
        FROM `project.dataset.table`
        WHERE DATE(timestamp) BETWEEN @start_date AND @end_date
          AND category = @category
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
            bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
            bigquery.ScalarQueryParameter("category", "STRING", category)
        ]
    )
    
    results = client.query(query, job_config=job_config).result()
    rows = [dict(row) for row in results]
    return jsonify(rows)

@app.route('/api/report/csv')
def export_csv():
    # Generate CSV from report data
    # Return as downloadable file
    pass
```

---

## Example 5: User Lookup Tool (Template)

**Use Case**: Search employees by name, ID, or email

**Architecture**:
- Frontend: Search box with user details
- Backend: Query Active Directory or HR database
- Features: Autocomplete, detailed profile view

**Code Sample** (`api_users.py`):
```python
from flask import Flask, jsonify, request
from google.cloud import bigquery

app = Flask(__name__)
client = bigquery.Client(project='your-project')

@app.route('/api/users/search')
def search_users():
    query_text = request.args.get('q', '')
    
    query = """
        SELECT 
            user_id,
            name,
            email,
            department,
            title
        FROM `project.dataset.users`
        WHERE LOWER(name) LIKE @query
           OR LOWER(email) LIKE @query
           OR user_id = @query
        LIMIT 20
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("query", "STRING", f"%{query_text.lower()}%")
        ]
    )
    
    results = client.query(query, job_config=job_config).result()
    users = [dict(row) for row in results]
    return jsonify(users)

@app.route('/api/users/<user_id>')
def get_user_details(user_id):
    query = """
        SELECT *
        FROM `project.dataset.users`
        WHERE user_id = @user_id
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id)
        ]
    )
    
    results = client.query(query, job_config=job_config).result()
    user = [dict(row) for row in results]
    return jsonify(user[0] if user else {})
```

---

## Example 6: Automated Data Pipeline

**Use Case**: Daily data refresh from source to BigQuery to UI

**Architecture**:
- **Step 1**: Windows Task Scheduler (5 AM)
- **Step 2**: Extract data from source (AD, API, database)
- **Step 3**: Upload to BigQuery
- **Step 4**: Code Puppy queries BigQuery
- **Step 5**: Users see fresh data

**Workflow** (`daily_update.ps1`):
```powershell
# Extract data
python extract_data.py

# Upload to BigQuery
bq load --replace --autodetect dataset.table data.csv

# Verify
bq query "SELECT COUNT(*) FROM dataset.table"
```

**Benefits**:
- Always current data
- No manual updates
- Automated logging
- Error notifications

---

## Best Practices from Production

### Performance
- **Use BigQuery for > 10K records**: Faster than CSV/JSON
- **Add indexes/partitions**: Speed up queries
- **Paginate results**: Don't load everything at once
- **Cache static data**: Reduce API calls

### User Experience
- **Loading indicators**: Always show progress
- **Error messages**: Clear, actionable feedback
- **Keyboard shortcuts**: Power user features
- **Responsive design**: Works on all screens

### Security
- **AD authentication**: Leverage Code Puppy's built-in auth
- **Read-only access**: Use `bigquery.dataViewer` not `admin`
- **Input validation**: Sanitize all user input
- **Audit logging**: Track who uses what

### Maintainability
- **Documentation**: README and inline comments
- **Version control**: Git for all files
- **Error logging**: Catch and log exceptions
- **Health checks**: `/health` endpoint for monitoring

---

## Common Patterns

### Pattern 1: Search + Filter + Export
1. User enters search term
2. Backend queries BigQuery with filters
3. Frontend displays paginated results
4. User can export to CSV

### Pattern 2: Dashboard with Auto-Refresh
1. Page loads, queries API
2. Displays metrics/charts
3. Auto-refreshes every X minutes
4. Shows "Last updated" timestamp

### Pattern 3: Form Submission + Processing
1. User fills out form
2. Frontend validates input
3. Backend processes and stores in BigQuery
4. Returns confirmation

### Pattern 4: Master-Detail View
1. Show list of items
2. Click item to see details
3. Load details from API
4. Navigate back to list

---

## Quick Copy-Paste Snippets

### Fetch with Error Handling
```javascript
async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to load data');
        return null;
    }
}
```

### BigQuery Query Template
```python
def query_bigquery(search_term):
    query = """
        SELECT *
        FROM `project.dataset.table`
        WHERE LOWER(column) LIKE @term
        LIMIT 100
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("term", "STRING", f"%{search_term.lower()}%")
        ]
    )
    
    results = client.query(query, job_config=job_config).result()
    return [dict(row) for row in results]
```

### Loading Indicator
```javascript
function showLoading() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('content').style.display = 'none';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('content').style.display = 'block';
}
```

---

**More Examples**: See individual project folders in `Spark-Playground/General Setup/`
