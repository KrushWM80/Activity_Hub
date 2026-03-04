# SQLite Cache Sync System - Knowledge Base

## Overview

The **Projects in Stores Dashboard** uses a three-tier data access strategy for optimal performance:

1. **SQLite Cache** (milliseconds) - Local database for fast dashboard loads
2. **BigQuery Queries** (seconds) - For user filters and searches  
3. **Metadata Tracking** - Error logs and sync history

---

## Cache Architecture

### Purpose
Provide instant dashboard response times without hitting BigQuery on every page load. The cache syncs from BigQuery every 15 minutes with built-in validation.

### How It Works

**Initial Load:**
- Backend starts → Initializes SQLite cache
- Background thread begins → `sync_from_bigquery()` triggers immediately
- Dashboard loads from cache once sync completes
- User searches/filters hit BigQuery for real-time accuracy

**Ongoing Sync:**
- Every 15 minutes: Background sync thread triggers automatically
- Validates record count before updating cache
- Logs all sync attempts (success and failures) to `sync_error_log` table
- Sends email alert if validation fails to prevent bad data

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

### Validation Rules

**Before updating cache, the sync must verify:**

1. ✓ **Record Count Check** - Synced record count must match or exceed minimum threshold
   - Minimum expected: **1,400,000 records** (allows 0.7% variance)
   - If below threshold → Validation fails → Cache NOT updated → Email sent

2. ✓ **Data Quality Check** - Validate required columns exist
   - Must have: `Division`, `Region`, `Market`, `Facility`, `Phase`, `OwnER`, `Status`
   - If missing → Validation fails → Cache NOT updated → Email sent

3. ✓ **Sync Duration Check** - Ensure sync completed successfully
   - Expected duration: 195-210 seconds
   - If sync took < 60s (likely incomplete) → Validation fails → Cache NOT updated

### Why This Matters

**Problem Case**: If BigQuery data becomes corrupted or a table schema changes, the old validation system would:
- Silently return 0 records (due to column name errors)
- Update cache with empty data
- Dashboard would show "No projects" instead of detecting the problem

**New Validation System**: 
- Detects when sync returns far fewer records than expected
- Prevents overwriting good cache with bad data
- Sends immediate email alert for investigation
- Preserves old cache data until issue is resolved

---

## Sync History & Error Monitoring

### Check Cache Health

Run the monitoring script anytime:

```bash
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend"
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
- `error_message` - "SUCCESS: X records synced" or error description
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

### Does NOT Exist (Removed from query)
- ~~`Project_Title`~~ → Use `Title` instead
- ~~`WM_Week`~~ (integer) → Use as-is  
- ~~`FY`~~ (integer) → Use as-is

---

## Email Notifications

### When Email Is Sent

**Cache Sync Validation Fails** → Email to: `kendall.rush@walmart.com`

Email triggers on:
1. Record count drops below 1,400,000
2. Required columns missing from BigQuery
3. Sync took < 60 seconds (incomplete)
4. Sync error (exception caught)

### Email Contents

Subject: `⚠️ [ALERT] Projects in Stores Cache Sync Failed`

Body includes:
```
Sync Timestamp: 2026-03-03 18:45:23
Status: VALIDATION FAILED
Records Expected: ~1,420,000
Records Received: [actual number]
Sync Duration: [seconds]

Reason: Record count below threshold (1,400,000 minimum)

Action Required:
1. Check BigQuery IH_Intake_Data table
2. Verify Status='Active' records are present
3. Confirm no schema changes occurred
4. Review BigQuery audit logs for failures
5. If issue persists, manually trigger cache resync

Current Cache Status:
- Last Valid Sync: [timestamp]
- Records in Cache: [count]
- Age: [time since last valid sync]
```

---

## Manual Cache Operations

### Force Full Resync
```bash
# 1. Stop backend server
# 2. Delete cache file
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend"
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
3. Delete cache.db and restart backend

### Cache Syncs Every 15 Minutes But Dashboard Stale
**Cause**: Cache updating but data quality degraded
**Fix**:
1. Check email for validation failure alerts
2. Run monitor script to see record count
3. Compare to expected 1,420,000
4. If lower, check BigQuery data quality
5. Validate WHERE Status='Active' filter is working

### Email Not Received After Failed Sync
**Cause**: Could be SMTP configuration or email service
**Fix**:
1. Check backend console for email send errors
2. Verify recipient email `kendall.rush@walmart.com` is valid
3. Check if running on Walmart network/VPN (required for SMTP)
4. Check email_service logs

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

## Related Files

- **sqlite_cache.py** - Cache sync logic with validation
- **monitor_cache_health.py** - Dashboard health monitoring script
- **main.py** - Backend server and API endpoints
- **projects_cache.db** - Actual SQLite cache file (~500MB)

---

## Key Contacts

- **Cache Maintenance**: Check `monitor_cache_health.py` output
- **Email Alerts**: Sent to `kendall.rush@walmart.com`
- **Dashboard Issues**: Check `/api/summary` and `/api/projects` endpoints
- **BigQuery Questions**: Check `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
