# SQLite Cache Sync System - Knowledge Base

**Updated**: March 10, 2026  
**Location**: `docs/CACHE/`

---

## Overview

The **Projects in Stores Dashboard** uses a three-tier data access strategy for optimal performance:

1. **SQLite Cache** (milliseconds) - Local database for fast dashboard loads
2. **BigQuery Queries** (seconds) - For user filters and searches  
3. **Metadata Tracking** - Error logs and sync history

---

## Cache Architecture

### Purpose
Provide instant dashboard response times without hitting BigQuery on every page load. The cache syncs from BigQuery every 15 minutes with built-in validation and smart retry logic.

### How It Works

**Initial Load:**
- Backend starts → Initializes SQLite cache
- Background thread begins → `sync_from_bigquery()` triggers immediately
- Dashboard loads from cache once sync completes
- User searches/filters hit BigQuery for real-time accuracy

**Ongoing Sync (Every 15 minutes):**
1. BigQuery query executes (~180 seconds)
2. Data validated against smart parameters
3. If valid → Cache updated + Logged as SUCCESS
4. If invalid → Cache rolled back + Logged + Email sent (if not retry)
5. Partners synced from IH_Branch_Data table
6. Next sync scheduled in 15 minutes

---

## Data Validation Strategy

### The 1.4M Record Expectation

The cache syncs approximately **1,420,167 records** from BigQuery's `IH_Intake_Data` table:

```
SELECT COUNT(*) FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Status = 'Active'
```

This high count includes:
- **Project-Facility Records**: Each project is duplicated for each facility it affects
- **Realty Heavy**: ~1,418,869 records are Phase='Realty'
- **Operations**: ~149,446 records from Project_Source='Operations'
- **Multiple Divisions**: EAST (376K), WEST (264K), SOUTHWEST (232K), etc.

### Smart Validation Rules (March 2026+)

**Before updating cache, the sync validates:**

1. ✓ **Variance Check** - Records within ±50,000 of expected (1,400,000)
   - Range: 1,350,000 to 1,450,000 → **VALID** (no email)
   - Outside range → **INVALID** (email sent)
   - Why: Daily data fluctuations are normal

2. ✓ **Zero Records Check** - If 0 records synced
   - Retry 1: Silently retry (may be mid-sync)
   - Retry 2: Silently retry (gives sync time)
   - Retry 3+: Email sent (likely stuck)
   - Why: Sync takes 15-35 minutes, gives buffer time

3. ✓ **Sync Duration Check** - Sync must take ≥ 60 seconds
   - < 60 seconds → **INVALID** (incomplete)
   - ≥ 60 seconds → Likely valid
   - Why: Detects incomplete/error states

### Cache Protection

If validation fails:
- ✓ Transaction is **rolled back** - no bad data written
- ✓ Old cache data is **preserved** - dashboard continues working
- ✓ Failure is **logged** - you see in monitor output
- ✓ **Email sent** (if not in retry window) - you're notified

---

## Sync History & Error Monitoring

### Check Cache Health

Run the monitoring script anytime:

```bash
cd backend
python monitor_cache_health.py
```

**Output Shows:**
- [1] CACHE STATUS - Current record count and validity
- [2] LAST SYNC - When and how long ago cache was updated
- [3] SYNC HISTORY - Last 30 sync attempts with results
- [4] RECORD BREAKDOWN - Records by Division, Phase, FY, Source
- [5] RECOMMENDATIONS - Actions based on cache health

### Database Tables

#### `sync_error_log` Table
Tracks every sync attempt (success and failure):

```sql
SELECT * FROM sync_error_log ORDER BY timestamp DESC LIMIT 10
```

Columns:
- `timestamp` - When sync was attempted
- `error_message` - "SUCCESS: X records synced" or error/retry description
- `record_count` - How many records were synced
- `sync_duration_seconds` - How long the sync took
- Index: `idx_sync_errors_timestamp` (timestamp ordered)

