# DC to Store Manager Change Detection - Knowledge Base
## PayCycle Automation System (April 2026 - PRODUCTION)

**Last Updated:** April 17, 2026  
**Status:** ✅ PRODUCTION ACTIVE  
**Current PayCycle:** PC-06 (Completed) → PC-07 through PC-26 Scheduled  
**Version:** 3.0 - SMTP Gateway Email Method (Reliable, Proven)

---

## 🎯 System Overview

Automated email notification system that detects manager changes at Walmart stores and sends notifications to Distribution Center (DC) leadership on a biweekly PayCycle schedule.

**Key Features:**
- ✅ 21 PayCycles fully automated (PC-06 through PC-26)
- ✅ Production-grade email via SMTP gateway (reliable, no Outlook required)
- ✅ Smart DC targeting (only affected DCs receive emails)
- ✅ Complete tracking and audit trail
- ✅ Internal team monitoring via BCC
- ✅ Tested and verified (PC-06 successfully sent April 17, 2026)

---

## 📁 Project File Structure

```
DC to Store Change Management Emails/
├── Core Systems
│   ├── send_pc06_production_email.py  [MAIN] Production email sender
│   ├── email_helper.py                [CORE] Email via SMTP gateway
│   ├── dc_email_config.py             [CONFIG] Settings (TEST_MODE=False)
│   ├── dc_leadership_config.py        [CONFIG] DC recipient mapping
│   └── dc_change_grouper.py           [CORE] Smart DC identification
│
├── Task Scheduling & Automation
│   ├── CREATE_ALL_PAYCYCLE_TASKS.ps1  [ADMIN] PowerShell - creates PC-07-26 tasks
│   ├── CREATE_PC06_TASK.ps1           [ADMIN] Emergency PC-06 task (reference)
│   ├── paycycle_tracking.json         [LOG] Tracks all 26 PayCycles execution
│   └── setup_tasks_revised.ps1        [LEGACY] Previous version (reference only)
│
├── Documentation (NEW - April 17, 2026)
│   ├── EMAIL_SYSTEM_STANDARDS.md           [REFERENCE] SMTP email standards
│   ├── PRODUCTION_LAUNCH_NOTES.md          [SUMMARY] PC-06 launch details
│   ├── README_EMAIL_STANDARDS_KB.md        [KNOWLEDGE BASE] System-wide pattern
│   ├── PRODUCTION_DEPLOYMENT_READY.md      [CHECKLIST] Pre-launch verification
│   └── PRE_LAUNCH_CHECKLIST.md             [CHECKLIST] Launch readiness
│
├── Configuration & Templates
│   ├── dc_to_stores_lookup.json       DC-to-store mapping
│   ├── dc_contacts_template.json      DC contact structure
│   ├── alignment_type_mapping.json    DC type mappings
│   ├── vpn_retry_tracker.json        VPN retry history
│   └── email_send_queue.txt          Email queue for Code Puppy
│
├── Reference Documentation
│   ├── RECIPIENTS_REFERENCE.txt      How recipient routing works
│   ├── RECIPIENT_TRACKING_GUIDE.md   Managing recipients
│   ├── PAYCYCLE_SCHEDULE_SETUP_GUIDE.md
│   ├── TEST_EMAIL_EXPLANATION.md     Why test email wasn't sent initially
│   ├── WALMART_PAYCYCLE_GUIDE.md     PayCycle date reference
│   └── WALMART_PAYCYCLE_SCHEDULE.md  Complete 26-date schedule
│
├── Folders
│   ├── emails_sent/                  Backup copies of all sent emails
│   ├── emails_pending/               Queue for unsent emails
│   ├── snapshots_local/              Manager data snapshots
│   ├── templates/                    HTML email templates
│   └── reports/                      Generated reports
│
└── Legacy/Archive
    ├── test_no_changes_email.py
    ├── setup_hourly_task.bat
    └── [Other legacy files]
```

---

## 🚀 Current Status - April 17, 2026 (PRODUCTION LAUNCH)

