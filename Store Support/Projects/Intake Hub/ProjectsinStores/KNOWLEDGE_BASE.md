# 📚 Knowledge Base & Dependency Mapping

## ⚠️ Automation & Recovery (April 2, 2026)

### Scheduled Tasks

| Task Name | Schedule | Purpose |
|-----------|----------|--------|
| `Activity_Hub_ProjectsInStores_AutoStart` | On logon | Starts `start_projects_in_stores_24_7.bat` → backend on port 8001 |

### Bat Files (`Automation/`)
- `start_projects_in_stores_24_7.bat` — Port-kill block + restart loop. Primary crash recovery (5-7 sec downtime)

### Recovery Layers
1. **Bat restart loop** — primary (5-7 sec recovery on crash)
2. **Continuous monitor** (`continuous_monitor.ps1`) — checks all 7 services every 5 min

### ⚠️ NEVER use `Stop-Process -Name python`
This kills ALL Python processes on the machine — all 7 services go down.

**Safe way to restart only Projects in Stores (port 8001):**
```powershell
$p = (netstat -ano | Select-String ":8001.*LISTENING" | ForEach-Object { ($_ -split "\s+")[-1] }) | Select-Object -First 1
if ($p) { taskkill /F /PID $p }
# Bat loop restarts automatically within 5-7 seconds
```

### Adding/Changing This Service
If the port, entry point, or bat file changes, update ALL of:
1. `Automation/start_projects_in_stores_24_7.bat`
2. `Automation/register_tasks_cmd.bat`
3. `continuous_monitor.ps1` services array
4. `MONITOR_AND_REPORT.ps1` services list
5. `Documentation/KNOWLEDGE_HUB.md` Active Services table
6. This file

---

## System Overview

**Projects in Stores Dashboard** is a full-stack web application that displays project inventory across Walmart stores using real-time data from Google BigQuery.

- **Frontend**: Single-page HTML5 app with vanilla JavaScript
- **Backend**: Python FastAPI REST API with SQLite caching
- **Data Source**: Google BigQuery (✅ **VERIFIED CONNECTED**)
- **Environments**: Dev (localhost:8002) & Production (weus42608431466.homeoffice.wal-mart.com:8001)

### ✅ Verified Status (February 17, 2026)
- **BigQuery Project**: `wmt-assetprotection-prod`
- **Dataset**: `Store_Support_Dev`
- **Table**: `IH_Intake_Data`
- **Authentication**: ✅ Working (credentials already configured)
- **Backend Status**: ✅ Running on port 8002
- **API Status**: ✅ All endpoints responding with real data
- **Last Sync**: 2026-02-17T12:10:35+00:00

### 📖 Quick Navigation

For detailed information, see these companion documents:

- **☁️ [GOOGLE_CLOUD_SETUP.md](GOOGLE_CLOUD_SETUP.md)** - Google Cloud configuration, BigQuery access, authentication
- **📊 [DATA_MODEL_REFERENCE.md](DATA_MODEL_REFERENCE.md)** - Data structures, schemas, field mappings, examples
- **🔗 [DEPENDENCY_MAPPING.md](DEPENDENCY_MAPPING.md)** - Code dependencies, packages, versions, relationships
- **💾 [CACHE_FALLBACK_STRATEGY.md](CACHE_FALLBACK_STRATEGY.md)** - Cache data source logic, fallback behavior, troubleshooting (March 12, 2026 update)

---

## 0. CRITICAL: Cache Fallback Strategy (March 12, 2026)

### ⚠️ Fix Summary

**Issue Fixed**: Dashboard showing incomplete data after cache ages beyond 30 minutes, even though cache had good data.

**Root Cause**: Time-based cache expiration (30 min) conflicted with smart validation protection. When sync failed validation, cache wasn't updated. Cache aged past 30 min → system abandoned good cached data → fallback to BigQuery → received incomplete/stale data.

**Solution Implemented** (March 11-12, 2026):
1. Changed from TIME-BASED to DATA-BASED cache fallback logic
2. Added `/api/cache/usage` endpoint for visibility
3. Enhanced documentation with detailed strategy

### 🔄 How Cache Fallback Works NOW (Corrected)

**Cache First Strategy:**
```
API Request → Check: Does cache have data?
    ├─ YES → Use SQLite Cache (milliseconds)
    └─ NO → Fall back to BigQuery (seconds)
```

