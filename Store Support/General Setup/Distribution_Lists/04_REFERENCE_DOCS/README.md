# 📧 Distribution List Selector

## Overview

A comprehensive web-based tool for managing and composing emails to Walmart's **134,681+ distribution lists**. Data is automatically extracted from Active Directory daily and stored in BigQuery for fast, real-time access.

---

## 📖 Where to Start

1. **START_HERE.md** - 5-minute quick start
2. **README.md** - Full overview (this file)
3. **CODE_PUPPY_DEPLOYMENT_GUIDE.md** - Detailed deployment
4. **BIGQUERY_SETUP.md** - BigQuery configuration

**Everything is in**: `C:\Users\krush\Documents\VSCode\Spark-Playground\General Setup\Distribution_Lists\`

---

## Key Features

- 🔍 **Powerful Search** - Search by email, name, or description with instant results
- 🏷️ **Smart Filtering** - Filter by category and member count
- ⚡ **Type-Ahead Autocomplete** - Quickly find lists as you type
- ✅ **Multi-Select** - Select multiple lists with visual tags
- 📨 **One-Click Email** - Compose emails in Outlook Web
- 🔄 **Auto-Updated** - Daily refresh from Active Directory at 5:00 AM
- ☁️ **BigQuery Powered** - Fast queries, always current data
- 🔒 **AD Authentication** - Secure access via Code Puppy Pages

---

## 🚀 Quick Start

### Local Testing (5 Minutes)

```powershell
cd "C:\Users\krush\Documents\VSCode\Spark-Playground\General Setup\Distribution_Lists"
python -m http.server 8000
```

Open: **http://localhost:8000**

### Production Deployment

**Method 1: Cloud Run + Code Puppy** (Recommended):

1. **Deploy Backend API to Cloud Run**:
   ```powershell
   .\REDEPLOY.ps1
   ```

2. **Upload Frontend to Code Puppy**:
   - Upload `index.html` to Code Puppy Pages
   - Update API URL with Cloud Run service URL

3. **Test**:
   ```bash
   curl https://distribution-list-api-xxxxx.us-central1.run.app/health
   ```

**Method 2: Code Puppy Built-in API**:

See: **`CODE_PUPPY_DEPLOYMENT_GUIDE.md`** for detailed steps

### Redeployment (Updates)

When you update the API code:
```powershell
.\REDEPLOY.ps1
```

This redeploys to Cloud Run in 30-60 seconds. No downtime.

### Schedule Daily Updates

```powershell
.\setup_daily_schedule.ps1
```

This runs daily at 5:00 AM to extract DLs from AD and upload to BigQuery.

---

## 📊 Data Statistics

### Current Data (as of December 17, 2025)

**Total Distribution Lists**: 134,681
- **General**: 109,850 lists
- **Market**: 7,750 lists
- **Team**: 7,509 lists
- **Operations**: 3,847 lists
- **Support**: 2,392 lists
- **Management**: 1,858 lists
- **Region**: 1,475 lists

**BigQuery Table**: `wmt-assetprotection-prod.Store_Support_Dev.dl_catalog`

---

## 🗄️ BigQuery Configuration

**Project**: `wmt-assetprotection-prod`  
**Dataset**: `Store_Support_Dev`  
**Table**: `dl_catalog`

**Check data**:
```sql
SELECT COUNT(*) as total, MAX(last_updated) as last_update
FROM `wmt-assetprotection-prod.Store_Support_Dev.dl_catalog`
```

---

## 🔄 Daily Automation

The system automatically updates every day at 5:00 AM:

1. **Extract** - All distribution lists from Active Directory
2. **Upload** - To BigQuery table
3. **Cleanup** - Remove old CSV files (keeps 7 days)
4. **Log** - Everything to `logs/daily_update_YYYYMMDD.log`

**Setup once**:
```powershell
.\setup_daily_schedule.ps1
```

**Monitor**:
```powershell
Get-Content "logs\daily_update_*.log" | Select-Object -Last 50
```

---

## 📂 Project Files

### Frontend
- **`index.html`** - Web UI (BigQuery-only version)

### Backend APIs
- **`api_distribution_lists.py`** - Python/Flask API
- **`api_distribution_lists.js`** - Node.js API (alternative)

### Data Extraction
- **`extract_all_dls_optimized.py`** - Extract from Active Directory
- **`ad_group_extractor.py`** - Original OPS Support extractor

### BigQuery Integration
- **`upload_to_bigquery_simple.ps1`** - Upload to BigQuery via gcloud CLI

### Daily Automation
- **`daily_update_to_bigquery.ps1`** - Complete daily workflow
- **`setup_daily_schedule.ps1`** - Setup Windows Task Scheduler

### Documentation
- **`START_HERE.md`** - Quick start guide
- **`CODE_PUPPY_DEPLOYMENT_GUIDE.md`** - Deploy to Code Puppy Pages
- **`BIGQUERY_SETUP.md`** - BigQuery configuration
- **`SYSTEM_SPECIFICATION.md`** - Full system design

### Data Files
- **`all_distribution_lists.csv`** - Latest DL catalog
- **`all_distribution_lists_*.csv`** - Timestamped backups

---

## 🌐 Code Puppy Pages Deployment

### Files to Deploy
1. Upload `index.html` to Code Puppy Pages
2. Create API endpoint `/api/distribution-lists` using `api_distribution_lists.py`
3. Grant BigQuery access to Code Puppy service account

### Full Guide
See: **`CODE_PUPPY_DEPLOYMENT_GUIDE.md`**

---

## 🛠️ Manual Operations

### Extract DLs from AD
```powershell
python extract_all_dls_optimized.py
```

### Upload to BigQuery
```powershell
.\upload_to_bigquery_simple.ps1
```

### Run Complete Update
```powershell
.\daily_update_to_bigquery.ps1
```

### Test Scheduled Task
```powershell
Start-ScheduledTask -TaskName "DL_BigQuery_Daily_Update"
```

---

## 🆘 Troubleshooting

### Data Not Loading
Check BigQuery:
```sql
SELECT COUNT(*) FROM `wmt-assetprotection-prod.Store_Support_Dev.dl_catalog`
```

### API Not Working
Verify:
1. Route exists: `/api/distribution-lists`
2. Service account has BigQuery dataViewer role
3. Check browser console (F12) for errors

### Schedule Not Running
```powershell
Get-ScheduledTask -TaskName "DL_BigQuery_Daily_Update"
Get-Content "logs\daily_update_*.log" | Select-Object -Last 50
```

---

## 📚 Additional Documentation

| Document | Purpose |
|----------|---------|
| `START_HERE.md` | 5-minute quick start |
| `CODE_PUPPY_DEPLOYMENT_GUIDE.md` | Production deployment |
| `CODE_PUPPY_API_SETUP.md` | API endpoint setup |
| `BIGQUERY_SETUP.md` | BigQuery detailed configuration |
| `BIGQUERY_QUICK_START.md` | BigQuery quick reference |
| `SYSTEM_SPECIFICATION.md` | 16-week implementation plan |

---

## 📈 Performance

- **Load Time**: < 2 seconds for 134,681 lists
- **Search**: Instant client-side filtering
- **BigQuery Query**: ~1-2 seconds
- **Daily Update**: ~5 minutes (AD extraction + BigQuery upload)

---

## 🎉 Success!

Everything is ready. Choose your next step:

1. **Local Testing**: `python -m http.server 8000` → http://localhost:8000
2. **Schedule Updates**: `.\setup_daily_schedule.ps1`
3. **Deploy Production**: Follow `CODE_PUPPY_DEPLOYMENT_GUIDE.md`

---

**Last Updated**: December 17, 2025  
**Version**: 2.0 (BigQuery Integration)  
**Status**: ✅ Ready for Production
      "department": ""
    },
    ...
  ]
}
```

