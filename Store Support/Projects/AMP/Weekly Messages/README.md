# Adobe Analytics to BigQuery Migration Pipeline

**Project Path**: `Store Support\Projects\AMP\Weekly Messages\`

**Overview**: Automated pipeline to load weekly Adobe Analytics reports (Weekly Messages FY27 + Playbook Hub) into BigQuery tables, enabling Tableau Prep auto-refresh workflows.

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [File Structure](#file-structure)
3. [Setup Instructions](#setup-instructions)
4. [How to Run](#how-to-run)
5. [Configuration](#configuration)
6. [Troubleshooting](#troubleshooting)
7. [BigQuery Validation Queries](#bigquery-validation-queries)
8. [Tableau Prep Integration](#tableau-prep-integration)
9. [Windows Task Scheduler](#windows-task-scheduler)
10. [FAQ](#faq)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+ installed on Windows
- `gcloud` CLI installed ([download](https://cloud.google.com/sdk/docs/install))
- GCP credentials configured (`gcloud auth application-default login`)
- Tableau Prep installed (optional, for Tableau integration)
- Admin rights to create Windows scheduled tasks

### Setup (5 minutes)

```powershell
# 1. Authenticate GCP (one-time setup)
gcloud auth application-default login
# (Browser opens → sign in → return to terminal)

# 2. Navigate to project folder
cd "Store Support\Projects\AMP\Weekly Messages"

# 3. Run deployment script (creates venv + installs deps + creates BQ tables + loads data)
powershell -NoProfile -ExecutionPolicy Bypass -File deploy_adobe_pipeline.ps1

# 4. Check logs
type logs\adobe_loader.log
```

**That's it!** The script handles:
- ✅ GCP authentication check
- ✅ BigQuery tables creation (Phase 0, automated)
- ✅ Python environment setup
- ✅ Data loading to BigQuery
- ✅ Validation & verification

### First Run (Fully Automated)

```powershell
# Navigate to project folder
cd "Store Support\Projects\AMP\Weekly Messages"

# Run deployment script (does everything automatically)
powershell -NoProfile -ExecutionPolicy Bypass -File deploy_adobe_pipeline.ps1

# This script will:
#   1. Check GCP credentials
#   2. Create BigQuery tables (if not exist) ← Phase 0, automatic
#   3. Install Python dependencies
#   4. Run data loader
#   5. Validate row counts in BigQuery
#   6. Show SUCCESS message

# Check logs if needed
type logs\adobe_loader.log
```

**What gets created automatically:**
- ✅ Datasets: `Weekly_Message_FY27`, `Playbook_Hub_Data`
- ✅ Tables: 3 tables with proper schema, partitioning, clustering
- ✅ Data: Loaded from Excel files in source folder
- ✅ Validation: Row counts verified in BigQuery

**No manual BigQuery work required!**

---

## 📁 File Structure

```
Store Support\Projects\AMP\Weekly Messages\
│
├── adobe_to_bigquery_loader.py         Main Python script (parses Excel → loads BigQuery)
├── adobe_config.yaml                    Configuration file (paths, GCP project, tables)
├── deploy_adobe_pipeline.ps1            Deployment script (setup + run + validate)
├── README.md                            This file
├── Phase1_create_bigquery_tables.sql    BigQuery table creation DDL
│
├── Docs\                                Reference documentation
│   └── [doc images go here]
│
├── logs\                                Execution logs
│   ├── adobe_loader.log                Main log file (updated each run)
│   └── [other logs]
│
└── tests\                               Test/validation resources (optional)
    ├── adobe_test_workflow.tflx         Tableau Prep test workflow (optional)
    └── [test data]
```

---

## 🔧 Setup Instructions

### Step 1: GCP Authentication

```powershell
# Run authentication command (only needed ONCE)
gcloud auth application-default login

# Browser will open → Sign in with your Walmart GCP account
# Accept permissions
# Return to terminal
```

**Verification**:
```powershell
# Check credentials file exists
$CredPath = "$env:APPDATA\gcloud\application_default_credentials.json"
Test-Path $CredPath  # Should return True
```

### Step 2: Automated BigQuery Setup

The deployment script automatically creates all BigQuery datasets and tables. **No manual BigQuery work needed!**

The `setup_bigquery_tables.py` script will:
- Create 2 datasets: `Weekly_Message_FY27` and `Playbook_Hub_Data`
- Create 3 tables with proper schema, partitioning, and clustering
- Skip if tables already exist

This runs automatically as **Phase 0** of the deployment script.

### Step 3: Verify Python Environment

```powershell
# Navigate to project folder
cd "Store Support\Projects\AMP\Weekly Messages"

# Run deployment with dry-run to check setup
powershell -NoProfile -ExecutionPolicy Bypass -File deploy_adobe_pipeline.ps1 -DryRun -SkipValidation
```

---

## ▶️ How to Run

### Manual Run (Testing)

```powershell
cd "Store Support\Projects\AMP\Weekly Messages"