**Key Points:**
- ✅ Cache is used regardless of age (smart validation prevents bad data)
- ✅ Only falls back to BigQuery if cache is completely empty
- ✅ Sync validation protects cache from contamination (0-records retries, variance checks)
- ✅ Dashboard visibility via `/api/cache/usage` endpoint

**Why This Works:**
- Smart validation (March 5) prevents bad data from ever entering cache
- Age doesn't matter if data quality is guaranteed
- Graceful degradation: If sync fails, keep good old data rather than switch to potentially incomplete BigQuery data
- Last valid data persists until new valid data arrives

### 📊 Status Endpoint: `/api/cache/usage`

Returns which data source is active and why:

```json
{
  "data_source": "SQLite Cache (LOCAL)",
  "reason": "Cache has valid data",
  "cache_populated": true,
  "record_count": 1350000,
  "last_sync_time": "2026-03-12T08:45:30.123456",
  "cache_age_minutes": 45,
  "cache_age_seconds": 2700,
  "cache_location": "backend/cache.db",
  "notes": [
    "✓ Fallback logic uses DATA presence, not age",
    "✓ Smart validation prevents bad data in cache",
    "Cache created 45 minutes ago"
  ]
}
```

**Use This To:**
- Verify you're using cache (not BigQuery)
- Check why dashboard shows specific data source
- Monitor cache age (non-critical, validation protects quality)
- Troubleshoot data freshness questions

---

## 1. Component Architecture

### 1.1 Frontend Components

| Component | File | Purpose | Dependencies |
|-----------|------|---------|--------------|
| **Dashboard UI** | `frontend/index.html` | Main application interface | None (fetch API) |
| **Static Assets** | `frontend/spark-logo.png` | Branding | Served by FastAPI |
| **Summary Stats** | HTML/JS in index.html | Display project counts | `/api/summary` |
| **Filter System** | HTML/JS in index.html | Multi-select filters | `/api/filters` |
| **Quick Review** | HTML/JS in index.html | Project card preview | Project data |
| **Project List** | HTML/JS in index.html | Hierarchical view | Project data |
| **Sparky AI Chat** | HTML/JS in index.html | AI assistant | `/api/ai/query` |
| **Feedback Modal** | HTML/JS in index.html | User feedback form | `/api/feedback` |

### 1.2 Backend Components

| Component | File | Purpose | Dependencies |
|-----------|------|---------|--------------|
| **FastAPI App** | `backend/main.py` | HTTP REST server | FastAPI, Uvicorn |
| **Database Service** | `backend/database.py` | BigQuery queries | google-cloud-bigquery |
| **SQLite Cache** | `backend/sqlite_cache.py` | Local data cache | SQLite3 |
| **AI Agent** | `backend/ai_agent.py` | Query processing | Anthropic Claude API |
| **Email Reports** | `backend/report_runner.py` | Email scheduling | SMTP, APScheduler |
| **Models** | `backend/models.py` | Pydantic schemas | Pydantic |

### 1.3 Infrastructure Services

| Service | Type | Purpose | Status | Endpoint |
|---------|------|---------|--------|----------|
| **Google BigQuery** | Cloud Database | Source of truth for all project data | ✅ **VERIFIED CONNECTED** | `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data` |
| **SQLite Local DB** | File-based Cache | Speeds up API responses (100ms vs 10s) | ✅ Working | `backend/cache.db` |
| **Uvicorn Server** | App Server | Serves FastAPI | ✅ Running | localhost:8002 (dev) / weus42608431466.homeoffice.wal-mart.com:8001 (prod) |

---

## 2. Dependency Graph

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Browser)                       │
│                      frontend/index.html                        │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                 ┌────────────┴────────────┐
                 │                         │
          ┌──────▼─────────┐      ┌──────▼─────────┐
          │ API Endpoints  │      │  Static Files  │
          └──────┬─────────┘      └──────┬─────────┘
                 │                         │
    ┌────────────┼─────────────────────────┼──────────────┐
    │            │                         │              │
    ▼            ▼                         ▼              ▼
