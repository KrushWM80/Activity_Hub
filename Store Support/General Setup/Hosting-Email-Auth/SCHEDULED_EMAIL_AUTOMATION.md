# Scheduled Email Automation — Windows Task Scheduler

## Overview

This guide documents how to set up reliable **automated scheduled emails** on Windows using Task Scheduler + Outlook COM automation. These lessons were learned from the **TDA Initiatives Insights** weekly email project and apply to any project that needs recurring automated emails.

---

## Architecture

```
Windows Task Scheduler
        ↓ (triggers .bat file on schedule)
send_email.bat
        ↓ (sets env vars, activates venv, runs script)
Python Script (send_weekly_report.py)
        ↓ (queries BigQuery, builds HTML, generates PPT)
Outlook COM Automation (win32com)
        ↓ (sends email with HTML body + attachment)
Recipients' Inboxes
```

### Key Components
| Component | Purpose |
|-----------|---------|
| **Batch file (.bat)** | Sets environment variables (GCP creds), changes to working directory, runs Python script with logging |
| **Python script** | Queries data, builds email HTML, generates PPT attachment, sends via Outlook COM |
| **Task Scheduler** | Triggers the batch file on a recurring schedule |
| **Outlook** | Must be installed and logged in — COM automation sends through the user's Outlook profile |

---

## Critical Task Scheduler Settings

### ⚠ Common Failure: "Last Result: 267011"

Error code `267011` (hex `0x41303`) means the task was **never actually run / skipped**. The most common causes:

| Issue | Symptom | Fix |
|-------|---------|-----|
| **Battery restriction** | Task won't fire when laptop is on battery | Set `-AllowStartIfOnBatteries` |
| **Stops on battery** | Task starts but gets killed when switching to battery | Set `-DontStopIfGoingOnBatteries` |
| **No working directory** | Script can't find relative paths, fails silently | Set `-WorkingDirectory` in the action |
| **Missed schedule** | Laptop was asleep/off at trigger time | Set `-StartWhenAvailable` |
| **Won't wake computer** | Computer stays asleep through scheduled time | Set `-WakeToRun` |
| **Run level** | Script needs admin privileges, task runs as standard user | Set `-RunLevel Highest` |

### ✅ Correct Task Creation (PowerShell)

```powershell
# ---- VARIABLES ----
$taskName    = "Activity_Hub_TDA_Weekly_Email"
$batPath     = "C:\path\to\Automation\send_tda_weekly_email.bat"
$workDir     = "C:\path\to\TDA Insights"

# ---- ACTION ----
$action = New-ScheduledTaskAction `
    -Execute $batPath `
    -WorkingDirectory $workDir          # CRITICAL: set working directory

# ---- TRIGGER (Weekly - Thursdays at 11am) ----
$trigger = New-ScheduledTaskTrigger `
    -Weekly -DaysOfWeek Thursday -At '11:00AM'

# ---- TRIGGER (Hourly for testing) ----
# $trigger = New-ScheduledTaskTrigger `
#     -Once -At (Get-Date).AddMinutes(2) `
#     -RepetitionInterval (New-TimeSpan -Hours 1) `
#     -RepetitionDuration (New-TimeSpan -Days 7)

# ---- SETTINGS (ALL FIVE ARE REQUIRED) ----
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `          # 1. Run even on battery
    -DontStopIfGoingOnBatteries `       # 2. Don't kill if switching to battery
    -StartWhenAvailable `               # 3. Catch up if schedule was missed
    -WakeToRun `                        # 4. Wake computer from sleep
    -ExecutionTimeLimit (New-TimeSpan -Hours 1)

# ---- PRINCIPAL ----
$principal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType Interactive `            # Needed for Outlook COM access
    -RunLevel Highest

# ---- REGISTER ----
Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Force                              # Overwrites if exists
```

### ❌ Bad Pattern: Using `schtasks.exe`

```powershell
# DON'T DO THIS — can't set battery/wake settings properly
schtasks /Create /TN "MyEmail" /SC WEEKLY /D THU /ST 11:00 /TR "path\to\script.bat"
# Results in: No Start On Batteries, Start In: N/A → task never fires
```

Always use `Register-ScheduledTask` PowerShell cmdlet instead of `schtasks.exe`.

---

## Batch File Template

```batch
@echo off
setlocal enabledelayedexpansion

set ProjectRoot=C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub
set ScriptPath=%ProjectRoot%\Store Support\Projects\YOUR_PROJECT
set PythonExe=%ProjectRoot%\.venv\Scripts\python.exe
set LogFile=%ScriptPath%\weekly_email.log

REM Set credentials (use ABSOLUTE paths, not %APPDATA% — SYSTEM user can't resolve it)
set GOOGLE_APPLICATION_CREDENTIALS=C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json

echo [%date% %time%] ====== Email Run Starting ====== >> "%LogFile%"

cd /d "%ScriptPath%"

echo [%date% %time%] Running script... >> "%LogFile%"
"%PythonExe%" your_email_script.py >> "%LogFile%" 2>&1

if %errorlevel% equ 0 (
    echo [%date% %time%] Email sent successfully >> "%LogFile%"
) else (
    echo [%date% %time%] ERROR: Failed with code !ERRORLEVEL! >> "%LogFile%"
)

echo [%date% %time%] ====== Email Run Complete ====== >> "%LogFile%"
echo. >> "%LogFile%"
```

