# Activity Hub - Scheduled Tasks Inventory

> **Last Updated:** April 28, 2026

## All Registered Tasks

| Task Name | Schedule | Next Run | Script | Purpose |
|-----------|----------|----------|--------|---------|
| `ActivityHub_Email_Test` | Daily 7:00 AM | Apr 29, 2026 | `run_email_scheduler.bat` | Projects email (Mon/Wed/Thu) |
| `Activity_Hub_ActivityHub_AutoStart` | On Startup | Running | Auto-start services | Core services keep-alive |
| `Activity_Hub_TDA_Daily_Email` | Daily 6:00 AM | Apr 29, 2026 | TDA daily email | TDA Insights daily report |
| `Activity_Hub_TDA_Weekly_Email` | Weekly Thu 11 AM | Apr 30, 2026 | TDA weekly email | TDA Insights weekly summary |
| `Activity_Hub_VET_Daily_Email` | Daily 6:00 AM | Apr 29, 2026 | VET daily email | V.E.T. Dashboard daily report |

---

## Projects Email Task: `ActivityHub_Email_Test`

### Overview
Sends Activity Hub project emails on a weekly cadence to a test group of 3 people.

### Schedule
- **Frequency:** Daily at 7:00 AM (script checks day-of-week)
- **Monday:** Owner email (all active projects) to Kendall Rush
- **Wednesday:** Owner email (projects not updated this WM week) to Kendall Rush
- **Thursday:** Leadership summaries to Matt Farnworth (Director) + Kristine Torres (Sr. Director)
- **Tue/Fri/Sat/Sun:** No emails — logs "No emails scheduled"

### Recipients (TEST_MODE = True)
| Person | Role | Email | Days |
|--------|------|-------|------|
| Kendall Rush | Owner | kendall.rush@walmart.com | Mon, Wed |
| Matt Farnworth | Director | matthew.farnworth@walmart.com | Thu |
| Kristine Torres | Sr. Director | kristine.torres@walmart.com | Thu |

### Files
| File | Location | Purpose |
|------|----------|---------|
| `run_email_scheduler.bat` | `Activity_Hub/` | Batch wrapper (Task Scheduler entry point) |
| `run_scheduled_emails.py` | `Activity_Hub/Interface/` | Python scheduler (day-of-week logic) |
| `send_projects_emails.py` | `Activity_Hub/Interface/` | Email generation + SMTP sending |
| `Spark_Blank.png` | `Activity_Hub/Interface/` | Spark logo (CID-attached in emails) |

### Log
- **File:** `Activity_Hub/logs/email_scheduler.log`
- **Format:** Appends each run with timestamps

### How to Manage

**Check task status:**
```cmd
schtasks /query /tn "ActivityHub_Email_Test" /fo list /v
```

**Run manually (immediate):**
```cmd
cd "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"
.venv\Scripts\python Interface\run_scheduled_emails.py
```

**Disable temporarily:**
```cmd
schtasks /change /tn "ActivityHub_Email_Test" /disable
```

**Re-enable:**
```cmd
schtasks /change /tn "ActivityHub_Email_Test" /enable
```

**Remove task:**
```cmd
schtasks /delete /tn "ActivityHub_Email_Test" /f
```

**Recreate task:**
```cmd
schtasks /create /tn "ActivityHub_Email_Test" /tr "'c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\run_email_scheduler.bat'" /sc daily /st 07:00 /f
```

### Transitioning to Production
When ready to go live with all owners:
1. Edit `Interface/run_scheduled_emails.py`
2. Set `TEST_MODE = False`
3. Populate `TEST_OWNERS`, `TEST_DIRECTORS`, `TEST_SR_DIRECTORS` with full lists (or query from BigQuery)
4. Update task description: `schtasks /change /tn "ActivityHub_Email_Test" /tn "ActivityHub_Email_Production"`

### Email Features
- Spark logo embedded via CID MIME attachment (Outlook-compatible)
- Color-coded health status (green/orange/red)
- Clickable project titles linking to Activity Hub or Intake Hub
- Missing director/sr_director warning callout (orange box, Mon/Wed only)
- Warning indicators on individual projects missing hierarchy data

### Dependencies
- Python venv at `.venv/` with `google-cloud-bigquery`, `smtplib`
- SMTP: `smtp-gw1.homeoffice.wal-mart.com:25` (no auth, internal only)
- BigQuery: `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
- GCP credentials: Application Default Credentials
