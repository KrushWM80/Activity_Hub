# Pricing Callouts - Quick Reference

## Start/Stop Commands

```powershell
# 1. Activate Python environment
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"
& ".\.venv\Scripts\Activate.ps1"

# 2. Navigate to Callouts folder
cd "Store Support\Projects\Pricing\Callouts"

# 3. SETUP (one-time)
python setup_bigquery.py

# 4. START Flask Server (keep running)
python pricing_callouts_server.py
# Access: http://weus42608431466:8091/
```

## Testing Commands

```bash
# Test email preview
python send_pricing_callouts_email.py --preview
# Output: email_preview_wk##.html (open in browser)

# Test email send (to kendall.rush@walmart.com)
python send_pricing_callouts_email.py --test

# Send for real (to all recipients)
python send_pricing_callouts_email.py
```

## Task Scheduler Setup

### PowerShell (Run as Administrator)

```powershell
$taskName = "PricingOps-Callouts-Email-Friday"
$scriptPath = "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Pricing\Callouts\send_callouts_email.bat"

# Create action
$action = New-ScheduledTaskAction -Execute $scriptPath

# Create trigger: Friday 3:55 PM CT
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Friday -At "3:55 PM"

# Register task
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Description "Pricing Callouts Weekly Email" -RunLevel Highest

# Verify
Get-ScheduledTask -TaskName $taskName
```

### GUI (Windows Task Scheduler)

1. Open Task Scheduler (`tasksched.msc`)
2. Click "Create Task"
3. **General Tab**:
   - Name: `PricingOps-Callouts-Email-Friday`
   - Description: `Pricing Callouts Weekly Email`
   - Check "Run with highest privileges"
4. **Triggers Tab**:
   - Click "New..."
   - Begin task: On a schedule
   - Recur every: 1 week(s), on Friday
   - Start time: 3:55 PM
   - Repeat task every: *(leave blank)*
5. **Actions Tab**:
   - Action: Start a program
   - Program/script: `C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Pricing\Callouts\send_callouts_email.bat`
   - Start in: `C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Pricing\Callouts`
6. **Conditions Tab**:
   - Uncheck all (allow to run anytime)
7. **Settings Tab**:
   - Check "Allow task to be run on demand"
   - Uncheck "Stop task if running longer than: ..."
8. Click OK

## Directory Structure

```
Store Support/Projects/Pricing/Callouts/
├── README.md                          (Setup & usage guide)
├── QUICKSTART.md                      (This file)
├── pricing_callouts_server.py         (Flask backend, port 8091)
├── dashboard.html                     (Frontend UI)
├── send_pricing_callouts_email.py     (Email generator)
├── setup_bigquery.py                  (BigQuery table setup)
├── send_callouts_email.bat            (Windows Task Scheduler batch)
├── logs/                              (Application logs)
│   ├── pricing_callouts_server.log
│   ├── pricing_callouts_email.log
│   └── task_scheduler.log
└── [temp files]                       (Screenshots, preview HTML)
```

## Environment Variables

Automatically set by batch file:
- `PYTHONPATH`: Points to Activity_Hub folder
- `GOOGLE_APPLICATION_CREDENTIALS`: Points to gcloud credentials

## Key URLs

| Resource | URL |
|----------|-----|
| **Callouts Dashboard** | `http://weus42608431466:8091/` |
| **Tableau Dashboard** | `https://tableau-prep-prod.homeoffice.wal-mart.com/#/views/PricingForecast/PricingForecast?:iid=1` |
| **BigQuery Tables** | `wmt-pricingops-analytics.Pricing_Ops.Weekly_Callouts` |
| | `wmt-pricingops-analytics.Pricing_Ops.Callout_Email_Recipients` |

## Email Test Recipients

For testing, emails go to: `kendall.rush@walmart.com`

Add real recipients via dashboard UI after server starts.

## Friday 4 PM Email Timeline

| Time | Action |
|------|--------|
| 3:55 PM CT | Task Scheduler executes batch file |
| 3:56 PM | Edge captures Tableau screenshot |
| 3:57 PM | Query BigQuery for next week's callouts |
| 3:58 PM | Build HTML email |
| 3:59 PM | Fetch recipient list |
| 4:00 PM | Send email via SMTP |
| 4:01 PM | Cleanup + logging |

## Logs

```bash
# Flask server log
tail -f logs/pricing_callouts_server.log

# Email sender log
tail -f logs/pricing_callouts_email.log

# Task Scheduler execution log
tail -f logs/task_scheduler.log
```

## Debugging

### Check if Flask server is running
```powershell
Get-NetTCPConnection -LocalPort 8091 | Select-Object State, OwningProcess
```

### Check Task Scheduler history
1. Open Task Scheduler
2. Navigate to: Task Scheduler Library
3. Find "PricingOps-Callouts-Email-Friday"
4. Right-click → Properties → History tab

### Test database connection
```python
from google.cloud import bigquery
client = bigquery.Client(project='wmt-pricingops-analytics')
print(client.list_datasets())
```

## Common Issues

| Issue | Solution |
|-------|----------|
| "ModuleNotFoundError: No module named 'flask'" | Activate venv: `. .venv\Scripts\Activate.ps1` |
| \"Port 8091 already in use\" | Kill process: `Get-Process python \\| Stop-Process -Force` |
| "Email not sending" | Run test: `python send_pricing_callouts_email.py --test` |
| "BigQuery not found" | Run setup: `python setup_bigquery.py` |
| "Edge not found" | Install Microsoft Edge or update path in script |

## Dashboard Features Cheat Sheet

### Adding Callout
1. Select week (Current or Next)
2. Enter title (optional)
3. Enter content (required, supports any text)
4. Click "Add Callout"
5. Callout appears in table immediately

### Editing Callout
1. Click ✏️ Edit button on callout row
2. Modal opens with current content
3. Update content
4. Click "Save Changes"

### Adding Email Recipient
1. Enter email in sidebar
2. Click "Add Recipient"
3. Recipient appears in list
4. Will receive Friday email

### Removing Email Recipient
1. Click "Remove" button next to email
2. Confirm deletion
3. Will not receive future emails

## Important Notes

- **WM Week**: Walmart fiscal week (Feb 1 = WK1)
- **Email Day**: Friday 4:00 PM CT (email is for NEXT week)
- **Default User**: Emails from `kendall.rush@walmart.com` signed by Emily Varner
- **Recipients**: Managed via dashboard, not synced from directory
- **History**: All callouts retained (soft delete for audit trail)
- **Screenshot**: Automatically captured right before email send

---

**Questions?** Check README.md or logs for troubleshooting.