### Key Rules for the Batch File
1. **Use absolute paths** for everything — task may run from an unexpected working directory
2. **Set `GOOGLE_APPLICATION_CREDENTIALS`** with full path (not `%APPDATA%`) — if the task ever runs as SYSTEM, environment variables differ
3. **`cd /d`** to the script directory before running Python
4. **Log everything** with timestamps to a log file for debugging
5. **Redirect stderr** (`2>&1`) into the log so errors are captured

---

## Outlook COM Email (Python)

```python
import win32com.client

def send_email(recipients, subject, html_body, attachment_path=None):
    """Send email via Outlook COM automation."""
    outlook = win32com.client.Dispatch('Outlook.Application')
    mail = outlook.CreateItem(0)  # 0 = olMailItem
    mail.To = '; '.join(recipients)
    mail.Subject = subject
    mail.HTMLBody = html_body
    if attachment_path:
        mail.Attachments.Add(str(attachment_path))
    mail.Send()
```

### Requirements
- **Outlook must be installed** and the user must be logged in
- **LogonType must be `Interactive`** in the task principal — COM automation needs a desktop session
- Task must run as the **same user** who has Outlook configured (not SYSTEM)
- If the laptop is locked, Outlook COM still works as long as the user session exists

---

## Verification Checklist

After creating a scheduled email task, verify ALL of these:

```powershell
# Query task settings
$t = Get-ScheduledTask -TaskName "YOUR_TASK_NAME"
$info = $t | Get-ScheduledTaskInfo

# Check these values
"State:            $($t.State)"                                    # Should be: Ready
"DisallowBattery:  $($t.Settings.DisallowStartIfOnBatteries)"     # Should be: False
"StopOnBattery:    $($t.Settings.StopIfGoingOnBatteries)"          # Should be: False
"StartWhenAvail:   $($t.Settings.StartWhenAvailable)"              # Should be: True
"WakeToRun:        $($t.Settings.WakeToRun)"                      # Should be: True
"WorkingDir:       $($t.Actions[0].WorkingDirectory)"              # Should NOT be empty
"NextRun:          $($info.NextRunTime)"                           # Should be a valid future date
"LastResult:       $($info.LastTaskResult)"                        # 0 = success, 267011 = never ran
```

---

## Debugging Guide

### Task Shows "Last Result: 267011"
- Task was **skipped** — check battery settings, check if computer was asleep
- Fix: Recreate with all five settings above, set `-StartWhenAvailable`

### Task Shows "Last Run: 11/30/1999"
- Task has **never executed** — it may have been created but its trigger time hasn't arrived, or it was skipped every time
- Fix: Set trigger to a few minutes from now for immediate testing

### Log File is Empty
- The batch file never ran — confirm the task actually fired (check `LastRunTime`)
- If `LastRunTime` is valid but log is empty, check the batch file path in the task action

### Script Runs but Email Not Sent
- Check if Outlook is open/available
- Verify LogonType is `Interactive` (not `S4U` or `Password`)
- Run the Python script manually first: `python send_weekly_report.py`

### Script Fails with "No module named..."
- The task may be using a different Python than expected
- Use absolute path to the venv Python in the batch file: `%ProjectRoot%\.venv\Scripts\python.exe`

---

## Hourly Test Pattern

When setting up a new email schedule, use hourly repetition to validate before going to production:

```powershell
# Hourly test — fires every hour for 7 days
$trigger = New-ScheduledTaskTrigger `
    -Once -At (Get-Date).AddMinutes(2) `
    -RepetitionInterval (New-TimeSpan -Hours 1) `
    -RepetitionDuration (New-TimeSpan -Days 7)
```

Once confirmed working, replace with the production schedule and delete the test task.

---

## Alternative: APScheduler (In-Process)

The **Projects in Stores** dashboard uses a different pattern — scheduling lives inside the backend server via APScheduler:

```python
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(send_report, 'cron', day_of_week='thu', hour=11)
scheduler.start()
```

| Approach | Pros | Cons |
|----------|------|------|
| **Task Scheduler + .bat** | Works independently of server, survives server crashes, clear logging | Requires proper task settings, battery/sleep issues |
| **APScheduler in-process** | Simpler setup, no external config needed | Dies if server restarts, harder to debug missed triggers |

For critical emails, **Task Scheduler is more reliable** — as long as the five settings above are configured correctly.

---

## Working Examples in This Repo

| Project | File | Schedule | Method |
|---------|------|----------|--------|
| **TDA Insights** | `Automation/send_tda_weekly_email.bat` → `send_weekly_report.py` | Thursdays 11am | Task Scheduler |
| **Projects in Stores** | `install_email_reporting.ps1` → backend API | In-process | APScheduler |

---

## Quick Reference: Five Required Settings

```
1. AllowStartIfOnBatteries     → Run even on battery power
2. DontStopIfGoingOnBatteries  → Don't kill if switching to battery
3. StartWhenAvailable          → Catch up missed triggers
4. WakeToRun                   → Wake computer from sleep
5. WorkingDirectory            → Set in the Action, not just cd in bat
```

If any of these are missing, the task will silently fail with error 267011.
