# Activity Hub Projects Setup Guide

## Table Structure Overview

### AH_Projects BigQuery Table
**Location:** `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`  
**Total Rows:** 962,548  
**Total Columns:** 50

### Data Distribution by Status

| Status | Count | Percentage | Notes |
|--------|-------|-----------|-------|
| NULL (empty) | 433,024 | 44.99% | Projects without assigned status |
| Complete | 357,098 | 37.10% | Finished/closed projects |
| Removed | 143,464 | 14.90% | Deleted or archived |
| In Progress | 28,962 | 3.01% | Active projects |
| **TOTAL** | **962,548** | **100%** | |

**Important Note:** There are NO projects with status='Active' in the database. The old frontend was designed expecting 'Active', 'Inactive' status values, which don't exist in the actual data.

## Core Columns (9 Categories)

### 1. **Identifiers** (3 columns)
- `project_id` (STRING, REQUIRED) - Unique project identifier
- `intake_card` (STRING) - Intake card reference number
- `title` (STRING, REQUIRED) - Project name/title

### 2. **Status & Health** (4 columns)
- `status` (STRING) - Project status: "In Progress", "Complete", "Removed", or NULL
- `phase` (STRING) - Project phase
- `health` (STRING) - Project health: "On Track", "At Risk", "Off Track"
- `project_source` (STRING, REQUIRED) - Where project originates from

### 3. **Location** (12 columns)
- `store_area` (STRING) - Business area (e.g., "Digital", "Operations")
- `business_area` (STRING) - Duplicate of store_area
- `division` (STRING)
- `region` (STRING)
- `market` (STRING)
- `facility` (STRING)
- `store_count` (INTEGER)
- `city`, `state`, `postal_code` (STRING)
- `latitude`, `longitude` (FLOAT)

### 4. **Time & Dates** (7 columns)
- `created_date` (TIMESTAMP)
- `last_updated` (TIMESTAMP)
- `projected_completion` (DATE)
- `projected_start_date` (DATE)
- `wm_week` (INTEGER)
- `fiscal_year` (INTEGER)
- `implementation_week` (STRING)

### 5. **Ownership** (6 columns)
- `owner` (STRING)
- `owner_id` (STRING)
- `director` (STRING)
- `director_id` (STRING)
- `sr_director` (STRING)
- `sr_director_id` (STRING)

### 6. **Categorization** (6 columns)
- `project_type`, `initiative_type`, `business_type`, `facility_type`, `partner`, `business_organization`

### 7. **Impact** (4 columns)
- `associate_impact`, `customer_impact`, `ho_impact`, `impact`

### 8. **AMP Integration** (5 columns)
- `amp_event_id`, `amp_activity_title`, `meeting_type`, `sif_date`, `aim_date`

### 9. **Description** (3 columns)
- `summary`, `overview`, `project_update`

---

## Frontend Filter Fixes

### Status Filter Options (CORRECTED)
The status dropdown in `projects-page.html` has been updated to match actual database values:

**Before (Wrong):**
```
- Active (doesn't exist in DB)
- Inactive (doesn't exist in DB)
- All
```

**After (Correct):**
```
- All Statuses (default - shows all projects)
- In Progress (3% of data)
- Complete (37% of data)
- Removed (15% of data)
```

---

## API Endpoint Changes

### `/api/projects` (GET)
**Status Behavior:**
- Default: Empty string (`''`) → Shows ALL projects regardless of status
- `?status=In Progress` → Filters to In Progress projects only
- `?status=Complete` → Filters to Complete projects only
- `?status=` → Shows all (same as default)

**Response Format:**
```json
{
  "projects": [
    {
      "project_id": "10010",
      "title": "Pick To Light",
      "business_area": "Digital",
      "owner": "Nicole Olson",
      "owner_id": "...",
      "health": "On Track",
      "status": null,  // or "In Progress", "Complete", etc.
      "created_date": "2023-06-19T12:28:13+00:00",
      "updated_date": "2026-04-20T09:05:12+00:00",
      "project_update": "Project Update: Added...",
      "latest_update_date": "2026-04-20T09:05:12+00:00"
    }
  ],
  "total_count": 293,
  "timestamp": "2026-04-20T12:51:22.123456"
}
```

