# 📅 PayCycle-Based Email Scheduling Setup Guide

**Status:** ✅ Ready for Implementation  
**Date:** February 25, 2026  
**Document:** PayCycle Auto-Schedule Configuration

---

## 🎯 Objective

Configure Windows Task Scheduler to automatically send manager change notification emails on each Walmart PayCycle end date.

**Result:** Fully automated email system sending on 26 predetermined dates in 2026.

---

## 📊 PayCycle Schedule Overview

### FY27 2026 Calendar (26 PayCycles)

```
PC 01:   2/6/26   (Friday)  ← Passed (1/19 days ago)
PC 02:   2/20/26  (Friday)  ← Passed (5 days ago)

→ TODAY: 2/25/26  (Wednesday)

PC 03:   3/6/26   (Friday)  ← NEXT - 9 DAYS ⭐ FIRST AUTO SEND
PC 04:   3/20/26  (Friday)
PC 05:   4/3/26   (Friday)
PC 06:   4/17/26  (Friday)
... [20 more cycles through January 2027]
```

**Key Dates:**
- **First Automated Send:** PC 03 on March 6, 2026 at 6:00 AM
- **Total Cycles:** 24 in 2026, 2 in 2027
- **All PayCycles:** Friday end dates (consistent biweekly)

---

## 🔧 Implementation Options

### Option A: Simple Recurring Task (Easiest)
**Recommended for initial testing**

Creates ONE recurring task that runs every 2 weeks starting from first date.

**Pros:**
- ✅ Simple to set up
- ✅ Easy to modify
- ✅ Single task to manage

**Cons:**
- ⚠️ Less visibility into individual cycles
- ⚠️ Harder to skip a specific PayCycle if needed

**Setup Time:** 5 minutes

---

### Option B: Individual PayCycle Tasks (Recommended for Production)
**Recommended for full control and visibility**

Creates 26 separate tasks, one per PayCycle end date.

**Pros:**
- ✅ Maximum visibility
- ✅ Can disable/skip individual cycles
- ✅ Better for audit/compliance
- ✅ Easy to see all scheduled dates

**Cons:**
- ⚠️ More setup time
- ⚠️ More tasks to manage

**Setup Time:** 15-20 minutes

---

## 🚀 Implementation Method

### **Option A: Simple Recurring Task (5 minutes)**

**Step 1: Open Task Scheduler**
```
Windows Key + R
Type: taskschd.msc
Press Enter
```

**Step 2: Create New Folder**
1. Expand "Task Scheduler Library" (left panel)
2. Right-click > "New Folder"
3. Name: `DC to Store Change Management Emails`
4. Click OK

**Step 3: Create New Task**
1. Right-click new folder > "Create Task"
2. **General Tab:**
   - Name: `DC-EMAIL-PayCycle-Recurring`
   - Description: "DC Manager Change Detection - Every PayCycle"
   - Security: Run with "Run with highest privileges" ✓
   - Hidden ✗ (uncheck)

3. **Triggers Tab → New Trigger**
   - Begin the task: "On a schedule"
   - Schedule: "Weekly"
   - Repeat every: 2 weeks
   - On Friday
   - At: 06:00:00
   - Start date: 3/6/2026 (first PayCycle)
   - Click OK

4. **Actions Tab → New Action**
   - Action: "Start a program"
   - Program/script: `C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe`
   - Add arguments: `daily_check_smart.py`
   - Start in: `C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails`
   - Click OK

5. **Settings Tab:**
   - Allow start if on batteries ✓
   - Do not stop if on batteries ✓
   - Start if available ✓
   - Run task as soon as possible ✓
   - If task fails, retry: ✓ Every 1 hour (for 7 attempts)

6. Click OK to create task

---

### **Option B: Individual PayCycle Tasks (Automated Script)**

**Step 1: Open PowerShell as Administrator**
```
Windows Key
Type: PowerShell
Right-click > Run as Administrator
```

**Step 2: Navigate to Project Folder**
```powershell
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails"
```

