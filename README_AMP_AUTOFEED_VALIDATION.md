# AMP AutoFeed Daily Validation System

## Overview

This system automatically validates that the data from your two daily emails are consistent:
1. **QuickBase API Response Data** - What QuickBase sends to AMP
2. **Processed AutoFeed Details** - What AMP reports receiving

The system:
- ✅ Runs daily validation and compares the two emails
- ✅ Detects discrepancies and logs them
- ✅ Generates daily HTML email reports
- ✅ Creates historical analysis reports (last year of data)
- ✅ Identifies patterns of issues over time

## Setup Instructions

### Step 1: Install Python Dependencies

Run this PowerShell command as Administrator:

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope CurrentUser -Force
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"
.\setup_amp_autofeed_validation.ps1
```

This will install:
- `beautifulsoup4` - HTML parsing
- `pywin32` - Outlook COM integration

### Step 2: Verify Outlook Folder Structure

The system expects emails in TWO separate folders:

**Folder 1 - QuickBase API Response Data:**
```
Inbox > ATC > Reports > AMP > Quick Base API Response Data
```

**Folder 2 - AMP AutoFeed Details:**
```
Inbox > ATC > Reports > AMP > Auto Feed
```

⚠️ **Important**: Verify this exact folder structure in Outlook. If your folders are different, update the folder names in the script (see Troubleshooting section).

### Columns Being Compared

The system extracts and compares these specific columns from both emails:
- `AutoFeed Id` - Unique identifier for each autofeed
- `Message Title` - Title/name of the message
- `Stores` - Store numbers/identifiers
- `Anchor Walmart Week` - Week reference
- `Status` - Processing or delivery status

Any discrepancies in these columns across the two emails will be flagged.

### Step 3: Quick Test

Run a manual validation first:

```powershell
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"
python .\amp_autofeed_orchestrator.py daily
```

Expected output:
```
======================================================================
AMP AutoFeed Daily Validation
======================================================================
Started: 2026-04-14T09:00:00.123456

Fetching QuickBase API Response email...
Found QuickBase email: [timestamp]
Fetching AMP AutoFeed Details email...
Found AMP email: [timestamp]

Validation Status: PASS
✓ Data match verified

======================================================================
```

### Step 4: Check Log Files

After first run, examine:
- `amp_validation_logs/validation_history.json` - All validations
- `amp_validation_logs/daily_reports/validation_YYYY-MM-DD.json` - Today's report
- `amp_validation_logs/historical_report.json` - Historical analysis

### Step 5: Optional - Configure Email Reports

To receive daily email reports, set these environment variables:

**Windows Command Prompt (Admin):**
```cmd
setx VALIDATION_SENDER_EMAIL "your.email@gmail.com"
setx VALIDATION_SENDER_PASSWORD "your-app-specific-password"
setx VALIDATION_SMTP_SERVER "smtp.gmail.com"
```

**Or in PowerShell (Admin):**
```powershell
[Environment]::SetEnvironmentVariable("VALIDATION_SENDER_EMAIL", "your.email@gmail.com", "Machine")
[Environment]::SetEnvironmentVariable("VALIDATION_SENDER_PASSWORD", "your-app-specific-password", "Machine")
[Environment]::SetEnvironmentVariable("VALIDATION_SMTP_SERVER", "smtp.gmail.com", "Machine")
```

⚠️ **For Gmail**: You CANNOT use your regular password. You must:
1. Enable 2-Factor Authentication on your Google Account
2. Generate an [App-Specific Password](https://myaccount.google.com/apppasswords)
3. Use that password above

⚠️ **For Outlook/Office365**: Contact your IT department about SMTP relay or use your regular office password with `smtp-mail.outlook.com:587`

## Usage

### Daily Validation (Manual)
```powershell
python .\amp_autofeed_orchestrator.py daily
```

### Daily Validation with Email Report
```powershell
python .\amp_autofeed_orchestrator.py daily --send-email --recipient your.email@walmart.com
```

### Generate Historical Report
```powershell
python .\amp_autofeed_orchestrator.py historical --days 90
```

### Generate CSV Reports (for comprehensive analysis)
```powershell
# Generate all CSV reports (last 90 days)
python .\amp_autofeed_orchestrator.py csv-report