| Component | Status | Details |
|-----------|--------|---------|
| **System Version** | ✅ 3.0 | SMTP Gateway (Production) |
| **Email Delivery** | ✅ LIVE | SMTP Gateway (`smtp-gw1.homeoffice.wal-mart.com:25`) |
| **PyWin32** | ✅ Installed | v311 in venv (for task scheduling) |
| **21 PayCycle Tasks** | ✅ Created | PC-06 through PC-26 (Jan 22, 2027) |
| **PayCycle 06** | ✅ COMPLETED | Sent 4/17/26 @ 08:43 to 10 DC leaders |
| **Production Recipients** | ✅ Active | 5 affected DCs (6018, 6054, 6055, 6082, 6094) |
| **BCC Monitoring** | ✅ Active | Kristine, Matthew, Kendall Torres |
| **Tracking System** | ✅ Updated | paycycle_tracking.json - PC-06 complete |
| **Email Method** | ✅ VERIFIED | SMTP (same as TDA, VET, Audio systems) |

---

## 📋 The 26 PayCycles - Complete Schedule

All scheduled for **6:00 AM** on respective dates:

| # | PayCycle Date | Status | Details |
|---|---|---|---|
| 01-05 | Feb 6 - Apr 3, 2026 | ✅ Historical | Test/reference emails |
| **06** | **Apr 17, 2026** | **✅ COMPLETED** | **Production launch - 10 recipients** |
| 07 | May 1, 2026 | ⏳ Scheduled | AUTOMATED |
| 08 | May 15, 2026 | ⏳ Scheduled | AUTOMATED |
| ... | ... | ⏳ Scheduled | AUTOMATED |
| 26 | Jan 22, 2027 | ⏳ Scheduled | AUTOMATED |

**View complete PayCycle schedule:** [WALMART_PAYCYCLE_SCHEDULE.md](WALMART_PAYCYCLE_SCHEDULE.md)

---

## 🔑 Key Documentation (Updated April 17, 2026)

### NEW: Email System Standards
**File:** `EMAIL_SYSTEM_STANDARDS.md`  
**Purpose:** Document SMTP gateway as standard email delivery method  
**Content:** Technical implementation, configuration, and best practices  

### NEW: Production Launch Notes
**File:** `PRODUCTION_LAUNCH_NOTES.md`  
**Purpose:** Complete deployment summary and next steps  
**Content:** PC-06 results, system changes, validation checklist

### NEW: Email Standards Knowledge Base
**File:** `README_EMAIL_STANDARDS_KNOWLEDGE_BASE.md`  
**Purpose:** System-wide email pattern reference  
**Content:** SMTP gateway integration, troubleshooting, testing guidelines

### Core Files (Updated/Maintained)

### 1. paycycle_tracking.json
**Purpose:** Track all 26 PayCycle sends with dates, times, and status  
**Updated:** April 17, 2026 (PC-06 completed)  
**Fields per PayCycle:**
- `pc_number` - PayCycle ID (1-26)
- `paycycle_date` - Date PayCycle ends
- `scheduled_send_time` - When email should send (6:00 AM)
- `actual_send_time` - When it actually sent (PC-06: 08:43)
- `status` - completed / scheduled / pending
- `recipients_count` - How many received it (PC-06: 10)
- `error_message` - Any errors encountered (PC-06: null)
- `task_name` - DC-EMAIL-PC-XX-FY27 PC XX

**PC-06 Example:**
```json
{
  "pc_number": 6,
  "paycycle_date": "2026-04-17",
  "actual_send_time": "08:43",
  "actual_send_datetime": "2026-04-17T08:43:32.351347",
  "status": "completed",
  "notes": "Sent to 5 affected DC leadership (10 emails: GM+AGM)",
  "recipients_count": 10,
  "error_message": null
}
```

### 2. dc_email_config.py  
**Purpose:** System configuration and settings  
**Current State:**
- `TEST_MODE` = False (PRODUCTION)
- `BCC_RECIPIENTS` = [Kristine Torres, Matthew Farnworth, Kendall Rush]
- `SEND_FROM_EMAIL` = supplychainops@email.wal-mart.com
    }
  }
}
```

### 3. manage_paycycle.py (NEW)
**Purpose:** CLI tool to manage PayCycles and recipients  
**Size:** 12.08 KB  
**All Commands Tested & Working:**

```bash
# View PayCycle schedule
python manage_paycycle.py schedule

# View current recipients
python manage_paycycle.py recipients

# Add a recipient
python manage_paycycle.py add-recipient test john@walmart.com "John Doe" "Store Manager"
python manage_paycycle.py add-recipient production maria@walmart.com "Maria Garcia" "DC Manager"

# Remove a recipient
python manage_paycycle.py remove-recipient test john@walmart.com

# Switch between modes
python manage_paycycle.py switch-mode production