### 3. **Email List** (`email_list_YYYYMMDD_HHMMSS.txt`)
Simple one-email-per-line format for copy/paste into distribution lists.

```
ABrunner@walmart.com
ADAM.EDGAR@walmart.com
ADebrine@walmart.com
...
```

## Usage

### Run the Extractor

```bash
python ad_group_extractor.py
```

The script will:
1. Query both AD groups
2. Extract user details in parallel (10 concurrent workers)
3. Deduplicate across groups
4. Export all three formats
5. Print a summary

### Customize Groups

Edit the `main()` function in `ad_group_extractor.py`:

```python
groups = [
    "OPS_SUP_MARKET_TEAM",
    "OPS_SUP_REGION_TEAM",
    "YOUR_NEW_GROUP",  # Add more groups here
]
```

## Using the Email List for Distribution Lists

### Option 1: Microsoft 365 Web UI
1. Go to https://outlook.office365.com
2. Click "Groups" → "New Group"
3. Copy/paste emails from `email_list_*.txt`

### Option 2: PowerShell (Automated)

```powershell
# Read emails from file
$emails = Get-Content 'email_list_20251215_153336.txt'

# Create distribution list
New-DistributionGroup -Name "OPS_SUP_Market_DL" -DisplayName "OPS Support Market Team"

# Add members
$emails | foreach {
    Add-DistributionGroupMember -Identity "OPS_SUP_Market_DL" -Member $_
}
```

### Option 3: CSV Import
1. Use the CSV file with your bulk import tool
2. Filter by department, title, or group
3. Select subset of users

## Performance

- **Group Query**: ~5-10 seconds for both groups
- **User Detail Lookup**: ~3 minutes for 2,500+ users
- **Total Time**: ~4 minutes
- **Parallelization**: 10 concurrent threads (configurable)

## Next Steps

### Next Phase: Dashboard & Hierarchy Navigation

Once you confirm this data is good, we can build:

1. **Flask Web Dashboard**
   - Browse users by group
   - Filter by manager/hierarchy
   - Select subsets for bulk operations
   - Export filtered lists

2. **Automated Distribution List Creation**
   - Connect to MS 365 via Graph API
   - Auto-create/update DLs
   - Scheduled refreshes

3. **Hierarchy Drill-Down**
   - Show manager relationships
   - Select by reporting structure
   - View org charts

## Requirements

- Python 3.8+
- Windows (uses PowerShell DirectorySearcher)
- Connected to Walmart network
- Valid AD credentials

## Troubleshooting

### No emails found?
- Ensure you're on Walmart VPN
- Check user has valid email in AD
- Run: `powershell -NoProfile -Command "[adsisearcher]::new('(sAMAccountName=mclary)').FindOne()"`

### Timeout errors?
- Increase timeout in script: `timeout=5` → `timeout=10`
- Reduce worker threads: `max_workers=10` → `max_workers=5`

### Users missing email?
- Those 7 users may not have email set in AD
- Export CSV and manually look them up

## Questions?

Reach out! This is a living tool - we can expand it with more features as needed.

---

**Generated**: December 15, 2025  
**Created by**: Code Puppy 🐶