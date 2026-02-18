# Code Puppy Pages Deployment Guide

## What You Need to Deploy

### 1. Frontend (HTML)
- **File**: `index.html`
- **Where**: Upload to Code Puppy Pages as your main page

### 2. Backend API
- **File**: `api_distribution_lists.py` (Python) OR `api_distribution_lists.js` (Node.js)
- **Route**: `/api/distribution-lists`

---

## Deployment Options

### Option A: Cloud Run Deployment (Production - Recommended)

Deploy the backend API to Google Cloud Run for production use:

**1. Deploy API to Cloud Run**:
```bash
cd api/

gcloud run deploy distribution-list-api \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

**2. Note the Service URL**:
```
https://distribution-list-api-xxxxx.us-central1.run.app
```

**3. Update Frontend**:
Update `index.html` with the Cloud Run API URL:
```javascript
const API_BASE = 'https://distribution-list-api-xxxxx.us-central1.run.app';
const ENDPOINT = `${API_BASE}/api/distribution-lists`;
```

**4. Upload Frontend to Code Puppy**:
- Upload `index.html` to Code Puppy Pages
- Set page title: "Distribution List Selector"
- Access at: `https://your-page.codepuppy.com`

**5. Test Deployment**:
```bash
# Test health endpoint
curl https://distribution-list-api-xxxxx.us-central1.run.app/health

# Test API endpoint
curl https://distribution-list-api-xxxxx.us-central1.run.app/api/distribution-lists?limit=5
```

**6. Redeployment** (for updates):
```powershell
# Windows PowerShell - Use REDEPLOY.ps1
.\REDEPLOY.ps1

# Or manual:
cd api
gcloud run deploy distribution-list-api --source . --region us-central1 --allow-unauthenticated
```

### Option B: Code Puppy Built-in API (If Available)

If Code Puppy Pages has a built-in way to create API endpoints:

1. **Upload `index.html`** to Code Puppy Pages
2. **Create API endpoint** in Code Puppy's API builder:
   - Route: `/api/distribution-lists`
   - Method: GET
   - Code:
   ```python
   from google.cloud import bigquery
   
   client = bigquery.Client(project='wmt-assetprotection-prod')
   query = """
       SELECT email, name, display_name, description, member_count, category
       FROM `wmt-assetprotection-prod.Store_Support_Dev.dl_catalog`
       ORDER BY name
   """
   results = client.query(query).result()
   return [dict(row) for row in results]
   ```

### Option C: Deploy Separate Backend Service

If Code Puppy requires a separate backend deployment:

#### For Python/Flask:
1. Upload `api_distribution_lists.py`
2. Create `requirements.txt`:
   ```
   flask>=2.3.0
   google-cloud-bigquery>=3.11.0
   ```
3. Deploy as a service
4. Update `index.html` API URL if needed (e.g., `https://your-api.codepuppy.com/api/distribution-lists`)

#### For Node.js:
1. Upload `api_distribution_lists.js`
2. Create `package.json`:
   ```json
   {
     "name": "dl-api",
     "version": "1.0.0",
     "dependencies": {
       "@google-cloud/bigquery": "^7.0.0",
       "express": "^4.18.0"
     }
   }
   ```
3. Deploy as a service

---

## API Endpoint Specification

### GET /api/distribution-lists

**Description**: Retrieve distribution lists with optional filtering and pagination

**Parameters**:
| Parameter | Type | Default | Max | Example |
|-----------|------|---------|-----|----------|
| search | string | (none) | - | `store support` |
| store | string | (none) | - | `1234` |
| department | string | (none) | - | `Loss Prevention` |
| limit | int | 100 | 200 | `50` |
| offset | int | 0 | - | `100` |

**Example Requests**:
```bash
# Get all (with limit)
curl "https://your-api.run.app/api/distribution-lists?limit=100"

# Search by name
curl "https://your-api.run.app/api/distribution-lists?search=store+support&limit=50"

# Filter by store
curl "https://your-api.run.app/api/distribution-lists?store=1234"

# Filter by department
curl "https://your-api.run.app/api/distribution-lists?department=Operations"

# Pagination
curl "https://your-api.run.app/api/distribution-lists?limit=50&offset=100"
```

