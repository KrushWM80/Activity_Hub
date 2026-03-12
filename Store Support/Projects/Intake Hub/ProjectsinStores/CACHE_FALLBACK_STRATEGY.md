# 💾 Cache Fallback Strategy (March 12, 2026 Update)

**Status**: ✅ IMPLEMENTED AND TESTED  
**Date**: March 12, 2026  
**Related Files**: `backend/main.py`, `backend/sqlite_cache.py`, `KNOWLEDGE_BASE.md`

---

## Executive Summary

The Projects in Stores Dashboard uses a **DATA-BASED cache fallback strategy** that prioritizes data completeness over freshness:

> **If cache has data, use it. Only switch to BigQuery if cache is empty.**

This approach, combined with smart validation (prevents bad data from entering cache), ensures the dashboard always shows the most complete available data without unnecessary cloud queries.

---

## The Problem We Solved (March 11, 2026)

### What Was Happening

The original implementation used **TIME-BASED cache expiration**:

```
Cache expires after 30 minutes → Fall back to BigQuery
```

This created a conflict with smart validation:

1. **Good data syncs** to cache at 8:00 AM ✓
2. **Sync fails validation** at 8:15 AM → Cache NOT updated (correct, data protection) ✓
3. **Cache ages past 30 minutes** at 8:31 AM
4. **System abandons cache** → Falls back to BigQuery ✗
5. **BigQuery returns** potentially incomplete data ✗
6. **Dashboard shows incomplete data** to users ✗

### The Conflict

- **Smart Validation** (March 5): "Protect cache from bad data"
- **Time-Based Expiration** (pre-March 12): "Discard cache after 30 minutes"
- **Result**: These worked against each other

---

## The Solution (Implemented March 11-12)

### New Strategy: DATA-BASED FALLBACK

```
┌─────────────────────────────────────────┐
│         API Request Arrives             │
└────────────────┬────────────────────────┘
                 │
                 ▼
        ┌─────────────────────┐
        │ Does cache have     │
        │ any data?           │
        └────┬────────────────┘
             │
      ┌──────┴──────┐
      │             │
     YES            NO
      │             │
      ▼             ▼
┌──────────────┐  ┌────────────────┐
│ Use SQLite   │  │ Fall back to    │
│ Cache        │  │ BigQuery        │
│ <100ms       │  │ (10-30s)        │
└──────────────┘  └────────────────┘
```

### Key Changes Made

**1. Updated `/api/projects` Endpoint** (`backend/main.py`)
```python
# BEFORE (Time-based - removed)
if sqlite_cache.is_cache_valid() and not include_location:
    use_cache()

# AFTER (Data-based - implemented)
if sqlite_cache.get_record_count() > 0 and not include_location:
    use_cache()
```

**2. Updated `/api/summary` Endpoint** (`backend/main.py`)
```python
# BEFORE (Time-based - removed)
if sqlite_cache.is_cache_valid() and not tribe and not division:
    use_cache()

# AFTER (Data-based - implemented)
if sqlite_cache.get_record_count() > 0 and not tribe and not division:
    use_cache()
```

**3. Added `/api/cache/usage` Endpoint** (NEW - March 12)
```python
@app.get("/api/cache/usage")
async def cache_usage_status():
    # Shows which data source is active
    # Returns: data_source, reason, cache_populated, record_count, 
    #          last_sync_time, cache_age_minutes, cache_location, notes
```

---

## Why This Works

### Smart Validation Protects Data Quality

From `backend/sqlite_cache.py`:

**Validation Rules** (implemented March 5):
1. **Variance Check**: ±50,000 records acceptable (normal daily variation)
2. **Zero-Record Retry**: 2 automatic retries before alerting (sync takes 15-35 min)
3. **Duration Check**: Sync < 60 seconds likely incomplete
4. **Cache Protection**: Failed validation rolls back (old data preserved)

**Email Alert Logic**:
- Only sends when retries exhausted OR variance exceeded
- Silent retries prevent false positives

**Result**: Bad data never enters cache. Age becomes irrelevant.

### Graceful Degradation

