# ELM Banner Codes Integration Guide

**Created**: April 16, 2026  
**Purpose**: Integrate WM Stores & Facilities data (ELM) as authoritative source for Banner Codes  
**Status**: ✅ Ready for Implementation

---

## Overview

This guide explains how to:
1. Query ELM (Enterprise Location Management) datasource for complete banner code definitions
2. Update the Aligned dashboard with real banner codes and descriptions
3. Maintain current data with scheduled updates

---

## Quick Start

### Option 1: Load Banner Codes from ELM (Recommended)

```powershell
# Navigate to project directory
cd "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend"

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run query to fetch banner codes from ELM
python query_elm_banner_codes.py --divisions 1 10 --output all --show

# Output files generated:
# - banner_codes_YYYYMMDD_HHMMSS.json   (JSON format)
# - banner_codes_YYYYMMDD_HHMMSS.csv    (CSV format)
# - banner_codes_YYYYMMDD_HHMMSS.js     (JavaScript constant)
```

### Option 2: Use Dashboard API

Once backend is running, banner codes load automatically:

```
GET /api/banner-codes
```

Response:
```json
{
  "status": "ok",
  "total": 7,
  "banner_codes": [
    {"code": "WAL", "desc": "Walmart Supercenter"},
    {"code": "NHM", "desc": "Neighborhood Market"},
    {"code": "SAM", "desc": "Sam's Club"},
    {"code": "HTO", "desc": "Home Town"},
    {"code": "DVT", "desc": "Discount"},
    {"code": "O3", "desc": "Aligned"},
    {"code": "RX", "desc": "Pharmacy"}
  ],
  "dropdown_options": [
    "WAL - Walmart Supercenter",
    "NHM - Neighborhood Market",
    ...
  ]
}
```

---

## Components

### 1. Python Script: `query_elm_banner_codes.py`

**Location**: `backend/query_elm_banner_codes.py`

**Purpose**: Query ELM datasource and extract banner codes

**Data Sources**:
- **Table**: `wmt-loc-cat-prod.catalog_location_views.division_view`
- **Divisions**: 
  - Division 1 = WM US Stores
  - Division 10 = Health & Wellness (H&W)

**Usage**:
```powershell
# Fetch all divisions, output all formats
python query_elm_banner_codes.py

# Fetch specific divisions only
python query_elm_banner_codes.py --divisions 1

# Output specific format
python query_elm_banner_codes.py --output json
python query_elm_banner_codes.py --output csv
python query_elm_banner_codes.py --output js

# Show results in console
python query_elm_banner_codes.py --show
```

**Output Formats**:

**JSON (`banner_codes_YYYYMMDD_HHMMSS.json`):**
```json
{
  "generated_at": "2026-04-16T10:30:00.123456",
  "total_unique_banners": 7,
  "banners": [
    {
      "banner_code": "O3",
      "banner_desc": "Aligned",
      "store_count": 450,
      "division": 1
    }
  ],
  "dropdown_options": ["O3 - Aligned", ...]
}
```

**CSV (`banner_codes_YYYYMMDD_HHMMSS.csv`):**
```
banner_code,banner_desc,store_count,division,dropdown_format
O3,Aligned,450,1,O3 - Aligned
WAL,Walmart Supercenter,3200,1,WAL - Walmart Supercenter
...
```

**JavaScript (`banner_codes_YYYYMMDD_HHMMSS.js`):**
```javascript
const BANNER_CODE_OPTIONS = [
  "O3 - Aligned",
  "RX - Pharmacy",
  "SAM - Sam's Club",
  "WAL - Walmart Supercenter",
  ...
];
```

### 2. Backend Module: `banner_codes_manager.py`

**Location**: `backend/banner_codes_manager.py`

**Purpose**: Manage banner codes data locally

**Features**:
- Load/save banner codes from cache
- Format for dropdown display
- Update from ELM datasource
- Provide API responses

**Usage in Backend**:
```python
from banner_codes_manager import BannerCodesManager, get_banner_codes_api

# Initialize manager
manager = BannerCodesManager()

# Get all banner codes
codes = manager.get_banner_codes()

# Get dropdown format
options = manager.get_dropdown_options()
# Returns: ["O3 - Aligned", "WAL - Walmart Supercenter", ...]

# Update from ELM data
elm_data = [
    {"banner_code": "O3", "banner_desc": "Aligned"},
    {"banner_code": "WAL", "banner_desc": "Walmart Supercenter"}
]
updated = manager.update_banner_codes_from_elm(elm_data)
print(f"Updated {updated} banners")

# Save to cache
manager.save_banner_codes(codes)

# Get API response
api_response = get_banner_codes_api()
```

### 3. Backend API Endpoint: `/api/banner-codes`

**Location**: `backend/main.py` (lines ~2050+)

**Purpose**: Serve banner codes to frontend

**HTTP Method**: GET

**Response**:
```json
{
  "status": "ok",
  "banner_codes": [...],
  "dropdown_options": [...],
  "total": 7,
  "generated_at": "2026-04-16T10:30:00.123456"
}
```

**Frontend Integration**:
```javascript
// Fetch banner codes from API
async function loadBannerCodesAsync() {
    const response = await fetch('/api/banner-codes');
    const data = await response.json();
    
    if (data.dropdown_options) {
        populateDropdown('banner-codes-dropdown', data.dropdown_options);
    }
}

// Call when opening assign team modal
loadBannerCodesAsync();
```

### 4. Frontend Update: `frontend/index.html`

**Changes Made**:
- Line ~1819: Changed from hardcoded list to `loadBannerCodesAsync()`
- Added `loadBannerCodesAsync()` function to fetch from API
- Added `loadBannerCodesDefault()` function as fallback

