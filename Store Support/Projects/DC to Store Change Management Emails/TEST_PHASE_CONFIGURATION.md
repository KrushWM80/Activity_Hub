# DC to Store Change Management System
## Test Deployment Configuration
**Created:** February 25, 2026  
**Status:** Ready for Testing Phase  
**Test Recipients:** 3 people

---

## ✅ Test Recipients Configured

### Test Email Recipients
The system is now configured to send test emails to:

1. ✅ **Kristine.Torres@walmart.com**
2. ✅ **Matthew.Farnworth@walmart.com**
3. ✅ **Kendall.Rush@walmart.com**

**Configuration Updated In:**
- `config.py` - Added `TEST_EMAILS` list with 3 recipients
- `dc_email_config.py` - Added `TEST_RECIPIENTS` list with 3 recipients
- **TEST_MODE = True** - All emails will go to these 3 people only

---

## ⚠️ IMPORTANT: Walmart PayCycle Question

### About PayCycles as Trigger

You mentioned you want emails to go out based on **Walmart PayCycles** instead of hourly.

**I don't have the specific 2026 Walmart PayCycle dates**, but I can help once you provide them.

### Get the PayCycle Schedule

**Action Required:**
- Contact: Walmart Payroll/HR Department
- Ask for: 2026 Biweekly PayCycle Schedule
  - Format needed: PayCycle Start Dates (Sundays) and End Dates (Saturdays)
  - Example: 
    - PC 1: Jan 5 - Jan 18, 2026
    - PC 2: Jan 19 - Feb 1, 2026
    - PC 3: Feb 2 - Feb 15, 2026
    - etc.

**Where to Find:**
- Walmart Payroll calendar (usually on WalmartOne)
- HR systems (ADP payroll)
- Your paycheck stubs (shows current pay period)

---

## 📅 Timeline Based on PayCycles (Once You Provide Dates)

Once you provide the 2026 PayCycle calendar, I'll create a timeline like this:

### Example Timeline (Placeholder)

```
PAYROLL CYCLE SCHEDULE 2026

PC 1: Jan 5 - Jan 18
      │
      └─→ TEST EMAIL SEND: Jan 19 (Monday after cycle ends)
          └─ Recipients: Kristine, Matthew, Kendall
          └─ Email: "Manager Changes Detected - PC1 Report"

PC 2: Jan 19 - Feb 1  
      │
      └─→ TEST EMAIL SEND: Feb 2 (Monday after cycle ends)
          └─ Recipients: Kristine, Matthew, Kendall
          └─ Email: "Manager Changes Detected - PC2 Report"

PC 3: Feb 2 - Feb 15
      │
      └─→ TEST EMAIL SEND: Feb 16 (Monday after cycle ends)
          └─ Recipients: Kristine, Matthew, Kendall
          └─ Email: "Manager Changes Detected - PC3 Report"

[And so on for all PayCycles...]
```

---

## 🔧 How to Implement PayCycle-Based Sending

Once you provide the PayCycle dates, I'll:

1. **Update `config.py`** - Add PayCycle calendar dates
2. **Modify trigger logic** - Change from hourly to PayCycle-end dates
3. **Create schedule** - Define when each email should send
4. **Test locally** - Validate on this system before production

### Option 1: Manual Trigger (Simplest for Testing)
```python
# You manually run the script when a PayCycle ends
python daily_check_smart.py
```

### Option 2: Scheduled by Date
```python
# System automatically runs on PayCycle end dates (e.g., every other Monday)
# Windows Task Scheduler runs daily, but only sends if it's a PayCycle end date
```

---

## 🚀 Running on This System Right Now

To get it running on your current system (this Windows machine):

### Step 1: Verify Environment
```powershell
# Already done - you have Python active in terminal
python --version  # Should show Python 3.8+
```

### Step 2: Run Initial Test
```powershell
# Navigate to project folder
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails"

# Run the setup wizard
python SETUP_WIZARD.py

# Follow prompts to configure system
```

