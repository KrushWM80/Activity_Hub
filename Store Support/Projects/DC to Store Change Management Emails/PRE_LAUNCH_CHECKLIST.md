# DC to Store Change Management System
## Pre-Launch Checklist & Action Items
**For:** Project Managers & IT Leadership  
**Created:** February 25, 2026  
**Status:** Ready for Execution

---

## 📋 MANAGEMENT DECISION CHECKLIST

Before proceeding with any technical work, management must decide:

### ☐ **Step 1: Choose Deployment Path**

```
Choose ONE:

☐ Path A: FULL PRODUCTION LAUNCH
  Timeline: March 15, 2026
  Scope: All DCs nationwide
  Effort: 70 hours, ~$7,000
  Risk: LOW
  Recommendation: ✅ THIS ONE

☐ Path B: PILOT PROGRAM (Limited)
  Timeline: March 1-31, 2026
  Scope: 5-10 selected DCs
  Effort: 50 hours, ~$5,000
  Risk: LOW

☐ Path C: EXTENDED STUDY
  Timeline: Next 90 days
  Scope: ROI analysis only
  Effort: 20 hours, ~$1,500
  Risk: MEDIUM (delay)
```

**Approved Path:** _________________ **Date:** _____  
**Approved By:** _________________________________

### ☐ **Step 2: Allocate Resources**

- [ ] Kendall Rush assigned to project (primary)
- [ ] IT Support assigned (shared mailbox setup)
- [ ] Server allocated (Windows server for production)
- [ ] Executive sponsor identified
- [ ] Emergency escalation contact named

**Resource Owner:** _________________________  
**Phone:** ___________________ **Email:** __________________

### ☐ **Step 3: Approve Budget**

- [ ] One-time setup: $6,000-8,000 approved
- [ ] Monthly operations: $750/month approved
- [ ] Contingency (10%): approved
- [ ] Cost code/project number assigned

**Budget Approved:** ${_________}  
**Finance Contact:** _________________________

### ☐ **Step 4: Schedule Go-Live Date**

Choose a date that:
- ✅ Is NOT a holiday or store closure
- ✅ Is NOT during peak retail season
- ✅ Has IT support available
- ✅ Is 3+ weeks away (time for setup)

**Recommended:** March 15, 2026 (Saturday, low retail impact for testing)

**Go-Live Date Chosen:** ____________________  
**Approved By:** _____________________________

---

## 🔧 IT TEAM CHECKLIST (Week 1)

### ☐ **Access & Permissions Setup**

**Task 1.1: Shared Mailbox Request** (3-5 days)
- [ ] Identify target mailbox for email sends
  - Recommendation: supplychainops@email.wal-mart.com (or similar)
- [ ] Request "Send As" permissions from mailbox owner
- [ ] Request "Full Access" permissions (recommended)
- [ ] Add mailbox to Outlook: File → Account Settings → Advanced
- [ ] Test sending email from mailbox in Outlook
- [ ] Provide mailbox name to Kendall for config update
- [ ] Verify from which server/desktop this will function

**Status:** ☐ In Progress / ☐ Complete  
**Mailbox Assigned:** _____________________________  
**Date Completed:** ___________

---

**Task 1.2: VPN & API Access Verification** (1 day)
- [ ] Test SDL access (while on VPN)
  - URL: https://elmsearchui.prod.elm-ui.telocmdm.prod.walmart.com/
  - Expected: Can log in and view manager data
  - Contact: [SDL Team if issues]
- [ ] Test LAS API access (DC alignment)
  - URL: http://dcalignment.telocmdm.prod.us.walmart.com/
  - Expected: Returns DC-to-store mappings
  - Contact: [LAS Team if issues]
- [ ] Verify VPN stability (no frequent disconnects)
- [ ] Document any access issues for troubleshooting

**Status:** ☐ In Progress / ☐ Complete  
**SDL Access:** ☐ Verified / ☐ Issues (____________)  
**LAS API Access:** ☐ Verified / ☐ Issues (____________)  
**Date Completed:** ___________

---

**Task 1.3: Server Allocation** (Same day)
- [ ] Allocate Windows Server (2016 or higher)
- [ ] Allocate server disk space (10-20 GB minimum)
- [ ] Confirm Python 3.8+ already installed
- [ ] Verify Outlook desktop client installed on server
- [ ] Set up service account with VPN access
- [ ] Configure auto-login if needed (for scheduled tasks)
- [ ] Provide server name/IP and credentials to Kendall

