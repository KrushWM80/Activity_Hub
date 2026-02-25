# 📊 PayCycle Tracking & Recipient Management Quick Guide

**Status:** ✅ Ready to use  
**Date:** February 25, 2026

---

## 🎯 What These Tools Do

You now have a complete system for:
1. **Tracking** when each PayCycle email is scheduled and sent
2. **Managing recipients** easily (test vs. production)
3. **Recording sends** for audit trail
4. **Switching modes** between testing and production

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `paycycle_tracking.json` | Records when emails were sent and delivery status |
| `email_recipients.json` | Manages test and production recipient lists |
| `manage_paycycle.py` | CLI utility to manage both files |

---

## 🚀 Quick Start

### View Schedule
```powershell
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails"
& "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe" manage_paycycle.py schedule
```

**Output shows:** All 26 PayCycles with dates, times, and status

### View Current Recipients
```powershell
python manage_paycycle.py recipients
```

**Output shows:** Who emails are currently being sent to

---

## 🔧 Common Tasks

### Task 1: Add DC Manager to Production Recipients

**Step 1:** Identify the email address  
Example: `dc.manager@walmart.com` | Name: `John Smith`

**Step 2:** Add to system
```powershell
python manage_paycycle.py add-recipient production dc.manager@walmart.com "John Smith" "DC Manager"
```

**Result:** ✓ Email added to production mode

**Step 3:** Verify
```powershell
python manage_paycycle.py recipients
```

---

### Task 2: Add Multiple Production Recipients

**Repeat Task 1 for each person:**

```powershell
# Add DC manager 1
python manage_paycycle.py add-recipient production maria.garcia@walmart.com "Maria Garcia" "DC Manager"

# Add DC manager 2
python manage_paycycle.py add-recipient production james.lee@walmart.com "James Lee" "Store Support Manager"

# Add distribution list
python manage_paycycle.py add-recipient production dc-managers@walmart.com "DC Managers Distribution" "Distribution List"
```

---

### Task 3: Switch from Test to Production

**When:** After validating first 2-3 PayCycles work correctly

**Step 1:** Verify production recipients are added
```powershell
python manage_paycycle.py recipients
```

**Step 2:** Switch mode
```powershell
python manage_paycycle.py switch-mode production
```

**Result:** ✓ System now sends to production recipients on next PayCycle

**Step 3:** Verify switch
```powershell
python manage_paycycle.py recipients
```

---

### Task 4: Record a PayCycle Send (After Email Sent)

**When:** After the system sends emails automatically

**Step 1:** Confirm send was successful (check inbox)

**Step 2:** Record it
```powershell
python manage_paycycle.py record-send 3 success
```

**Output:** ✓ SENT PC 03 at [time]

**To record failures:**
```powershell
python manage_paycycle.py record-send 3 failed "Network timeout"
```

---

### Task 5: Remove a Recipient

```powershell
python manage_paycycle.py remove-recipient test kendall.rush@walmart.com
```

**Result:** ✓ Removed from active recipient list (can be re-added)

---

## 📋 Full Command Reference

### View Commands

```powershell
# View all PayCycle dates and status
python manage_paycycle.py schedule

# View current recipients (test or production)
python manage_paycycle.py recipients

# Get emails as JSON (useful for scripts)
python manage_paycycle.py get-emails
```

### Management Commands

```powershell
# Add recipient
python manage_paycycle.py add-recipient <mode> <email> "<name>" "<role>"

# Remove recipient
python manage_paycycle.py remove-recipient <mode> <email>

# Switch between test and production
python manage_paycycle.py switch-mode <mode>

# Record email send
python manage_paycycle.py record-send <pc_number> [success|failed] [error_msg]
```

### Examples

```powershell
# Add John to production
python manage_paycycle.py add-recipient production john@walmart.com "John Best" "DC Manager"

# Remove John
python manage_paycycle.py remove-recipient production john@walmart.com

# Switch to production mode
python manage_paycycle.py switch-mode production

# Record PC 03 send
python manage_paycycle.py record-send 3 success

# Record failed send
python manage_paycycle.py record-send 4 failed "VPN not available"
```

---

## 📊 File Details

### paycycle_tracking.json

**Purpose:** Records execution history for audit trail

**Structure:**
```json
{
  "paycycles": [
    {
      "pc_number": 1,
      "paycycle_date": "2026-02-06",
      "scheduled_send_time": "06:00",
      "actual_send_time": null,
      "status": "pending",
      "recipients_count": 0,
      "error_message": null
    }
  ],
  "summary": {
    "total_paycycles": 26,
    "completed": 0,
    "scheduled": 24,
    "failed": 0
  }
}
```

**When Updated:**
- Automatically by system on each send
- Manually via `manage_paycycle.py record-send`

**Use Cases:**
- Audit trail: "When was PC 03 sent?"
- Compliance: "What recipients received each email?"
- Troubleshooting: "Which PayCycle failed and why?"

---

### email_recipients.json

**Purpose:** Centralized recipient management