# Record a PayCycle send
python manage_paycycle.py record-send 3 success
python manage_paycycle.py record-send 3 failed "SDL API timeout"

# Get current recipient emails as JSON
python manage_paycycle.py get-emails
```

### 4. dc_contacts_template.json (NEW)
**Purpose:** Template for organizing DC contacts by region  
**Size:** 3.5 KB  
**Structure for 5 DCs:**
- Dallas (DC 6020 - Ambient, DC 6040 - Perishable)
- Atlanta
- Chicago
- Denver
- Los Angeles

**Workflow:**
1. User populates this with real DC contact data
2. We import into `email_recipients.json` production mode
3. Switch to production mode when ready

### 5. Automated Email Senders (NEW)

#### send_test_email_working.py
- Multi-method email sender
- Tries: Outlook COM → SMTP → Code Puppy queue
- ✅ Tested and working

#### send_test_debug.py
- Detailed debug output
- Step-by-step email creation and sending
- ✅ Sent successfully to all 3 recipients

#### send_historical_paycycles.py
- Sends production-style historical emails
- ✅ Sent PayCycle 01 & 02 emails (no test labels)

### 6. setup_tasks_revised.ps1 (UPDATED)
**Purpose:** Create all 26 PayCycle tasks in Windows Task Scheduler  
**Status:** ✅ Successfully created all 26 tasks on March 5, 2026  
**How to Run:**
```powershell
# Run as Administrator in PowerShell
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails"
.\setup_tasks_revised.ps1
```

---

## 🔄 How the System Works

### Daily Flow (Every PayCycle Day at 6:00 AM)

1. **Task Triggers** → Windows Task Scheduler runs `DC-EMAIL-PC-XX`
2. **Python Executes** → `daily_check_smart.py` starts
3. **Data Fetch** → Downloads manager data from SDL
4. **Comparison** → Compares with previous snapshot
5. **Changes Detected** → Identifies manager changes
6. **Email Generation** → Creates HTML email with:
   - Change summary
   - Store information
   - Old manager → New manager
   - Effective dates
   - DC information
7. **Email Sending** → Sends via Outlook COM to test/production recipients
8. **Tracking Update** → Records:
   - Actual send time
   - Status (success/failed)
   - Recipients count
   - Any errors
9. **Backup Created** → HTML saved to `emails_sent/` folder
10. **Log Updated** → `paycycle_tracking.json` updated automatically

### Email Routing

**TEST MODE (Active Now):**
- Recipient: All 3 test recipients
- File: `email_recipients.json` with `active_mode: "test"`

**PRODUCTION MODE (When Ready):**
- Recipients: DC managers by region
- File: Update `email_recipients.json` with `active_mode: "production"`
- Command: `python manage_paycycle.py switch-mode production`

---

## 📊 Test Results (March 5, 2026)

### Email 1: Debug Test
- ✅ Subject: "✅ TEST EMAIL - Actually Sent from Python"
- ✅ Sent to: 3 recipients
- ✅ Method: Outlook COM
- ✅ Status: Delivered

### Email 2: Format Test
- ✅ Subject: "✅ TEST - Manager Change Detection System (ACTUAL SEND)"
- ✅ Sent to: 3 recipients
- ✅ Method: Outlook COM
- ✅ Status: Delivered

### Email 3: Historical PC 01
- ✅ Subject: "Manager Changes - PayCycle 01 (Week Ending 2/6/2026)"
- ✅ Content: Production-style with realistic manager changes
- ✅ Sent to: 3 recipients
- ✅ Status: Delivered

### Email 4: Historical PC 02
- ✅ Subject: "Manager Changes - PayCycle 02 (Week Ending 2/20/2026)"
- ✅ Content: Production-style with realistic manager changes
- ✅ Sent to: 3 recipients
- ✅ Status: Delivered

---

## 🎓 Common Tasks & How-Tos

### Task 1: Check PayCycle Schedule
```bash
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails"
python manage_paycycle.py schedule
```
Shows all 26 PayCycles with status.

### Task 2: Add a DC Manager to Production
```bash
python manage_paycycle.py add-recipient production john.smith@walmart.com "John Smith" "DC 6020 General Manager"
```

### Task 3: Add Multiple Recipients at Once
```bash
python manage_paycycle.py add-recipient production maria.garcia@walmart.com "Maria Garcia" "DC Manager"
python manage_paycycle.py add-recipient production james.lee@walmart.com "James Lee" "Market Manager"
python manage_paycycle.py add-recipient production sarah.johnson@walmart.com "Sarah Johnson" "Regional Manager"
```

### Task 4: Switch to Production Mode
```bash
python manage_paycycle.py switch-mode production
```
⚠️ After this, emails go to all production recipients, not test recipients!

### Task 5: Record a PayCycle Send (Manually)
```bash
# If send succeeded
python manage_paycycle.py record-send 3 success

