# Code Puppy Pages - Quick Reference

## 🚨 CRITICAL: Don't Use Localhost in Deployed Code

```javascript
// ❌ WRONG - Will fail when deployed
const API_BASE_URL = 'http://localhost:5000/api';

// ✅ CORRECT - Use relative paths
const API_BASE_URL = '/api';

// ✅ OR - Use environment detection
const API_BASE_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:5000/api'  // Local dev
    : '/api';  // Production
```

**Why?** When deployed, users' browsers try to fetch from `localhost` (their computer), not your server. Use relative paths so Code Puppy routes requests to your backend.

---

## ⚡ Architecture Quick Comparison

| Approach | Speed | Best For | Complexity |
|----------|-------|----------|------------|
| **Embedded Static Data** | 🚀 400ms | Daily updates | Low |
| **Live API Calls** | 🐌 2-5s | Real-time data | Medium |
| **Hybrid (Cached + API)** | ⚡ 1s | Balanced needs | High |

### When to Use What

```javascript
// ✅ Data updates daily → Embed it (10x faster)
const STATIC_DATA = { stores: [...], summary: {...} };

// ✅ Data updates every second → Live API
const data = await fetch('/api/live-data');

// ✅ User submissions → Always live API
await fetch('/api/submit', { method: 'POST', body: data });
```

**Performance Reality**:
- Embedded: 400ms load, 0 API calls
- Live API: 3000ms load, 3+ API calls
- **Embedded is 7.5x faster** for dashboards!

---

## Common Commands

### Local Testing
```powershell
# Simple HTTP server
python -m http.server 8000

# Flask backend
python api_endpoint.py
```

### BigQuery Access
```bash
# Grant service account access
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:SA_EMAIL" \
    --role="roles/bigquery.dataViewer"

# Test query
bq query --use_legacy_sql=false 'SELECT COUNT(*) FROM `project.dataset.table`'
```

---

## File Templates

### Minimal Frontend (`index.html`)
```html
<!DOCTYPE html>
<html>
<head>
    <title>Your App</title>
</head>
<body>
    <div id="app">Loading...</div>
    
    <script>
        async function loadData() {
            try {
                const response = await fetch('/api/endpoint');
                const data = await response.json();
                document.getElementById('app').textContent = JSON.stringify(data);
            } catch (error) {
                document.getElementById('app').textContent = 'Error: ' + error.message;
            }
        }
        loadData();
    </script>
</body>
</html>
```

### Minimal Backend (`api_endpoint.py`)
```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/endpoint')
def get_data():
    return jsonify({'message': 'Hello World'})

if __name__ == '__main__':
    app.run(port=8080)
```

### BigQuery Backend (`api_bigquery.py`)
```python
from flask import Flask, jsonify
from google.cloud import bigquery

app = Flask(__name__)
client = bigquery.Client(project='your-project')

@app.route('/api/data')
def query_data():
    query = "SELECT * FROM `project.dataset.table` LIMIT 100"
    results = client.query(query).result()
    rows = [dict(row) for row in results]
    return jsonify(rows)

if __name__ == '__main__':
    app.run(port=8080)
```

---

## Deployment Checklist

- [ ] **CRITICAL**: No `localhost` URLs in JavaScript (use `/api` instead)
- [ ] **Architecture**: Chose right approach (embedded for daily updates, API for real-time)
- [ ] Test locally (backend + frontend both running)
- [ ] Backend file uploaded (`api_endpoint.py` or `api_endpoint.js`) - if using API
- [ ] API routes configured in Code Puppy - if using API
- [ ] Grant BigQuery permissions (if needed)
- [ ] Set AD group restrictions
- [ ] Test deployed version
- [ ] Open browser console (F12) - check for errors
- [ ] Verify data loads correctly
- [ ] Check page load speed (should be under 1 second for dashboards)
- [ ] Share URL with team

---

## Embedded Data Template

**For dashboards that update daily/weekly** (10x faster than API calls):