**Status:** ☐ In Progress / ☐ Complete  
**Server Name:** _____________________________  
**IP Address:** _____________________________  
**Service Account:** _____________________________  
**Python Version:** ____________  
**Outlook Installed:** ☐ Yes / ☐ No (needs install)  
**Date Completed:** ___________

---

### ☐ **System Requirements Validation**

**Task 1.4: Environment Verification** (Same day)
- [ ] Python 3.8+ installed and in PATH
  ```
  Command: python --version
  Expected: Python 3.8+
  ```
- [ ] Required Python packages available
  ```
  Command: pip list | findstr "pandas requests pywin32 flask"
  Expected: All packages listed
  ```
- [ ] Outlook COM support available
  ```
  Start Excel, Tools > Macros, confirm VBA works
  ```
- [ ] Network connectivity to Walmart systems
  ```
  Command: ping elmsearchui.prod.elm-ui.telocmdm.prod.walmart.com
  ```

**Status:** ☐ In Progress / ☐ Complete  
**Python Version:** ____________  
**All Packages Found:** ☐ Yes / ☐ No  
**COM Support:** ☐ Verified / ☐ Failed  
**Network Connectivity:** ☐ Verified / ☐ Failed  
**Date Completed:** ___________

---

## 🚀 KENDALL'S TEAM CHECKLIST (Week 1)

### ☐ **Configuration & Validation**

**Task 2.1: Configuration File Review** (2 hours)
- [ ] Review `config.py`:
  - [ ] Update `TEST_EMAIL` → current test recipient address
  - [ ] Update `SHARED_MAILBOX` → mailbox name from IT
  - [ ] Verify `SDL_URL` is current
  - [ ] Verify `LAS_API_URL` is current
  - [ ] Set `TEST_MODE = True` initially
  - [ ] Document all changes

- [ ] Review `dc_email_config.py`:
  - [ ] Verify `REPLY_TO_EMAIL` = ATCTEAMSUPPORT@walmart.com
  - [ ] Check email footer messaging
  - [ ] Verify DC recipient patterns
  - [ ] Document any changes

- [ ] Review `dc_to_stores_lookup.json`:
  - [ ] Verify DC numbers are current
  - [ ] Confirm all 40+ DCs listed
  - [ ] Check store-to-DC mappings accuracy
  - [ ] Update if discrepancies found

**Status:** ☐ In Progress / ☐ Complete  
**All Configs Reviewed:** ☐ Yes  
**TEST_MODE Set:** ☐ True (for validation)  
**Date Completed:** ___________

---

**Task 2.2: Test Environment Run** (3 hours)
- [ ] Run `python SETUP_WIZARD.py` to configure system
- [ ] Run `python vpn_checker.py`
  - Expected: VPN connection detected
  - If fails: Troubleshoot with IT
- [ ] Run `python create_snapshot.py`
  - Expected: Creates manager snapshot
  - If fails: Check SDL access (IT issue)
- [ ] Run `python compare_snapshots.py`
  - Expected: Identifies manager changes
  - If fails: Check snapshot data quality
- [ ] Run `python dc_email_generator_html.py`
  - Expected: Generates test email HTML
  - If fails: Check template file
- [ ] View generated email in browser
  - Expected: Professional Spark branding
  - If fails: Check logo path
- [ ] Document any issues and solutions

**Status:** ☐ In Progress / ☐ Complete  
**VPN Check:** ☐ Passed / ☐ Failed  
**Snapshot Creation:** ☐ Passed / ☐ Failed  
**Change Detection:** ☐ Passed / ☐ Failed  
**Email Generation:** ☐ Passed / ☐ Failed  
**Email Design:** ☐ Looks Good / ☐ Needs Adjustment  
**Date Completed:** ___________

---

**Task 2.3: Dashboard Validation** (2 hours)
- [ ] Run `python dashboard.py`
- [ ] Open http://localhost:5000 in browser
- [ ] Verify dashboard displays:
  - [ ] Total Changes Detected metric
  - [ ] Total Emails Sent metric
  - [ ] Changes by Role pie chart
  - [ ] Email Delivery Status bar chart
  - [ ] Daily Trend line chart
  - [ ] DC Territory table