### Step 3: Test Email Generation
```powershell
# Generate test snapshot
python create_snapshot.py

# Check if it detects changes
python compare_snapshots.py

# Generate test email (without sending yet)
python dc_email_generator_html.py

# Open generated email in browser to review design
start MOCK_EMAIL_TEMPLATE.html
```

### Step 4: Test Email Sending
```powershell
# Run the main check (will try to send email to 3 test recipients)
python daily_check_smart.py

# Check logs for success/errors
Get-Content manager_snapshot.log | Select-Object -Last 20
```

### Step 5: Verify Receipt
- Check: Kristine.Torres@walmart.com (for test email)
- Check: Matthew.Farnworth@walmart.com (for test email)
- Check: Kendall.Rush@walmart.com (for test email)
- Should see email with Spark branding and manager change info

---

## ⏱️ Timeline for Testing Phase

### **Immediate (This Week - Feb 25)**
```
☐ Provide Walmart PayCycle calendar for 2026
☐ Decide: Manual trigger or auto-scheduled?
☐ System ready - waiting for PayCycle dates
```

### **Upon Receiving PayCycle Dates**
```
WEEK 1:
☐ Configure PayCycle dates in system
☐ Set up trigger scheduling
☐ Run first test manually
☐ Verify email reaches all 3 recipients
☐ Review email content with Kristine, Matthew, Kendall

WEEK 2:
☐ Run second test on next PayCycle end date
☐ Verify automated scheduling works
☐ Check dashboard metrics
☐ Gather feedback from test recipients

WEEK 3:
☐ Make any adjustments based on feedback
☐ Prepare recipient expansion
☐ Document learnings

WEEK 4:
☐ Expand to production recipients (all DCs)
☐ Full rollout
```

---

## 📧 What Each Email Will Contain

Each test email will include:

✅ **Subject:** `Manager Changes Detected - [DC Number] [Date]`

✅ **Content:**
- Spark logo and branding
- Summary of manager changes by role:
  - Store Manager changes
  - Market Manager changes
  - Regional GM changes
  - DC GM/AGM changes
- Stores affected (count by area)
- "Send Feedback" button
- "View Store Managers" link

✅ **Recipients:** BCC'd (no one sees others' emails)

✅ **Reply-To:** ATCTEAMSUPPORT@walmart.com

---

## 🔍 What You'll Monitor During Testing

### Daily Checks:
- [ ] Did email send on expected PayCycle date?
- [ ] Did all 3 recipients receive it?
- [ ] Is email content accurate?
- [ ] Does dashboard show email count?
- [ ] Any error messages in logs?

### Weekly Review:
- [ ] Email quality/formatting
- [ ] Content accuracy
- [ ] Recipient feedback
- [ ] System stability
- [ ] Performance (how long to process)

---

## 🛑 Known Considerations

### VPN Requirement
- System MUST be on Walmart VPN to:
  - Access SDL (manager data source)
  - Send emails through Outlook
  - If VPN disconnects: System has 7-day retry window

### Outlook Requirement
- Microsoft Outlook desktop client must be running
- Web Outlook won't work
- Service must run under account with Outlook configured

### One Test Per PayCycle
- Suggestion: Send one test email per PayCycle
- This gives 2 weeks between tests
- Enough time to review, gather feedback, make adjustments

---

## ✅ Next Actions

### IMMEDIATE:
1. **Provide PayCycle Dates**
   - Email/send Walmart 2026 PayCycle calendar
   - Format: Start date (Sunday) and End date (Saturday) for each cycle

2. **Confirm Testing Approach**
   - Manual run: You execute Python script when PayCycle ends
   - Auto-scheduled: System runs automatically on specific dates
   - Which preferred?

3. **Confirm Test Recipients**
   - Kristine Torres - Confirms she should receive
   - Matthew Farnworth - Confirms he should receive
   - Kendall Rush - Confirms she should receive

### THEN:
- I'll configure the exact schedule
- System will be ready to run
- First test can begin

---

**Testing Configuration:** READY  
**Test Recipients:** CONFIGURED (3 people)  
**PayCycle Schedule:** ⏳ AWAITING INPUT  
**System Status:** ✅ Ready to deploy and test locally

**What's Blocked:** PayCycle dates (needed to set trigger schedule)

