# Cache Validation & Email Alert System - Implementation Guide

**Updated**: March 10, 2026  
**Location**: `docs/CACHE/`

---

## Overview

The Projects in Stores cache system includes a **validation mechanism** to prevent bad data from corrupting the cache and to notify immediately when issues occur.

---

## What Changed

### 1. Database Schema Enhancement
- Added `sync_error_log` table to track all sync attempts (success and failures)
- Logs include: `timestamp`, `error_message`, `record_count`, `sync_duration_seconds`
- Any sync attempt (good or bad) is recorded and queryable

### 2. Validation Logic
Before the cache is updated, the system now validates:

| Check | Rule | Action if Failed |
|-------|------|------------------|
| Record Count | Must be ≥ 1,400,000 records | Rollback cache, send email |
| Variance | Must be ≤ ±50,000 from expected | Rollback cache, send email |
| Sync Duration | Must take ≥ 60 seconds | Indicates error/incompleteness |

### 3. Email Alerts
When validation fails:
- **Email To**: `kendall.rush@walmart.com`
- **Subject**: `⚠️ [ALERT] Projects in Stores Cache Sync Failed`
- **Contents**: Detailed reason, record counts, cache status, debugging help

### 4. Cache Protection
If validation fails:
- ✓ Transaction is **rolled back** - no bad data written
- ✓ Old cache data is **preserved** - dashboard continues working
- ✓ Failure is **logged** - you see in monitor script
- ✓ **Email sent** - you're notified immediately (if not in retry window)

### 5. Smart Retry Logic (NEW - March 2026)
- **0 records**: Retried 2 times automatically (Mid-sync protection)
- **Variance ±50k**: Accepted as normal (No email)
- **Result**: Fewer false alerts, more reliable notifications

---

## Testing the System

### Test 1: Verify Normal Sync Works

```bash
# 1. Monitor real-time sync
cd backend

# 2. Watch backend logs for validation messages
python main.py

# Expected output:
# [SQLite] Fetched 1420167 rows from BigQuery
# [SQLite] Syncing partner data...
# [SQLite] Synced 12345 partner records
# [SQLite] ✓ Validation passed - updating cache with 1,420,167 records
# [SQLite] Sync complete! 1420167 rows in 203.5s
```

### Test 2: Check Cache Health After Sync

```bash
# Wait 15 minutes for automatic sync, then:
python monitor_cache_health.py

# Expected output in [3] SYNC HISTORY:
# 2026-03-03 18:15:23  ✓ SUCCESS  1420167  203.5s  SUCCESS: 1420167 records synced...
```

### Test 3: Monitor Validation Logs

```python
# Query validation logs directly
import sqlite3
conn = sqlite3.connect('projects_cache.db')
cursor = conn.cursor()

# See all recent sync attempts
cursor.execute("""
    SELECT timestamp, error_message, record_count, sync_duration_seconds
    FROM sync_error_log
    ORDER BY timestamp DESC
    LIMIT 10
""")

for row in cursor.fetchall():
    print(f"{row[0]} | {row[1][:50]} | {row[2]:,} records | {row[3]:.1f}s")
```

### Test 4: Simulate Validation Failure (Optional)

To test the email alert without breaking production data:

```python
# In sqlite_cache.py, temporarily change the threshold:
# MIN_EXPECTED_RECORDS = 2_000_000  # Intentionally too high

# This will cause next sync to fail validation and send email
# Then restore the original value
```

---

## Monitoring Going Forward

### Daily Health Check
Run weekly to verify everything is working:
```bash
python monitor_cache_health.py
```

**Green Indicators:**
- ✓ Total records: 1,420,000+ 
- ✓ Last sync: Within the last 30 minutes
- ✓ Status: RECENT - Cache is current
- ✓ [3] SYNC HISTORY shows: All ✓ SUCCESS (no errors)

**Red Indicators:**
- ❌ Total records < 1,400,000
- ❌ Last sync > 30 minutes ago
- ❌ Status: STALE - Sync may be failing
- ❌ [3] SYNC HISTORY shows: Recent ✗ ERROR entries

### If You Don't Receive an Email When Expected

Email alert would trigger if:
1. Record count drops below 1,400,000
2. Record count exceeds 1,450,000
3. Sync completes in < 60 seconds (incomplete)
4. BigQuery query error occurs
5. **NOT**: 0 records on retry 1-2 (these are intentional)

This means the system is working correctly and data is valid!

### If You DO Receive an Email Alert

**Immediate Actions:**
1. **Read the email** - It contains the specific validation failure reason
2. **Check the data** - Log into BigQuery and inspect `IH_Intake_Data` table:
   ```sql
   SELECT COUNT(*) 
   FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
   WHERE Status = 'Active'
   ```
3. **Verify the count** - Should be ~1.4M records
4. **Check for schema changes** - Did someone add/remove columns?
5. **Review audit logs** - Check BigQuery audit logs for recent changes

**If Data is Confirmed Valid:**
- Force a manual cache resync:
  ```bash
  # Delete old cache
  rm projects_cache.db
  
  # Restart backend (will recreate cache)
  python main.py
  ```

**If Data Quality Issue Found:**
- Contact BigQuery data team to fix source data
- Don't update cache until source is fixed
- Dashboard will show old data (which is better than bad data)

---

## Configuration

If you need to adjust validation thresholds, edit `backend/sqlite_cache.py`:

```python
# Current Settings
MIN_EXPECTED_RECORDS = 1_400_000       # Minimum records required
MAX_ALLOWED_VARIANCE = 50_000           # Allow ±50K variance
MIN_SYNC_DURATION = 60                  # Must take at least 60 seconds
ZERO_RECORD_RETRY_COUNT = 2             # Retry attempts for 0 records
ZERO_RECORD_RETRY_TIMEOUT = 2700        # 45 minute window

NOTIFY_EMAIL = "kendall.rush@walmart.com"
SMTP_SERVER = "smtp-gw1.homeoffice.wal-mart.com"
```

### Adjusting Thresholds

If you observe legitimate variance in record counts over time:

```python
# Example: If you see normal range is 1.35M to 1.45M:
MIN_EXPECTED_RECORDS = 1_350_000
MAX_ALLOWED_VARIANCE = 100_000  # ±100K variance

# Then test by running:
# python monitor_cache_health.py
# Review [3] SYNC HISTORY to ensure no false failures
```

---

## Email Details

### Sample Email Content

```
Subject: ⚠️ [ALERT] Projects in Stores Cache Sync Failed

CACHE VALIDATION FAILED - INVESTIGATION REQUIRED

Sync Timestamp: 2026-03-03 18:45:23
Status: VALIDATION FAILED

Data Quality Check:
- Records Synced: 500,000
- Expected: ~1,400,000
- Variance: ±900,000 (threshold: ±50,000)
- Sync Duration: 120.5 seconds

Failure Reason: Record count too low (500,000 < 1,400,000)

System Protection:
✓ Cache NOT updated - using last valid version
✓ Previous data preserved and serving
✓ Cache Age: 0d 0h 15m
✓ Records in Cache: 1,420,167

Current Protection:
- Dashboard continues working with valid cached data
- System will attempt recovery on next sync cycle
- You will receive another email only if issue persists
```

---

## Log Messages to Watch For

### Good Logs (Normal Operation)
```
[SQLite] Fetched 1420167 rows from BigQuery
[SQLite] ✓ Validation passed - updating cache with 1,420,167 records
[SQLite] ✓ Valid sync (variance: ±15,000 within ±50,000)
[SQLite] Sync complete! 1420167 rows in 203.5s
```

### Retry Logs (Expected During Sync)
```
[SQLite] ⏳ 0 records received (retry 1/2) - likely mid-sync - will retry
[SQLite] ⏳ 0 records received (retry 2/2) - likely mid-sync - will retry
[SQLite] Retry scenario detected - not emailing yet
```

### Warning Logs (Investigate)
```
[SQLite] ❌ VALIDATION FAILED: Record count too low (500000 < 1400000)
[SQLite] Rolling back transaction - cache will NOT be updated
[SQLite] Sending validation failure alert...
[SQLite] Cache NOT updated. Keeping previous valid data.
```

### Error Logs (Immediate Action)
```
[SQLite] Sync error: [Errno 10048] Address already in use
[SQLite] Partner sync warning: Table not found
[Email] Failed to send alert: SMTP timeout
```

---

## Files Modified

1. **sqlite_cache.py**
   - Added email imports and configuration
   - Added `validate_bigquery_sync()` method
   - Added `_should_send_email()` method (smart retry logic)
   - Added `send_validation_failure_email()` method
   - Track zero-record retry attempts: `_zero_record_failures`
   - Creates and maintains `sync_error_log` table

2. **monitor_cache_health.py**
   - Shows complete sync history with statuses
   - Reports validation reasons
   - Color-coded success/failure indicators

3. **docs/CACHE/** (NEW)
   - 01_SMART_PARAMETERS.md - Smart validation rules
   - 02_IMPLEMENTATION_GUIDE.md - This file
   - 03_KNOWLEDGE_BASE.md - Complete system reference

---

## Verification Checklist

After deployment, verify:

- [ ] Backend starts without errors
- [ ] Monitor script shows cache records (should be 1,420,000+)
- [ ] Monitor script [3] section shows sync history
- [ ] Wait 15 minutes and run monitor script again to see new sync logged
- [ ] Recent syncs show ✓ SUCCESS status
- [ ] Dashboard displays projects normally
- [ ] No unexpected email alerts received (unless data is bad)

---

## Next Steps

1. **Monitor for 24 hours** - Ensure system runs without issues
2. **Review first email alert (if any)** - Could be legitimate data quality issue
3. **Adjust thresholds if needed** - Based on observed patterns
4. **Document in team processes** - Share cache health monitoring approach

---

## Support

If validation keeps failing:

1. Run `python monitor_cache_health.py` to see detailed logs
2. Check [3] SYNC HISTORY section for failure patterns
3. Query BigQuery directly to verify data count
4. Check backend console logs for detailed errors
5. Review [01_SMART_PARAMETERS.md](01_SMART_PARAMETERS.md#expected-behavior) for expected scenarios
6. See [03_KNOWLEDGE_BASE.md](03_KNOWLEDGE_BASE.md#troubleshooting) for troubleshooting guide

---

## Related Documentation

- [01_SMART_PARAMETERS.md](01_SMART_PARAMETERS.md) - User-friendly validation rules
- [03_KNOWLEDGE_BASE.md](03_KNOWLEDGE_BASE.md) - Complete system reference
- [README.md](README.md) - Cache documentation index