# Option 1: Use deployment script (recommended)
powershell -NoProfile -ExecutionPolicy Bypass -File deploy_adobe_pipeline.ps1

# Option 2: Run Python script directly
.\venv\Scripts\Activate.ps1
python adobe_to_bigquery_loader.py
deactivate
```

### Check Logs

```powershell
# View log file in real-time
Get-Content logs\adobe_loader.log -Tail 50 -Wait

# Or open in text editor
notepad logs\adobe_loader.log
```

### Check Execution Results

```powershell
# Query BigQuery from terminal
bq query --project_id=wmt-assetprotection-prod --use_legacy_sql=false @

# Example queries in section below
```

---

## ⚙️ Configuration

### adobe_config.yaml

All settings in one place:

```yaml
source_files:
  weekly_messages_path: "C:\\Users\\krush\\...\\Weekly Messages Area Reports - Tables FY27.xlsx"
  playbook_hub_path: "C:\\Users\\krush\\...\\Playbook Hub and Active Playbooks - Weekly Report.xlsx"

gcp:
  project_id: "wmt-assetprotection-prod"
  location: "US"

bigquery:
  datasets:
    weekly_messages: "Weekly_Message_FY27"
    playbook_hub: "Playbook_Hub_Data"
  tables:
    weekly_devices: "bq_weekly_messages_devices"
    weekly_metrics: "bq_weekly_messages_metrics"
    playbook: "bq_playbook_hub_metrics"

logging:
  log_dir: "logs"
  log_file: "adobe_loader.log"
  log_level: "INFO"

execution:
  report_date_mode: "today"  # Use current date or parse from file
```

**To customize**:
- Edit `adobe_config.yaml` and change paths/settings
- Python loader automatically reads config on each run
- No code changes needed

---

## 🐛 Troubleshooting

### Error: "gcloud not found"

**Solution**: Install Google Cloud SDK
```powershell
# Download and install from: https://cloud.google.com/sdk/docs/install
# Or use Chocolatey:
choco install google-cloud-sdk
```

### Error: "Application-default credentials not found"

**Solution**: Run authentication
```powershell
gcloud auth application-default login
```

### Error: "Table not found: `wmt-assetprotection-prod.Weekly_Message_FY27.bq_weekly_messages_devices`"

**Solution**: Create BigQuery tables
1. Run `Phase1_create_bigquery_tables.sql` in BigQuery Console
2. Or run: `bq mk` commands (see Setup section)

### Error: "File not found: Weekly Messages Area Reports..."

**Solution**: Update paths in `adobe_config.yaml`
```yaml
source_files:
  weekly_messages_path: "C:\\actual\\path\\to\\file.xlsx"
```

### Error: "ModuleNotFoundError: No module named 'pandas'"

**Solution**: Install dependencies
```powershell
# Run deployment script to install all deps
powershell -NoProfile -ExecutionPolicy Bypass -File deploy_adobe_pipeline.ps1
```

### Loader runs but loads 0 rows

**Possible causes**:
1. Excel file format not matching expected structure
2. Column names don't match parser expectations
3. Missing sheet tabs

**Debug**:
1. Check logs: `type logs\adobe_loader.log`
2. Verify Excel file structure matches comments in `adobe_to_bigquery_loader.py`
3. Enable DEBUG logging in `adobe_config.yaml`: `log_level: "DEBUG"`

---

## 🔍 BigQuery Validation Queries

### Check Today's Data

```sql
-- Weekly Messages Devices
SELECT report_date, category, COUNT(*) as row_count, SUM(total_page_views) as total_views
FROM `wmt-assetprotection-prod.Weekly_Message_FY27.bq_weekly_messages_devices`
WHERE DATE(extracted_date) = CURRENT_DATE()
GROUP BY report_date, category
ORDER BY category;

-- Weekly Messages Metrics
SELECT report_date, category, COUNT(*) as row_count
FROM `wmt-assetprotection-prod.Weekly_Message_FY27.bq_weekly_messages_metrics`
WHERE DATE(extracted_date) = CURRENT_DATE()
GROUP BY report_date, category
ORDER BY category;

-- Playbook Hub
SELECT playbook_category, COUNT(*) as row_count, SUM(total_page_views) as total_views
FROM `wmt-assetprotection-prod.Playbook_Hub_Data.bq_playbook_hub_metrics`
WHERE DATE(extracted_date) = CURRENT_DATE()
GROUP BY playbook_category
ORDER BY playbook_category;
```

### Check Row Counts Over Time

```sql
-- Weekly Messages Devices (last 7 days)
SELECT DATE(extracted_date) as load_date, COUNT(*) as row_count
FROM `wmt-assetprotection-prod.Weekly_Message_FY27.bq_weekly_messages_devices`
WHERE DATE(extracted_date) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
GROUP BY load_date
ORDER BY load_date DESC;
```

### Sample Data Preview

```sql
-- Preview Weekly Messages Devices
SELECT * FROM `wmt-assetprotection-prod.Weekly_Message_FY27.bq_weekly_messages_devices`
LIMIT 10;