- [ ] Test time period filters (7/30/60/90 days)
- [ ] Test refresh button
- [ ] Verify data accuracy vs. generated emails
- [ ] Document any display issues

**Status:** ☐ In Progress / ☐ Complete  
**Dashboard Loads:** ☐ Yes / ☐ No  
**All Metrics Display:** ☐ Yes / ☐ No  
**Charts Render:** ☐ Yes / ☐ No  
**Data Accurate:** ☐ Yes / ☐ No  
**Date Completed:** ___________

---

## 📧 STAKEHOLDER CHECKLIST (Week 2)

### ☐ **DC Manager Communication**

**Task 3.1: Identify Recipients** (1 hour)
- [ ] Compile list of all DC managers (40+ DCs)
- [ ] Verify contact information is current
- [ ] Confirm email addresses match system patterns
- [ ] Identify any special cases or exceptions
- [ ] Share list with Kendall for final validation

**Status:** ☐ In Progress / ☐ Complete  
**DC Manager List:** ☐ Compiled / ☐ Verified  
**Date Completed:** ___________

---

**Task 3.2: Pre-Announcement Communication** (Half day)
- [ ] Draft "Coming Soon" announcement email
- [ ] Include: Purpose, benefits, go-live date, how to provide feedback
- [ ] Get executive sponsor approval
- [ ] Send to all DC GMs (1 week before launch)
- [ ] Follow up with regional managers

**Email Template Sections:**
```
Subject: Manager Change Notification System - Coming Soon

Section 1: Purpose
- Explain what the system does
- How it benefits DC operations

Section 2: What They'll Receive
- Daily emails with manager changes
- Grouped by DC territory
- Professional format

Section 3: Go-Live Date
- Announce launch date
- First email date/time

Section 4: Dashboard Access
- Link to dashboard
- How to request access

Section 5: Feedback
- How to submit feedback
- Support contact info
```

**Status:** ☐ In Progress / ☐ Complete  
**Draft Approved:** ☐ Yes / ☐ Date: ________  
**Sent to GMs:** ☐ Yes / ☐ Date: ________  
**Date Completed:** ___________

---

## 🧪 STAGING DEPLOYMENT CHECKLIST (Week 2)

### ☐ **Test Deployment on Production Server**

**Task 4.1: Deploy Code to Server** (2 hours)
- [ ] Copy all Python files to server
- [ ] Copy all template files to server
- [ ] Copy all config files to server  
- [ ] Install Python dependencies: `pip install -r requirements.txt`
- [ ] Run SETUP_WIZARD.py to configure
- [ ] Verify all paths are correct for server
- [ ] Test file permissions (can write to logs/db)

**Status:** ☐ In Progress / ☐ Complete  
**Code Location:** _____________________________  
**Dependencies Installed:** ☐ Yes / ☐ No  
**Configuration Complete:** ☐ Yes / ☐ No  
**Date Completed:** ___________

---

**Task 4.2: Scheduled Task Setup** (1 hour)
- [ ] Run `setup_hourly_task_auto.bat` as Administrator
- [ ] Verify Windows Task Scheduler shows:
  - [ ] Task Name: "DC_Manager_Change_Detection"
  - [ ] Schedule: Hourly, starting 2:00 AM
  - [ ] Run with highest privileges
  - [ ] Account: Service account
- [ ] Open Task Scheduler and verify task details
- [ ] Right-click task → Run to test immediately
- [ ] Check logs for successful execution
- [ ] Verify snapshot created in expected location

**Status:** ☐ In Progress / ☐ Complete  
**Task Created:** ☐ Yes / ☐ No  
**Schedule Correct:** ☐ Yes / ☐ No  
**Test Run:** ☐ Success / ☐ Failed  
**Date Completed:** ___________

---

**Task 4.3: Validate Production Setup** (1 day)
- [ ] Wait for first hourly execution (2 AM + 1 hour)
- [ ] Check logs: `/logs/daily_check.log`
- [ ] Expected log entries:
  ```
  [TIME] - Starting daily check
  [TIME] - VPN connection OK
  [TIME] - Snapshot created: 2026-02-26
  [TIME] - Changes detected: N
  [TIME] - Email generated for DC XXXX
  [TIME] - Email sent successfully
  [TIME] - Process complete
  ```