**Step 3: Run Setup Script**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
& .\setup_paycycle_tasks.ps1
```

**Step 4: Verify Tasks Created**
```
Task Scheduler > Task Scheduler Library > DC to Store Change Management Emails
Should see 26 tasks: DC-EMAIL-PC-01 through DC-EMAIL-PC-26
```

---

## 📋 Manual PayCycle Task Creation (If Scripts Don't Work)

If the automated script doesn't work, create tasks manually:

**For Each PayCycle (1-26):**

1. Open Task Scheduler
2. Right-click "DC to Store Change Management Emails" folder
3. Create New Task:
   - Name: `DC-EMAIL-PC-{##}` (e.g., PC-03, PC-04)
   - Description: `FY27 PC {##} - {DATE}`
   
4. Triggers Tab:
   - Once
   - Start: {DATE} at 06:00
   
5. Actions Tab:
   - Program: `C:\...\python.exe`
   - Arguments: `daily_check_smart.py`
   - Start in: `C:\...\DC to Store Change Management Emails`

**Example for PC 03 (3/6/26):**
```
Task: DC-EMAIL-PC-03
Date: 3/6/2026
Time: 06:00 AM
Script: daily_check_smart.py
Folder: .../DC to Store Change Management Emails
```

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Task Scheduler folder created: "DC to Store Change Management Emails"
- [ ] All tasks visible in Task Scheduler
- [ ] First task scheduled for PC 03 (3/6/26 at 6:00 AM)
- [ ] Task action configured with correct Python exe path
- [ ] Task action configured with correct working directory
- [ ] Task triggers set to run on PayCycle dates
- [ ] Settings configured for retry on failure

---

## 🧪 Testing Tasks

### Test 1: Verify Task Configuration
1. Open Task Scheduler
2. Navigate to "DC to Store Change Management Emails" folder
3. Right-click any task > "Properties"
4. Verify:
   - Trigger shows correct date/time
   - Action shows correct Python path
   - Directory is correct

### Test 2: Run Task Manually
1. Right-click task > "Run"
2. Task should execute immediately
3. Check: Emails should be sent to 3 test recipients
4. Look for generated HTML file in `emails_sent/` folder

### Test 3: Check Task Execution
1. Task Scheduler > History tab (on task)
2. Should see execution entries
3. Status should be "Task Completed"
4. Exit code: 0 (success)

### Test 4: Wait for Automatic Execution
1. Let system run at scheduled time
2. PC 03: 3/6/26 at 6:00 AM
3. Monitor inbox for emails to 3 recipients
4. Check `emails_sent/` folder for generated files

---

## 🐛 Troubleshooting

### Task Not Running

**Problem:** Task shows in scheduler but doesn't execute

**Solutions:**
1. Check trigger date/time is in future
2. Verify Python path is correct (right-click > Properties > Actions)
3. Verify working directory exists
4. Run task manually first (right-click > Run)
5. Check Task Scheduler History for errors

### Emails Not Sending

**Problem:** Task runs but emails not received

**Solutions:**
1. Verify Outlook is running on system
2. Verify pywin32 installed: `pip install pywin32`
3. Check `emails_sent/` folder for generated HTML
4. Review email_helper.py for error handling
5. Check Outlook sent items

### Network/VPN Issues

**Problem:** Task runs but SDL data not available

**Solution:**
1. System has 7-day VPN retry built-in
2. First failure: Retries hourly for 7 days
3. After 7 days: Sends error notification
4. Once VPN available: Completes successfully

---

## 📝 Task Execution Details

### What Happens When Task Runs

1. **Activation:** Task Scheduler triggers at scheduled time
2. **Execution:** Runs `daily_check_smart.py`
3. **VPN Check:** System checks SDL connection
4. **Data Fetch:** Downloads manager data from SDL
5. **Comparison:** Creates snapshot & compares with previous
6. **Change Detection:** Identifies manager changes
7. **Email Generation:** Creates HTML email with changes
8. **Send:** Sends to 3 test recipients (or DC list in production)
9. **Logging:** Records execution in `manager_snapshot.log`

### Typical Execution Time

- **Quick Check (No changes):** 2-3 minutes
- **Normal Run (1-5 changes):** 5-10 minutes
- **Large Run (100+ changes):** 10-15 minutes
- **VPN Timeout:** 30-60 seconds (will retry next hour)

---

## 📊 Monitoring & Maintenance

### Daily Monitoring
- Check inbox for emails at expected times
- Verify all 3 recipients received emails
- Monitor `emails_sent/` folder for generated files

### Weekly Monitoring
- Check Task Scheduler History for failures
- Review `manager_snapshot.log` for errors
- Verify no stale snapshot files

### Monthly Monitoring
- Review full month of executions
- Check for any missed PayCycles
- Validate email counts match expected (usually 0-2 changes/PayCycle)

---

## 🎛️ Advanced Options

### Modify Task Time
If 6:00 AM doesn't work:
1. Open Task Scheduler
2. Select task
3. Double-click "Trigger" in Triggers list
4. Change "Start time" to preferred time
5. Click OK

### Disable Task Temporarily
1. Right-click task
2. "Disable" (will skip next execution)
3. "Enable" to resume

### Delete All Tasks
```powershell
# For recurring task:
Unregister-ScheduledTask -TaskName "DC-EMAIL-PayCycle-Recurring" -TaskPath "\DC to Store Change Management Emails\" -Confirm:$false

# For individual tasks (if created):
Get-ScheduledTask -TaskPath "\DC to Store Change Management Emails\" | Unregister-ScheduledTask -Confirm:$false
```

---

## 📞 Support & Escalation

### Issue: Task Not Created
- Check admin privileges
- Verify PowerShell execution policy: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned`

### Issue: Python Not Running
- Verify .venv is activated: `.venv\Scripts\Activate.ps1`
- Check python path: `.venv\Scripts\python.exe -V`

### Issue: SQL Database Lock
- Stop all running tasks
- Run: `daily_check_smart.py` manually
- Resume tasks

### Issue: Outlook COM Error
- Ensure Outlook is installed
- Install pywin32: `pip install pywin32`
- Restart Outlook

---

## ✨ Summary

| Aspect | Details |
|--------|---------|
| **Setup Time** | 5-20 minutes |
| **Automation** | 26 PayCycles × 1 year = Full 2026 coverage |
| **Recipients** | 3 test recipients (Kristine, Matthew, Kendall) |
| **First Run** | PC 03: March 6, 2026 at 6:00 AM |
| **Frequency** | Every 2 weeks (biweekly) |
| **Status** | ✅ Ready to deploy |

---

**Next Step:** Choose implementation method above and proceed with setup.  
**Questions?** Review troubleshooting section or check email logs.

