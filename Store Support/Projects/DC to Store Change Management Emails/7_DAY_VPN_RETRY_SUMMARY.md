# 7-Day VPN Retry Logic - Summary

**Created:** January 13, 2026  
**Purpose:** Keep trying for up to 7 days instead of giving up after 4 hours

---

## 🎯 What Changed

### **Before (4-hour window):**
- Task ran once daily at 2:00 AM
- Retried every 30 min for 4 hours
- If no VPN by 6 AM → gave up and sent error email
- **Problem:** Laptop off/not on VPN for days = daily error emails

### **After (7-day window):**
- Task runs **HOURLY** starting at 2:00 AM
- Quick VPN check (no long waits)
- Keeps trying hourly for up to **7 DAYS**
- Only sends error email after 7 days
- **Benefit:** Laptop can be off for days, will catch up when VPN available

---

## 📅 How It Works

### **Scenario 1: On VPN (Normal Operation)**

**Monday 2:00 AM:**
- Hourly task runs
- VPN check passes
- Daily check runs
- Snapshot created
- Emails sent
- ✅ Done

**Monday 3:00 AM - 11:59 PM:**
- Hourly task runs
- Sees snapshot exists for Monday
- Exits immediately (already processed today)

**Tuesday 2:00 AM:**
- New day starts
- Process repeats

---

### **Scenario 2: Off VPN for 3 Days (Laptop in Backpack)**

**Monday 2:00 AM:**
- Task runs, VPN check fails
- Creates `vpn_retry_tracker.json` to track first attempt
- Exits

**Monday 3 AM - 11 PM:**
- Task runs hourly
- VPN check fails each time
- Exits and waits for next hour

**Tuesday - Wednesday:**
- Same pattern
- No error emails (still within 7-day window)
- Logs show: "Will keep trying (day 2/7)", etc.

**Thursday 4:15 PM:**
- You open laptop and connect to VPN
- Next hourly run (5:00 PM) detects VPN
- Daily check runs successfully
- Creates Monday's snapshot (3 days late)
- Sends emails
- Deletes `vpn_retry_tracker.json`
- ✅ Caught up!

**Thursday 6:00 PM onwards:**
- Hourly task sees snapshot exists
- Exits (already processed)

---

### **Scenario 3: Off VPN for 8+ Days (Extended Outage)**

**Monday 2:00 AM:**
- Task runs, VPN fails
- Starts 7-day countdown

**Monday - Sunday:**
- Retries hourly (168 attempts)
- No VPN detected

**Next Monday 2:00 AM (Day 8):**
- Retry tracker shows 7+ days have passed
- Sends error email: "VPN unavailable for 7 days, manual intervention required"
- Deletes retry tracker
- Stops trying for that date

**Next Monday 3:00 AM:**
- New day starts
- Fresh 7-day window begins for Tuesday's snapshot

---

## ⚙️ Configuration

### **config.py:**
```python
VPN_RETRY_ENABLED = True
VPN_MAX_RETRY_DAYS = 7  # Keep trying for up to 7 days
VPN_RETRY_INTERVAL_HOURS = 1  # Check every hour
```

### **Task Scheduler:**
- **Trigger:** Hourly (every 1 hour)
- **Start time:** 2:00 AM
- **Script:** `daily_check_smart.py`

---

## 📧 Email Notifications

### **Success (every day with VPN):**
- No special notification for successful VPN connection
- Standard "changes detected" or "no changes" emails

### **Already Ran Today:**
- Subject: "Daily Check - Already Completed"
- Sent when hourly task runs but snapshot already exists

### **Error After 7 Days:**
- Subject: "ERROR: Manager Change Detection Failed - YYYY-MM-DD"
- Content: "VPN unavailable for 7 days (since YYYY-MM-DD HH:MM). Manual intervention required."
- **Only sent once per 7-day period**

---

## 📂 New Files

1. **`vpn_retry_tracker.json`** (auto-created)
   - Tracks first attempt timestamp
   - Tracks target date
   - Auto-deleted on success
   
2. **`setup_hourly_task.bat`** (NEW)
   - Replaces Task Scheduler task with hourly trigger
   - Run this to update your existing task

---

## 🔧 Setup Instructions

### **1. Update Task Scheduler to Hourly:**

```bash
cd C:\Users\jhendr6\puppy\elm
setup_hourly_task.bat
```

This will:
- Delete old daily task
- Create new hourly task
- Set to run every hour starting at 2:00 AM

### **2. Test VPN Detection:**

```bash
python vpn_checker.py
```

Should show `CONNECTED` if on VPN, `NOT CONNECTED` if not.

### **3. Test Smart Wrapper:**

```bash
python daily_check_smart.py
```

If today's snapshot exists: Skips
If not: Checks VPN and runs if available

---

## 📊 Benefits

✅ **No more daily error emails** - Only notified after 7 days  
✅ **Laptop can be off** - Will catch up when VPN available  
✅ **No stale data** - Only uses fresh SDL exports  
✅ **Automatic recovery** - Picks up where it left off  
✅ **Smart deduplication** - Won't run twice on same day  
✅ **168 retry attempts** - Very high chance of success within 7 days  

---

## 🔍 Monitoring

### **Check if retrying:**
```bash
dir vpn_retry_tracker.json
```
- If exists: Currently retrying for a date
- If not found: Not currently retrying

### **View retry details:**
```bash
type vpn_retry_tracker.json
```
Shows:
- First attempt timestamp
- Target date

### **Check logs:**
```bash
type daily_run_log_20260113.txt
```
Shows all hourly attempts and VPN check results

---

## ❓ FAQ

**Q: Will this run 24 times a day?**  
A: The task TRIGGERS hourly, but the script exits immediately if snapshot already exists. Only runs ONCE per day when VPN becomes available.

**Q: What if I'm never on VPN?**  
A: After 7 days, you'll get an error email. You can then manually run the daily check when on VPN, or adjust the schedule.

**Q: Can I change from 7 days to something else?**  
A: Yes! Edit `config.py` and change `VPN_MAX_RETRY_DAYS = 7` to any number you want.

**Q: Can I change from hourly to every 2 hours?**  
A: Yes! Edit `setup_hourly_task.bat` and change `/SC HOURLY` to `/SC HOURLY /MO 2` (every 2 hours).

---

## 🚀 Ready to Deploy

Run the setup script to enable hourly checking:

```bash
setup_hourly_task.bat
```

That's it! The system will now:
- Check every hour
- Keep trying for 7 days
- Only process each day once
- Send one error email after 7 days of no VPN
