# Walmart PayCycle Information & Testing Schedule
## For DC to Store Change Management System Testing
**Created:** February 25, 2026

---

## 📅 Understanding Walmart PayCycles

### Standard Walmart PayCycle Format

Walmart typically operates on a **biweekly (14-day) pay cycle**:

- **Schedule:** Sunday through Saturday
- **Frequency:** 26 pay periods per year (2 per month)
- **Pay Day:** Usually Friday (or sometimes Thursday evening via direct deposit)
- **Example:** 
  - PC01: Jan 5 (Sun) - Jan 18 (Sat)
  - PC02: Jan 19 (Sun) - Feb 1 (Sat)
  - PC03: Feb 2 (Sun) - Feb 15 (Sat)
  - etc.

---

## 🔍 How to Find 2026 Walmart PayCycle Calendar

### Option 1: WalmartOne (Self-Service Portal)
1. Go to: walmartone.walmart.com
2. Login with your Walmart credentials
3. Navigate: Pay/Time → Pay Calendar
4. Display: 2026 calendar with all pay periods
5. Screenshot or download all dates

### Option 2: ADP/Payroll System
1. Contact: Your HR Department or Payroll Team
2. Ask: "Can you provide the 2026 biweekly PayCycle dates?"
3. Request format: 
   ```
   PayCycle 1: Jan 5, 2026 - Jan 18, 2026
   PayCycle 2: Jan 19, 2026 - Feb 1, 2026
   [etc for all 26 cycles]
   ```

### Option 3: Your Recent Paystub
1. Open: Any Walmart paystub received recently
2. Look for: "Pay Period" or "Period Ending" date
3. Calculate backward: That date + 1 day = next PayCycle start
4. Then count forward by 14 days for each cycle

### Option 4: Email Payroll/HR
```
Subject: Request - 2026 Biweekly PayCycle Calendar

Hi [HR/Payroll Team],

Could you please provide a list of all 26 biweekly pay cycles 
for 2026 with their start and end dates? We need this to 
schedule manager change notifications to distribution centers 
at the end of each pay period.

Format preferred:
- PayCycle #: [Start Date] - [End Date]

Thank you!
```

---

## 📋 2026 Walmart PayCycle Estimate

**Based on historical patterns**, 2026 likely follows this schedule:

```
Q1 2026:
PC01: Jan 5 - Jan 18
PC02: Jan 19 - Feb 1
PC03: Feb 2 - Feb 15
PC04: Feb 16 - Mar 1
PC05: Mar 2 - Mar 15
PC06: Mar 16 - Mar 29
PC07: Mar 30 - Apr 12 (approx)

Q2 2026:
PC08: Apr 13 - Apr 26
PC09: Apr 27 - May 10
PC10: May 11 - May 24
PC11: May 25 - Jun 7
PC12: Jun 8 - Jun 21
PC13: Jun 22 - Jul 5 (approx)

[etc...]
```

**⚠️ IMPORTANT:** These are ESTIMATES. Actual dates may vary.
**Get official PayCycle calendar to confirm.**

---

## 🚀 Running the System on This Computer

### Step 1: Verify Setup (5 minutes)

```powershell
# Open PowerShell in project folder
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails"

# Activate Python environment (if not already)
& "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\Activate.ps1"

# Verify Python
python --version
# Expected output: Python 3.8+

# Verify required packages
pip list | findstr "pandas requests pywin32"
# Expected: All packages listed
```

### Step 2: Initial Configuration (10 minutes)

```powershell
# Run setup wizard
python SETUP_WIZARD.py

# Follow prompts:
# 1. Confirm output folder (snapshots location)
# 2. Confirm SDL URL
# 3. Choose: Manual test (now) or Auto (scheduler)
```

### Step 3: Test Data Collection (5-10 minutes)

```powershell
# Test: Can we create a snapshot?
python create_snapshot.py

# Expected output:
# ✓ VPN check: OK
# ✓ Connecting to SDL...
# ✓ Downloaded manager data
# ✓ Snapshot saved: manager_snapshot_2026-02-25.json
# ✓ Total locations: 5,207

# If error: Check VPN connection
#   Command: ipconfig /all
#   Look for: Cisco VPN adapter (should show)
```

### Step 4: Test Change Detection (5 minutes)

```powershell
# Test: Generate a second snapshot (or copy existing)
python create_snapshot.py

# Compare with previous
python compare_snapshots.py

# Expected output:
# Total changes detected: [number]
# - Store Manager: [number] changes
# - Market Manager: [number] changes
# - Regional GM: [number] changes
# etc.
```

### Step 5: Test Email Generation (5 minutes)

```powershell
# Generate test email template
python dc_email_generator_html.py

# Expected output:
# ✓ Email generated: MOCK_EMAIL_TEMPLATE.html

# View in browser
start MOCK_EMAIL_TEMPLATE.html

# Check:
# ✓ Spark logo visible?
# ✓ Colors correct (navy/blue)?
# ✓ Manager changes listed?
# ✓ "Send Feedback" button visible?
# ✓ "View Store Managers" button visible?
```

