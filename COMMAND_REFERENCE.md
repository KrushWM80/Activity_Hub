# AMP AutoFeed Validation - Quick Command Reference

## 🚀 First Time Setup (Do This First)

```powershell
# Run as Administrator
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope CurrentUser -Force
.\setup_amp_autofeed_validation.ps1
```

**Wait for all installs to complete. You'll see ✓ checkmarks for each component.**

---

## ⚠️ BEFORE RUNNING: Verify Folder Structure

**Required Outlook Folders:**
```
Inbox
  └─ ATC
      └─ Reports
          └─ AMP
              ├─ Quick Base API Response Data  ← QuickBase sends here
              └─ Auto Feed                       ← AMP processes here
```

**Cannot proceed without these exact folders!** If different, post the actual folder names and we'll update the script.

---

## ✅ Verify Setup (Do This After Setup)

```powershell
# Load PowerShell helper functions
. .\AMP_VALIDATION_COMMANDS.ps1

# Check if scheduled tasks were created
Get-AMPScheduledTasks

# Should show:
# ✓ AMP-AutoFeed-DailyValidation (runs daily at 7:00 AM)
# ✓ AMP-AutoFeed-WeeklyReport (runs Monday at 6:00 AM)
```

---

## 🔄 Daily Workflows

### Run Validation Immediately
```powershell
. .\AMP_VALIDATION_COMMANDS.ps1
Start-AMPValidation
```

Output shows: `PASS` or `FAIL` with details

### Run Validation + Send Email Report
```powershell
Start-AMPValidation -SendEmail -Recipient "your.email@walmart.com"
```

(Requires email config - see Email Setup section)

### Check Latest Results
```powershell
Get-AMPValidationStatus
```

Shows recent 7 days of validation results

### Analyze What's Being Compared
```powershell
python .\analyze_amp_emails.py
```

Shows the exact columns and values extracted from today's emails

---

## 📊 Weekly/Comprehensive Analysis

### Generate CSV Reports (Best for Sharing)
```powershell
Get-AMPCSVReports
# OR
Get-AMPCSVReports -Days 30
# OR  
Get-AMPCSVReports -Days 90
```

**Creates 4 CSV files:**
1. `daily_summary_*.csv` - Summary of each day
2. `discrepancies_*.csv` - All issues found
3. `records_comparison_*.csv` - Record-by-record comparison
4. `trend_statistics_*.csv` - Pass rate, error rate, etc.

**Location:** `amp_validation_logs/csv_reports/`

### View Reports in Excel
```powershell
Start amp_validation_logs/csv_reports/
```

Open any CSV in Excel, apply filters, analyze

### Generate Text Report
```powershell
Get-AMPHistoricalReport
# OR
Get-AMPHistoricalReport -Days 30
```

Creates `historical_report.txt` with human-readable summary

---

## 📁 Access Results

### View Today's Detailed Report
```powershell
cat amp_validation_logs/daily_reports/validation_$(Get-Date -Format 'yyyy-MM-dd').json
```

### Open All Logs
```powershell
Open-AMPValidationLogs
```

Folder opens: `amp_validation_logs/` with all reports

### Raw JSON History
```powershell
cat amp_validation_logs/validation_history.json
```

Complete history of all validations

---

## 📧 Email Setup (Optional)

### For Gmail
```powershell
# 1. Go to: myaccount.google.com
# 2. Security > App passwords > Create password for "Mail"
# 3. Copy the generated password

# 4. Set in PowerShell (Admin):
[Environment]::SetEnvironmentVariable("VALIDATION_SENDER_EMAIL", "your.email@gmail.com", "Machine")
[Environment]::SetEnvironmentVariable("VALIDATION_SENDER_PASSWORD", "generated-password-here", "Machine")

# 5. Test:
python .\amp_autofeed_orchestrator.py daily --send-email --recipient your.email@walmart.com
```

### For Outlook/Office365
```powershell
[Environment]::SetEnvironmentVariable("VALIDATION_SENDER_EMAIL", "your.email@walmart.com", "Machine")
[Environment]::SetEnvironmentVariable("VALIDATION_SENDER_PASSWORD", "your-office-password", "Machine")
[Environment]::SetEnvironmentVariable("VALIDATION_SMTP_SERVER", "smtp-mail.outlook.com", "Machine")

# Test:
python .\amp_autofeed_orchestrator.py daily --send-email --recipient your.email@walmart.com
```

---