# If send failed
python manage_paycycle.py record-send 3 failed "SDL API timeout error"
```

### Task 6: View Who Will Receive Emails Today
```bash
python manage_paycycle.py recipients
```

### Task 7: Verify PayCycle 03 is Ready
```bash
Get-ScheduledTask -TaskName "DC-EMAIL-PC-03" | Select-Object TaskName, State, NextRunTime
```

### Task 8: View Sent Emails
All backup copies stored in: `emails_sent/`
Format: `TEST_EMAIL_YYYYMMDD_HHMMSS.html`

### Task 9: Check Tracking Data
```bash
# View paycycle_tracking.json to see send history
# After PayCycle 03 runs, this will show:
# - actual_send_time: 2026-03-06 06:00:XX
# - status: completed
# - recipients_count: 3
```

---

## 🔧 Troubleshooting

### Issue: "Access is Denied" When Creating Tasks
**Solution:** Run PowerShell as Administrator
```powershell
Right-click PowerShell → "Run as Administrator"
cd "...DC to Store Change Management Emails"
.\setup_tasks_revised.ps1
```

### Issue: Tasks Not Running at Scheduled Time
**Check:**
1. Is Outlook running? (needed for COM automation)
2. Is the venv Python available?
3. View Task Scheduler → DC-EMAIL-PC-XX → History tab

### Issue: Email Not Sent
**Check in this order:**
1. Look in `emails_sent/` folder - was HTML generated?
2. Check `paycycle_tracking.json` - what's the status?
3. Run: `python check_outlook_accounts.py` - is Outlook configured?
4. Check `email_send_queue.txt` - is email queued for Code Puppy?

### Issue: Wrong Recipients Receiving Emails
**Check:**
1. `python manage_paycycle.py recipients` - see current mode
2. `email_recipients.json` - verify active_mode
3. `python manage_paycycle.py switch-mode [mode]` - switch if needed

---

## 📞 Recipients Reference

### Current Test Recipients (Active)
- Kristine.Torres@walmart.com
- Matthew.Farnworth@walmart.com
- Kendall.Rush@walmart.com

### DC Recipient Pattern (Production)
Format: `<DC_NUMBER><ROLE>@email.wal-mart.com`
- Example: `6020GM@email.wal-mart.com` (DC 6020 General Manager)
- Example: `6020AGM@email.wal-mart.com` (DC 6020 Assistant GM)

**Roles:**
- GM = General Manager
- AGM = Assistant General Manager
- (Can be customized in `dc_leadership_config.py`)

---

## 📅 March 6, 2026 - PayCycle 3 Completed ✅

### Execution Summary

**Time:** 2026-03-06 @ 13:00 (1:00 PM)  
**Trigger:** Manual execution (via send_paycycle3_email.py)  
**Data:** Live SDL export - 9,511 managers current as of 3/6/26  

### Email Details

**File:** `DC-EMAIL-PC-03-REVIEW-20260306_140000.html`  
**Recipients:** 3 test recipients  
- Kristine.Torres@walmart.com
- Matthew.Farnworth@walmart.com  
- Kendall.Rush@walmart.com

**Status:** ✅ Delivered via Outlook COM automation  

**Changes Detected:**
- 5 Store Manager assignments changed
- 3 Market Manager assignments changed
- **Total: 8 manager changes**

### Fixes Applied Before Sending

1. ✅ **Removed Store Refresh Program Section**
   - This section was NOT in original PayCycle 1 & 2 emails
   - Contained unrelated performance metrics (users, actions, store coverage, etc.)
   - Removed lines 324-340 from generated email

2. ✅ **Fixed Spark Logo Display**
   - Copied `Spark Blank.png` from Design folder to emails_sent folder
   - Updated image path for HTTP server compatibility
   - Yellow Spark logo now displays correctly in email header

3. ✅ **Fixed Intro Text Visibility**
   - Added dark text color (#1F2937) to blue intro banner
   - Text now displays properly on light blue background

4. ✅ **Cleaned Up Button Formatting**
   - Removed emoji icons from Send Feedback button  
   - Removed emoji icons from View Store Managers button
   - Clean, professional appearance

### Email Format Verification

- ✅ Matches PayCycle 1 & 2 format exactly
- ✅ Proper intro section with change impact statement
- ✅ Manager changes grouped by role (Store Manager / Market Manager)
- ✅ Store links to SDL with ELM buttons
- ✅ Summary stats (8 total changes, 3 test recipients)
- ✅ Action buttons (Send Feedback, View Store Managers)
- ✅ Professional footer

### Delivery Confirmation

```
[EMAIL] Sending via Outlook COM automation:
  To: Kristine.Torres@walmart.com, Matthew.Farnworth@walmart.com, Kendall.Rush@walmart.com
  Subject: PayCycle 3 - Recent Field Leadership Updates (March 6, 2026)
  From: supplychainops@email.wal-mart.com
  [OK] Email sent successfully!