┌────────┐   ┌──────────┐   ┌──────────────┐   ┌─────────────────┐
│/api/*  │   │/health   │   │spark-logo    │   │index.html.prod  │
│routes  │   │check     │   │favicon.ico   │   │simple.html.orig │
└────┬───┘   └────┬─────┘   └──────────────┘   └─────────────────┘
     │            │
     └────────┬───┘
              │
    ┌─────────▼───────────┐
    │  backend/main.py    │
    │  (FastAPI Router)   │
    └─────────┬───────────┘
              │
    ┌─────────┴──────────┬──────────────┬─────────────┐
    │                    │              │             │
    ▼                    ▼              ▼             ▼
┌─────────────┐  ┌──────────────┐  ┌──────────┐  ┌──────────┐
│ database.py │  │sqlite_cache  │  │ai_agent  │  │models.py │
│(BigQuery)   │  │.py (Cache)   │  │.py (AI)  │  │(schemas) │
└──────┬──────┘  └──────┬───────┘  └────┬─────┘  └──────────┘
       │                │               │
       │                │         ┌─────▼──────┐
       │                │         │ Anthropic  │
       │                │         │ Claude API │
       │                │         └────────────┘
       │          ┌─────▼────────┐
       │          │ SQLite DB    │
       │          │ cache.db     │
       │          └──────────────┘
       │
       └─────────────┬──────────────┐
                     │              │
                ┌────▼───────┐  ┌──▼─────────┐
                │ BigQuery   │  │ BigQuery   │
                │ IH_Dataset │  │ Auth Token │
                │ (Tables)   │  │ (Service   │
                └────────────┘  │  Account)  │
                                └────────────┘
```

---

## 3. Data Dependencies

### 3.1 Frontend → Backend

| Frontend Action | API Call | Response Fields | Cache Time |
|-----------------|----------|-----------------|-----------|
| Page Load | GET `/api/summary` | `total_active_projects`, `total_stores`, `realty_projects`, `last_updated` | 1 hour |
| Initial Data Load | GET `/api/projects?limit=50000` | Project array with all fields | SQLite cache |
| Filter Selection | GET `/api/filters` | Arrays: divisions, regions, markets, phases, sources | 1 hour |
| Search/Filter | GET `/api/projects?title=X&source=Y...` | Filtered project rows | None (dynamic) |
| AI Query | POST `/api/ai/query` | `answer`, `data` (filter suggestions) | None |
| Feedback | POST `/api/feedback` | `{success: true}` | None |

### 3.2 Backend → External Services

| Service | Call Type | Purpose | Auth | Rate Limit |
|---------|-----------|---------|------|-----------|
| Google BigQuery | SQL Query | Fetch/filter projects | Service account JSON | 1000 req/min |
| SQLite Local | File I/O | Cache/retrieve data | File system access | N/A |
| Anthropic Claude | REST API | AI query processing | API Key (env var) | Per account |
| SMTP (Email) | SMTP connection | Send report emails | Credentials in .env | None |

---

## 4. Configuration & Environment Variables

### 4.1 Development Setup (localhost:8002)

```bash
ENVIRONMENT=dev
API_BASE=window.location.origin  # http://localhost:8002
RELOAD=true                       # Hot reload enabled
PORT=8002
FRONTEND_FILE=index.html          # Latest version
```

**Startup**: `START_BACKEND.bat` (with --reload flag)

### 4.2 Production Setup (weus42608431466.homeoffice.wal-mart.com:8001)

```bash
ENVIRONMENT=prod
API_BASE=window.location.origin   # http://weus42608431466.homeoffice.wal-mart.com:8001
RELOAD=false                      # No hot reload
PORT=8001
FRONTEND_FILE=index.html.production  # Stable version
```

**Startup**: `backend/run_server.ps1` (no --reload flag)

### 4.3 Required Environment Variables

```bash
# Google BigQuery
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
GCP_PROJECT_ID=wmt-assetprotection-prod
BQ_DATASET=Store_Support_Dev
BQ_TABLE=IH_Intake_Data

# Anthropic AI
ANTHROPIC_API_KEY=sk-...

# Email Reporting (optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=...
EMAIL_PASSWORD=...
```

---

## 5. Database Schema Reference

### 5.1 BigQuery Table: `IH_Intake_Data`

**Location**: `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`

**Key Columns**:
- `Intake_Card` - Project ID (string, nullable)
- `Facility` - Store number (integer)
- `Project_Title` - Initiative name (string)
- `Project_Source` - 'Operations' or 'Realty' (string)
- `Division`, `Region`, `Market` - Location hierarchy (strings)
- `Phase` - Project phase (string)
- `WM_Week`, `FY` - Time dimensions (string)
- `Status` - 'Active', 'Completed', etc. (string)
- `Owner`, `Partner` - Contact info (string)
- `Last_Updated` - BigQuery column timestamp (datetime)

**Record Count**: ~1,375,544 active records

**Query Optimization**: Status='Active' indexed, queries typically < 5 seconds

### 5.2 SQLite Cache: `cache.db`

**Location**: `backend/cache.db`

**Tables**:
- **projects** - Denormalized project data (20+ columns)
- **sync_metadata** - Last sync timestamp and cache status

**Update Frequency**: Full sync on backend startup (5-10 seconds)

**Purpose**: Serve 50,000 records in <100ms vs 10+ seconds from BigQuery

---

## 6. API Contract

### 6.1 Core Endpoints

#### GET `/api/summary`
Returns aggregate stats without detailed rows.

**Response**:
```json
{
  "total_active_projects": 1181,
  "total_stores": 1181,
  "intake_hub_projects": 0,
  "realty_projects": 1181,
  "last_updated": "2026-02-17T14:36:42.123456"
}
```

#### GET `/api/projects?title=X&project_source=Y&limit=1000`
Returns filtered project rows.

**Query Params**:
- `title` - Substring search in project title
- `project_source` - 'Operations' or 'Realty'
- `division`, `region`, `market`, `store`, `phase` - Exact match filters
- `limit` - Max rows (default: 1000, max: 50000)

**Response**: Array of project objects with all fields

#### GET `/api/filters`
Returns available filter values.

**Response**:
```json
{
  "divisions": ["EAST", "SOUTH", ...],
  "regions": [Array],
  "markets": [Array],
  "stores": [Array],
  "phases": ["Pending", "POC/POT", ...],
  "project_sources": ["Operations", "Realty"]
}
```

#### POST `/api/ai/query`
Processes natural language query through Claude AI.

**Request Body**:
```json
{
  "query": "Show me realty projects in the northeast",
  "context": {
    "total_projects": 1181,
    "all_projects": [...],
    "filters": {...}
  }
}
```

**Response**:
```json
{
  "answer": "Found 45 realty projects in northeastern region",
  "data": {
    "region_filter": "NORTHEAST",
    "project_source": "Realty",
    "suggested_filter": "..."
  }
}
```

---

## 7. Critical Dependencies

### 7.1 Python Packages (backend/requirements.txt)

```
fastapi==0.109.0           # REST framework
uvicorn==0.27.0            # ASGI server
google-cloud-bigquery      # BigQuery client
anthropic                  # Claude AI API
pydantic==2.5.0            # Request validation
python-dotenv              # Env config
apscheduler                # Background tasks
```

### 7.2 Browser Requirements (Frontend)

- ES6+ JavaScript support
- Fetch API
- LocalStorage
- CSS Grid & Flexbox

**Supported Browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

---

## 8. Known Issues & Constraints

| Issue | Impact | Workaround | Status |
|-------|--------|-----------|--------|
| Duplicate rows in results | Stats count inflated | DISTINCT in SQLite query | ✅ Fixed |
| Missing favicon.ico | Browser 404 error | Served via static mount | ✅ Fixed |
| Spark logo not loading | UI broken | Static files route added | ✅ Fixed |
| Store count = Project count on filtered Realty | Stats misleading | Count by title not ID | ✅ Fixed |
| BigQuery queries > 10s | UI freezes | SQLite cache layer | ✅ Implemented |
| /api/filters returns 500 error | Dashboard filters unavailable | Removed @async_wrap decorator | ✅ Fixed (Feb 18) |

---

### 9. Deployment Checklist

✅ **VERIFIED & COMPLETE as of February 18, 2026:**

- [x] BigQuery credentials configured (✅ **WORKING** - gcloud auth application-default login)
- [x] SQLite cache syncs on startup (✅ Backend connected)
- [x] Dev server runs on localhost:8002 with --reload (✅ Running)
- [x] Production server runs on 0.0.0.0:8001 (✅ Running & accessible)
- [x] Frontend routing serves correct HTML per environment (✅ Environment-based)
- [x] Static files mount enabled (logos, favicons) (✅ spark-logo.png serving)
- [x] API responses have CORS headers configured (✅ All endpoints working)
- [x] Error handling returns proper HTTP status codes (✅ Tested)
- [x] Summary stats count unique titles, not rows (✅ Fixed & verified)
- [x] /api/filters endpoint functional (✅ Returns all 17 filter types)
- [x] **API calls use relative URLs** (✅ **WORKS FROM ANY SYSTEM** - Feb 18, 2026)
- [x] Windows Firewall rules added for ports 8001 & 8002 (✅ Inbound traffic allowed)
- [ ] Email reporting scheduled (if enabled) (Optional feature)

---

## 10. Common Debugging Steps

### Issue: Data not loading
1. Check `/api/health` endpoint returns 200
2. Verify BigQuery credentials: `echo $GOOGLE_APPLICATION_CREDENTIALS`
3. Check SQLite cache: `sqlite3 backend/cache.db "SELECT COUNT(*) FROM projects;"`
4. Review backend logs for SQL errors

### Issue: Filters not applying
1. Open browser DevTools (F12) → Console
2. Look for "[Stats]" or "[Filter]" log messages
3. Check Network tab for API requests/responses
4. Verify selectedFilters object contains values

### Issue: Slow response times
1. Check if using SQLite cache vs BigQuery: Look for "[API] Using..." log
2. If BigQuery, run `SELECT COUNT(*) FROM ... WHERE Status='Active'` directly
3. Consider increasing SQLite cache refresh interval
4. Profile bottleneck with `python -m cProfile backend/main.py`

---

## 11. Testing & QA

### Manual Test Scenarios

```gherkin
Scenario: Filter by source and search
  Given user opens dashboard
  When user selects "Realty" from All Sources
  And user types "store" in search
  Then stats show 2 Realty Projects / 1181 Stores
  And Quick Review shows 2 project cards
  And Project List shows hierarchical view with 1181 rows
```

### Performance Benchmarks

| Operation | Target | Current | Status |
|-----------|--------|---------|--------|
| Page load (API) | < 2s | 1.2s | ✅ Pass |
| Filter apply | < 1s | 0.3s | ✅ Pass |
| Search (50K rows) | < 500ms | 400ms | ✅ Pass |
| AI query | < 5s | 2.1s | ✅ Pass |

---

## 12. Maintenance & Updates

### Code Update Workflow

1. **Dev Testing**: Edit `frontend/index.html`, test on localhost:8002
2. **Git Commit**: Commit changes to dev branch
3. **Production Deploy**: Merge to main, copy to `index.html.production`
4. **Restart**: Restart production server (port 8001)
5. **Verify**: Test on http://weus42608431466.homeoffice.wal-mart.com:8001/

### Cache Invalidation

- **Manual**: Delete `backend/cache.db`, restart backend
- **Automatic**: Cache refreshes on backend startup
- **TTL**: 1-hour max age before next query

### BigQuery Schema Changes

If BigQuery schema changes:
1. Update column mapping in `backend/database.py`
2. Update `backend/sqlite_cache.py` sync query
3. Clear cache.db
4. Restart backend
5. Test on dev first

---

**Document Version**: 2.2  
**Last Updated**: February 18, 2026 15:45 UTC  
**Status**: ✅ **FULLY FUNCTIONAL - ALL ENDPOINTS WORKING**
**Google Cloud Connection**: ✅ **ACTIVE & WORKING**
**Deployment Status**: ✅ **PRODUCTION READY**
  - Prod URL: http://weus42608431466.homeoffice.wal-mart.com:8001/
  - Dev URL: http://localhost:8002/ (local only)
  - **Remote Access**: Works from ANY system on the network
  - **Why**: All API calls use relative URLs (`/api/...`), so access works via hostname, IP, or any network route
  - Keep-Awake Script: Active (C:\Users\krush\Documents\keep-awake.ps1)

---

## Remote Access & Multi-System Support

### How It Works (Feb 18, 2026 Update)

✅ **The dashboard NOW works from any system** - no special configuration needed:

1. **Original Issue**: Using `window.location.origin` caused problems when users accessed from different systems
   - User A accessing via hostname → Different origin than User B accessing via IP
   - Result: API calls would fail with `net::ERR_CONNECTION_REFUSED`

2. **Solution Implemented**: All API calls now use **relative URLs** (e.g., `/api/projects` instead of `http://host:port/api/projects`)
   - Frontend and backend served from same server
   - Relative URLs work regardless of hostname, IP, or port
   - No hostname resolution issues
   - Works across different networks

### Access from Remote Systems

**Any user on any system can access:**
```
http://weus42608431466.homeoffice.wal-mart.com:8001/
```

**OR via IP address** (if hostname doesn't resolve):
```
http://<server-ip>:8001/
```

**Requirements:**
- Server machine has Windows Firewall rules for ports 8001 & 8002 ✅
- Both dev and prod backends running ✅
- No VPN or special network config needed (standard network access)
**Verified By**: System Test - All API endpoints tested (summary, projects, filters)
**Maintainer**: Development Team
