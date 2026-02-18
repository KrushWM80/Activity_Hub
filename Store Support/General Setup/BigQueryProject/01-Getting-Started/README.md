# 🔗 BigQuery Integration Hub
## Consolidated BigQuery Connection Resources for Walmart AMP Projects

**Last Updated:** November 24, 2025  
**Purpose:** Centralized BigQuery connection tools, scripts, and documentation for accessing Walmart AMP data

---

## 📊 Data Source Information

**BigQuery Table:** `wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Prep`  
**Purpose:** Published AMP titles for store associates  
**Access Level:** Read-only via authenticated Google Cloud credentials  
**Typical Dataset Size:** 75+ published titles per fiscal week  

---

## 📁 File Organization

### 🔐 Authentication & Connection Files

#### JavaScript Connectors
- **`bigquery-auth.js`** - Browser-based authentication handler
- **`bigquery-tester.js`** - Connection testing utilities
- **`unlimited-bigquery-connector.js`** - Direct API connector for unlimited data access
- **`amp-data-connector.js`** - Specialized AMP data connector
- **`bigquery-cli-test.js`** - CLI testing scripts

#### Python Scripts
- **`connect_bigquery.py`** - Primary Python BigQuery connector
- **`bigquery_service.py`** - Service wrapper for BigQuery operations
- **`bigquery_rest_service.py`** - REST API service for BigQuery data
- **`export_real_bigquery_data.py`** - Export complete datasets to JSON/CSV
- **`fetch_live_data.py`** - Live data fetching script
- **`amp_bigquery_complete_integration.py`** - Generates complete BigQuery integration SQL (all 95 fields)
- **`amp_bigquery_trigger_generator.py`** - Creates automated data pipeline triggers

#### PowerShell Scripts
- **`connect_direct_bigquery.ps1`** - Direct connection via PowerShell
- **`export-complete-data.ps1`** - Complete data export automation
- **`install_gcloud.ps1`** - Google Cloud SDK installation
- **`setup_gcloud_auth.ps1`** - Authentication setup wizard
- **`setup_live_data.ps1`** - Live data connection setup
- **`Test-BigQuery.ps1`** - PowerShell connection testing
- **`deploy_bigquery_phase1.ps1`** - Phase 1 BigQuery deployment
- **`deploy_bigquery_complete.ps1`** - Complete BigQuery deployment automation

### 📚 Documentation Files
- **`BIGQUERY_REST_SETUP.md`** - REST API setup guide
- **`COMPLETE_BIGQUERY_EXPORT.md`** - Complete export instructions
- **`GCLOUD_INSTALLATION_GUIDE.md`** - Step-by-step gcloud SDK installation
- **`LIVE_DATA_SETUP_INSTRUCTIONS.md`** - Live data connection guide
- **`REAL_DATA_SETUP.md`** - Real data connection setup

### 📦 Data Files
- **`bigquery-complete-export.json`** - Full dataset export (all fields)
- **`bigquery-export.json`** - Standard dataset export
- **`live_amp_data.json`** - Live data snapshot
- **`real-amp-data.csv`** - CSV export of real AMP data
- **`sample-real-data.csv`** - Sample dataset for testing

### 🗄️ SQL Schema Files
- **`amp_bigquery_complete_integration_20251028_071747.sql`** - Complete 95-field integration schema
- **`amp_bigquery_trigger_system_20251028_072802.sql`** - Automated trigger system for data updates
- **`amp_bigquery_enhanced_multisource_system_20251028_080418.sql`** - Enhanced multi-source integration

---

## 🚀 Quick Start Guide

### Option 1: JavaScript (Browser/Node.js)

```javascript
// Import the unlimited connector
import { connectToBigQuery, fetchAMPData } from './unlimited-bigquery-connector.js';

// Connect and fetch data
const data = await fetchAMPData({
    project: 'wmt-assetprotection-prod',
    dataset: 'Store_Support_Dev',
    table: 'AMP_Data_Prep'
});
```

### Option 2: Python

```python
# Use the primary connector
from connect_bigquery import connect_and_fetch

# Fetch data
df = connect_and_fetch(
    project='wmt-assetprotection-prod',
    dataset='Store_Support_Dev',
    table='AMP_Data_Prep'
)
```

### Option 3: PowerShell

```powershell
# Run the connection script
.\connect_direct_bigquery.ps1

# Or use the test script
.\Test-BigQuery.ps1
```

---

## 🔧 Setup Requirements

### 1. Google Cloud SDK
- **Required for:** Authentication and direct BigQuery access
- **Install:** Run `install_gcloud.ps1` or see `GCLOUD_INSTALLATION_GUIDE.md`
- **Command:** `gcloud auth login`

### 2. Python Dependencies
```bash
pip install google-cloud-bigquery google-auth google-auth-oauthlib pandas
```

### 3. Node.js Dependencies (if using JavaScript)
```bash
npm install @google-cloud/bigquery
```

---

## 📋 Common Use Cases

### Use Case 1: Dashboard Data Loading
**Goal:** Load AMP titles for interactive dashboard  
**Recommended:** `unlimited-bigquery-connector.js` + `bigquery-auth.js`  
**Output:** JSON array of AMP objects with all fields

### Use Case 2: Video Creator Title Selection
**Goal:** Fetch titles for video generation workflow  
**Recommended:** `real-amp-data.csv` (cached) or `fetch_live_data.py` (live)  
**Output:** CSV with Title, Week, Preview Link, Content Area

### Use Case 3: Bulk Data Export
**Goal:** Export entire dataset for analysis  
**Recommended:** `export_real_bigquery_data.py`  
**Output:** Complete JSON/CSV export with all 75+ titles