✓ PayCycle 3 email sent successfully to all recipients!
```

---

## 🎯 Next Steps

1. ✅ **PayCycle 03 Complete** - Email delivered to test recipients
2. **Continue Monitoring:** Use `paycycle_tracking.json` to track PayCycle 04 (March 20, 2026)
3. **Prepare for Production:** When ready to expand beyond test recipients:
   - Populate `dc_contacts_template.json` with DC contact data
   - Add production contacts: `python manage_paycycle.py add-recipient production [email] "[name]" "[title]"`
   - Switch modes: `python manage_paycycle.py switch-mode production`
4. **Track all 26 sends** via `paycycle_tracking.json`
5. **Verify automatic execution** of remaining PayCycles via Task Scheduler

---

## 📚 Related Documentation

- [RECIPIENTS_REFERENCE.txt](RECIPIENTS_REFERENCE.txt) - How recipient routing works
- [RECIPIENT_TRACKING_GUIDE.md](RECIPIENT_TRACKING_GUIDE.md) - Managing recipients
- [WALMART_PAYCYCLE_SCHEDULE.md](WALMART_PAYCYCLE_SCHEDULE.md) - All 26 dates
- [PAYCYCLE_SCHEDULE_SETUP_GUIDE.md](PAYCYCLE_SCHEDULE_SETUP_GUIDE.md) - Setup details
- [TEST_EMAIL_EXPLANATION.md](TEST_EMAIL_EXPLANATION.md) - Email delivery notes
- [EMAIL_FLOW_DOCUMENTATION.txt](EMAIL_FLOW_DOCUMENTATION.txt) - Email system details

---

## 📝 Log of Changes (This Session)

**Phase 1 - Setup & Configuration (March 5, 2026)**
- ✅ Created `paycycle_tracking.json` - PayCycle tracking system
- ✅ Created `email_recipients.json` - Recipient management config
- ✅ Created `manage_paycycle.py` - CLI utility for management
- ✅ Created `dc_contacts_template.json` - DC contact template
- ✅ Created `send_test_email_working.py` - Multi-method emailer
- ✅ Created `send_test_debug.py` - Debug emailer
- ✅ Created `send_historical_paycycles.py` - Historical email sender
- ✅ Installed `pywin32` (v311) - Outlook COM support
- ✅ Created 26 scheduled tasks in Task Scheduler
- ✅ Tested all email sending methods
- ✅ Sent 4 test emails successfully
- ✅ Verified PayCycle 03 ready for 3/6/2026

**Phase 2 - PayCycle 3 Execution (March 6, 2026)**
- ✅ Installed Playwright browser automation for SDL data fetch
- ✅ Downloaded live SDL manager data (9,511 managers)
- ✅ Created manager snapshot for March 6, 2026
- ✅ Generated PayCycle 3 email with 8 manager changes
- ✅ Identified template issue: Email included Store Refresh Program metrics NOT in original PayCycle 1 & 2
- ✅ Removed Store Refresh Program section from email (lines 324-340)
- ✅ Fixed Spark logo display (copied PNG to emails_sent folder)
- ✅ Fixed intro text visibility (dark text on blue background)
- ✅ Cleaned up button formatting (removed emoji icons)
- ✅ Created `send_paycycle3_email.py` script for sending corrected version
- ✅ Sent verified email to 3 test recipients via Outlook COM
- ✅ Confirmed delivery success to all recipients
- ✅ Updated documentation

**Status:** ✅ 100% Production Ready & Active

---

**All files created in this session are stored in this folder:**
```
C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails
```

**No external dependencies outside this folder!** 🎯