```html
<!DOCTYPE html>
<html>
<head>
    <title>Fast Dashboard</title>
</head>
<body>
    <div id="app">Loading...</div>
    <div id="lastUpdate"></div>
    
    <script>
        // ✅ Embed data directly (update via GitHub Actions daily)
        const STATIC_DATA = {
            lastUpdated: "2026-01-09T06:00:00Z",
            stores: [
                {id: 1, name: "Store A", completion: 85},
                {id: 2, name: "Store B", completion: 92}
                // ... all your data
            ],
            summary: {
                total: 4500,
                completed: 3200
            }
        };
        
        // Instant load - no API calls!
        function loadData() {
            const app = document.getElementById('app');
            app.innerHTML = STATIC_DATA.stores
                .map(s => `<div>${s.name}: ${s.completion}%</div>`)
                .join('');
            
            document.getElementById('lastUpdate').textContent = 
                `Last updated: ${new Date(STATIC_DATA.lastUpdated).toLocaleString()}`;
        }
        
        window.addEventListener('DOMContentLoaded', loadData);
    </script>
</body>
</html>
```

**Update script** (`scripts/embed-data.js`):
```javascript
const fs = require('fs');

// Fetch fresh data
const stores = JSON.parse(fs.readFileSync('stores.json', 'utf8'));

// Read template
const template = fs.readFileSync('template.html', 'utf8');

// Embed data
const output = template.replace(
    '/* EMBED_DATA */',
    `const STATIC_DATA = ${JSON.stringify({
        lastUpdated: new Date().toISOString(),
        stores: stores
    })};`
);

fs.writeFileSync('index.html', output);
```

**GitHub Actions** (`.github/workflows/update.yml`):
```yaml
name: Update Data
on:
  schedule:
    - cron: '0 6 * * *'  # Daily 6 AM
jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: curl https://your-api/data > stores.json
      - run: node scripts/embed-data.js
      - name: Deploy
        run: |
          # Upload index.html to Code Puppy
```

---

## Deployment Checklist

- [ ] **CRITICAL**: No `localhost` URLs in JavaScript (use `/api` instead)
- [ ] Test locally (backend + frontend both running)
- [ ] Backend file uploaded (`api_endpoint.py` or `api_endpoint.js`)
- [ ] API routes configured in Code Puppy
- [ ] Grant BigQuery permissions (if needed)
- [ ] Set AD group restrictions
- [ ] Test deployed version
- [ ] Open browser console (F12) - check for errors
- [ ] Verify data loads correctly
- [ ] Share URL with team

---

## Troubleshooting Quick Fixes

| Issue | Quick Fix |
|-------|-----------|
| No data showing | Check console (F12) for `localhost` API errors → Change to `/api` |
| 404 Not Found | Verify backend file uploaded and route configured |
| 403 Forbidden | Grant BigQuery dataViewer role to service account |
| Works locally, fails deployed | Remove all `localhost` URLs, use `/api` paths |
| CORS errors | Add `flask_cors` to backend or use `/api` routes |

---

## Quick Debug Commands

```javascript
// Check what URL is being called
console.log('API URL:', API_BASE_URL);
console.log('Hostname:', window.location.hostname);

// Test if backend is reachable
fetch('/api/health')
    .then(res => res.json())
    .then(data => console.log('Backend:', data))
    .catch(err => console.error('Backend down:', err));
```

```powershell
# Test backend from terminal
Invoke-WebRequest -Uri "https://your-page.puppy.walmart.com/api/health"
```

---

## Troubleshooting Quick Fixes

| Issue | Solution |
|-------|----------|
| 404 API Error | Check route configuration `/api/endpoint` |
| BigQuery Access Denied | Grant `bigquery.dataViewer` role |
| Blank Page | Check browser console (F12) |
| Data Not Loading | Test API endpoint directly |
| Permission Denied | Verify AD group membership |

---

## Contact Info

**Code Puppy Admin**: [Ask your admin for contact]  
**GCP Project**: [Your project ID]  
**Service Account**: [Your SA email]

---

**Quick Start**: See `CODE_PUPPY_GUIDE.md` for full documentation
