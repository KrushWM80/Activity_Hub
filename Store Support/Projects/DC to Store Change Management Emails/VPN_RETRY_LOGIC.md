# VPN Connectivity and Retry Logic

## Overview

The daily manager change detection system now includes intelligent VPN detection and retry logic to ensure we never use stale data.

---

## How It Works

### 1. **VPN Connectivity Check**

Before attempting to fetch SDL data, the system checks if you're connected to VPN by:

1. **DNS Resolution** - Can we resolve internal hostnames (elmsearchui.prod.elm-ui.telocmdm.prod.walmart.com)?
2. **HTTP Access** - Can we reach the SDL endpoint?
3. **LAS API** - Can we access the DC alignment API?

If ANY of these succeed, VPN is considered connected.

### 2. **Retry Logic - 7 Day Window**

Task Scheduler runs **HOURLY** starting at 2:00 AM.

Each hour:
1. Check if today's snapshot exists
2. If exists: Exit (already processed today)
3. If not: Quick VPN check
4. If VPN available: Run daily check
5. If VPN unavailable: Exit and retry next hour

**Retry Window:** Up to **7 DAYS** (168 hours)

**Example Timeline (if off VPN for days):**
- **Day 1** (Monday 2 AM): VPN check fails → retry every hour
- **Day 2** (Tuesday): Still no VPN → keep trying hourly
- **Day 3** (Wednesday): Still no VPN → keep trying
- ... continues ...
- **Day 7** (Sunday): Still no VPN → keep trying
- **Day 8** (Monday 2 AM): Send error email, stop trying

**If VPN connects on Day 3 at 4 PM:**
- Next hourly run (5 PM) detects VPN
- Runs daily check successfully
- Creates snapshot
- Stops retrying (done for the day)

### 3. **What Happens If VPN Never Connects?**

After **7 days** of hourly retries (168 attempts):

1. ❌ **Task stops retrying** for that date
2. ✉️ **Error notification email sent** to admin (one email after 7 days)
3. 📝 **All attempts logged** to daily run log files
4. 🔄 **Next day starts fresh** with a new 7-day window

No snapshot is created with stale data.

### 4. **What Happens If VPN Connects?**

1. ✅ **SDL data is fetched** (fresh export)
2. ✅ **Snapshot created** with current data
3. ✅ **Changes detected** and emails sent

---

## Configuration

You can adjust retry behavior in `daily_check.py`:

```python
vpn_connected, vpn_message = wait_for_vpn(
    max_retries=8,          # Number of retry attempts
    retry_delay_minutes=30  # Minutes between retries
)
```

**Recommendations:**
- **Desktop PC (always on):** 8 retries @ 30 min (4 hour window)
- **Laptop (unpredictable):** 12 retries @ 15 min (3 hour window with more frequent checks)

---

## Error Notifications

If VPN is unavailable after all retries, you'll receive an email:

**Subject:** `ERROR: Manager Change Detection Failed - YYYY-MM-DD`

**Content:**
- Error message: "VPN not available after X attempts"
- Manual restart instructions
- Troubleshooting steps

---

## Troubleshooting

### **Q: Task is taking 4+ hours to complete**
**A:** This is normal if VPN isn't available. The task is retrying every 30 minutes.

### **Q: I got an error email but I'm on VPN**
**A:** Check:
1. Can you access https://elmsearchui.prod.elm-ui.telocmdm.prod.walmart.com/ in a browser?
2. Check the Task Scheduler log: `daily_run_log_YYYYMMDD.txt`
3. Run `python vpn_checker.py` manually to test connectivity

### **Q: Can I force it to use old data as fallback?**
**A:** Not recommended, but you can comment out the `sys.exit(1)` in daily_check.py after the VPN check fails. However, this defeats the purpose of having fresh data.

### **Q: What if I'm never on VPN at 2 AM?**
**A:** Two options:
1. Change Task Scheduler time to when you're typically on VPN (e.g., 8 AM)
2. Leave laptop/PC on and connected to VPN overnight

---

## Benefits

✅ **No stale data** - Never creates snapshots with yesterday's export  
✅ **Automatic retry** - Waits for VPN instead of failing immediately  
✅ **4-hour window** - Reasonable window to catch VPN connectivity  
✅ **Clear notifications** - Know immediately if something went wrong  
✅ **Logged retries** - All retry attempts logged to daily run log  

---

## Files Modified

- `vpn_checker.py` (NEW) - VPN connectivity detection and retry logic
- `daily_check.py` - Integrated VPN check before SDL fetch
- No fallback to old data - exits gracefully if VPN unavailable

---

## Testing

Test VPN detection manually:

```bash
cd C:\Users\jhendr6\puppy\elm
python vpn_checker.py
```

**On VPN:** Should show `CONNECTED`  
**Off VPN:** Should show `NOT CONNECTED`