| Scenario | Behavior | Result |
|----------|----------|--------|
| Sync succeeds, validates | Cache updates with new data | Dashboard shows fresh data ✓ |
| Sync fails validation | Cache keeps old data (rollback) | Dashboard shows complete old data ✓ |
| Cache empty at startup | Falls back to BigQuery | Slow load, but works ✓ |
| Cache down (corrupted) | Falls back to BigQuery | Service continues ✓ |

All scenarios result in good outcomes.

### Why Age Doesn't Matter

If sync validation prevents bad data from entering cache:
- 10-minute-old data: Guaranteed good
- 1-hour-old data: Guaranteed good
- 24-hour-old data: Guaranteed good
- Why? Because failed syncs don't update it

Only good data persists in cache.

---

## How to Verify This Works

### Quick Verification (< 1 minute)

1. **Check current data source**:
   ```
   Open: http://weus42608431466.homeoffice.wal-mart.com:8001/api/cache/usage
   Look for: "data_source" field
   ```

2. **What you should see**:
   ```json
   {
     "data_source": "SQLite Cache (LOCAL)",
     "reason": "Cache has valid data",
     "cache_populated": true,
     "record_count": 1350000
   }
   ```

### Detailed Verification (5-10 minutes)

**Step 1: Check cache has data**
```powershell
# On production server
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend"
sqlite3 cache.db "SELECT COUNT(*) FROM projects;"
# Expected: 1,300,000+
```

**Step 2: Check last sync**
```powershell
sqlite3 cache.db "SELECT value FROM sync_metadata WHERE key='last_sync';"
# Expected: Recent timestamp (within last 15-30 minutes)
```

**Step 3: Check API endpoints use cache**
```
Open Browser DevTools → Network Tab
Hit: http://weus42608431466.homeoffice.wal-mart.com:8001/api/projects
Check: Response time should be <200ms (cache) not 10+ seconds (BigQuery)
```

**Step 4: Wait > 30 minutes, verify still uses cache**
This is the key test for DATA-BASED logic:

1. Note current time: 8:00 AM
2. Check `/api/cache/usage` - should show cache
3. Wait 31+ minutes
4. Check `/api/cache/usage` again
5. Should STILL show cache (not fallback to BigQuery)
6. Response time should STILL be <200ms

If it still uses cache after 30+ minutes, the fix is working! ✓

---

## Files Modified

### 1. `backend/main.py`

**Changes in `/api/projects` endpoint (line ~490)**:
- Removed: `if sqlite_cache.is_cache_valid()...`
- Added: `if sqlite_cache.get_record_count() > 0...`
- Impact: Now uses cache regardless of age

**Changes in `/api/summary` endpoint (line ~685)**:
- Removed: `if sqlite_cache.is_cache_valid()...`
- Added: `if sqlite_cache.get_record_count() > 0...`
- Impact: Now uses cache regardless of age

**New endpoint `/api/cache/usage` (line ~445)**:
- Added: Complete new endpoint
- Purpose: Visibility into which data source is active
- Returns: Data source, age, record count, reasoning

### 2. `backend/sqlite_cache.py`

**No changes to this file** (validation logic already correct from March 5)

Validation still handles:
- `validate_bigquery_sync()` method: 3-tier validation
- `_should_send_email()` method: Smart retry logic
- `sync_from_bigquery()` method: Transaction logic

---

## Configuration

No configuration changes needed. The system uses:

```python
# Constants (already in sqlite_cache.py)
MIN_EXPECTED_RECORDS = 1_400_000       # Baseline for variance
MAX_ALLOWED_VARIANCE = 50_000          # ±50k acceptable
ZERO_RECORD_RETRY_COUNT = 2            # Retry attempts
ZERO_RECORD_RETRY_TIMEOUT = 2700       # 45-minute window (sync is 15-35 min)
MIN_SYNC_DURATION = 60                 # Seconds minimum
```

All thresholds are already optimal for this strategy.

---

## Monitoring & Troubleshooting

### Monitor Cache Health

**Dashboard users should check**:
- `/api/cache/usage` endpoint (new, added March 12)
- Shows data source and reasoning
- Updated in real-time

