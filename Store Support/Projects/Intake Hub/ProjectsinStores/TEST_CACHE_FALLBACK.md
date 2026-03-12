# 🧪 Testing Cache Fallback Implementation (March 12, 2026)

**Purpose**: Verify the data-based cache fallback strategy is working correctly  
**Estimated Time**: 10-15 minutes  
**Required**: Backend server running, network access to production server

---

## Quick Test (< 2 minutes)

### Step 1: Start the Backend Server

If not already running on port 8001:

```powershell
# Navigate to backend directory
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend"

# Start the server (creates/connects to cache.db)
python main.py
```

**Expected output**:
```
[Startup] Initializing SQLite cache...
[Background] Cache is valid with 1300000+ records
[Startup] Background sync thread started, server ready for requests
Uvicorn running on http://127.0.0.1:8001
```

### Step 2: Test the New Endpoint in Browser

Open in any browser:

**Local (Dev - Port 8002)**:
```
http://localhost:8002/api/cache/usage
```

**Production (Port 8001)**:
```
http://weus42608431466.homeoffice.wal-mart.com:8001/api/cache/usage
```

**Expected response** (when cache has data):
```json
{
  "data_source": "SQLite Cache (LOCAL)",
  "reason": "Cache has valid data",
  "cache_populated": true,
  "record_count": 1350000,
  "last_sync_time": "2026-03-12T09:30:45.123456",
  "cache_age_minutes": 5,
  "cache_age_seconds": 300,
  "cache_location": "C:\\...\\backend\\cache.db",
  "notes": [
    "✓ Fallback logic uses DATA presence, not age",
    "✓ Smart validation prevents bad data in cache",
    "Cache created 5 minutes ago"
  ]
}
```

✅ **If you see this**, the endpoint is working!

---

## Detailed Tests (5-10 minutes each)

### Test 1: Verify Cache Is Being Used

**Command 1A - HTML Browser**:
1. Open Developer Tools (F12)
2. Go to **Network** tab
3. Navigate to: `http://localhost:8001/` (or production URL)
4. Click on `/api/projects` request
5. Check **Response Time**

**Expected**: Should be <200ms (indicates cache hit, not BigQuery)

**Command 1B - PowerShell Quick Test**:
```powershell
# Time a single request
$sw = [System.Diagnostics.Stopwatch]::StartNew()
$result = Invoke-WebRequest -Uri "http://localhost:8001/api/cache/usage" -UseBasicParsing
$sw.Stop()
Write-Host "Response time: $($sw.ElapsedMilliseconds)ms"
Write-Host "Data source: $($result.Content | ConvertFrom-Json | Select-Object -ExpandProperty data_source)"
```

**Expected output**:
```
Response time: 15ms
Data source: SQLite Cache (LOCAL)
```

---

### Test 2: Verify Fallback Works (Cache Empty Scenario)

**Setup**: Delete the cache file to simulate cache failure

```powershell
# Stop backend server first (Ctrl+C)

# Delete cache
Remove-Item "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\Intake Hub\Intake Hub\ProjectsinStores\backend\cache.db"

# Restart backend
cd "backend"
python main.py
```

**Test 1 - Fallback endpoint**:
```
Open: http://localhost:8001/api/cache/usage
Expected: "data_source": "BigQuery (CLOUD)"
Expected: "reason": "Cache is empty, using BigQuery"
Expected: "record_count": 0
```

**Test 2 - Slower response time**:
```powershell
$sw = [System.Diagnostics.Stopwatch]::StartNew()
$result = Invoke-WebRequest -Uri "http://localhost:8001/api/projects?limit=100" -UseBasicParsing
$sw.Stop()
Write-Host "Response time: $($sw.ElapsedMilliseconds)ms (should be 5000+ ms - BigQuery fallback)"
```

**Expected**: 5000-10000+ milliseconds (BigQuery is slow, this proves fallback is working)

