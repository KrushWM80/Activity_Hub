# 🚀 PayCycle Automation - Complete Setup Implementation Guide

**Status:** ✅ Ready to Deploy  
**Date:** February 25, 2026

---

## 📋 What We Have Built

### ✅ Complete (Ready Now)
1. **PayCycle Tracking System** - `paycycle_tracking.json`
   - Records all 26 PayCycle dates
   - Tracks when each email is sent
   - Maintains audit trail

2. **Recipient Management System** - `email_recipients.json`
   - Easy to switch between test and production
   - Add/remove recipients without code changes
   - Support for DC managers and store managers

3. **Management Utility** - `manage_paycycle.py`
   - View schedule: `python manage_paycycle.py schedule`
   - View recipients: `python manage_paycycle.py recipients`
   - Add recipients: `python manage_paycycle.py add-recipient production email@walmart.com "Name" "Title"`
   - Switch modes: `python manage_paycycle.py switch-mode production`
   - Record sends: `python manage_paycycle.py record-send 3 success`

### ⏳ Needs Setup (Pick One Below)
Create 26 individual PayCycle tasks in Windows Task Scheduler

---

## 🎯 OPTION 1: Manual Setup (Recommended - Most Control)

**Time:** 30-45 minutes  
**Difficulty:** Easy (no coding)  
**Best For:** First-time setup, understanding the system

### Quick Setup For One Task (Then Repeat 26 Times)

**Step 1: Open Task Scheduler**
```
Windows Key + R
taskschd.msc
Enter
```

**Step 2: Create Task (PC 03 Example)**
1. Right-click "Task Scheduler Library"
2. Click "Create Basic Task"
3. Fill in:
   - **Name:** `DC-EMAIL-PC-03`
   - **Description:** `DC Manager Change Detection - PayCycle 3 (March 6, 2026)`
   - Click **Next**

**Step 3: Set Trigger**
1. Select: "One time"
2. Click **Next**
3. Set date/time:
   - **Date:** 03/06/2026  (For PC 03; adjust for each PC)
   - **Time:** 06:00:00
   - Click **Next**

**Step 4: Set Action**
1. Select: "Start a program"
2. Click **Next**
3. Enter:
   - **Program/script:** `C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe`
   - **Add arguments:** `daily_check_smart.py`
   - **Start in:** `C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails`
4. Click **Next**

**Step 5: Finish**
1. Check: **Open the Properties dialog for this task when I click Finish**
2. Click **Finish**

**Step 6: Task Scheduler Options**
1. **General tab:**
   - Check: "Run with highest privileges"
2. **Triggers tab:**
   - Select trigger → **Edit**
   - Check: "Enabled"
   - Set: "Repeat task every" → N/A (one time only)
3. **Actions tab:**
   - Verify action is set correctly
4. **Settings tab:**
   - Check: "If the task fails, retry every: 1 hour (for 7 attempts)"
   - Check: "Run task as soon as possible after a scheduled start is missed"
5. Click **OK**

**Repeat for all 26 PayCycles** (use the dates/times from paycycle_tracking.json)

---

## 🎯 OPTION 2: PowerShell Script (If Admin Available)

**Time:** 5 minutes  
**Difficulty:** Easy  
**Best For:** Admins, batch creation

### Prerequisites
- PowerShell run as Administrator
- Task Scheduler access

### Steps

1. **Open PowerShell as Administrator**
   - Right-click PowerShell → Run as Administrator
   - Click Yes

2. **Navigate to project**
   ```powershell
   cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails"
   ```