- [ ] Verify test emails received at `kendall.rush@walmart.com`
- [ ] Check dashboard shows new email count
- [ ] Test feedback submission from email
- [ ] Verify feedback appears in admin dashboard
- [ ] Document any issues

**Status:** ☐ In Progress / ☐ Complete  
**Logs Generated:** ☐ Yes / ☐ No  
**Test Emails Received:** ☐ Yes - Count: ___ / ☐ No  
**Dashboard Updated:** ☐ Yes / ☐ No  
**Feedback System:** ☐ Works / ☐ Errors  
**Overall Status:** ☐ Ready for Next / ☐ Issues to Fix  
**Date Completed:** ___________

---

**Task 4.4: One Week Monitoring** (5 min daily x 7 days)
Monitor these metrics daily:

```
Daily Check (Each morning):
├─ [ ] Check emails sent yesterday
├─ [ ] Verify count matches expected
├─ [ ] Check for any error messages
├─ [ ] Review dashboard metrics
└─ [ ] Document any anomalies

Weekly Summary:
├─ [ ] Total emails sent: ___
├─ [ ] Total DCs served: ___
├─ [ ] Any delivery failures: ___
├─ [ ] Feedback submissions: ___
├─ [ ] System errors: ___
└─ [ ] Overall status: ✅ / ⚠️
```

**Status:** ☐ In Progress / ☐ Complete  
**Monitoring Dates:** From _______ to _______  
**Issues Found:** [ ] None / [ ] Minor / [ ] Major  
**Ready for Production:** ☐ YES / ☐ NO  
**Date Completed:** ___________

---

## 🎯 PRODUCTION GO-LIVE CHECKLIST (Week 3)

### ☐ **Final Production Approval**

**Task 5.1: Executive Sign-Off** (1 day before launch)
- [ ] Schedule sign-off meeting with stakeholders
- [ ] Present: Project status, validation results, go-live plan
- [ ] Get approval to proceed:
  - [ ] Go-Live Date: Confirmed ___________
  - [ ] Recipient List: Approved ___________
  - [ ] Communication Plan: Approved ___________
  - [ ] Rollback Plan: In place ___________
- [ ] Identify escalation contact for launch day
- [ ] Assign IT help desk to handle questions

**Status:** ☐ In Progress / ☐ Complete  
**Sign-Off Obtained:** ☐ Yes / ☐ Date: ________  
**Escalation Contact:** _____________________________  
**Date Completed:** ___________

---

**Task 5.2: Production Configuration Switch** (2 hours before launch)
- [ ] Update `config.py`:
  - [ ] Change `TEST_MODE = False`
  - [ ] Verify all production settings correct
- [ ] Update `dc_email_config.py`:
  - [ ] Verify production recipient patterns
  - [ ] Confirm REPLY_TO address
- [ ] Run one final test:
  - [ ] Command: `python create_snapshot.py`
  - [ ] Expected: Snapshot created successfully
  - [ ] If fails: STOP and debug before proceeding
- [ ] Verify Windows Task Scheduler still shows task
- [ ] Have backup plan ready (manual email if needed)

**Status:** ☐ In Progress / ☐ Complete  
**TEST_MODE:** ☐ Changed to False  
**All Settings Verified:** ☐ Yes / ☐ No  
**Test Run Successful:** ☐ Yes / ☐ Failed  
**Ready to Launch:** ☐ YES / ☐ NO  
**Date/Time Completed:** ___________

---

**Task 5.3: Launch Day Preparation** (Morning of launch)
- [ ] Schedule launch-day team call: 1:00 AM-3:00 AM
- [ ] Prepare team:
  - [ ] Kendall (primary monitoring)
  - [ ] IT support (help desk)
  - [ ] Manager (escalation authority)
- [ ] Have communication channels ready:
  - [ ] Slack channel: #dc-manager-changes-launch
  - [ ] Phone: [Manager number]
  - [ ] Email: ATCTEAMSUPPORT@walmart.com
- [ ] Have rollback plan ready (just in case)
- [ ] Make sure everyone knows what to monitor

**Status:** ☐ In Progress / ☐ Complete  
**Team Assembled:** ☐ Yes  
**Communication Channels Tested:** ☐ Yes  
**Rollback Plan Ready:** ☐ Yes  
**Date Completed:** ___________