**Test 3 - Cache rebuilds on sync**:
```powershell
# Wait 15-30 seconds for background sync to run, then test again
Start-Sleep -Seconds 20

# Check again
$result = Invoke-WebRequest -Uri "http://localhost:8001/api/cache/usage" -UseBasicParsing
$content = $result.Content | ConvertFrom-Json
Write-Host "Data source now: $($content.data_source)"
Write-Host "Records now: $($content.record_count)"
```

**Expected**: 
```
Data source now: SQLite Cache (LOCAL)
Records now: 1300000+
```

✅ This proves cache rebuilt itself from BigQuery sync

---

### Test 3: The 30-Minute Test (Key Test for Data-Based Logic)

**Purpose**: Verify cache is used AFTER 30 minutes (proof that we're using data-based, not time-based, logic)

**Step 1 - Establish baseline**:
```powershell
# Get current time and cache status
Write-Host "Starting test at: $(Get-Date -Format 'HH:mm:ss')"
$initial = Invoke-WebRequest -Uri "http://localhost:8001/api/cache/usage" -UseBasicParsing | ConvertFrom-Json
Write-Host "Initial state: $($initial.data_source)"
Write-Host "Cache age: $($initial.cache_age_minutes) minutes"
```

**Step 2 - Wait 31+ minutes**:
```powershell
Write-Host "Waiting 31 minutes... (This is a timed wait, do not interrupt)"
for ($i = 0; $i -lt 31; $i++) {
    Start-Sleep -Seconds 60
    Write-Host "Elapsed: $($i + 1) minutes"
}
Write-Host "Finished waiting at: $(Get-Date -Format 'HH:mm:ss')"
```

**Step 3 - Test still uses cache**:
```powershell
# Key test: Should STILL use cache
$sw = [System.Diagnostics.Stopwatch]::StartNew()
$final = Invoke-WebRequest -Uri "http://localhost:8001/api/cache/usage" -UseBasicParsing | ConvertFrom-Json
$sw.Stop()

Write-Host "RESULTS:"
Write-Host "  Data source: $($final.data_source)"
Write-Host "  Cache age: $($final.cache_age_minutes) minutes"
Write-Host "  Response time: $($sw.ElapsedMilliseconds)ms"
Write-Host ""

# SUCCESS CRITERIA
if ($final.data_source -eq "SQLite Cache (LOCAL)" -and $sw.ElapsedMilliseconds -lt 500) {
    Write-Host "✅ SUCCESS: Using cache after 30+ minutes (data-based logic working!)"
} else {
    Write-Host "❌ FAILURE: Fell back to BigQuery (time-based logic still active?)"
}
```

**Expected output**:
```
RESULTS:
  Data source: SQLite Cache (LOCAL)
  Cache age: 31+ minutes
  Response time: <200ms

✅ SUCCESS: Using cache after 30+ minutes (data-based logic working!)
```

⚠️ **If you see BigQuery in results after 30+ min, the old code is still active**

---

### Test 4: Verify Cache Used in Dashboard

**Test the actual Dashboard API calls**:

```powershell
# Test /api/projects (uses new data-based logic)
$sw = [System.Diagnostics.Stopwatch]::StartNew()
$projects = Invoke-WebRequest -Uri "http://localhost:8001/api/projects?limit=100" -UseBasicParsing
$sw.Stop()
Write-Host "/api/projects response: $($sw.ElapsedMilliseconds)ms (should be <200ms)"

# Test /api/summary (uses new data-based logic)
$sw = [System.Diagnostics.Stopwatch]::StartNew()
$summary = Invoke-WebRequest -Uri "http://localhost:8001/api/summary" -UseBasicParsing
$sw.Stop()
Write-Host "/api/summary response: $($sw.ElapsedMilliseconds)ms (should be <200ms)"

# Test /api/filters (unchanged, uses cache)
$sw = [System.Diagnostics.Stopwatch]::StartNew()
$filters = Invoke-WebRequest -Uri "http://localhost:8001/api/filters" -UseBasicParsing
$sw.Stop()
Write-Host "/api/filters response: $($sw.ElapsedMilliseconds)ms (should be <200ms)"
```

**Expected**: All responses < 200-300ms

---

## Verification Checklist

Use this form to document your test results:

### Environment Info
- [ ] Backend running on: __ (localhost:8002 / weus42608431466.homeoffice.wal-mart.com:8001)
- [ ] Date/Time: __ __:__ (MM-DD HH:MM)
- [ ] Windows user: __ (for audit trail)

### Test Results

#### Quick Test (Required)
- [ ] **P1: Endpoint responds** 
  - [ ] `/api/cache/usage` returns 200 OK
  - [ ] Response contains `data_source` field
  - Status: __ PASS / __ FAIL

#### Test 1: Cache Being Used
- [ ] **T1A: Response time < 200ms**
  - Measured: __ ms
  - Status: __ PASS / __ FAIL

- [ ] **T1B: Shows cache data source**
  - Response: SQLite Cache (LOCAL) / BigQuery (CLOUD)
  - Status: __ PASS / __ FAIL

#### Test 2: Fallback Works
- [ ] **T2A: Cache empty state detected**
  - Fallback shows: BigQuery (CLOUD)
  - Status: __ PASS / __ FAIL

- [ ] **T2B: Response slow without cache**
  - Measured: __ ms (expected 5000+ ms)
  - Status: __ PASS / __ FAIL

- [ ] **T2C: Cache rebuilds on sync**
  - Records restored: __ (expected 1,300,000+)
  - Status: __ PASS / __ FAIL

#### Test 3: 30-Minute Test (Critical)
- [ ] **T3: Uses cache after 30+ minutes**
  - Data source after wait: SQLite Cache (LOCAL) / BigQuery (CLOUD)
  - Response time: __ ms (expected < 200ms)
  - Status: __ PASS / __ FAIL

#### Test 4: Dashboard APIs
- [ ] **T4A: /api/projects response time**
  - Measured: __ ms (expected < 200ms)
  - Status: __ PASS / __ FAIL

- [ ] **T4B: /api/summary response time**
  - Measured: __ ms (expected < 200ms)
  - Status: __ PASS / __ FAIL

- [ ] **T4C: /api/filters response time**
  - Measured: __ ms (expected < 200ms)
  - Status: __ PASS / __ FAIL

### Overall Result
- [ ] All tests PASSED ✅
- [ ] Some tests FAILED ❌ (details: __________________)

---

## Troubleshooting Test Failures

### Symptom: Endpoint returns 404 or error

**Cause**: Backend code not updated or server not restarted

**Fix**:
1. Verify you're running the latest version of `main.py`
2. Check the line with `@app.get("/api/cache/usage")` exists around line 445
3. Restart the server: `taskkill /F /IM python.exe` then `python main.py`

### Symptom: Still seeing BigQuery after 30 minutes

**Cause**: Old time-based logic still active

**Fix**:
1. Verify main.py has NEW code: `if sqlite_cache.get_record_count() > 0`
2. Search for `is_cache_valid()` - should NOT be in /api/projects or /api/summary logic
3. If old code exists, reapply the March 11-12 changes
4. Restart server

### Symptom: Response still slow (5000+ ms) for cache hits

**Cause**: Cache is empty or BigQuery is slow

**Fix**:
1. Check: `/api/cache/usage` - if record_count is 0, cache is empty
2. Wait 30 seconds for background sync to populate cache
3. Retry the test

---

## Next Steps

Once all tests PASS:

1. ✅ Verify in production dashboard that data is complete
2. ✅ Monitor `/api/cache/status` endpoint over next 24 hours
3. ✅ Verify no missing data reports from users
4. ✅ Check email alerts (should be minimal/none with good sync)

---

**Document Version**: 1.0  
**Created**: March 12, 2026  
**Status**: ✅ Ready for Testing