**Response Format**:
```json
{
  "distribution_lists": [
    {
      "email": "store-support@walmart.com",
      "name": "Store Support",
      "display_name": "Store Support Team",
      "description": "Support team for stores",
      "member_count": 523,
      "category": "Support"
    }
  ],
  "count": 1,
  "limit": 100,
  "offset": 0,
  "timestamp": "2025-12-17T10:30:00Z"
}
```

---

## Redeployment Scripts

### PowerShell Script (Windows)

Create `REDEPLOY.ps1` in project root:
```powershell
# REDEPLOY.ps1 - Quick redeploy to Cloud Run

Write-Host "Deploying Distribution List API to Cloud Run..." -ForegroundColor Cyan

cd api

gcloud run deploy distribution-list-api `
  --source . `
  --region us-central1 `
  --allow-unauthenticated

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nDeployment successful!" -ForegroundColor Green
    Write-Host "API URL: https://distribution-list-api-xxxxx.us-central1.run.app" -ForegroundColor Yellow
    Write-Host "Test: curl https://distribution-list-api-xxxxx.us-central1.run.app/health" -ForegroundColor Cyan
} else {
    Write-Host "`nDeployment failed!" -ForegroundColor Red
    exit 1
}
```

**Usage**:
```powershell
.\REDEPLOY.ps1
```

### Bash Script (Linux/Mac)

Create `REDEPLOY.sh` in project root:
```bash
#!/bin/bash
# REDEPLOY.sh - Quick redeploy to Cloud Run

echo "Deploying Distribution List API to Cloud Run..."

cd api

gcloud run deploy distribution-list-api \
  --source . \
  --region us-central1 \
  --allow-unauthenticated

if [ $? -eq 0 ]; then
    echo ""
    echo "Deployment successful!"
    echo "API URL: https://distribution-list-api-xxxxx.us-central1.run.app"
    echo "Test: curl https://distribution-list-api-xxxxx.us-central1.run.app/health"
else
    echo ""
    echo "Deployment failed!"
    exit 1
fi
```

**Usage**:
```bash
chmod +x REDEPLOY.sh
./REDEPLOY.sh
```

---

## Step-by-Step Deployment

### Step 1: Upload Frontend
1. Go to Code Puppy Pages dashboard
2. Create new page or edit existing
3. Upload `index.html`
4. Set page title: "Distribution List Selector"
5. Note the page URL (e.g., `https://your-page.codepuppy.com`)

### Step 2: Create API Endpoint

**Ask your Code Puppy admin:** "How do I create an API endpoint that queries BigQuery?"

They'll likely say one of:
- "Use the API Builder in the admin panel"
- "Upload a Python/Node.js file to the backend folder"
- "Create a serverless function"
- "Use our built-in BigQuery connector"

**Then follow their specific instructions** using the code from `api_distribution_lists.py` or `api_distribution_lists.js`

### Step 3: Grant BigQuery Access

Make sure Code Puppy's service account can read your BigQuery table:

```bash
# Get Code Puppy's service account email from your admin
# Then grant access:
gcloud projects add-iam-policy-binding wmt-assetprotection-prod \
    --member="serviceAccount:CODEPUPPY_SERVICE_ACCOUNT@wmt-assetprotection-prod.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataViewer"
```

### Step 4: Test the Deployment

1. Open your Code Puppy page URL
2. Check browser console (F12) for errors
3. Verify data loads (should see 134,681+ lists)
4. Test search and filters
5. Try composing an email

---

## Troubleshooting

### "Error loading distribution lists from BigQuery"

**Check these:**
1. API endpoint exists at `/api/distribution-lists`
2. Service account has BigQuery access
3. BigQuery table has data: 
   ```sql
   SELECT COUNT(*) FROM `wmt-assetprotection-prod.Store_Support_Dev.dl_catalog`
   ```

**View detailed error:**
- Open browser console (F12)
- Look for red error messages
- Share with Code Puppy support if needed

### "API endpoint not found (404)"

The API route isn't deployed correctly. Options:
1. Check Code Puppy API configuration
2. Verify route is `/api/distribution-lists` (exact match)
3. Restart the backend service
4. Check Code Puppy deployment logs

### "Permission denied" in BigQuery

