# 🚀 START HERE - Distribution List Selector

**5-Minute Quick Start Guide**

---

## What Is This?

A web-based tool to search, filter, and compose emails to Walmart's **134,681+ distribution lists**. Data is automatically updated daily from Active Directory and stored in BigQuery.

---

## 📂 Project Location

**Everything is in**: `C:\Users\krush\Documents\VSCode\Spark-Playground\General Setup\Distribution_Lists\`

---

## Quick Setup Options

### Option 1: Local Testing (Right Now)

```powershell
cd "C:\Users\krush\Documents\VSCode\Spark-Playground\General Setup\Distribution_Lists"
python -m http.server 8000
```

Then open: **http://localhost:8000**

### Option 2: Deploy to Code Puppy Pages (Production)

**Method A: Cloud Run + Code Puppy** (Recommended):

1. **Deploy Backend API**:
   ```powershell
   cd "C:\Users\krush\Documents\VSCode\Spark-Playground\General Setup\Distribution_Lists"
   .\REDEPLOY.ps1
   ```

2. **Upload Frontend**:
   - Upload `index.html` to Code Puppy Pages
   - Update API URL in `index.html` with Cloud Run service URL

3. **Test**:
   ```powershell
   # Test API
   curl https://distribution-list-api-xxxxx.us-central1.run.app/health
   
   # Hard refresh Code Puppy Page (Ctrl+Shift+R)
   ```

**Method B: Code Puppy Built-in API**:
- See: `CODE_PUPPY_DEPLOYMENT_GUIDE.md`

**Schedule Daily Updates**:
```powershell
.\setup_daily_schedule.ps1
```

---

## Key Files

| File | Purpose |
|------|---------|
| `index.html` | Frontend UI (BigQuery-only version) |
| `api_distribution_lists.py` | Backend API for Code Puppy |
| `api_distribution_lists.js` | Backend API (Node.js alternative) |
| `extract_all_dls_optimized.py` | Extract DLs from Active Directory |
| `upload_to_bigquery_simple.ps1` | Upload to BigQuery table |
| `daily_update_to_bigquery.ps1` | Complete daily automation |
| `setup_daily_schedule.ps1` | **Run once** to schedule updates |
| `REDEPLOY.ps1` | **Redeploy API** to Cloud Run |
| `REDEPLOY.sh` | **Redeploy API** (Linux/Mac) |

---

## BigQuery Configuration

**Project**: `wmt-assetprotection-prod`  
**Dataset**: `Store_Support_Dev`  
**Table**: `dl_catalog`  
**Full Path**: `wmt-assetprotection-prod.Store_Support_Dev.dl_catalog`

**Check if data exists**:
```sql
SELECT COUNT(*) as total, MAX(last_updated) as last_update
FROM `wmt-assetprotection-prod.Store_Support_Dev.dl_catalog`
```

Expected: **134,681+ rows**

---

## Daily Automation

### Setup (Run Once):
```powershell
.\setup_daily_schedule.ps1
```

This creates a Windows Task Scheduler job that runs **daily at 5:00 AM**:
1. Extracts all DLs from Active Directory
2. Uploads to BigQuery
3. Cleans up old files
4. Logs everything

### Test Immediately:
```powershell
# Open Task Scheduler
taskschd.msc

# Find: "DL_BigQuery_Daily_Update"
# Right-click → Run
```

### View Logs:
```powershell
Get-Content "logs\daily_update_*.log" | Select-Object -Last 50
```

---

## Features

✅ **Search** - By email, name, or description  
✅ **Filter** - By category (General, Market, Team, etc.) and size  
✅ **Autocomplete** - Type-ahead list selection  
✅ **Multi-select** - Select multiple DLs with visual tags  
✅ **Compose Email** - Opens Outlook Web with selected lists  
✅ **Pagination** - 50/100/250/500 per page  
✅ **Live Data** - Always current from BigQuery  

---

## Troubleshooting

### "No data loading"
- Check BigQuery table has data (run SQL above)
- Verify API endpoint is deployed
- Check browser console (F12) for errors

### "API endpoint not found"
- Confirm `/api/distribution-lists` route exists
- Check Code Puppy API configuration
- See: `CODE_PUPPY_DEPLOYMENT_GUIDE.md`

### "BigQuery upload failed"
- Run manually: `.\upload_to_bigquery_simple.ps1`
- Check logs: `logs\bigquery_upload_*.log`
- Verify gcloud CLI is authenticated

---

## Next Steps

1. ✅ **For Local Testing**: Run `python -m http.server 8000` → Open http://localhost:8000
2. ✅ **For Production**: Follow `CODE_PUPPY_DEPLOYMENT_GUIDE.md`
3. ✅ **For Daily Updates**: Run `.\setup_daily_schedule.ps1` once
4. ✅ **For Full Details**: Read `README.md`

---

## Quick Commands Reference

```powershell
# Test local server
python -m http.server 8000

# Extract DLs manually
python extract_all_dls_optimized.py

# Upload to BigQuery manually
.\upload_to_bigquery_simple.ps1

# Setup daily schedule (run once)
.\setup_daily_schedule.ps1

# View today's logs
Get-Content "logs\daily_update_$(Get-Date -Format 'yyyyMMdd').log"

# Check scheduled task
Get-ScheduledTask -TaskName "DL_BigQuery_Daily_Update"
```

---

## Support

- **Full Documentation**: `README.md`
- **Deployment Guide**: `CODE_PUPPY_DEPLOYMENT_GUIDE.md`
- **BigQuery Setup**: `BIGQUERY_SETUP.md`
- **API Reference**: `CODE_PUPPY_API_SETUP.md`

---

**Ready to go!** 🎉

Start with local testing, then deploy to Code Puppy Pages when ready.