**Structure:**
```json
{
  "active_mode": "test",
  "modes": {
    "test": {
      "active": true,
      "recipients": [
        {
          "name": "Kristine Torres",
          "email": "Kristine.Torres@walmart.com",
          "role": "Project Lead",
          "active": true
        }
      ]
    },
    "production": {
      "active": false,
      "recipients": []
    }
  }
}
```

**Key Fields:**
- `active_mode`: Which recipients to use ("test" or "production")
- `recipients[].active`: true = include in emails, false = skip
- `recipients[].email`: Email address (use [TO_BE_ADDED] as placeholder)

**Update Methods:**
- Manual: Edit file directly in VS Code
- Automated: Use `manage_paycycle.py add-recipient`

---

## 🔄 Typical Workflow

### Week 1: Testing Phase ✓
```
Current State: TEST mode with 3 testers
- Kristine Torres
- Matthew Farnworth
- Kendall Rush

PC 03 Send: 3/6/2026
  ✓ All 3 testers receive email
  ✓ Validate format, timing, content
  ✓ Record success: python manage_paycycle.py record-send 3 success
```

### Week 2-3: Prepare Production
```
Add DC managers:
  python manage_paycycle.py add-recipient production maria@walmart.com "Maria Garcia" "DC Manager"
  python manage_paycycle.py add-recipient production james@walmart.com "James Lee" "Manager"
  
Verify recipients list:
  python manage_paycycle.py recipients

Validate in PRODUCTION section
```

### Week 4: Switch to Production
```
python manage_paycycle.py switch-mode production

PC 04 Send: 3/20/2026
  ✓ Email sends to DC managers
  ✓ Record: python manage_paycycle.py record-send 4 success
  
If issues: Switch back to test
  python manage_paycycle.py switch-mode test
```

### Ongoing: Track All Sends
```
After each PayCycle send:
  python manage_paycycle.py record-send <pc_number> success

Monthly review:
  python manage_paycycle.py schedule
  → See all sends, any failures
```

---

## ⚙️ Integration with Email System

The email system automatically reads from `email_recipients.json`:

1. **System starts** (daily_check_smart.py)
2. **Checks active_mode** (test or production)
3. **Loads recipients** from that mode
4. **Sends emails** to all active recipients
5. **Logs sends** to paycycle_tracking.json

**Result:** Change recipients in JSON = change recipients system uses. No code changes needed.

---

## 📈 Monitoring

### Check Send Status
```powershell
python manage_paycycle.py schedule | grep "PC 03"
```

### See Recipient Count
```powershell
python manage_paycycle.py recipients
```

### Get All Recipient Emails (for debugging)
```powershell
python manage_paycycle.py get-emails
```

---

## 🐛 Troubleshooting

### Q: Emails not sent to new recipient?
**A:** 
1. Verify added: `python manage_paycycle.py recipients`
2. Check active flag: true or false?
3. Check active_mode: "test" or "production"?
4. Resave recipients file if edited manually

### Q: How to send to both test AND production?
**A:** Create "staging" mode in email_recipients.json with both groups, then `switch-mode staging`

### Q: Want to skip a PayCycle?
**A:** Disable task in Task Scheduler temporarily:
1. Task Scheduler > right-click task > Disable
2. Re-enable when ready

### Q: Want to audit who received PC 03?
**A:** Check paycycle_tracking.json:
```
PC 03: recipients_count: 3, status: completed, actual_send_time: [date]
```

---

## 📝 Best Practices

1. **Always verify recipients** before switching to production
   ```powershell
   python manage_paycycle.py recipients
   ```

2. **Record sends** immediately after verification
   ```powershell
   python manage_paycycle.py record-send 3 success
   ```

3. **Graduate slowly** from test → production
   - PC 03-04: Test mode
   - PC 05-06: Test with 1 production recipient
   - PC 07+: Full production

4. **Keep audit trail** - Never delete tracking files
   - paycycle_tracking.json
   - email_recipients.json

5. **Document changes** - Add notes to paycycle_tracking.json
   ```json
   "notes": "Switched to production after successful testing"
   ```

---

## ✨ Advanced Uses

### Create Seasonal Recipients
Edit email_recipients.json to add new mode:
```json
"holiday_mode": {
  "active": false,
  "recipients": [
    {"email": "holiday.team@walmart.com", "role": "Holiday Support"}
  ]
}
```

Then switch: `python manage_paycycle.py switch-mode holiday_mode`

### Backup Recipients
```powershell
Copy-Item email_recipients.json email_recipients_backup_20260225.json
```

### Compare Modes
```powershell
python manage_paycycle.py get-emails > emails_current.json
# Edit email_recipients.json to different mode
python manage_paycycle.py get-emails > emails_alternative.json
# Compare: diff emails_current.json emails_alternative.json
```

---

## 🎯 Summary

**You now have:**
- ✅ Automatic tracking of all 26 PayCycle sends
- ✅ Easy recipient management (test vs. production)
- ✅ CLI utility for quick updates
- ✅ Complete audit trail
- ✅ No code changes needed to switch recipients

**To add DC managers:**
```powershell
python manage_paycycle.py add-recipient production email@walmart.com "Name" "Title"
```

**To switch to production:**
```powershell
python manage_paycycle.py switch-mode production
```

**Done!** System sends to new recipients on next PayCycle.

