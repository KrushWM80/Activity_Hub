# 🚀 Quick Start - Adobe Analytics to BigQuery

**Everything is automated. Just run one command.**

---

## ⚡ 3 Steps (5 minutes)

### Step 1: Authenticate GCP (One-Time)

```powershell
gcloud auth application-default login
```

A browser window opens → Sign in with your Walmart GCP account → Accept permissions → Done

### Step 2: Navigate to Project Folder

```powershell
cd "Store Support\Projects\AMP\Weekly Messages"
```

### Step 3: Run Setup (Everything Automatic)

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File deploy_adobe_pipeline.ps1
```

**What this command does:**
- ✅ Creates BigQuery datasets & tables (if not exist)
- ✅ Installs Python dependencies
- ✅ Loads data from Excel files
- ✅ Validates everything in BigQuery
- ✅ Shows SUCCESS message

---

## 📊 Check Results

### View Logs
```powershell
type logs\adobe_loader.log
```

### Query BigQuery
Open BigQuery Console: https://console.cloud.google.com/bigquery?project=wmt-assetprotection-prod

Tables created:
- `Weekly_Message_FY27.bq_weekly_messages_devices`
- `Weekly_Message_FY27.bq_weekly_messages_metrics`
- `Playbook_Hub_Data.bq_playbook_hub_metrics`

Sample query:
```sql
SELECT report_date, category, COUNT(*) as rows
FROM `wmt-assetprotection-prod.Weekly_Message_FY27.bq_weekly_messages_devices`
WHERE DATE(extracted_date) = CURRENT_DATE()
GROUP BY report_date, category
```

---

## 🔄 Run Weekly (After Setup)

Every Sunday 6:00 AM automatically (Task Scheduler setup in PHASE3_4_SETUP_GUIDE.md)

Or run manually anytime:
```powershell
cd "Store Support\Projects\AMP\Weekly Messages"
powershell -NoProfile -ExecutionPolicy Bypass -File deploy_adobe_pipeline.ps1
```

---

## ❓ Issues?

1. **"gcloud not found"** → Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install

2. **"Permission denied"** → Run PowerShell as Administrator

3. **"Table not found"** → The setup script auto-creates tables. If you see this error, check logs and run setup again.

4. **Other issues** → Check file: `logs\adobe_loader.log`

**For detailed setup & troubleshooting**: Read `README.md`

---

**That's it! You're done with automation setup. Next: Set up Tableau Prep (see PHASE3_4_SETUP_GUIDE.md)**