Service account needs access:
```bash
# Check current permissions:
gcloud projects get-iam-policy wmt-assetprotection-prod \
    --flatten="bindings[].members" \
    --filter="bindings.members:serviceAccount:*codepuppy*"

# Grant if missing:
gcloud projects add-iam-policy-binding wmt-assetprotection-prod \
    --member="serviceAccount:YOUR_SA@wmt-assetprotection-prod.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataViewer"
```

---

## Alternative: Static JSON Export (No Backend Needed)

If Code Puppy doesn't support backend APIs easily, you can export BigQuery data to JSON:

### 1. Export BigQuery to JSON daily:
```powershell
# Add to your daily 5 AM task
bq query --format=json --use_legacy_sql=false `
'SELECT email, name, display_name, description, member_count, category 
 FROM `wmt-assetprotection-prod.Store_Support_Dev.dl_catalog` 
 ORDER BY name' > distribution_lists.json
```

### 2. Upload JSON to Code Puppy Pages

### 3. Modify `index.html` to load JSON instead:
```javascript
// Change this line in loadDistributionLists():
const response = await fetch('/api/distribution-lists');
// To this:
const response = await fetch('distribution_lists.json');
```

**Pros**: No backend API needed, simpler deployment  
**Cons**: Need to upload new JSON file daily (can automate), larger file size (~20MB)

---

## Troubleshooting

### Issue: 404 Error on /api/distribution-lists

**Problem**: Puppy Page shows "Failed to load distribution lists" or 404 error

**Solution**:
1. **Redeploy the API**:
   ```powershell
   .\REDEPLOY.ps1
   ```
   Or manually:
   ```bash
   cd api
   gcloud run deploy distribution-list-api --source . --region us-central1 --allow-unauthenticated
   ```

2. **Wait for deployment** (30-60 seconds)

3. **Test endpoint directly**:
   ```bash
   curl https://distribution-list-api-xxxxx.us-central1.run.app/api/distribution-lists?limit=1
   ```

4. **Hard refresh browser** (Ctrl+Shift+R) to clear cache

5. **Check browser console** (F12) for error details

### Issue: Deployment Problems

**"gcloud command not found"**:
- Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install

**"Permission denied"**:
```bash
gcloud auth login
gcloud config set project wmt-assetprotection-prod
```

**Deployment takes too long**:
- First deploy: 3-5 minutes (building Docker image)
- Subsequent deploys: 30-60 seconds

**Still getting 404 after redeploy**:
1. Check Cloud Run logs:
   ```bash
   gcloud run services logs read distribution-list-api --limit 50
   ```
2. Verify API URL in `index.html` matches deployed service URL
3. Test health endpoint:
   ```bash
   curl https://distribution-list-api-xxxxx.us-central1.run.app/health
   ```

### Rollback (If Needed)

```bash
# List revisions
gcloud run revisions list --service distribution-list-api

# Rollback to previous revision
gcloud run deploy distribution-list-api \
  --revision=<previous-revision-id> \
  --no-traffic-100 \
  --region us-central1
```

### View Logs

```bash
# Recent logs
gcloud run services logs read distribution-list-api --limit 50

# Follow logs in real-time
gcloud run services logs tail distribution-list-api
```

---

## Files Checklist

Ready for Code Puppy deployment:
- ✅ `index.html` - Frontend UI (BigQuery-only version)
- ✅ `api_distribution_lists.py` - Python backend API
- ✅ `api_distribution_lists.js` - Node.js backend API
- ✅ `all_distribution_lists.csv` - Data backup (optional)

---

## Next Steps

1. **Contact Code Puppy admin/support** and ask:
   - "How do I create an API endpoint in Code Puppy Pages?"
   - "Does Code Puppy have native BigQuery integration?"
   - "What's the service account email for BigQuery access?"

2. **Show them this file** - `api_distribution_lists.py` or `api_distribution_lists.js`

3. **Test locally first** (optional):
   ```powershell
   # If using Python version:
   pip install flask google-cloud-bigquery
   python api_distribution_lists.py
   # Opens on http://localhost:8080
   ```

4. **Deploy and test** on Code Puppy Pages

Need help? Share any error messages and I'll help troubleshoot! 🚀
