# 📊 Data Model & Schema Reference

## 1. Business Data Model

### 1.1 Core Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                     PROJECT TYPE (Source)                       │
│                  Distinguishes data origin                       │
│         ┌────────────────────────┬────────────────────────┐      │
│         │                        │                        │      │
│         ▼                        ▼                        ▼      │
│    Operations              Realty              [Future Types]   │
│    (Source: Internal)      (Source: CBRE)                       │
│         │                        │                              │
│         │                        │                              │
│         ▼                        ▼                              │
│  ┌─────────────────┐       ┌──────────────────┐               │
│  │   INITIATIVE    │       │   INITIATIVE     │               │
│  │ (Specific Title)│       │ (Specific Title) │               │
│  │                 │       │                  │               │
│  │ Example:        │       │ Example:         │               │
│  │ Quick Review v2 │       │ EXP - Speaker    │               │
│  │                 │       │ Upgrade          │               │
│  └────────┬────────┘       └────────┬─────────┘               │
│           │                         │                          │
│           │  (Multiple stores)      │  (Multiple weeks)        │
│           │                         │                          │
│           ▼                         ▼                          │
│  ┌──────────────────────────────────────────┐                │
│  │  STORE ASSIGNMENT (Individual Row)       │                │
│  │                                          │                │
│  │ Fields:                                  │                │
│  │  • Facility (Store #)                    │                │
│  │  • WM_Week (Week #)                      │                │
│  │  • FY (Fiscal Year)                      │                │
│  │  • Status (Active/Completed/...)         │                │
│  │  • Owner / Partner                       │                │
│  │                                          │                │
│  │ Example Row:                             │                │
│  │  {Initiative: EXP-Speaker Upgrade,       │                │
│  │   Store: 1234, Week: FY26-WK01, ...}     │                │
│  └──────────────────────────────────────────┘                │
│           ▲                    ▲                              │
│           │                    │                              │
│      1 initiative         1,181 unique stores                 │
│      → 1,181 rows        → 2 initiatives active               │
│                                                               │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Stats Calculation (CRITICAL)

**User Clarification**: "EXP and Remodel are examples of a Realty Project..."

```
CORRECT (After Fix):
├─ Project = unique TITLE/INITIATIVE
│   └─ Count by: new Set(projects.map(p => p.title))
│   └─ Result: 2 projects (EXP-Speaker Upgrade, Remodel-Speaker Upgrade)
│
├─ Stores = unique FACILITY
│   └─ Count by: new Set(projects.map(p => p.store))
│   └─ Result: 1,181 unique store numbers
│
└─ When filtered to Realty:
    ├─ Realty Projects: 2 (count by unique REALTY titles)
    ├─ Operations Projects: 0
    └─ Total Projects: 2

INCORRECT (Before Fix):
├─ Project = unique PROJECT_ID / row
│   └─ Result: 1,181 (wrong - this is store count)
│
├─ Stores = count of rows
│   └─ Result: 1,181 (coincidentally correct but for wrong reason)
│
└─ Stats = Stores (mismatch between stats and Quick Review)
```

---

## 2. Frontend Data Structures

### 2.1 Project Object (Individual Record)

```javascript
{
  // BigQuery Source Fields
  intake_card: "INT-2026-001",           // STRING | Project ID from source
  project_id: "id_12345",                // STRING | Internal reference (deprecated usage)
  title: "EXP - Store Speaker Upgrade",  // STRING | Initiative name (CRITICAL for stats)
  project_source: "Realty",              // STRING | "Operations" | "Realty"
  
  // Location Hierarchy
  division: "EAST",                      // STRING | Division code
  region: "NE",                          // STRING | Region code
  market: "BOSTON",                      // STRING | Market code
  store: "1234",                         // STRING | Facility number (CRITICAL for store count)
  facility: 1234,                        // INTEGER | Same as store
  
  // Time Dimensions
  wm_week: "FY26-WK01",                  // STRING | Walmart week identifier
  fy: "FY26",                            // STRING | Fiscal year
  
  // Project Status & Contacts
  status: "Active",                      // STRING | "Active" | "Completed" | "Pending"
  phase: "Execution",                    // STRING | Project phase
  owner: "john.doe@walmart.com",         // STRING | Person responsible
  partner: "CBRE",                       // STRING | External partner (nullable)
  
  // Administrative
  last_updated: "2026-02-17T14:36:42Z",  // ISO 8601 timestamp
}
```

### 2.2 Selected Filters Object

```javascript
selectedFilters = {
  divisions: ["EAST", "SOUTH"],         // Multi-select (AND between types, OR within)
  regions: ["NE", "SE"],
  markets: [],                          // Empty = all included
  stores: [],
  project_sources: ["Realty"],          // Also called "All Sources" in UI
  phases: ["Execution", "Pending"],
  owners: [],
  partners: ["CBRE"],
  
  // Special: Search text
  searchText: "store"                    // Substring match on project title
}
```

### 2.3 Filter Response Object (from `/api/filters`)

```javascript
{
  divisions: [
    "EAST", "MIDWEST", "SOUTH", "SOUTHWEST", "WEST", "NORTHEAST"
  ],
  regions: [
    "NE", "SE", "MW", "SW", "WEST", ...
  ],
  markets: [
    "BOSTON", "NEW YORK", "ATLANTA", ...
  ],
  stores: [
    "1", "2", "3", "4", "5", ..., "4588"  // All 4,588 unique stores
  ],
  phases: [
    "Pending", "POC/POT", "Execution", "Completed", "On Hold"
  ],
  project_sources: [
    "Operations", "Realty"
  ],
  owners: [
    "john.doe@walmart.com", "jane.smith@walmart.com", ...
  ],
  partners: [
    "CBRE", "Jones Lang LaSalle", "Cushman & Wakefield", ...
  ]
}
```

### 2.4 Summary Stats Object

```javascript
{
  total_active_projects: 2,        // COUNT(DISTINCT title) where status='Active'
  total_stores: 1181,              // COUNT(DISTINCT store) where status='Active'
  intake_hub_projects: 0,          // COUNT(DISTINCT title) where source='Operations'
  realty_projects: 2,              // COUNT(DISTINCT title) where source='Realty'
  last_updated: "2026-02-17T14:36:42"  // Timestamp from BigQuery sync
}
```

### 2.5 Quick Review Card

```javascript
// Represents single initiative/project in card format
{
  title: "EXP - Store Speaker Upgrade",        // Project name
  store_count: 1181,                           // Unique stores affected
  initiative_source: "Realty",                 // Project type
  preview_stores: ["1234", "5678", "9012"]     // Sample store numbers
}
```

---

## 3. Backend Data Structures

### 3.1 Pydantic Models (from `models.py`)

```python
class ProjectSchema(BaseModel):
    """Individual project record"""
    id: Optional[int] = None
    intake_card: Optional[str] = None
    title: str                         # CRITICAL FIELD
    project_source: Literal["Operations", "Realty"]
    facility: int
    store: str
    division: Optional[str] = None
    region: Optional[str] = None
    market: Optional[str] = None
    wm_week: Optional[str] = None
    fy: Optional[str] = None
    status: str
    phase: Optional[str] = None
    owner: Optional[str] = None
    partner: Optional[str] = None
    last_updated: Optional[datetime] = None

    class Config:
        from_attributes = True

class FilterSchema(BaseModel):
    """Available filter values"""
    divisions: List[str]
    regions: List[str]
    markets: List[str]
    stores: List[str]
    phases: List[str]
    project_sources: List[str]
    owners: List[str]
    partners: List[str]

class SummarySchema(BaseModel):
    """Aggregate statistics"""
    total_active_projects: int
    total_stores: int
    intake_hub_projects: int
    realty_projects: int
    last_updated: datetime
```

### 3.2 API Response Envelope

```python
class APIResponse(BaseModel):
    """Standard response wrapper"""
    success: bool
    data: Union[
        List[ProjectSchema],
        SummarySchema,
        FilterSchema,
        Dict[str, Any]
    ]
    error: Optional[str] = None
    timestamp: datetime = datetime.now()
```

---

## 4. Database Schema

### 4.1 BigQuery Source Table

**Table**: `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`

```sql
-- Schema (from exploration)
Column Name          | Type      | Nullable | Description
---------------------|-----------|----------|------------------------------------
Intake_Card          | STRING    | YES      | Project identifier
Facility             | INTEGER   | YES      | Store/facility number
Project_Title        | STRING    | NO       | Initiative name (CRITICAL FIELD)
Project_Source       | STRING    | YES      | 'Operations' or 'Realty'
Division             | STRING    | YES      | Geographic division
Region               | STRING    | YES      | Geographic region
Market               | STRING    | YES      | Geographic market
WM_Week              | STRING    | YES      | Walmart week (e.g., FY26-WK01)
FY                   | STRING    | YES      | Fiscal year
Status               | STRING    | YES      | Active/Completed/Pending
Phase                | STRING    | YES      | Project phase
Owner                | STRING    | YES      | Owner name/email
Partner              | STRING    | YES      | Partner organization
Last_Updated         | TIMESTAMP | YES      | Update timestamp

Total Rows: 1,375,544+ active records ✅ Verified February 17, 2026

**Verified Project Statistics**:
- Total Unique Projects (by title): **4,215** ✅
  - Operations: 263 projects
  - Realty: 3,952 projects
- Total Unique Stores: **4,588** ✅
  - Operations: 4,585 stores
  - Realty: 3,952 stores

**Last Updated**: 2026-02-17T12:10:35+00:00 ✅ (BigQuery sync timestamp)
```

### 4.2 SQLite Cache Schema

**File**: `backend/cache.db` (regenerated on startup)

```sql
-- Denormalized copy of BigQuery data
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    intake_card TEXT,
    title TEXT NOT NULL,
    project_source TEXT,
    facility INTEGER,
    store TEXT,
    division TEXT,
    region TEXT,
    market TEXT,
    wm_week TEXT,
    fy TEXT,
    status TEXT,
    phase TEXT,
    owner TEXT,
    partner TEXT,
    last_updated TIMESTAMP
);

-- Query: SELECT DISTINCT ... WHERE status='Active'
-- Purpose: Deduplicates identical records from BigQuery
-- Performance: Returns 50K rows in <100ms vs 10+ seconds from BigQuery

CREATE TABLE sync_metadata (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at TIMESTAMP
);

-- Sample rows:
-- ('total_synced_records', '1375544', '2026-02-17T14:36:42')
-- ('last_sync', '2026-02-17T14:36:42', '2026-02-17T14:36:42')
-- ('sync_status', 'success', '2026-02-17T14:36:42')
```

---

## 5. Data Flow Diagrams

### 5.1 Initialization Flow

```
┌─ User opens browser (localhost:8002) ──┐
                                         │
                      ▼
            Browser requests index.html
                      │
        ┌─────────────┴──────────────┐
        │                            │
        ▼ (ENVIRONMENT=dev)           ▼ (ENVIRONMENT=prod)
    index.html (latest)         index.html.production (stable)
        │                            │
        └─────────────┬──────────────┘
                      │
                      ▼
          JavaScript window.onload
                      │
        ┌─────────────┼──────────────┬───────────────┐
        │             │              │               │
        ▼             ▼              ▼               ▼
    GET /api/    GET /api/      GET /api/      GET /api/
    summary      projects       filters        project-titles
        │             │              │               │
        └─────────────┼──────────────┼───────────────┘
                      │
                  (in parallel)
                      │
        ┌─────────────┴──────────────────────┐
        │                                    │
        ▼                                    ▼
  updateSummaryStats()              updateProjectList()
        │                                    │
        ├─ Count unique titles           ├─ Render <div> elements
        ├─ Count unique stores           ├─ Add click handlers
        ├─ Display on page               └─ Show loading indicator
        └─ Add to LocalStorage
```

### 5.2 Filter Application Flow

```
User enters text in search box or selects filter
              │
              ▼
    filterProjects() function triggered
              │
    ┌─────────┴────────────┐
    │                      │
    ▼                      ▼
Show loading      Build query string
indicator         (from selectedFilters)
    │                      │
    │       ┌──────────────┘
    │       │
    │       ▼ (e.g., "?title=store&project_source=Realty&region=NE")
    │   GET /api/projects
    │       │
    │       ▼ (Backend processes query)
    │   sqlite_cache.py::get_projects()
    │       │
    │       ├─ Build WHERE clause
    │       ├─ Execute: SELECT DISTINCT ... FROM projects WHERE ...
    │       ├─ Return matching rows
    │       └─ Pydantic validates response
    │
    │       ▼ (JSON response arrives)
    │   updateSummaryStats(projects)
    │       │
    │       ├─ Count unique titles
    │       ├─ Update summary cards
    │       └─ Update Quick Review grid
    │
    │       ▼
    │   updateProjectList(projects)
    │       │
    │       ├─ Create hierarchical <div> tree
    │       ├─ Add expand/collapse handlers
    │       └─ Render to page
    │
    └─►Hide loading indicator
```

### 5.3 AI Query Flow

```
User types: "Find realty projects in northeast"
              │
              ▼
    POST /api/ai/query
    {
      "query": "Find realty projects in northeast",
      "context": {
        "all_projects": [...],
        "filters": {...}
      }
    }
              │
              ▼ (Backend receives)
    backend/ai_agent.py::process_query()
              │
              ├─ Send to Anthropic Claude API
              ├─ Prompt engineering: "Map the user query to filters: division, region, source..."
              └─ Claude responds with: {region: "NORTHEAST", source: "Realty"}
              │
              ▼
    Claude returns answer + suggested_filters
              │
              ▼ (Frontend receives)
    Display answer to user
    Optionally auto-apply suggested_filters
              │
              ▼
    Re-run filterProjects() with new filters
```

---

## 6. Field Mappings & Aliases

### 6.1 Frontend vs Backend Field Names

| Frontend | Backend | BigQuery | SQLite | Type | Notes |
|----------|---------|----------|--------|------|-------|
| title | title | Project_Title | title | STRING | CRITICAL for stats |
| store | store | Facility | store | STRING/INT | CRITICAL for store count |
| source | project_source | Project_Source | project_source | STRING | Values: Operations, Realty |
| id | project_id | Intake_Card | intake_card | STRING | May be nullable |
| region | region | Region | region | STRING | Location hierarchy |
| phase | phase | Phase | phase | STRING | Project phase |
| owner | owner | Owner | owner | STRING | Contact person |

### 6.2 Filter Names (UI vs Backend)

| UI Display | Query Param | SQLite Column | Values |
|------------|------------|---------------|--------|
| All Divisions | division | division | EAST, WEST, ... |
| All Regions | region | region | NE, SE, MW, ... |
| All Markets | market | market | BOSTON, NEW YORK, ... |
| All Stores | store | store | 1, 2, 3, ... 4588 |
| All Sources | project_source | project_source | Operations, Realty |
| All Phases | phase | phase | Pending, POC/POT, ... |
| All Owners | owner | owner | email addresses |
| All Partners | partner | partner | CBRE, Jones Lang, ... |

---

## 7. Data Quality Rules

### 7.1 Validation Rules

```javascript
// On frontend before display:
├─ title: Must not be empty (filter: p => p.title)
├─ store: Must not be empty string (filter: p => p.store && p.store.trim() !== '')
├─ project_source: Must be 'Operations' or 'Realty'
├─ facility: Must be positive integer
└─ last_updated: Must be valid ISO 8601 timestamp

// Backend returns:
├─ All rows from SQLite cache (with DISTINCT applied)
├─ No null titles (BigQuery constraint)
└─ Status='Active' filter applied
```

### 7.2 Known Data Issues (Fixed)

| Issue | Cause | Fix | Status |
|-------|-------|-----|--------|
| Duplicate rows appearing | BigQuery returns exact duplicates | DISTINCT in sqlite_cache.py | ✅ Fixed |
| Stats = Store count | Counting project_ids instead of titles | updateSummaryStats() rewrote | ✅ Fixed |
| Store count > Project count | Null/empty store values included | Filter: store && store.trim() !== '' | ✅ Fixed |
| UI not reflecting code changes | Browser cache + wrong HTML served | Hard refresh + static route | ✅ Fixed |

---

## 8. Sample Data Queries

### 8.1 Active Realty Projects with "Speaker" in Title

**Frontend Request**:
```
GET /api/projects?project_source=Realty&title=speaker
```

**SQL Executed** (backend):
```sql
SELECT DISTINCT 
  intake_card, title, facility, store, project_source, division, region, market,
  wm_week, fy, status, phase, owner, partner, last_updated
FROM projects
WHERE status='Active'
  AND project_source='Realty'
  AND title LIKE '%speaker%'
ORDER BY title, wm_week;
```

**Response** (partial):
```json
[
  {
    "title": "EXP - Store Speaker Upgrade",
    "project_source": "Realty",
    "store": "1234",
    "facility": 1234,
    "division": "EAST",
    "region": "NE",
    "market": "BOSTON",
    "owner": "john.doe@walmart.com",
    "partner": "CBRE",
    ...
  },
  {
    "title": "Remodel - Store Speaker Upgrade",
    "project_source": "Realty",
    "store": "5678",
    ...
  }
]
```

### 8.2 Stats Calculation Example

**Input**: 1,181 rows matching filter (all Realty, containing "store")

**Processing**:
```javascript
const uniqueTitles = new Set([
  "EXP - Store Speaker Upgrade",
  "EXP - Store Speaker Upgrade",
  "EXP - Store Speaker Upgrade",
  ...,
  "Remodel - Store Speaker Upgrade",
  "Remodel - Store Speaker Upgrade",
  ...
]);
// Set size: 2

const uniqueStores = new Set([
  "1234", "5678", "9012", ... (1,181 unique values)
]);
// Set size: 1,181
```

**Output**:
```
Total Active Projects: 2
Total Stores: 1,181
Realty Projects: 2
Operations Projects: 0
```

---

## 9. Data Consistency Checklist

- [ ] Every row has a non-empty `title` field
- [ ] Every row has a `store` value (not null/empty)
- [ ] Every row has `project_source` as 'Operations' or 'Realty'
- [ ] Stats' "total_active_projects" matches Quick Review card count
- [ ] Stats' "total_stores" matches number of distinct store values
- [ ] No rows appear twice in results (DISTINCT applied)
- [ ] Filter values in `/api/filters` match actual data
- [ ] `last_updated` timestamp within last 24 hours

---

**Data Model Version**: 3.1  
**Last Validated**: February 17, 2026 14:15 UTC  
**Verification Status**: ✅ **VERIFIED WITH LIVE DATA**  
**BigQuery Connection**: ✅ **ACTIVE & TESTED**  
**API Endpoint Tested**: GET /api/summary returning real production data  
**Documentation Accurate**: ✅ Yes