#### `sync_metadata` Table
- Stores last successful sync timestamp
- Used for cache age calculation

#### `projects` Table (1.4M records)
The actual cached data with columns:
```
project_id, intake_card, title, project_source, division, region,
market, store, facility, phase, wm_week, fy, status, owner, partner,
store_area, business_area, health, business_type, associate_impact,
customer_impact, last_updated, created_at
```

---

## BigQuery Column Mapping

The sync query maps BigQuery columns to SQLite cache columns:

### Critical Columns (Must Exist)
| BigQuery    | SQLite    | Type    |
|-----------|-----------|---------|
| `Division` | `division` | STRING  |
| `Region` | `region` | STRING  |
| `Market` | `market` | STRING  |
| `Facility` | `facility,store` | FLOAT→STRING |
| `Phase` | `phase` | STRING  |
| `Title` | `title` | STRING  |
| `Status` | `status` | STRING  |
| `Owner` | `owner` | STRING  |

### Optional Columns (Coalesced with PROJECT_* versions)
| BigQuery Primary | Fallback | Purpose |
|---|---|---|
| `Store_Area` | N/A | Store area classification |
| `Business_Area` | N/A | Business division |
| `Health` | `PROJECT_HEALTH` | Project health status |
| `Business_Type` | N/A | Type of business |
| `ASSOCIATE_IMPACT` | N/A | Employee impact |
| `CUSTOMER_IMPACT` | N/A | Customer impact |

---

## Email Notifications

### When Email IS Sent (Smart Logic)

**Cache Sync Validation Fails** → Email to: `kendall.rush@walmart.com`

Email triggers on:
1. **Variance Exceeds ±50k** (records far outside normal range)
2. **0 Records After Retries** (45+ minutes with no data)
3. **Sync < 60 Seconds** (incomplete/error state)
4. **BigQuery Error** (query exception)

**Does NOT trigger on:**
- ✓ Variance within ±50k (normal daily variation)
- ✓ 0 records on retry 1-2 (likely mid-sync)

### Email Contents

Subject: `⚠️ [ALERT] Projects in Stores Cache Sync Failed`

Body includes:
```
CACHE VALIDATION FAILED - INVESTIGATION REQUIRED

Sync Timestamp: 2026-03-10 14:45:23
Status: VALIDATION FAILED

Data Quality Check:
- Records Synced: [actual]
- Expected: ~1,400,000
- Variance: ±[amount] (threshold: ±50,000)
- Sync Duration: [seconds]

Failure Reason: [specific reason]

System Protection:
✓ Cache NOT updated - using last valid version
✓ Previous data preserved and serving
✓ Cache Age: [time since last valid sync]
✓ Records in Cache: [count]

Action Required:
1. Check if data sync is still running
2. If not, verify BigQuery IH_Intake_Data
3. Validate record count with WHERE Status='Active'
4. Check for schema changes
5. Review BigQuery audit logs
```

---

## Manual Cache Operations

### Force Full Resync
```bash
# 1. Stop backend server
# 2. Delete cache file
cd backend
Remove-Item "projects_cache.db" -Force

# 3. Restart backend (will create new cache and sync)
python main.py
```

### Monitor Sync in Real-Time
Watch the backend console logs:
```
[Startup] Initializing SQLite cache...
[Startup] Starting background cache sync...
[SQLite] Starting sync from BigQuery...
[SQLite] Fetched 1420167 rows from BigQuery
[SQLite] ✓ Validation passed - updating cache with 1,420,167 records
[SQLite] Sync complete! 1420167 rows in 203.5s
```

### Check Specific Sync Result
```python
# In monitor_cache_health.py output
# Look at [3] SYNC HISTORY section
# Each row shows: Timestamp, Status, Records, Duration
```

---

## Troubleshooting

### Cache Shows 0 Records
**Cause**: Sync failed or hasn't run yet
**Fix**: 
1. Check [3] SYNC HISTORY in monitor output
2. Look for ERROR status in recent attempts
3. Check backend console logs for BigQuery errors
4. Verify column names in sync query