# Generate reports for specific period
python .\amp_autofeed_orchestrator.py csv-report --days 30
```

CSV files will be saved to: `amp_validation_logs/csv_reports/`

### Check Recent Status
```powershell
python .\amp_autofeed_orchestrator.py status
```

## Automated Daily Runs

The setup script creates two scheduled tasks:

### 1. Daily Validation - 7:00 AM
- **Task Name**: `AMP-AutoFeed-DailyValidation`
- **Frequency**: Daily at 7:00 AM
- **Action**: Runs validation and logs results

Verify it exists:
```powershell
Get-ScheduledTask -TaskName "AMP-AutoFeed-DailyValidation" | Select-Object TaskName, State
```

### 2. Weekly Historical Report - Monday 6:00 AM
- **Task Name**: `AMP-AutoFeed-WeeklyReport`
- **Frequency**: Every Monday at 6:00 AM
- **Action**: Runs full validation + generates weekly historical report

## Reports

### Daily Report (JSON)
File: `amp_validation_logs/daily_reports/validation_2026-04-14.json`

Contains:
- Date and timestamp
- Email found status for both sources
- Extracted data from both emails (with focus on target columns)
- Comparison results
- Pass/Fail status
- Count of records in each email
- Details of any discrepancies

### CSV Reports (Comprehensive Analysis)
Generated by: `python .\amp_autofeed_orchestrator.py csv-report`

Location: `amp_validation_logs/csv_reports/`

Four CSV files are generated:

**1. daily_summary_[timestamp].csv**
- Columns: Date, Status, QB_Records, AMP_Records, Match, Differences, Missing_in_AMP, Extra_in_AMP
- Shows daily validation results in tabular format
- Easy to import into Excel or other tools for analysis

**2. discrepancies_[timestamp].csv**
- Columns: Date, Type, AutoFeed_Id, Field, QB_Value, AMP_Value
- Lists every discrepancy found
- Types: "Missing in AMP", "Extra in AMP", "Field Difference"
- Useful for identifying specific issues

**3. records_comparison_last[N]d_[timestamp].csv**
- Columns: AutoFeed_Id, Column, QB_Value, AMP_Value, Match, Last_Seen
- Shows actual record values from both emails
- Compares all target columns side-by-side
- Default: last 7 days of data

**4. trend_statistics_[N]d_[timestamp].csv**
- Columns: Metric, Value, Percentage
- Summary statistics: total validations, pass rate, failure rate, error rate
- Helpful for trend analysis and executive reporting

### Historical Report (Text)
File: `amp_validation_logs/historical_report.txt`

Example output:
```
AMP AutoFeed Validation - Historical Report
Generated: 2026-04-14T14:30:00.123456
Period: Last 90 days

=== Summary ===
Total Validations: 87
Passed: 84
Failed: 3
Errors: 0

=== Discrepancies Found ===

Date: 2026-04-10
  - Record count mismatch: QB=150, AMP=148
  - Missing in AMP: 2 records (IDs: 456, 789)
  - Field 'Status' differs in 1 records

Date: 2026-03-28
  - Record count mismatch: QB=205, AMP=203
```

## Email Report Format

Automated email reports include:
- ✓/✗ Email found status
- Validation result (PASS/FAIL/ERROR)
- Discrepancies list (if any)
- Data summary (tables/lists found)
- Color-coded status badge

## Troubleshooting

### "Folder not found" Error
**Problem**: `KeyError: 'ATC'` or similar when running validation

**Most Common Issue**: Email folder structure doesn't match expected path

**Solution**:
1. Open Outlook
2. Navigate to: Inbox > ATC > Reports > AMP
3. Verify these two folders exist:
   - "Quick Base API Response Data"
   - "Auto Feed"
4. If folder names are different, you need to update them in `amp_autofeed_validation.py`

**To fix in the script:**
```python
# In amp_autofeed_validation.py, look for this section:
if folder_name is None:
    if "Quick Base" in subject_pattern or "QuickBase" in subject_pattern:
        folder_name = "Quick Base API Response Data"  # <- Update this name if needed
    else:
        folder_name = "Auto Feed"  # <- Or update this name