---

**Task 5.4: Launch Event (At scheduled time)
- [ ] Launch-day monitoring call starts
- [ ] Verify 2:00 AM task execution begins
- [ ] Monitor for first email send
  - Expected: 2:05-2:15 AM (after VPN check + processing)
- [ ] Verify email arrives at recipients
- [ ] Check dashboard metrics updating
- [ ] Monitor for any errors in logs
- [ ] Confirm no critical issues
- [ ] Send "Launch Successful" notification
- [ ] Continue monitoring for 24 hours

**Status:** ☐ Not Started / ☐ In Progress / ☐ Complete  
**First Email Sent:** ☐ Yes / ☐ No / ☐ Time: ______  
**Delivery Confirmed:** ☐ Yes / ☐ Failed  
**Dashboard Active:** ☐ Yes / ☐ No  
**Critical Issues:** ☐ None / ☐ Yes: ____________  
**Overall Launch Status:** ✅ SUCCESS / ⚠️ ISSUES / ❌ ROLLBACK  
**Date/Time Completed:** ___________

---

## 📊 POST-LAUNCH MONITORING (Week 4)

### ☐ **First 30 Days Operation**

**Daily Checklist (Days 1-7):**
```
Each Morning:
☐ Check email count from yesterday
☐ Verify emails reached all recipients
☐ Review system logs for errors
☐ Check dashboard for accuracy
☐ Document any issues
☐ Update stakeholders on status
```

**Weekly Review (Day 7, 14, 21, 28):**
```
☐ Compile metrics report
☐ Total emails sent
☐ Total DCs served
☐ Email delivery success rate
☐ Dashboard accuracy validation
☐ Feedback submissions received
☐ Any system errors or warnings
☐ Update stakeholders
```

**Monthly Assessment (Day 30):**
```
☐ Schedule stakeholder review meeting
☐ Present metrics and performance
☐ Gather feedback from DC managers
☐ Identify any improvements needed
☐ Plan next month's priorities
☐ Document lessons learned
☐ Update team on any enhancements
```

**Status:** ☐ In Progress / ☐ Complete  
**First Week Results:**
- Emails Sent: ______
- Delivery Rate: ____%
- System Uptime: ____%
- Issues Reported: ______

**Date Completed:** ___________

---

## 📋 SIGN-OFF MATRIX

### Completion Status

| Phase | Owner | Status | Date |
|-------|-------|--------|------|
| Management Decision | [Manager] | ☐ Complete | ____ |
| IT Setup & Access | [IT Lead] | ☐ Complete | ____ |
| Configuration & Testing | [Kendall] | ☐ Complete | ____ |
| Stakeholder Communication | [Manager] | ☐ Complete | ____ |
| Staging Deployment | [Kendall] | ☐ Complete | ____ |
| Production Go-Live | [Kendall + IT] | ☐ Complete | ____ |
| Post-Launch Monitoring | [Kendall] | ☐ In Progress | ____ |

---

## 🚨 ESCALATION CONTACTS

```
TECHNICAL ISSUES:
├─ Kendall Rush (Primary): kendall.rush@walmart.com, (___)-___-____
├─ IT Help Desk: [Phone], [Email]
└─ VPN/SDL Issues: [Support Team], [Phone]

BUSINESS ISSUES:
├─ Project Manager: [Name], [Email], [Phone]
├─ Executive Sponsor: [Name], [Email], [Phone]
└─ HR/Data Quality: [Name], [Email], [Phone]

GENERAL SUPPORT:
└─ Team Email: ATCTEAMSUPPORT@walmart.com
```

---

## ✅ FINAL APPROVAL

**I have reviewed all items and confirm we are ready to proceed:**

| Role | Approval | Date | Signature |
|------|----------|------|-----------|
| **Project Manager** | ☐ Approved | ____ | _________________ |
| **IT Leadership** | ☐ Approved | ____ | _________________ |
| **Executive Sponsor** | ☐ Approved | ____ | _________________ |
| **Finance** | ☐ Approved | ____ | _________________ |

---

**Document Version:** 1.0  
**Created:** February 25, 2026  
**Status:** Ready for Execution  
**Next Review:** After launch completion