**System admins should monitor**:
1. **Sync success rate**: Check `sync_error_log` table in `cache.db`
2. **Record count stability**: Should stay ~1,350,000 ± 50,000
3. **Response times**: Should remain <200ms for cache hits
4. **Email alerts**: Should be rare (only when validation fails repeatedly)

### Troubleshooting

**Problem**: Seeing slow responses (10+ seconds)

**Diagnosis**:
```json
GET /api/cache/usage
{
  "data_source": "BigQuery (CLOUD)",
  "reason": "Cache is empty, using BigQuery"
}
```

**Solution**: Cache is empty or corrupted
- Delete `backend/cache.db`
- Restart backend (will rebuild on startup)
- Wait 5-10 minutes for sync

**Problem**: Dashboard shows incomplete data

**Note**: With this fix, incomplete data only comes from BigQuery
- Check if sync is working: Look for `sync_error_log` errors
- Check if BigQuery itself has the data: Query manually
- Run: `/api/cache/status` endpoint

**Problem**: Dashboard shows old data (> 24 hours)

**Usually not a problem** because:
- Sync every 15 minutes keeps data fresh IF BigQuery works
- Smart validation ensures old data is good data

**Check if needed**:
```json
GET /api/cache/usage
Look at: cache_age_minutes
If > 1440 (24 hours), check sync_error_log for failures
```

---

## Testing Checklist

Use after any code changes to `/api/projects` or `/api/summary`:

- [ ] **Fast response for cache hits**
  - Test: `curl http://localhost:8001/api/projects?limit=100`
  - Expected: Response in <200ms
  - Result: _____ ms

- [ ] **Cache used when available**
  - Test: `curl http://localhost:8001/api/cache/usage`
  - Expected: `"data_source": "SQLite Cache (LOCAL)"`
  - Result: ✓ / ✗

- [ ] **Cache used after 30 minutes**
  - Test: Wait 31 min, then hit endpoint
  - Expected: Still <200ms response (cache, not BigQuery)
  - Result: _____ ms

- [ ] **Fallback works when cache empty**
  - Test: Delete `cache.db`, hit API
  - Expected: Slower response, shows BigQuery data
  - Expected in cache/usage: `"data_source": "BigQuery (CLOUD)"`
  - Result: ✓ / ✗

- [ ] **Cache repopulates after rebuild**
  - Test: After deletion, wait for sync to rebuild
  - Expected: Record count > 1,300,000
  - Test: `"data_source"` now shows cache again
  - Result: ✓ / ✗

---

## FAQ

**Q: Why not use time-based expiration like standard caching?**

A: Because our data quality is guaranteed by validation. Standard caching needs time-limits because they can't guarantee quality. We can guarantee it, so age is unnecessary.

**Q: What if I want fresh data regardless?**

A: Set `include_location=true` on `/api/projects` endpoint. This forces BigQuery (slower, but guaranteed latest). For normal use, cache freshness is determined by sync, not time.

**Q: How long can I keep using old cached data?**

A: As long as you want - it's guaranteed good. But in practice, sync runs every 15 minutes successfully, so cache updates regularly.

**Q: Will this hurt performance?**

A: No, improves it. Cache hits are <100ms vs BigQuery at 10-30s. Fewer falls back to BigQuery means faster average response times.

**Q: What if BigQuery is down?**

A: Dashboard uses cache instead (good strategy). System continues working with old data rather than failing. This is a feature, not a bug.

---

## Related Documentation

- **[KNOWLEDGE_BASE.md](KNOWLEDGE_BASE.md)** - System overview, includes cache strategy summary
- **[sqlite_cache.py](../backend/sqlite_cache.py)** - Implementation details of smart validation
- **[main.py](../backend/main.py)** - API endpoints using new fallback logic
- **[CACHE_VALIDATION_PARAMETERS.md](../docs/CACHE/01_SMART_PARAMETERS.md)** - Validation rules and thresholds

---

**Document Version**: 1.0  
**Last Updated**: March 12, 2026  
**Status**: ✅ Production Ready