3. **Allow scripts to run**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
   ```

4. **Run setup script**
   ```powershell
   .\setup_tasks_revised.ps1
   ```

5. **Verify tasks created**
   ```powershell
   Get-ScheduledTask | Where-Object {$_.TaskName -like "DC-EMAIL-PC-*"} | Select-Object TaskName | Format-Table
   ```

---

## 🎯 OPTION 3: Use Your DevOps Team

**Time:** N/A (delegate to team)  
**Best For:** Organizations with dedicated DevOps

**What To Give Them:**
- `setup_tasks_revised.ps1` - PowerShell script
- `paycycle_tracking.json` - PayCycle dates
- Requirements:
  - Python executable: `.venv\Scripts\python.exe`
  - Working directory: `...DC to Store Change Management Emails`
  - All 26 tasks scheduled for PC dates at 06:00 AM

**Reference Dates:**
```
PC 01: 2026-02-06  (past)
PC 02: 2026-02-20  (past)
PC 03: 2026-03-06  (first auto send - 9 days away)
PC 04: 2026-03-20
... [through PC 26: 2027-01-22]
```

---

## 📊 All 26 PayCycle Dates (For Reference)

Use these dates when creating tasks:

```
PC 01: 2026-02-06 @ 06:00  | Historical
PC 02: 2026-02-20 @ 06:00  | Historical
PC 03: 2026-03-06 @ 06:00  | FIRST AUTO SEND ⭐
PC 04: 2026-03-20 @ 06:00
PC 05: 2026-04-03 @ 06:00
PC 06: 2026-04-17 @ 06:00
PC 07: 2026-05-01 @ 06:00
PC 08: 2026-05-15 @ 06:00
PC 09: 2026-05-29 @ 06:00
PC 10: 2026-06-12 @ 06:00
PC 11: 2026-06-26 @ 06:00
PC 12: 2026-07-10 @ 06:00
PC 13: 2026-07-24 @ 06:00
PC 14: 2026-08-07 @ 06:00
PC 15: 2026-08-21 @ 06:00
PC 16: 2026-09-04 @ 06:00
PC 17: 2026-09-18 @ 06:00
PC 18: 2026-10-02 @ 06:00
PC 19: 2026-10-16 @ 06:00
PC 20: 2026-10-30 @ 06:00
PC 21: 2026-11-13 @ 06:00
PC 22: 2026-11-27 @ 06:00
PC 23: 2026-12-11 @ 06:00
PC 24: 2026-12-25 @ 06:00
PC 25: 2027-01-08 @ 06:00
PC 26: 2027-01-22 @ 06:00
```

---

## ✨ What You Can Do RIGHT NOW (Without Tasks)

All these work TODAY with full tracking and recipient management:

### 1. View Full PayCycle Calendar
```powershell
python manage_paycycle.py schedule
```
**Output:** All 26 dates, status, notes

### 2. Manage Recipients
```powershell
python manage_paycycle.py recipients
```
**Output:** Current test/production recipients

### 3. Add Production Recipients
```powershell
python manage_paycycle.py add-recipient production john@walmart.com "John Smith" "DC Manager"
python manage_paycycle.py add-recipient production jane@walmart.com "Jane Doe" "Store Manager"
```

### 4. Switch to Production
```powershell
python manage_paycycle.py switch-mode production
```

### 5. Record Sends (After Manual Test)
```powershell
python manage_paycycle.py record-send 3 success
```

### 6. Track All Activity
View `paycycle_tracking.json` for complete history

---

## 🔄 Workflow Options

### Option A: Manual Testing + Auto Tasks
```
TODAY (2/25):
  1. Set up recipient management ✓ (DONE)
  2. Add production recipients
  3. Create 26 PayCycle tasks

3/6/2026 (PC 03):
  4. Tasks run automatically
  5. Record sends

3/20+ (PC 04+):
  6. Continue auto-sends
  7. Monitor via tracking system
```

### Option B: Manual Testing + Manual Sends
```
TODAY (2/25):
  1. Set up recipient management ✓ (DONE)
  2. Add production recipients

Each PayCycle (Starting 3/6):
  3. Manually run: python daily_check_smart.py
  4. Record via: python manage_paycycle.py record-send X success

Benefit: Full control, can test before each send
```

### Option C: Staged Rollout
```
PC 03-04 (3/6, 3/20):
  - Manual test sends
  - Validate with 3 testers
  - Record results

PC 05-06 (4/3, 4/17):
  - Add first DC manager
  - Test with production recipient
  - Continue manual sends

PC 07+:
  - Move to auto tasks if confident
  - Monitor first auto-send carefully
  - Expand to full DC roster
```

---

## 📝 Recipient Management - Easy Steps

### Step 1: Identify DC Recipients
Get email addresses for:
- [ ] DC managers (names/emails)
- [ ] Store manager distribution list (if available)
- [ ] Any other key recipients

### Step 2: Add to Production
```powershell
# DC Manager from Dallas DC
python manage_paycycle.py add-recipient production dallas.dc@walmart.com "Dallas DC" "DC Manager"