-- Preview Playbook Hub
SELECT * FROM `wmt-assetprotection-prod.Playbook_Hub_Data.bq_playbook_hub_metrics`
WHERE playbook_category = 'Valentines'
LIMIT 10;
```

---

## 📊 Tableau Prep Integration

### Connect Tableau Prep to BigQuery

1. **Open Tableau Prep**
2. **Create New Workflow** → Click "Add Connection" → Select **BigQuery**
3. **Fill in connection**:
   - Project ID: `wmt-assetprotection-prod`
   - Authentication: Use your GCP credentials
   - Click **Connect**
4. **Browse tables**:
   - Dataset: `Weekly_Message_FY27`
   - Tables: `bq_weekly_messages_metrics` or `bq_weekly_messages_devices`
5. **Load preview** to verify data

### Create Auto-Refresh Schedule

1. In Tableau Prep, right-click your workflow
2. Select **Schedule**
3. Set **Monday 8:00 AM** (Python loader runs Sunday 6:00 AM)
4. Enable **Auto-refresh**
5. Confirm in Tableau Prep Server schedule page

---

## 📅 Windows Task Scheduler

### Create Scheduled Task

```powershell
# Run as ADMINISTRATOR

# Define task parameters
$TaskName = "Adobe_Weekly_to_BigQuery_Loader"
$ScriptPath = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\AMP\Weekly Messages\deploy_adobe_pipeline.ps1"
$TriggerTime = "06:00:00"  # 6 AM

# Create trigger
$Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At $TriggerTime

# Create action
$Action = New-ScheduledTaskAction -Execute "powershell.exe" `
  -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$ScriptPath`""

# Create settings
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -RestartCount 2 -RestartInterval (New-TimeSpan -Minutes 15)

# Register task
Register-ScheduledTask -TaskName $TaskName -Trigger $Trigger -Action $Action `
  -Settings $Settings -RunLevel Highest -Force

Write-Host "Task created: $TaskName"
```

### Verify Task

```powershell
# Check if task exists
Get-ScheduledTask -TaskName "Adobe_Weekly_to_BigQuery_Loader"

# Run task manually
Start-ScheduledTask -TaskName "Adobe_Weekly_to_BigQuery_Loader"

# Check task history
Get-ScheduledTaskInfo -TaskName "Adobe_Weekly_to_BigQuery_Loader"
```

### Remove Task (if needed)

```powershell
Unregister-ScheduledTask -TaskName "Adobe_Weekly_to_BigQuery_Loader" -Confirm:$false
```

---

## ❓ FAQ

**Q: How often does the loader run?**  
A: Every Sunday at 6:00 AM (Windows Task Scheduler). Tableau Prep refreshes Monday 8:00 AM to consume the new data.

**Q: What if the same data is loaded twice?**  
A: The loader uses MERGE (upsert) logic. Loading the same data multiple times won't create duplicates—existing rows are updated.

**Q: Can I run the loader manually?**  
A: Yes! Run `deploy_adobe_pipeline.ps1` anytime. Good for testing or urgent updates.

**Q: Where are the logs stored?**  
A: `logs\adobe_loader.log` (auto-created, appended to each run)

**Q: How much data gets loaded?**  
A: ~1,500 rows for Weekly Messages devices, ~1,500 for metrics, ~5,000 for Playbook Hub (varies weekly)

**Q: What if Excel file is missing?**  
A: Loader logs error and exits. Check that Outlook VBA is saving files to the correct folder.

**Q: Can I change table names?**  
A: Yes, edit `adobe_config.yaml` and update the table name. Must match BigQuery table names exactly.

**Q: How do I debug parsing errors?**  
A: Set `log_level: "DEBUG"` in `adobe_config.yaml` to see detailed parsing logs.

**Q: Does this work with Excel 2016 or older?**  
A: Should work. Loader uses `openpyxl` library. Test with sample file first.

**Q: Can I add more data sources?**  
A: Yes! Modify `adobe_to_bigquery_loader.py` to add new file parsing functions. Follow the existing patterns.

**Q: What's the BigQuery cost?**  
A: Minimal. ~1 query operation per load (MERGE). ~$0.01-0.05 per run. No storage charges (partitioned tables).

---

## 📞 Support

**Issues?** Check:
1. Logs: `logs\adobe_loader.log`
2. Troubleshooting section above
3. BigQuery validation queries to confirm tables exist
4. GCP credentials: `gcloud auth list`

**Escalation**: Contact [your.email@walmart.com] with:
- Log file output (copy from `adobe_loader.log`)
- Error message
- Last successful run date

---

## 📝 Change Log

- **2026-03-26**: Initial release (Phase 1-4 implementation)
  - BigQuery datasets & tables created
  - Python loader script implemented
  - Deployment scripts and documentation added
  - Weekly Task Scheduler setup ready

---

**Last Updated**: March 26, 2026  
**Maintained By**: [Your Team]  
**Status**: ✅ Ready for Production
