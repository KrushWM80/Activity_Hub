# ⚡ QUICK START: PayCycle Schedule Implementation

**Target:** Set up automated DC Manager Change Detection emails for all 26 PayCycles in 2026

**Time Required:** 10-15 minutes  
**Difficulty:** Easy (no coding required)

---

## 🎯 OPTION A: Simple (5 minutes) ✅ RECOMMENDED FOR FIRST TEST

One recurring task = automatic sends every 2 weeks

### Quick Steps:

1. **Open Task Scheduler**
   - Windows Key + R → `taskschd.msc` → Enter

2. **Create Folder**
   - Right-click "Task Scheduler Library" → "New Folder"
   - Name: `DC to Store Change Management Emails`

3. **Create Task**
   - Right-click folder → "Create Task"
   - Name: `DC-EMAIL-PayCycle-Recurring`

4. **Set Trigger**
   - Triggers Tab → New
   - Weekly, every 2 weeks, Friday, 6:00 AM
   - Start: 3/6/2026
   - Click OK

5. **Set Action**
   - Actions Tab → New
   - Program: `C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe`
   - Arguments: `daily_check_smart.py`
   - Start in: `C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails`
   - Click OK

6. **Set Settings**
   - Settings Tab → Check:
     - Allow start if on batteries ✓
     - Don't stop if on batteries ✓
     - Start if available ✓
     - Run as soon as possible ✓

7. **Create** → Done!

**Result:** Automatic sends on 3/6, 3/20, 4/3, 4/17... every 2 weeks

---

## 🎯 OPTION B: Advanced (20 minutes) 🔧 RECOMMENDED FOR PRODUCTION

26 individual tasks = full visibility + granular control

### Quick Steps:

1. **Open PowerShell as Administrator**
   - Windows Key → PowerShell → Right-click → Run as Administrator

2. **Navigate to Project**
   ```powershell
   cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails"
   ```

3. **Allow Script Execution**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

4. **Run Setup Script**
   ```powershell
   .\setup_paycycle_tasks.ps1
   ```

5. **Verify**
   - Open Task Scheduler
   - View: Task Scheduler Library → DC to Store Change Management Emails
   - Should see 26 tasks: DC-EMAIL-PC-01 through DC-EMAIL-PC-26

**Result:** Individual tasks for each PayCycle, all visible in one folder

---

## ✅ Verification (Both Options)

After setup, verify in Task Scheduler:

- [ ] Folder exists: "DC to Store Change Management Emails"
- [ ] Task(s) created (1 recurring or 26 individual)
- [ ] Trigger set to Friday at 6:00 AM
- [ ] Start date is 3/6/2026 or future
- [ ] Action: Python exe + daily_check_smart.py
- [ ] Working directory correct

---

## 🧪 Test It

### Manual Test (First Validation)
1. Right-click task → "Run"
2. Task executes immediately
3. Check inbox for test emails
4. Look for HTML file in `emails_sent/` folder

### Automatic Test (2nd Validation)
1. Let system run at scheduled time
2. PC 03: March 6, 2026 at 6:00 AM
3. Check inbox for emails
4. Verify execution in Task History

---

## 📊 PayCycle Dates (For Reference)

```
PAST (Already happened):
✗ PC 01: 2/6/26
✗ PC 02: 2/20/26

CURRENT:
→ Today: 2/25/26

UPCOMING (Ready to schedule):
✓ PC 03: 3/6/26   ← FIRST AUTO SEND (9 days)
✓ PC 04: 3/20/26
✓ PC 05: 4/3/26
✓ PC 06: 4/17/26
✓ PC 07: 5/1/26
[... 19 more through 2027]
```

---

## 🚨 Common Issues & Quick Fixes

| Issue | Fix |
|-------|-----|
| **Execution Policy Error** | Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| **Task Not Running** | Edit task → verify trigger date is in future; Python path is correct |
| **Emails Not Sending** | Ensure Outlook running; check `emails_sent/` folder for HTML files |
| **Network Error** | System retries for 7 days; VPN access needed to fetch SDL data |

---

## 📞 Need Help?

See: **PAYCYCLE_SCHEDULE_SETUP_GUIDE.md** for:
- Step-by-step screenshots
- Troubleshooting section
- Advanced options (change time, disable tasks, etc.)

---

## 🎉 Summary

**What You're Setting Up:**
- Fully automated DC Manager Change Detection system
- Sends emails on each PayCycle end (3/6, 3/20, 4/3, 4/17, etc.)
- Sends to: Kristine Torres, Matthew Farnworth, Kendall Rush
- Set it once, runs automatically for entire 2026

**Time Investment:** 10 minutes  
**Benefit:** 100% automation for 26 PayCycles  
**ROI:** High (no manual intervention needed)

---

**Ready?** Pick Option A (5 min) or Option B (20 min) and get started!

