# 🚀 Quick Start: Testing Phase
## DC to Store Change Management System
**Date:** February 25, 2026  
**Status:** READY TO TEST  
**Recipients:** 3 people (Kristine, Matthew, Kendall)

---

## ⚡ 30-Second Summary

✅ **System configured** for 3 test recipients  
✅ **Ready to run** on this computer  
⏳ **Needs PayCycle dates** to schedule future sends  

**You can test RIGHT NOW or wait for PayCycle schedule—your choice.**

---

## 🎯 IMMEDIATE ACTION REQUIRED

### Action 1: Get PayCycle Dates (Best Option)
**Where:** WalmartOne → Pay/Calendar → 2026 PayCycle Calendar  
**What we need:** List of all 26 PayCycle start/end dates for 2026  
**Format example:**
```
PC 1:  Jan 5 - Jan 18
PC 2:  Jan 19 - Feb 1
PC 3:  Feb 2 - Feb 15
[etc for all 26]
```
**Time needed:** 5 minutes to find  
**Impact:** Once provided, I can set up automatic sends aligned to payroll

---

### Action 2: Choose Testing Approach

**Option A: Manual Testing** (Start RIGHT NOW)
```powershell
python daily_check_smart.py
# Run this whenever you want to send test email
```
- ✅ Sends immediately to 3 recipients
- ✅ Full control over timing
- ✅ Good for validation before PayCycle automation
- ⏱️ Takes ~5 min per run

**Option B: Automated PayCycle-Based** (After you provide dates)
```
System runs automatically on PayCycle end dates
Emails go to 3 recipients on schedule
No manual intervention needed
```
- ✅ Set it and forget it
- ✅ Guaranteed timing
- ⏳ Requires PayCycle calendar first

---

## 📋 What Each Test Email Will Show