**Behavior**:
1. Opens assign team modal
2. Calls `loadBannerCodesAsync()` to fetch from `/api/banner-codes`
3. If API succeeds: Populates with banner codes from ELM
4. If API fails: Falls back to default banner codes

### 5. Knowledge Base: `KNOWLEDGE_BASE.md`

**Updates**:
- Added "ELM Datasource - WM Stores & Facilities" section
- Documented division structure
- Included query templates for both divisions
- Listed banner codes reference table
- Explained usage in dashboard

---

## Data Flow

```
┌─────────────────────────────────────────────────────────┐
│ ELM Datasource (catalog_location_views.division_view)   │
│ Division 1: WM US Stores                                │
│ Division 10: Health & Wellness                          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ query_elm_banner_codes.py (Python Script)               │
│ - Queries BigQuery                                      │
│ - Extracts BANNER_CODE & BANNER_DESC                    │
│ - Generates JSON/CSV/JS output files                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ├─ banner_codes_YYYYMMDD.json
                     ├─ banner_codes_YYYYMMDD.csv
                     └─ banner_codes_YYYYMMDD.js
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ banner_codes_manager.py (Backend Module)                │
│ - Loads banner codes cache                              │
│ - Provides formatted options                            │
│ - API response formatting                               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ main.py - GET /api/banner-codes (FastAPI Endpoint)      │
│ Returns formatted dropdown options                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Frontend (index.html)                                   │
│ - loadBannerCodesAsync() function                       │
│ - Fetches from /api/banner-codes                        │
│ - Populates dropdown: "O3 - Aligned", etc.              │
└─────────────────────────────────────────────────────────┘
```

---

## Implementation Steps

### Step 1: Test Script

```powershell
cd "Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend"
python query_elm_banner_codes.py --show
```

**Expected Output**:
- Connects to BigQuery
- Queries Division 1 and 10 from ELM
- Displays 6-8 banner codes
- Generates output files

### Step 2: Verify API Endpoint

```powershell
# Start backend server
cd Interface
python activity_hub_server.py

# In another terminal, test endpoint
curl http://localhost:8088/api/banner-codes | jq
```

**Expected Response**:
- Status: "ok"
- 7+ banner codes
- Dropdown options with format "{CODE} - {DESC}"

### Step 3: Test Dashboard

1. Open browser: `http://localhost:8088/activity-hub/admin` (or `/aligned`)
2. Navigate to assign team tab
3. Click "Assign Team" button
4. Check banner codes dropdown - should show:
   - WAL - Walmart Supercenter
   - NHM - Neighborhood Market
   - SAM - Sam's Club
   - HTO - Home Town
   - DVT - Discount
   - **O3 - Aligned** ✅ (newly added)
   - RX - Pharmacy

### Step 4: Schedule Daily Updates

Create PowerShell scheduled task to run query daily:

```powershell
# Create task to run daily at 2:00 AM
$trigger = New-ScheduledTaskTrigger -Daily -At "2:00 AM"

$action = New-ScheduledTaskAction `
  -Execute "python.exe" `
  -Argument "query_elm_banner_codes.py --output json --divisions 1 10" `
  -WorkingDirectory "c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend"

Register-ScheduledTask `
  -TaskName "Aligned-ELM-BannerCodes-Sync" `
  -Trigger $trigger `
  -Action $action `
  -RunLevel Highest `
  -Description "Daily sync of banner codes from ELM datasource"
```

---

## Troubleshooting

### Problem: "403 Access Denied" when querying ELM

**Solution**: 
- Verify BigQuery credentials are configured
- Check VPN connection
- Ensure service account has access to `wmt-loc-cat-prod` project

### Problem: Script returns 0 banners

**Solution**:
- Check SQL WHERE conditions
- Verify `bu_status_desc != 'CLOSED'`
- Confirm date filter: `Date(new_bu_start_date) <= date_add(current_date(), INTERVAL 90 DAY)`

### Problem: Frontend still shows old banner codes

**Solution**:
- Clear browser cache
- Restart backend server
- Verify `/api/banner-codes` endpoint returns new codes

### Problem: "O3 - Aligned" not in dropdown

**Solution**:
1. Run `query_elm_banner_codes.py --show` to verify O3 is in ELM
2. Check `banner_codes_cache.json` for O3 entry
3. Verify `/api/banner-codes` includes O3
4. Clear frontend cache and refresh page

---

## Files Created/Modified

### New Files
- ✅ `backend/query_elm_banner_codes.py` - ELM query script
- ✅ `backend/banner_codes_manager.py` - Banner code manager module
- ✅ `KNOWLEDGE_BASE.md` (updated) - ELM datasource documentation
- ✅ `ELM_BANNER_CODES_INTEGRATION.md` - This file

### Modified Files
- ✅ `backend/main.py` - Added `/api/banner-codes` endpoint
- ✅ `frontend/index.html` - Updated to load codes from API

---

## Next Steps

1. Execute `query_elm_banner_codes.py` to test ELM connection
2. Verify banner codes appear in `/api/banner-codes` endpoint
3. Test dashboard dropdown population
4. Schedule daily updates to keep data current
5. Document in team wiki/confluence

---

## References

- **ELM Query**: `wmt-loc-cat-prod.catalog_location_views.division_view`
- **Output Tables**: 
  - `wmt-assetprotection-prod.Store_Support_Dev.Store Cur Div 1 Data`
  - `wmt-assetprotection-prod.Store_Support_Dev.Store Cur Div 10 Data`
- **Dashboard**: `Teaming/dashboard/frontend/index.html` - Banner codes dropdown
- **Backend**: `Teaming/dashboard/backend/main.py` - `/api/banner-codes` endpoint
