# AMP AutoFeed Daily Validation - Updated Workflow (April 15, 2026)

## Daily Schedule

| Time | Step | Component | Status |
|------|------|-----------|--------|
| 4:00 AM | Emails arrive | Outlook | Automated |
| ~4:05 AM | VB exports HTML | Your automation | Manual setup needed |
| 5:00 AM | Python validates | Scheduled task | Automated (NEW TIME) |

## What Happens at Each Step

### 4:00 AM - Emails Arrive
- QuickBase API Response Data email arrives in Outlook
- AMP AutoFeed email arrives in Outlook
- No action needed - automatic

### ~4:05 AM - VB Extracts and Saves HTML
Your VB script should:
1. Open the "Quick Base API Response Data" email
2. Copy the HTML body (the table content)
3. Save to: `C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\amp_autofeed_data\quickbase_responses.html`
4. Do the same for "Auto Feed" email
5. Save to: `C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\amp_autofeed_data\amp_autofeed.html`

**Important**: The VB script must save the email body as HTML (preserves table structure)

### 5:00 AM - Python Validation Runs
Scheduled task automatically executes `amp_run_daily.bat` which:
1. Reads both HTML files
2. Parses tables to extract these columns:
   - AutoFeed Id
   - Message Title
   - Stores
   - Anchor Walmart Week
   - Status
3. Matches records by AutoFeed Id
4. Compares field values
5. Logs results to: `amp_validation_logs\daily_execution.log`

## System Files

### Data Folder
```
amp_autofeed_data/
├── quickbase_responses.html    (VB saves here)
└── amp_autofeed.html           (VB saves here)
```

### Python Scripts
- `amp_autofeed_validation.py` - Main validation engine (NEW VERSION: reads HTML files)
  - `EmailFetcher` - Reads HTML files from disk
  - `HTMLEmailParser` - Parses HTML tables
  - `AutoFeedValidator` - Compares records
  - `validate_daily()` - Main function
  
- `amp_run_daily.bat` - Wrapper batch file (runs at 5:00 AM)

### Scheduled Tasks
- **AMP-AutoFeed-DailyValidation** - Runs daily at 5:00 AM
  - User: HOMEOFFICE\Dev-krush
  - Command: `amp_run_daily.bat`
  - Log file: `amp_validation_logs\daily_execution.log`

## How to Set Up the Scheduled Task

**Note**: Already configured to run at 5:00 AM. Just verify it's enabled.

1. Open Windows Task Scheduler
2. Find: "AMP-AutoFeed-DailyValidation"
3. Verify:
   - Enabled: Yes
   - Trigger: Daily at 5:00 AM
   - Action: `C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\amp_run_daily.bat`

## Manual Testing

To test without waiting for scheduled time:

```powershell
# Open PowerShell in Activity_Hub folder

# First, create test HTML files
echo "<table><tr><th>AutoFeed Id</th><th>Message Title</th><th>Stores</th><th>Anchor Walmart Week</th><th>Status</th></tr><tr><td>123</td><td>Test</td><td>Store 1</td><td>Week 1</td><td>Pending</td></tr></table>" > amp_autofeed_data\quickbase_responses.html

# Do same for AMP file
echo "<table><tr><th>AutoFeed Id</th><th>Message Title</th><th>Stores</th><th>Anchor Walmart Week</th><th>Status</th></tr><tr><td>123</td><td>Test</td><td>Store 1</td><td>Week 1</td><td>Pending</td></tr></table>" > amp_autofeed_data\amp_autofeed.html

# Run validation manually
& ".\.venv\Scripts\python.exe" amp_autofeed_validation.py
```

## Expected Output

```
============================================================
AMP AutoFeed Daily Validation - 2026-04-15 05:00:00
============================================================
✓ Data directory: amp_autofeed_data
✓ Loaded quickbase_responses.html (1234 bytes)
✓ QuickBase: 42 records
✓ Loaded amp_autofeed.html (1245 bytes)
✓ AMP AutoFeed: 42 records

------------------------------------------------------------
VALIDATION RESULTS
------------------------------------------------------------
QuickBase records: 42
AMP records: 42
Matched: 42
QuickBase only: 0
AMP only: 0
Field mismatches: 0

Validation Status: PASS
============================================================
```

## Troubleshooting

### Files Not Found Error
```
FileNotFoundError: HTML file not found: amp_autofeed_data/quickbase_responses.html
VB should save email HTML bodies here daily at ~4:05 AM
```
**Solution**: Verify VB script is running and saving files at correct paths

### No Records Found
- Check that HTML files contain `<table>` tags
- Verify column headers match target columns (case-insensitive)
- Look for data rows after header row

### Scheduled Task Not Running
1. Open Task Scheduler
2. Right-click "AMP-AutoFeed-DailyValidation"
3. Select "Run" to test immediately
4. Check `amp_validation_logs\daily_execution.log` for errors

## Next Steps

1. **VB Setup** (You)
   - Create VB macro in Outlook
   - Extract email HTML bodies
   - Save to folder at ~4:05 AM

2. **Test** (You)
   - Run VB script manually to test file extraction
   - Run Python validation manually to verify parsing
   - Check results in log file

3. **Verify Scheduled Task** (You)
   - Open Task Scheduler
   - Right-click "AMP-AutoFeed-DailyValidation" > Run
   - Confirm it executes and generates log

4. **Monitor** (Ongoing)
   - Check `daily_execution.log` each morning
   - Review validation results
   - Adjust if needed

## Current Status

✅ Python validation system ready (HTML file-based)  
✅ Scheduled task configured for 5:00 AM  
⏳ Waiting for VB script to extract and save HTML files  
⏳ Ready to test once HTML files are available
