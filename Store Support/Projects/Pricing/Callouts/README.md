# Pricing Operations Callouts Dashboard

**Purpose**: Home Office users intake pricing forecast callouts for the coming Walmart week. Every Friday at 4:00 PM CT, an automated email sends all callouts + Tableau dashboard screenshot to configured recipients.

**Location**: `Store Support/Projects/Pricing/Callouts/`

**URL**: `http://weus42608431466:8091/PricingOperationsCallouts` (or `http://weus42608431466:8091/`)

---

## Quick Start

### 1. Initialize BigQuery Tables (One-Time)

```bash
cd "Store Support\Projects\Pricing\Callouts"
python setup_bigquery.py
```

### 2. Start Flask Server

```bash
cd "Store Support\Projects\Pricing\Callouts"
python pricing_callouts_server.py
```

Server runs on **port 8091**: `http://weus42608431466:8091/`

### 3. Test Email System

```bash
# Preview email (no send)
python send_pricing_callouts_email.py --preview

# Test send to kendall.rush@walmart.com
python send_pricing_callouts_email.py --test
```

### 4. Schedule Friday Email (Windows Task Scheduler)

Create a new task:
- **Name**: `PricingOps-Callouts-Email-Friday`
- **Trigger**: Every Friday at 3:55 PM CT (so capture + send completes by 4:00 PM)
- **Action**: Run batch file `send_callouts_email.bat`
- **Working Directory**: `C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Pricing\Callouts`

**PowerShell Command** (if creating task via script):
```powershell
$action = New-ScheduledTaskAction -Execute "C:\path\to\send_callouts_email.bat"
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Friday -At "3:55 PM"
Register-ScheduledTask -TaskName "PricingOps-Callouts-Email-Friday" -Action $action -Trigger $trigger
```

---

## Files

| File | Purpose |
|------|---------|
| `pricing_callouts_server.py` | Flask backend server (port 8091) |
| `dashboard.html` | Frontend dashboard UI |
| `send_pricing_callouts_email.py` | Weekly email generator + Tableau screenshot |
| `setup_bigquery.py` | Initialize BigQuery tables |
| `send_callouts_email.bat` | Windows batch file for Task Scheduler |
| `logs/` | Application logs |

---

## Dashboard Features

### Main Dashboard (`http://weus42608431466:8091/`)