### Step 6: Test Email Sending (10 minutes)

```powershell
# First: Make sure Outlook is running
# File menu → Verify you're logged in

# Then: Run the main check
python daily_check_smart.py

# Expected output:
# [TIME] Starting daily check
# [TIME] VPN check: OK
# [TIME] Snapshot created: manager_snapshot_2026-02-25.json
# [TIME] Changes detected: [number]
# [TIME] Email generated
# [TIME] Email sent to 3 test recipients
# [TIME] Process complete

# If error: Check logs
Get-Content manager_snapshot.log | Select-Object -Last 30
```

### Step 7: Verify Email Receipt (10 minutes)

**Check email inbox for all 3 recipients:**

1. **Kristine.Torres@walmart.com**
   - [ ] Email received?
   - [ ] Sender: supplychainops@email.wal-mart.com
   - [ ] Content looks right?
   - [ ] All buttons work?

2. **Matthew.Farnworth@walmart.com**
   - [ ] Email received?
   - [ ] Same content as Kristine?
   - [ ] Can reply?

3. **Kendall.Rush@walmart.com**
   - [ ] Email received?
   - [ ] Same content?
   - [ ] Check reply-to address

---

## 📊 Dashboard Access (Optional)

If you want to see the real-time metrics dashboard:

```powershell
# In a new PowerShell window (keep current one for monitoring)
cd "[project folder]"

# Start dashboard server
python dashboard.py

# Output: 
# Running on http://localhost:5000

# Open browser:
# http://localhost:5000

# You should see:
# - Total Changes Detected: [number]
# - Total Emails Sent: 3 (to test group)
# - Charts and metrics
```

---

## ⏰ Timeline: When to Test Based on PayCycles

### Once You Provide PayCycle Dates:

```
EXAMPLE SCHEDULE (using estimate dates):

WEEK 1: Feb 24-Mar 1
┌─ Feb 25 (TODAY)
│  └─ Setup & Configuration
│     └─ Run test manually NOW
│     └─ Confirm 3 recipients receive email
│     └─ Gather feedback

WEEK 2: Mar 2-8  
└─ Mar 1 (PayCycle ends)
   └─ Auto email should send
   └─ Verify scheduled send works
   └─ Review results

WEEK 3: Mar 9-15
└─ Mar 15 (PayCycle ends)
   └─ Second auto send
   └─ Compare with first test
   └─ Implementation decisions

WEEK 4: Mar 16-22
└─ Mar 29 (PayCycle ends - next one)
   └─ Final validation
   └─ Prepare for production rollout
```

---

## ✅ Checklist: Ready to Test

- [ ] PayCycle calendar obtained (or estimated dates)
- [ ] System running on this computer
- [ ] 3 test recipients confirmed
- [ ] Outlook desktop client running
- [ ] VPN connected
- [ ] First test email sent
- [ ] All 3 recipients confirmed receipt
- [ ] Email content reviewed
- [ ] Buttons tested (Send Feedback, View Managers)
- [ ] Dashboard checked
- [ ] No errors in system logs
- [ ] Ready to schedule future sends

---

## 🔔 What Happens When You Don't Provide PayCycle Dates

**Without PayCycle dates, you have two options:**

### Option A: Manual Testing (Recommended for now)
```
You: Run python daily_check_smart.py
System: Sends email immediately to 3 recipients
Result: Email sent when you choose to run it
```

### Option B: Hourly Testing (Current default)
```
Windows Task Scheduler: Runs hourly at 2:00 AM+
System: Checks if managers changed, sends if yes
Result: Email could send multiple times if changes persist
```

**Recommendation:** Use Option A until you have PayCycle dates.

---

## 📞 Who to Contact for PayCycle Dates

**Ask these people at Walmart:**

1. **Your Direct Manager**
   - "Do you have the 2026 PayCycle calendar?"
   
2. **HR Department**
   - "Can you provide 2026 biweekly PayCycle dates?"
   
3. **Payroll Department**
   - "What are all 26 pay periods in 2026?"
   
4. **WalmartOne Support**
   - Call helpdesk if you can't find calendar online

**Fast way:** Go to WalmartOne, it's always there under Pay/Calendar.

---

## 🎯 Summary

| Item | Status | Next Step |
|------|--------|-----------|
| **System Setup** | ✅ Ready | Run SETUP_WIZARD.py |
| **Test Recipients** | ✅ Configured | Kristine, Matthew, Kendall |
| **Email Config** | ✅ Ready | Will send to all 3 |
| **PayCycle Dates** | ⏳ NEEDED | Get from WalmartOne/HR |
| **First Test** | ✅ Can run NOW | Manual execution anytime |
| **Scheduled Tests** | ⏳ NEEDS dates | Once PayCycles provided |

---

**Status:** Ready to begin testing  
**Next Block:** PayCycle calendar dates  
**Can proceed:** YES - manual testing can start now