```

Replace the names with your actual folder names from Outlook.

**Debug: List Available Folders**

Run this to see what folders exist:
```powershell
python .\analyze_amp_emails.py
```

The error message will list the available folders, helping you find the correct names.

### "pywin32_postinstall failed" Error
**Problem**: Outlook COM access not working

**Solution**:
```powershell
# Run in admin PowerShell
python -m pip install pywin32
python -m pip install pypiwin32
$pythonPath = python -c "import sys; print(sys.executable -replace 'python.exe', '')"
& "$pythonPath\Scripts\pywin32_postinstall.py" -install
```

### "No QuickBase email found" Error
**Problem**: Email not retrieved even though it exists

**Possible causes**:
1. Wrong folder path (see Troubleshooting #1)
2. Email subject doesn't match pattern
3. Email is from a different sender
4. Email is older than 24 hours

**Solution**:
- Verify email subject contains: "Quick Base API Response"
- Check email date is from today
- Manually copy email subject and update search pattern

### Email Report Not Sending
**Problem**: Report generated but email not sent

**Solution**:
1. Verify environment variables set:
   ```powershell
   $env:VALIDATION_SENDER_EMAIL
   $env:VALIDATION_SENDER_PASSWORD
   $env:VALIDATION_SMTP_SERVER
   ```

2. Test SMTP connection:
   ```powershell
   python
   >>> import smtplib
   >>> smtplib.SMTP("smtp.gmail.com", 587).starttls()
   >>> # Should connect without error
   ```

3. Check that you're using app-specific password (if Gmail)

## Data Comparison Logic

The system compares the two emails by:

1. **Email Presence**: Both emails must exist in their respective folders
2. **Record Extraction**: Extracts records from tables with target columns:
   - AutoFeed Id
   - Message Title
   - Stores
   - Anchor Walmart Week
   - Status
3. **Record Count**: Number of records must match
4. **Record Matching**: Uses AutoFeed Id as unique key to match records
5. **Field Comparison**: Each target field is compared across both emails
6. **Content Hashing**: Full content hash is computed for overall change detection

### Matching Rules

| Check | Match Criteria | Fail If |
|-------|---|---|
| **Emails Found** | Both emails exist | Either email missing |
| **Record Count** | QB records = AMP records | Counts differ |
| **Record IDs** | Same AutoFeed Ids in both | IDs missing or extra |
| **Field Values** | Each field matches exactly | Any field differs |
| **Content Hash** | SHA256 hash identical | Content differs |

### What Triggers a FAIL

The validation fails if any of these occur:
- ❌ QuickBase email not found
- ❌ AMP email not found  
- ❌ Record counts don't match
- ❌ AutoFeed Ids differ between emails
- ❌ Any target column value differs

## API/Integration Points

### If You Want to Integrate With Other Systems

#### Read Validation Results Programmatically
```python
import json
from pathlib import Path

report_file = Path("amp_validation_logs/daily_reports/validation_2026-04-14.json")
with open(report_file) as f:
    result = json.load(f)

print(f"Status: {result['status']}")
if result['status'] == 'FAIL':
    for diff in result['comparison']['differences']:
        print(f"  - {diff}")
```

#### Send Custom Report
```python
from amp_autofeed_email_reporter import send_validation_report

send_validation_report(
    recipient_email="alert@example.com",
    date="2026-04-14"
)
```

#### Query Historical Issues
```python
import json
from pathlib import Path

with open("amp_validation_logs/validation_history.json") as f:
    history = json.load(f)

issues = {date: result for date, result in history.items() if result['status'] != 'PASS'}
print(f"Found {len(issues)} days with issues")
```

## Files Created

```
Activity_Hub/
├── amp_autofeed_validation.py           # Core validation logic
├── amp_autofeed_email_reporter.py       # Email report generation
├── amp_autofeed_csv_reporter.py         # CSV report generation
├── amp_autofeed_orchestrator.py         # Main entry point
├── analyze_amp_emails.py                # Email data analyzer
├── setup_amp_autofeed_validation.ps1    # Setup script
├── AMP_VALIDATION_COMMANDS.ps1          # PowerShell helpers
├── README_AMP_AUTOFEED_VALIDATION.md    # This file
└── amp_validation_logs/                 # Auto-created
    ├── validation_history.json          # All validations
    ├── historical_report.json           # Historical analysis (JSON)
    ├── historical_report.txt            # Historical analysis (text)
    ├── config.json                      # Configuration
    ├── csv_reports/                     # CSV reports for sharing
    │   ├── daily_summary_[timestamp].csv
    │   ├── discrepancies_[timestamp].csv
    │   ├── records_comparison_[timestamp].csv
    │   └── trend_statistics_[timestamp].csv
    └── daily_reports/
        ├── validation_2026-04-13.json
        ├── validation_2026-04-14.json
        └── ...more daily reports...
```

## Next Steps

1. ✅ Run setup script (Step 1)
2. ✅ Verify Outlook folders (Step 2)
3. ✅ Test manually (Step 3)
4. ✅ Check logs (Step 4)
5. ✅ Configure email (Step 5)
6. 📍 Automated tasks now run daily
7. ⏰ Review weekly reports from scheduled task

## Monitoring the System

### Daily Check
```powershell
# Check if automated task ran
Get-ScheduledTask -TaskName "AMP-AutoFeed-DailyValidation" | Select-Object LastRunTime, LastTaskResult

# View today's results
Get-Content "amp_validation_logs/daily_reports/validation_$(Get-Date -Format 'yyyy-MM-dd').json"
```

### Weekly Review
```powershell
# Read historical report after Monday morning run
Get-Content "amp_validation_logs/historical_report.txt"
```

## Support & Questions

For issues or enhancements:
1. Check Troubleshooting section above
2. Review detailed logs in `amp_validation_logs/`
3. Verify Outlook folder structure
4. Test manual run: `python .\amp_autofeed_orchestrator.py daily`

---

**Version**: 1.0  
**Last Updated**: April 14, 2026  
**System**: AMP AutoFeed Validation
