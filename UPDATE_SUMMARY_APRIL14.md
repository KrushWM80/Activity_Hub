# AMP AutoFeed Validation - Updated Configuration Summary

**Updated**: April 14, 2026  
**Status**: Ready for deployment with admin access

## ✅ Updates Completed

### 1. ✓ Folder Structure Updated
- Changed from single combined folder to **two separate folders**:
  - **Folder 1**: `Inbox > ATC > Reports > AMP > Quick Base API Response Data`
  - **Folder 2**: `Inbox > ATC > Reports > AMP > Auto Feed`
- Updated `EmailFetcher` class to handle both folders
- Updated `analyze_amp_emails.py` to use new folder structure
- System auto-detects folder based on email type

### 2. ✓ Column-Specific Extraction
System now extracts and compares these exact columns:
- ✓ **AutoFeed Id** - Unique identifier for each autofeed
- ✓ **Message Title** - Name/title of the message
- ✓ **Stores** - Store identifiers/numbers
- ✓ **Anchor Walmart Week** - Week reference
- ✓ **Status** - Message/processing status

**Comparison Logic**:
- Records matched by `AutoFeed Id`
- Each column value compared field-by-field
- Discrepancies flagged with specific field names
- Missing/extra records tracked separately

### 3. ✓ CSV Report Generator Added
New module: `amp_autofeed_csv_reporter.py`

**Four CSV Report Types Generated**:

1. **daily_summary_[timestamp].csv**
   - Columns: Date, Status, QB_Records, AMP_Records, Match, Differences, Missing_in_AMP, Extra_in_AMP
   - One row per validation day
   - Shows PASS/FAIL status and counts

2. **discrepancies_[timestamp].csv**
   - Columns: Date, Type, AutoFeed_Id, Field, QB_Value, AMP_Value
   - Every discrepancy found with details
   - Types: "Missing in AMP", "Extra in AMP", "Field Difference"
   - Shareable with team for investigation

3. **records_comparison_[timestamp].csv**
   - Columns: AutoFeed_Id, Column, QB_Value, AMP_Value, Match, Last_Seen
   - Record-by-record comparison
   - Shows all target columns side-by-side
   - Default: Last 7 days, configurable

4. **trend_statistics_[timestamp].csv**
   - Columns: Metric, Value, Percentage
   - Summary: Pass rate, failure rate, error rate, total discrepancies
   - For trend analysis and executive reporting

### 4. ✓ CLI Commands Enhanced

New command in `amp_autofeed_orchestrator.py`:
```powershell
python .\amp_autofeed_orchestrator.py csv-report --days 90
```

### 5. ✓ PowerShell Functions Added

New PowerShell function: `Get-AMPCSVReports`
```powershell
Get-AMPCSVReports              # Generate for last 90 days
Get-AMPCSVReports -Days 30     # Generate for last 30 days
Get-AMPCSVReports -Days 365    # Generate for full year
```

---

## 📋 How to Deploy

### Prerequisites
- Admin access (confirmed: ✓ You have it)
- PowerShell as Administrator
- Outlook configured with correct folder structure

### Step 1: Run Setup (2 min)
```powershell
# In Administrator PowerShell
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope CurrentUser -Force
.\setup_amp_autofeed_validation.ps1
```

This will:
- Install Python dependencies
- Create scheduled tasks (daily + weekly)

### Step 2: Verify Folder Structure

Open Outlook and navigate to: **Inbox > ATC > Reports > AMP**

Look for these two folders:
- [ ] "Quick Base API Response Data"
- [ ] "Auto Feed"

If folder names are different, update them in `amp_autofeed_validation.py` (lines 53-56).

### Step 3: Test Manual Validation
```powershell
python .\amp_autofeed_orchestrator.py daily
```

Expected output:
```
Validation Status: PASS ✓
Data match verified
```

### Step 4: Test CSV Report Generation
```powershell
python .\amp_autofeed_orchestrator.py csv-report --days 7
```

Four CSV files should be created in: `amp_validation_logs/csv_reports/`

### Step 5: System Active
- Daily validation at **7:00 AM**
- Weekly CSV reports Monday **6:00 AM** (optional)
- Reports automatically saved to `amp_validation_logs/`

---

## 📊 Daily Workflow

### Morning (Auto)
1. 7:00 AM - System fetches both emails from Outlook
2. Extracts target columns from each
3. Compares AutoFeed Ids and field values
4. Logs results as JSON
5. (Optional) Sends you email with results

### Weekly (Manual or Scheduled)
```powershell
# On Monday or whenever you want to analyze:
Get-AMPCSVReports -Days 90
```

This creates 4 CSVs you can:
- View in Excel
- Filter by date/status
- Share with team
- Post to shared drive
- Import into dashboards

---

## 🔍 Check Results

### See Today's Status
```powershell
Get-AMPValidationStatus
```

### Open Logs Folder
```powershell
Open-AMPValidationLogs
```

### Generate CSV Report for Last Month
```powershell
Get-AMPCSVReports -Days 30
```

### Analyze What's Being Compared
```powershell
python .\analyze_amp_emails.py
```

---

## 📧 Optional: Email Reports

To receive daily HTML email reports of validation results:

```powershell
# Set environment variables
[Environment]::SetEnvironmentVariable("VALIDATION_SENDER_EMAIL", "your.email@gmail.com", "Machine")
[Environment]::SetEnvironmentVariable("VALIDATION_SENDER_PASSWORD", "app-specific-password", "Machine")

# Test
python .\amp_autofeed_orchestrator.py daily --send-email --recipient your.email@walmart.com
```

⚠️ For Gmail: Use app-specific password from Account Security settings, not your regular password.

---

## 🎯 Key Differences from Initial Setup

| Aspect | Before | After |
|--------|--------|-------|
| **Folders** | Single combined folder | Two separate folders |
| **Column Focus** | All data extracted | 5 specific columns only |
| **Comparison** | Generic data matching | Record-by-record with AutoFeed Id key |
| **Reports** | JSON + text | JSON + 4 CSV types |
| **Sharing** | Email/manual | Easy CSV export for stakeholders |
| **Analysis** | Historical trends | Detailed discrepancy reports + trends |

---

## 📂 Files Modified

1. ✓ `amp_autofeed_validation.py` - Folder paths + column extraction
2. ✓ `amp_autofeed_csv_reporter.py` - NEW! CSV generation
3. ✓ `amp_autofeed_orchestrator.py` - Added csv-report command
4. ✓ `analyze_amp_emails.py` - Updated for new folders
5. ✓ `AMP_VALIDATION_COMMANDS.ps1` - Added Get-AMPCSVReports
6. ✓ `README_AMP_AUTOFEED_VALIDATION.md` - Updated documentation
7. ✓ `QUICKSTART_AMP_AUTOFEED.txt` - Updated quick start guide

---

## 🚀 Next Steps

1. **Verify Outlook folders** match expected structure
2. **Run setup script** with admin PowerShell
3. **Test with**: `python .\amp_autofeed_orchestrator.py daily`
4. **Generate sample CSV**: `python .\amp_autofeed_orchestrator.py csv-report --days 7`
5. **System is now active** - runs daily at 7 AM

---

## 💾 Location of Everything

- **Scripts**: Current Activity_Hub folder
- **Logs**: `amp_validation_logs/` (auto-created)
- **CSV Reports**: `amp_validation_logs/csv_reports/`
- **Daily JSON**: `amp_validation_logs/daily_reports/`
- **Historical**: `amp_validation_logs/historical_report.txt`

---

**Ready to proceed?** Run the setup script with admin access!