# DC Manager from Atlanta DC
python manage_paycycle.py add-recipient production atlanta.dc@walmart.com "Atlanta DC" "DC Manager"

# Store Manager distribution (optional)
python manage_paycycle.py add-recipient production store-mgrs@walmart.com "Store Managers" "Distribution List"
```

### Step 3: Verify
```powershell
python manage_paycycle.py recipients
```

### Step 4: Switch
```powershell
python manage_paycycle.py switch-mode production
```

### Step 5: Test (Run Manually)
```powershell
python daily_check_smart.py
```

### Step 6: Record
```powershell
python manage_paycycle.py record-send 3 success
```

---

## 🎯 Immediate Next Steps

### Must Do (Today if Possible)
1. ✅ Decide which setup option (Manual/PowerShell/DevOps)
2. ✅ Create the 26 tasks using chosen method
3. ✅ Verify tasks appear in Task Scheduler

### Should Do (By 3/5/2026)
1. Add actual DC recipient emails
2. Switch to production mode
3. Do final verification before first auto-send

### Nice To Have (Before Going Live)
1. Test one manual send to validate format
2. Get feedback from test recipients
3. Document any custom changes

---

## 📞 Troubleshooting Setup

### PowerShell Script Won't Run
**Error:** "Access is denied"  
**Solution:** Run PowerShell as Administrator

**Error:** "Cannot find path"  
**Solution:** Verify working directory path is correct

**Error:** "Python not found"  
**Solution:** Verify `.venv\Scripts\python.exe` exists

### Manual Task Won't Execute
**Check:**
1. Is date in future? (past dates won't trigger)
2. Is Outlook running? (for email sending)
3. Is Python path correct?
4. Is working directory correct?

**Test:**
1. Right-click task → Run
2. Task should execute immediately
3. Check `emails_sent/` folder for output

### Emails Not Received
**Check:**
1. Task ran? (check Task History)
2. Recipients list updated? (`manage_paycycle.py recipients`)
3. Are emails in `emails_sent/` folder?
4. Outlook COM available? (might need `pip install pywin32`)

---

## ✅ Verification Checklist

After setup, verify each item:

- [ ] 26 tasks created in Task Scheduler
- [ ] All tasks show date/time from PayCycle schedule
- [ ] All tasks point to correct Python executable
- [ ] All tasks have correct working directory
- [ ] All tasks set to "Run with highest privileges"
- [ ] First task (PC 03) scheduled for 3/6/2026 @ 6:00 AM
- [ ] Recipient management system working
- [ ] Can view schedule: `python manage_paycycle.py schedule`
- [ ] Can view recipients: `python manage_paycycle.py recipients`
- [ ] Can add recipients: `python manage_paycycle.py add-recipient...`
- [ ] Can switch modes: `python manage_paycycle.py switch-mode production`

---

## 📊 Status Summary

| Component | Status | Action |
|-----------|--------|--------|
| PayCycle Tracking | ✅ Ready | Start using now |
| Recipient Management | ✅ Ready | Start using now |
| Management Utility | ✅ Ready | Start using now |
| Manual Test | ✅ Completed | Validated 2/25 |
| 26 PayCycle Tasks | ⏳ Pending | Choose setup method |
| Production Recipients | ⏳ Pending | Identify emails |
| Git Continuous Updates | ✅ Ready | Track all changes |

---

## 🎯 Your Next Action

**Choose one:**

**A) I'm technical → Use PowerShell Script**
```
1. Open PowerShell as Administrator
2. Run: .\setup_tasks_revised.ps1
3. Verify: Get-ScheduledTask | Where-Object {$_.TaskName -like "DC-EMAIL-PC-*"}
```

**B) I prefer visual → Manual Setup via GUI**
```
1. Open: taskschd.msc
2. Create 26 tasks manually using dates above
3. Takes ~2 hours for all 26
```

**C) I'll delegate → Give to DevOps/IT**
```
1. Send them: setup_tasks_revised.ps1 and paycycle_tracking.json
2. Reference dates above
3. They run as admin
```

**After tasks are created:**
```
1. Add production recipients
2. Test with manual send
3. Record via tracking utility
4. Go live! 🚀
```

---

**Questions?** Refer to RECIPIENT_TRACKING_GUIDE.md for detailed management examples.