**Email Recipients:** Kristine, Matthew, Kendall (BCC'd)

**Email Content:**
```
FROM: supplychainops@email.wal-mart.com
SUBJECT: Manager Changes Detected - [DC] - [Date]

BODY:
├─ Spark Logo
├─ Manager Changes Summary
│  ├─ Store Manager changes: X
│  ├─ Market Manager changes: X
│  ├─ Regional GM changes: X
│  └─ DC GM/AGM changes: X
├─ Affected Stores (by area)
├─ [Send Feedback] button
├─ [View Store Managers] button
└─ Footer with contact info

REPLY-TO: ATCTEAMSUPPORT@walmart.com
```

---

## ✅ Test Recipients Confirmed

### Test Email Group (3 people):
- [x] **Kristine.Torres@walmart.com**
- [x] **Matthew.Farnworth@walmart.com**
- [x] **Kendall.Rush@walmart.com**

**Configuration Location:** `config.py` and `dc_email_config.py`

---

## 🎬 How to Run First Test (Right Now)

### Step 1: Open Terminal
```powershell
# Navigate to project
cd "Store Support\Projects\DC to Store Change Management Emails"

# Activate Python (if not already)
& ".venv\Scripts\Activate.ps1"
```

### Step 2: Verify Setup
```powershell
python --version  # Should show Python 3.8+
```

### Step 3: Test System
```powershell
# Test data collection
python create_snapshot.py
# Expected: Creates snapshot with ~5,200 locations

# Generate test email
python dc_email_generator_html.py
# Expected: Creates MOCK_EMAIL_TEMPLATE.html

# Open in browser to review
start MOCK_EMAIL_TEMPLATE.html
```

### Step 4: Send Email to Test Group
```powershell
# Make sure Outlook is running first!

# Send emails to 3 recipients
python daily_check_smart.py

# Check logs
Get-Content manager_snapshot.log | tail -20
```

### Step 5: Verify
- [ ] Check Kristine's email
- [ ] Check Matthew's email
- [ ] Check Kendall's email
- All should have same Spark-branded email with manager changes

---

## 📅 Timeline Based on PayCycles

### Once YOU Provide PayCycle Dates:

```
Timeline [Placeholder - will fill exactly once dates arrive]

Week 1 (Now):
  ✓ Manual test send to 3 recipients
  ✓ Verify content & delivery
  ✓ Gather feedback

Week 2-4:
  ✓ Configure automatic PayCycle schedule
  ✓ Run on official PayCycle end dates
  ✓ Validate automation works
  ✓ Prepare expansion to all DCs

Timeline will be exact once PayCycle dates received.
```

---

## 📊 What Gets Tested

| Item | Status | Test |
|------|--------|------|
| **Email generation** | ✅ Ready | First run will test |
| **Spark branding** | ✅ Ready | Visual check in email |
| **3 recipients** | ✅ Configured | Will send to all 3 |
| **Email delivery** | ✅ Ready | Check of inbox |
| **Dashboard** | ✅ Ready | Optional: check metrics |
| **Manager data accuracy** | ✅ Ready | Manual review |
| **System performance** | ✅ Ready | Check timing |

---

## ⚠️ Requirements Before Testing

### Must Have (Blocking):
- [x] Windows computer (this one)
- [x] Python 3.8+ (already installed)
- [x] Walmart VPN (for SDL access)
- [x] Outlook desktop client (installed on this system?)
- [x] System on VPN when running test

### Should Have (Recommended):
- [x] Test recipients' email access (for verification)
- [x] 10-15 minutes free time (for first test)
- [ ] PayCycle calendar (nice to have, not blocking)

---

## 🔍 Troubleshooting at a Glance

| Issue | Solution |
|-------|----------|
| "VPN not found" | Connect to Walmart VPN, retry |
| "Outlook not running" | Open Outlook, log in, retry |
| "SDL connection failed" | Verify VPN, check SDL URL in config |
| "Email not received" | Check spam folder, verify recipient list |
| "Permission denied" | Run PowerShell as Administrator |

---

## 📞 Next Step: You Need to Do Two Things

### 1️⃣ Provide PayCycle Calendar (Critical for Scheduling)
```
Email or message me:
- All 26 PayCycle start/end dates for 2026
- Format: "PC X: Jan 5 - Jan 18" (repeat for all)
- Or: Screenshot of WalmartOne PayCycle calendar
```

### 2️⃣ Choose Testing Approach
```
Tell me:
- Option A: Manual testing (run script when I say)
- Option B: Automated (run on specific dates)
- Or: Start with A, move to B later
```

---

## 📁 New Documents Created

All in: `Store Support\Projects\DC to Store Change Management Emails\`

- ✅ **TEST_PHASE_CONFIGURATION.md** - Current state, what's configured
- ✅ **WALMART_PAYCYCLE_GUIDE.md** - How to find & use PayCycle dates
- ✅ **This file** - Quick reference

---

## 🆘 Questions?

**"How do I find the PayCycle calendar?"**
→ See WALMART_PAYCYCLE_GUIDE.md

**"How do I run the first test?"**
→ See section "How to Run First Test (Right Now)" above

**"What happens during a test?"**
→ See section "What Each Test Email Will Show"

**"Can we test right now without PayCycle dates?"**
→ YES! Use Option A (Manual) in section 2️⃣ above

---

## ✅ Completion Checklist

For you:
- [ ] Read this document
- [ ] Get PayCycle calendar (or confirm manual testing OK)
- [ ] Choose testing approach (A or B)
- [ ] Message results
- [ ] Ready to proceed!

For me (once dates received):
- [ ] Configure exact PayCycle dates
- [ ] Set up trigger schedule
- [ ] Create exact timeline
- [ ] System ready for automated sends

---

## 🎯 Status

**Configuration:** ✅ 100% Complete  
**System Ready:** ✅ YES  
**Can Test NOW:** ✅ YES  
**Needs PayCycle Dates:** ⏳ For automation

**BLOCKED BY:** PayCycle calendar dates (for scheduled sends)

**NOT BLOCKED:** Can do manual testing anytime

---

**Awaiting:** Your PayCycle calendar + testing approach choice  
**Ready:** To configure exact schedule & timeline once received

