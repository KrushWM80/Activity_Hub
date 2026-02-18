# Code Puppy Pages - BigQuery API Setup

## Overview
Your `index.html` now queries BigQuery through an API endpoint instead of loading a CSV file. This provides real-time data from your daily updates.

## What Changed

### Frontend (index.html)
✅ **Already Updated** - Now tries these methods in order:
1. **API endpoint** `/api/distribution-lists` (for Code Puppy deployment)
2. **CSV fallback** `all_distribution_lists.csv` (for local testing)
3. **File upload** (manual CSV selection)

### Backend API Required
You need to create an API endpoint in Code Puppy Pages that queries BigQuery.

---

## Setup Instructions for Code Puppy Pages

### Step 1: Create API Endpoint

In your Code Puppy Pages project, create a new API route:

**File**: `api_distribution_lists.js` (provided in this folder)

**Route**: `/api/distribution-lists`

### Step 2: Configure BigQuery Access

Make sure your Code Puppy service account has access to BigQuery:

```bash
gcloud projects add-iam-policy-binding wmt-assetprotection-prod \
    --member="serviceAccount:YOUR_CODEPUPPY_SA@wmt-assetprotection-prod.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataViewer"
```

### Step 3: Deploy to Code Puppy

1. Upload `index.html` to Code Puppy Pages
2. Upload `api_distribution_lists.js` as backend API
3. Configure route: `GET /api/distribution-lists`
4. Set AD group restrictions (if needed)

### Step 4: Test the Deployment

Open your Code Puppy Pages URL and verify:
- Page loads without asking for CSV upload
- Distribution lists appear in the table
- Search and filters work correctly
- Member counts display properly

---

## API Endpoints Available

### 1. Get All Distribution Lists
```
GET /api/distribution-lists
```
Returns all 134,681+ distribution lists from BigQuery

**Response**:
```json
[
    {
        "email": "example@email.wal-mart.com",
        "name": "Example DL",
        "display_name": "Example Distribution List",
        "description": "Description here",
        "member_count": 150,
        "category": "General"
    },
    ...
]
```

### 2. Search Distribution Lists
```
GET /api/distribution-lists/search?q=ops
```
Search by keyword (email, name, or description)

### 3. Get by Category
```
GET /api/distribution-lists/category/Operations
```
Filter by specific category

### 4. Get Statistics
```
GET /api/distribution-lists/stats
```
Get category counts and member statistics

---

## Alternative: Simpler Python API

If Code Puppy uses Python instead of Node.js, use this:

```python
from google.cloud import bigquery
from flask import Flask, jsonify

app = Flask(__name__)
bigquery_client = bigquery.Client(project='wmt-assetprotection-prod')

@app.route('/api/distribution-lists')
def get_distribution_lists():
    query = """
        SELECT 
            email,
            name,
            display_name,
            description,
            member_count,
            category
        FROM `wmt-assetprotection-prod.Store_Support_Dev.dl_catalog`
        ORDER BY name
    """
    
    query_job = bigquery_client.query(query)
    results = query_job.result()
    
    rows = []
    for row in results:
        rows.append({
            'email': row.email,
            'name': row.name,
            'display_name': row.display_name,
            'description': row.description,
            'member_count': row.member_count,
            'category': row.category
        })
    
    return jsonify(rows)
```

---

## Local Testing (Without API)

For local testing before deploying to Code Puppy:

1. Keep the CSV file in the same folder as `index.html`
2. Run a local web server:
   ```powershell
   python -m http.server 8000
   ```
3. Open: http://localhost:8000
4. The page will automatically fall back to CSV loading

---

## Data Flow

```
┌─────────────────────┐
│   Daily 5AM Task    │
│  (Your Server)      │
└──────────┬──────────┘
           │
           │ Uploads new data
           ▼
┌─────────────────────┐
│     BigQuery        │
│  dl_catalog table   │
└──────────┬──────────┘
           │
           │ Queries data
           ▼
┌─────────────────────┐
│  Code Puppy API     │
│  /api/distribution- │
│       lists         │
└──────────┬──────────┘
           │
           │ Returns JSON
           ▼
┌─────────────────────┐
│   index.html        │
│  (User Browser)     │
└─────────────────────┘
```

---

## Troubleshooting

### "Failed to fetch" error
- Check that `/api/distribution-lists` endpoint is deployed
- Verify BigQuery permissions for Code Puppy service account
- Check browser console for detailed error messages

### Data not loading
- Test BigQuery access directly: `bq query --use_legacy_sql=false 'SELECT COUNT(*) FROM \`wmt-assetprotection-prod.Store_Support_Dev.dl_catalog\`'`
- Verify API endpoint returns JSON (test in browser or Postman)
- Check Code Puppy logs for backend errors

### Old CSV data showing
- Clear browser cache (Ctrl+Shift+Delete)
- Verify BigQuery table has latest data
- Check `last_updated` timestamp in BigQuery

---

## Next Steps

1. ✅ Upload `index.html` to Code Puppy Pages
2. ⏳ Create API endpoint using `api_distribution_lists.js`
3. ⏳ Configure BigQuery permissions
4. ⏳ Test the deployment
5. ⏳ Set up AD group restrictions

Once deployed, your Distribution List Selector will always show live data from BigQuery! 🚀