## 🔧 Manual Commands (If Not Using PowerShell Functions)

```powershell
# Daily validation
python .\amp_autofeed_orchestrator.py daily

# Check status
python .\amp_autofeed_orchestrator.py status

# Generate CVS reports (last 90 days)
python .\amp_autofeed_orchestrator.py csv-report

# Generate CSV reports for specific period
python .\amp_autofeed_orchestrator.py csv-report --days 30

# Generate historical text report
python .\amp_autofeed_orchestrator.py historical --days 90

# Analyze today's emails
python .\analyze_amp_emails.py
```

---

## ❌ Troubleshooting

### Error: "Folder not found"
- Check Outlook for correct folders
- Verify folder names exactly match:
  - `Quick Base API Response Data`
  - `Auto Feed`
- If different, edit `amp_autofeed_validation.py` lines 50-56

### Error: "No emails found"
- Both emails must exist in Outlook from TODAY
- Check emails went to correct folders
- Run analyzer to debug: `python .\analyze_amp_emails.py`

### Error: "pywin32_postinstall failed"
- Run setup again with admin PowerShell
- Or manually: 
  ```powershell
  python -m pip install --upgrade pywin32
  python -m pip install pypiwin32
  $path = python -c "import sys; print(sys.executable -replace 'python.exe', '')"
  & "$path\Scripts\pywin32_postinstall.py" -install
  ```

### Email not sending
- Check environment variables are set:
  ```powershell
  $env:VALIDATION_SENDER_EMAIL
  $env:VALIDATION_SENDER_PASSWORD
  ```
- For Gmail: Must use app-specific password (not regular password)
- Check SMTP server is correct

---

## 📅 Automated Schedule (No Action Needed)

These run automatically after setup:

**Daily at 7:00 AM:**
- Validates both emails
- Logs results
- (Optional) Sends email if configured

**Weekly Monday at 6:00 AM:**
- Analyzes last 90 days
- Generates historical report
- Creates CSV exports

View scheduled tasks:
```powershell
Get-ScheduledTask -TaskName "AMP-AutoFeed-*" | Select-Object TaskName, State, LastRunTime
```

---

## 📊 CSV Reports Explained

### daily_summary.csv
```
Date       | Status | QB_Records | AMP_Records | Match | Differences
2026-04-14 | PASS   | 150        | 150         | Yes   | None
2026-04-13 | FAIL   | 148        | 150         | No    | Missing in AMP: 2
```

### discrepancies.csv
```
Date       | Type                 | AutoFeed_Id | Field        | QB_Value | AMP_Value
2026-04-13 | Missing in AMP       | 456         | N/A          | Present  | Missing
2026-04-13 | Field Difference     | 789         | Status       | Active   | Pending
```

### records_comparison.csv
```
AutoFeed_Id | Column              | QB_Value           | AMP_Value          | Match
123         | AutoFeed Id         | 123                | 123                | Yes
123         | Message Title       | Weekly Promo       | Weekly Promo       | Yes
123         | Stores              | 1001-2050          | 1001-2050          | Yes
123         | Anchor Walmart Week | Week 15            | Week 14            | No
```

### trend_statistics.csv
```
Metric                    | Value | Percentage
Total Validations         | 87    | 100%
Passed                    | 84    | 96.6%
Failed                    | 2     | 2.3%
Errors                    | 1     | 1.1%
Total Discrepancies Found | 5     | N/A
```

---

## 🎯 Typical Usage Pattern

### Morning
- System auto-validates at 7:00 AM
- Check email if configured

### Weekly (Monday)
- System auto-generates CSV reports at 6:00 AM
- OR run manually: `Get-AMPCSVReports -Days 7`

### Before Meetings
```powershell
# Quick status check
Get-AMPValidationStatus

# Generate detailed CSV to share
Get-AMPCSVReports -Days 30

# Open folder to select CSV files
Open-AMPValidationLogs
```

### Monthly Review
```powershell
# Full month analysis
Get-AMPCSVReports -Days 30

# Or specific lookback
Get-AMPCSVReports -Days 365  # Full year
```

---

## 📞 Support

1. **Check docs:** `README_AMP_AUTOFEED_VALIDATION.md`
2. **Run analyzer:** `python .\analyze_amp_emails.py`
3. **Check logs:** Open `amp_validation_logs/`
4. **Review errors:** Check latest JSON in `daily_reports/`

---

**System is ready to deploy with admin access!** 🚀