- **Alert Banner** (top): Shows "Email sends at 4:00 PM CT Friday" with countdown timer
- **Week Selector**: Choose Current Week or Next Week (for Friday's email)
- **Callout Intake Form**: Add new callouts with title + content
- **Callouts Table**: View, edit, delete callouts for selected week
- **Email Recipients** (sidebar):
  - View count of active recipients
  - Add new recipients (email validation)
  - Remove recipients
- **Callout History** (collapsible): View all past callouts + edit history
- **Email Preview** (sidebar): Shows what Friday email will look like

### Default Email Signature

```
Thank you,

Emily Varner
Senior Manager - Pricing
Walmart US - Operations Support
479-387-8916
```

---

## Email Format

**Subject**: `Weekly Pricing Forecast Callouts - WK##`

**Body**:
```
Hello, team!

Please see below for next week's forecast.

Callouts:
[List of callouts OR "There are no Callouts this week."]

Dashboard:
[Tableau screenshot image (with link to dashboard)]

Please let me know if you have any questions.

Thank you,
Emily Varner
Senior Manager - Pricing
Walmart US - Operations Support
479-387-8916
```

---

## API Reference

### Callouts

```bash
# Get callouts for WM week
GET /api/callouts/<wm_week>

# Create callout
POST /api/callouts
{
  "wm_week": 35,
  "title": "Optional title",
  "content": "Required content",
  "created_by": "User Name"
}

# Update callout
PUT /api/callouts/<callout_id>
{
  "title": "Updated title",
  "content": "Updated content"
}

# Delete callout (soft)
DELETE /api/callouts/<callout_id>
```

### Email Recipients

```bash
# Get active recipients
GET /api/email-recipients

# Add recipient
POST /api/email-recipients
{
  "email": "user@walmart.com"
}

# Remove recipient (soft)
DELETE /api/email-recipients/<recipient_id>
```

### Dashboard Info

```bash
# Get dashboard info (WM weeks, current time, etc.)
GET /api/dashboard-info
```

---

## BigQuery Tables

### Weekly_Callouts
```
- id: STRING (unique ID)
- wm_week: INTEGER (WK# 1-53)
- title: STRING (optional)
- content: STRING (required)
- created_date: TIMESTAMP
- created_by: STRING
- last_modified_date: TIMESTAMP
- status: STRING (active, archived, deleted)
```

### Callout_Email_Recipients
```
- id: STRING (unique ID)
- email: STRING (email address)
- added_date: TIMESTAMP
- is_active: BOOLEAN
```

---

## Walmart Week Calculation

Formula: `(days_since_fy_start // 7) + 1`
- FY Start: February 1 each year
- Week numbers: 1-53
- Example: If today is March 15, and Feb 1 was the start, then `(42 // 7) + 1 = WK7`

---

## Email Flow (Friday 4:00 PM CT)

1. **3:55 PM**: Task Scheduler executes `send_callouts_email.bat`
2. **3:56 PM**: Edge headless captures Tableau dashboard screenshot
3. **3:57 PM**: Query BigQuery for next WM week's callouts
4. **3:58 PM**: Build HTML email with Emily Varner's signature
5. **3:59 PM**: Fetch email recipient list from BigQuery
6. **4:00 PM**: Send email via SMTP to all recipients
7. **4:01 PM**: Log completed, cleanup screenshot file

---

## Logging

All logs written to `logs/`:
- `pricing_callouts_server.log` - Flask server logs
- `pricing_callouts_email.log` - Email sender logs
- `task_scheduler.log` - Task Scheduler batch execution logs

---

## Configuration

Edit these variables in scripts as needed:

**pricing_callouts_server.py**:
- `PORT = 8091` - Flask server port
- `BQ_PROJECT = 'wmt-pricingops-analytics'` - BigQuery project
- `BQ_DATASET = 'Pricing_Ops'` - BigQuery dataset

**send_pricing_callouts_email.py**:
- `SMTP_SERVER = 'smtp-gw1.homeoffice.wal-mart.com'` - SMTP server
- `FROM_EMAIL = 'kendall.rush@walmart.com'` - From email address
- `TABLEAU_URL = '...'` - Tableau dashboard URL
- `CALLOUTS_DASHBOARD_URL = 'http://weus42608431466:8091/'` - Dashboard URL
- `EDGE_PATH = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'` - Edge browser path

---

## Troubleshooting

### Dashboard not loading
- Check Flask server is running: `python pricing_callouts_server.py`
- Verify port 8091 is accessible: `http://weus42608431466:8091/`
- Check logs: `logs/pricing_callouts_server.log`

### Email not sending
- Verify email recipients configured in dashboard
- Run test send: `python send_pricing_callouts_email.py --test`
- Check logs: `logs/pricing_callouts_email.log`
- Verify SMTP connectivity to `smtp-gw1.homeoffice.wal-mart.com:25`

### Tableau screenshot failed
- Check Edge browser installed: `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`
- Verify Tableau URL is accessible
- Run test email with `--preview` flag to debug

### BigQuery errors
- Verify `GOOGLE_APPLICATION_CREDENTIALS` set correctly
- Check credentials file exists: `C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json`
- Verify dataset exists: `wmt-pricingops-analytics.Pricing_Ops`
- Run setup: `python setup_bigquery.py`

---

## Future Enhancements

1. **Approval Workflow**: Add approval step before Friday email send
2. **Email Preview UI**: Show email preview in dashboard before send
3. **Custom Recipients by Team**: Different recipient groups for different teams
4. **Callout Categories**: Tag callouts by type (price, promotion, supply, etc.)
5. **Historical Reports**: Generate weekly/monthly reports of all callouts
6. **Slack Integration**: Also post callouts to Slack channel
7. **Mobile App**: Mobile-friendly UI for on-the-go updates
8. **Two-Factor Authentication**: Secure dashboard access

---

## Support

For questions or issues, contact Pricing Operations team or check logs in `logs/` directory.

---

**Last Updated**: April 28, 2026  
**Version**: 1.0.0  
**Status**: Production Ready