### Cache Has Wrong Column Names Error
**Cause**: BigQuery schema changed or query references wrong columns
**Example Error**: `Unrecognized name: Project_Title; Did you mean Project_Type?`
**Fix**:
1. Query BigQuery schema to find correct column names
2. Update `sqlite_cache.py` sync query
3. Delete projects_cache.db and restart backend

### Cache Syncs Every 15 Minutes But Dashboard Stale
**Cause**: Cache updating but data quality degraded, or within validation threshold
**Fix**:
1. Run monitor script to see last sync time and record count
2. Check if within ±50k variance (normal if yes)
3. If outside variance, check BigQuery data quality
4. Validate WHERE Status='Active' filter is working

### Receiving "0 records" Emails Frequently
**Cause**: Might be syncs happening during long-running queries
**Fix**:
1. Check [3] SYNC HISTORY - count how many 0 records appear
2. If 1-2 per day: Normal (system is retrying correctly)
3. If more: May need to adjust ZERO_RECORD_RETRY_TIMEOUT
4. See [01_SMART_PARAMETERS.md](01_SMART_PARAMETERS.md#configuration) for settings

### Email Not Received After Failed Sync
**Cause**: Could be SMTP configuration or email service
**Fix**:
1. Check backend console for email send errors
2. Verify recipient email `kendall.rush@walmart.com` is valid
3. Check if running on Walmart network/VPN (required for SMTP)
4. Verify SMTP_SERVER in sqlite_cache.py is correct

---

## Performance Notes

### Sync Times
- **Full cache sync**: 195-210 seconds (~1.4M records)
- **BigQuery data retrieval**: ~180 seconds  
- **SQLite insert batch**: ~15-20 seconds
- **Partner data sync**: ~5 seconds

### Cache Performance
- **Dashboard initial load**: ~500ms (from SQLite)
- **Project list /api/projects**: <100ms
- **Summary stats /api/summary**: <50ms
- **Filter searches**: 2-5 seconds (hits BigQuery for accuracy)

### Database Indexes
Created for fast filtering:
```
idx_project_id, idx_title, idx_division, idx_region, idx_market,
idx_store, idx_phase, idx_fy, idx_project_source, idx_owner,
idx_partner, idx_store_area, idx_business_area, idx_health,
idx_business_type, idx_sync_errors_timestamp
```

---

## Related Documentation

- [01_SMART_PARAMETERS.md](01_SMART_PARAMETERS.md) - Smart validation rules (user-friendly)
- [02_IMPLEMENTATION_GUIDE.md](02_IMPLEMENTATION_GUIDE.md) - Technical implementation & testing
- [README.md](README.md) - Cache documentation index

### Related Files in Backend

- **sqlite_cache.py** - Cache sync logic with validation
- **monitor_cache_health.py** - Dashboard health monitoring script
- **main.py** - Backend server and API endpoints
- **projects_cache.db** - Actual SQLite cache file (~500MB)

---

## Key Settings

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `MIN_EXPECTED_RECORDS` | 1,400,000 | Baseline for variance check |
| `MAX_ALLOWED_VARIANCE` | 50,000 | ±50k acceptable daily variation |
| `ZERO_RECORD_RETRY_COUNT` | 2 | Attempts before email |
| `ZERO_RECORD_RETRY_TIMEOUT` | 2700s (45 min) | Retry window |
| `MIN_SYNC_DURATION` | 60 seconds | Minimum valid sync time |
| `SYNC_INTERVAL` | 900 seconds (15 min) | How often to sync |

---

## Questions?

Start at:
1. **User-facing?** → [01_SMART_PARAMETERS.md](01_SMART_PARAMETERS.md)
2. **Technical?** → [02_IMPLEMENTATION_GUIDE.md](02_IMPLEMENTATION_GUIDE.md)
3. **Full reference?** → This file (03_KNOWLEDGE_BASE.md)
4. **Still unclear?** → Check backend logs with `python main.py`