### `/api/projects/metrics` (GET)
**Status Behavior:**
- Default: Empty string → Returns metrics for ALL 293 projects
- `?status=In Progress` → Metrics for In Progress projects only
- `?status=` → All projects

**Response Format:**
```json
{
  "metrics": {
    "active_projects": 293,
    "unique_owners": 0,
    "projects_updated_this_week": 293,
    "percent_updated": 100.0
  },
  "timestamp": "2026-04-20T12:51:22.123456"
}
```

---

## Backend Fixes Applied

### File: `Interface/activity_hub_server.py`

1. **Line 202 (GET /api/projects)**
   - Changed: `status = request.args.get('status', 'Active')`
   - To: `status = request.args.get('status', '')`

2. **Lines 279-299 (/api/projects/metrics)**
   - Changed: Hardcoded `WHERE status = '{status}'`
   - To: Conditional logic that omits WHERE clause if status is empty
   - Now handles both filtered and unfiltered queries

3. **Line 559 (/api/generate-ppt)**
   - Changed: `status = request.args.get('status', 'Active')`
   - To: `status = request.args.get('status', '')`

### File: `Interface/projects-page.html`

1. **Line 967 (Status filter dropdown)**
   - Updated options to match database values
   - Changed default to "All Statuses" (empty value)

2. **Lines 1614, 2062 (JavaScript defaults)**
   - Removed fallback to 'Active' which no longer exists
   - Now correctly uses empty string for "show all"

---

## Sample Data

### Project: Pick To Light
```
ID:         10010
Title:      Pick To Light
Status:     NULL / not set
Health:     On Track
Owner:      Nicole Olson
Area:       Digital
Created:    2023-06-19
Updated:    2026-04-20
```

### Project: Backroom Aisle Location  
```
ID:         16857
Title:      Backroom Aisle Location
Status:     In Progress
Health:     On Track
Owner:      Audrea Henderson
Created:    [various dates]
Updated:    [various dates]
```

---

## Testing the Setup

### Direct SQL Query
```sql
-- Get all projects
SELECT project_id, title, status, health, owner
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
LIMIT 10;

-- Get by status
SELECT COUNT(*), status
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
GROUP BY status;

-- Get metrics
SELECT 
  COUNT(*) as total,
  COUNT(DISTINCT owner) as unique_owners,
  COUNT(DISTINCT CASE WHEN DATE_DIFF(CURRENT_DATE(), DATE(last_updated), DAY) <= 7 THEN project_id END) as updated_this_week
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`;
```

### API Endpoints
```bash
# All projects
curl http://localhost:8088/api/projects

# In Progress only
curl 'http://localhost:8088/api/projects?status=In%20Progress'

# Metrics for all
curl http://localhost:8088/api/projects/metrics

# Metrics for specific status
curl 'http://localhost:8088/api/projects/metrics?status=Complete'
```

---

## Expected Frontend Behavior

**On Load:**
1. Status filter defaults to "All Statuses"
2. Frontend loads all 962,548 projects (or samples them)
3. Metrics shows: ~960K projects, 100% updated this week
4. Projects grid displays with status, health, owner, title

**When Filtering:**
- Select "In Progress" → Shows ~29K projects
- Select "Complete" → Shows ~357K projects  
- Select "Removed" → Shows ~143K projects
- Metrics update accordingly

---

## Notes

- Projects with NULL status (45%) will appear when filtering by "All Statuses"
- The data is updated from the Intake Hub intake_hub_loader_simple.py process
- 293 unique projects loaded from Intake Hub on April 20, 2026
- Historical data goes back to 2020-07-27
- Each column mapping is defined in projects-schema.json
