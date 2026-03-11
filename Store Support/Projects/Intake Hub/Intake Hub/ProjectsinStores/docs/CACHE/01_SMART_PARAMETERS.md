# Cache Validation Smart Parameters

**Updated**: March 10, 2026  
**Status**: ✅ ACTIVE  
**Location**: `docs/CACHE/`

---

## Overview

The cache validation system now includes intelligent parameters that reduce false-positive email alerts by understanding the sync timeline and normal data variance.

---

## Smart Validation Rules

### 1️⃣ Variance Within ±50k (Allow, Don't Email)

**What It Means**:
- Expected records: ~1,400,000
- Acceptable range: 1,350,000 to 1,450,000
- If synced records fall within this range → **VALID** (no email)

**Why**:
- Daily data changes naturally cause variance
- BigQuery table may gain/lose records based on Status='Active' filter
- ±50k variation is normal operational behavior

**Example**:
```
Expected: 1,400,000
Synced: 1,385,000  → Variance: ±15,000 ✓ VALID (no email)
Synced: 1,420,000  → Variance: ±20,000 ✓ VALID (no email)
Synced: 1,470,000  → Variance: ±70,000 ✗ INVALID (email sent)
```

---

### 2️⃣ Records Synced = 0 (Retry before Email)

**What It Means**:
- When sync returns 0 records, it likely means the sync is still running (mid-sync)
- System automatically retries up to 2 times without sending email
- Only emails after retries exhausted + timeout exceeded

**Timeline**:
```
8:36 AM  → Sync starts (takes 15-35 minutes)
8:51-9:11 AM → Sync completes (normal window)

Retry Logic:
- Sync attempt 1 (say 8:35 AM): 0 records → Retry, don't email
- Sync attempt 2 (say 8:50 AM): 0 records → Retry, don't email  
- Sync attempt 3 (say 9:05+ AM): 0 records → Email sent (retry count exceeded)
```

**Why**:
- Prevents email spam during normal sync operations
- Gives sync 15-35 min + buffer (45 min total window)
- Only alerts if sync appears truly stuck

**Configuration** (in `sqlite_cache.py`):
```python
ZERO_RECORD_RETRY_COUNT = 2  # Retry 2 times max
ZERO_RECORD_RETRY_TIMEOUT = 2700  # 45 minutes
```

---

### 3️⃣ Use Last Good Cache Version Until Fixed

**What It Means**:
- When validation fails, cache is **NOT updated** (transaction rolled back)
- Dashboard continues serving the previous valid cached data
- Users see no outage or data loss

**How It Works**:
```
Sync Fails → Don't update cache
         ↓
Dashboard still accessible
         ↓
Users see last valid cached version
         ↓
You get email alert with details
         ↓
Next sync will proceed normally if data is now valid
```

**Protection**:
- ✓ Bad data never overwrites good cache
- ✓ Dashboard never shows "Error" or "No Data"
- ✓ Graceful degradation during problems
- ✓ Full transparency in monitoring dashboard

---

## Email Alert Flow

### When Email IS Sent:

1. **Variance Exceeds ±50k** (> 1,450,000 or < 1,350,000)
   - Indicates significant data quality issue
   - Immediate email alert

2. **Records = 0 After 2 Retries** (45+ minutes with no data)
   - Indicates sync is stuck
   - Retried silently first
   - Email sent only when retries exhausted

3. **Sync Takes < 60 Seconds**
   - Indicates incomplete/error state
   - Email sent immediately

### When Email NOT Sent:

1. **Variance Within ±50k** ✓
2. **Records = 0 on Retry 1-2** ✓
3. **Sync Successful** ✓

---

## Monitoring Dashboard

Check cache health anytime with:

```powershell
cd backend
python monitor_cache_health.py
```

**Output Shows**:
- [1] Cache status & record count
- [2] Last sync timestamp & age
- [3] Sync history (last 30 attempts) with retry status
- [4] Record breakdown by divisions/phases
- [5] Health recommendations

---

## Configuration

All parameters in `backend/sqlite_cache.py`:

```python
MIN_EXPECTED_RECORDS = 1_400_000       # Expected records
MAX_ALLOWED_VARIANCE = 50_000           # ±50k allowed
ZERO_RECORD_RETRY_COUNT = 2             # Retry attempts for 0 records
ZERO_RECORD_RETRY_TIMEOUT = 2700        # 45 minute window
MIN_SYNC_DURATION = 60                  # Minimum sync time (seconds)
```

**To Adjust** (if you observe different patterns):
1. Edit the constants above
2. Review [02_IMPLEMENTATION_GUIDE.md](02_IMPLEMENTATION_GUIDE.md#configuration) for guidance
3. Test with `monitor_cache_health.py` to verify no false positives

---

## Expected Behavior

### Normal Day
```
✓ 8:50 AM: Sync completes with 1,420,000 records → Cache updated
✓ 9:05 AM: Sync completes with 1,418,500 records → Cache updated (within ±50k)
✓ 9:20 AM: Sync completes with 1,402,000 records → Cache updated (within ±50k)
✓ No emails sent (all syncs valid)
```

### Mid-Sync Scenario
```
8:35 AM: Sync starts (runs 15-35 min)
8:40 AM: Check hits 0 records → Log retry #1, don't email
8:45 AM: Check hits 0 records → Log retry #2, don't email
8:52 AM: Sync completes with 1,415,000 records → Cache updated, retries cleared
✓ No email sent (within retry window)
```

### Real Failure Scenario
```
8:36 AM: Sync starts
8:51 AM: Sync returns 0 records → Retry #1
9:00 AM: Sync returns 0 records → Retry #2
9:30 AM: Still 0 records → Email SENT (exceeded timeout)
📧 Alert: "0 records after 2 retry attempts (45+ minutes) - data sync appears stuck"
```

### Variance Issue Scenario
```
7:00 PM: Sync returns 1,250,000 records (150k below minimum)
⚠️ Variance: ±150,000 > ±50,000 threshold
📧 Alert: "Record count variance too high"
✓ Cache NOT updated, using previous good version
```

---

## Quick Reference

| Scenario | Action | Email? |
|----------|--------|--------|
| Variance ±10k | Accept, update cache | ❌ No |
| Variance ±75k | Reject, keep old cache | ✅ Yes |
| 0 records (retry 1) | Retry, don't email | ❌ No |
| 0 records (retry 2) | Retry, don't email | ❌ No |
| 0 records (retry 3+) | Reject, email alert | ✅ Yes |
| < 60 second sync | Reject, keep old cache | ✅ Yes |
| Successful sync | Update cache | ❌ No |

---

## Next Steps

- Want full technical details? → See [02_IMPLEMENTATION_GUIDE.md](02_IMPLEMENTATION_GUIDE.md)
- Need complete system reference? → See [03_KNOWLEDGE_BASE.md](03_KNOWLEDGE_BASE.md)
- Back to cache documentation index? → See [README.md](README.md)

---

## Questions?

The smart parameters ensure:
- ✅ No false email alerts during normal sync operations
- ✅ Dashboard stays online with good cached data
- ✅ Real problems are caught and investigated
- ✅ Graceful behavior under data quality issues