### Use Case 4: REST API Service
**Goal:** Provide data to multiple applications via API  
**Recommended:** `bigquery_rest_service.py`  
**Output:** REST endpoints at `http://localhost:8081/api/data`

---

## 🔄 Data Refresh Workflow

### Manual Refresh
1. Run: `python fetch_live_data.py`
2. Output: Updates `live_amp_data.json`
3. Use in dashboards without authentication

### Automated Refresh (Recommended)
1. Set up: `.\setup_live_data.ps1`
2. Schedule: Windows Task Scheduler or cron
3. Frequency: Daily at 6 AM (after AMP publishes)

### Real-Time Connection
1. Authenticate: `gcloud auth login`
2. Use: `unlimited-bigquery-connector.js`
3. Benefit: Always current, no caching needed

---

## 🎯 Integration Patterns

### Pattern 1: Cached Data (Fast, No Auth)
```
CSV/JSON file → Local dashboard → No authentication needed
Pros: Fast, offline-capable
Cons: Must refresh manually
```

### Pattern 2: REST API (Medium Speed, Single Auth)
```
BigQuery → REST Service → Multiple dashboards
Pros: One authentication point, multiple consumers
Cons: Service must stay running
```

### Pattern 3: Direct Connection (Real-Time, Per-User Auth)
```
Browser/App → BigQuery API → Real-time data
Pros: Always current, no cache
Cons: Each user needs authentication
```

---

## 📊 Data Schema Reference

### Key Fields in AMP_Data_Prep
```
- Activity_Title (string) - AMP title text
- WM_Week (integer) - Fiscal week number
- WM_Year (integer) - Fiscal year
- Preview_Link (string) - amp2-cms.prod.walmart.com preview URL
- Content_Area (string) - Category (Health, Safety, Culture, etc.)
- Published_Date (timestamp) - When AMP was published
- Verification_Status (string) - Published/Verified status
- Region (string) - Geographic region
- Market (string) - Market designation
- Store (string) - Store number
```

---

## 🔍 Troubleshooting

### Issue: "Authentication Failed"
**Solution:** Run `gcloud auth login` and authenticate with Walmart Google account

### Issue: "Permission Denied"
**Solution:** Verify you have read access to `wmt-assetprotection-prod` project

### Issue: "Module not found"
**Solution:** Install dependencies with pip/npm (see Setup Requirements)

### Issue: "CORS Error in Browser"
**Solution:** Use REST service (`bigquery_rest_service.py`) instead of direct browser connection

### Issue: "Quota Exceeded"
**Solution:** Use cached data files or implement caching layer

---

## 🎓 Best Practices

### ✅ DO:
- Cache data locally when possible (use CSV/JSON exports)
- Refresh cached data daily
- Use REST service for multiple dashboard consumers
- Implement error handling for network issues
- Log authentication attempts for debugging

### ❌ DON'T:
- Store authentication credentials in code
- Make BigQuery calls on every page load
- Expose service credentials in client-side code
- Skip error handling
- Refresh data more often than needed (quota limits)

---

## 🔗 Project Integration

### Store Updates Dashboard
**Location:** `../../Store Updates Dashboard/`  
**Uses:** `real-data-loader.js` to load from CSV  
**Integration:** Add `<script src="../General Setup/BigQueryProject/gcp_setup/unlimited-bigquery-connector.js"></script>`

### AMP Video Creator
**Location:** `../AMP Video/`  
**Uses:** `amp_selector_dashboard.html` needs title data  
**Integration:** Load from `real-amp-data.csv` or connect directly

### AMP Infographic Generator
**Location:** `../AMP Infographic/`  
**Uses:** Title and content data for infographic creation  
**Integration:** Use cached JSON for offline generation

---

## 📈 Performance Metrics

### Connection Methods Performance
| Method | Speed | Auth Required | Real-Time | Offline |
|--------|-------|---------------|-----------|---------|
| CSV File | ⚡⚡⚡ Fast | ❌ No | ❌ No | ✅ Yes |
| JSON File | ⚡⚡⚡ Fast | ❌ No | ❌ No | ✅ Yes |
| REST API | ⚡⚡ Medium | ✅ Once | ✅ Yes | ❌ No |
| Direct BigQuery | ⚡ Slow | ✅ Per User | ✅ Yes | ❌ No |

---

## 🆘 Support & Resources

### Internal Resources
- **BigQuery Console:** https://console.cloud.google.com/bigquery
- **Project:** wmt-assetprotection-prod
- **Documentation:** All `.md` files in this folder

### Google Cloud Documentation
- BigQuery API: https://cloud.google.com/bigquery/docs/reference/rest
- Authentication: https://cloud.google.com/docs/authentication
- Client Libraries: https://cloud.google.com/bigquery/docs/reference/libraries

---

## 🔄 Version History

**v1.0** (November 2025) - Initial consolidation
- Moved all BigQuery files to dedicated folder
- Created comprehensive documentation
- Established integration patterns

---

## 📝 Notes for Future Development

### Planned Enhancements
- [ ] Automated daily data refresh script
- [ ] Caching layer with TTL (Time To Live)
- [ ] WebSocket connection for real-time updates
- [ ] GraphQL API wrapper for flexible queries
- [ ] Docker container for REST service
- [ ] Monitoring and alerting for connection health

### Known Limitations
- Google Cloud SDK required for direct connections
- Browser-based connections have CORS restrictions
- BigQuery has daily query quotas
- Authentication tokens expire after 1 hour

---

**For questions or issues, consult the individual documentation files in this folder.**