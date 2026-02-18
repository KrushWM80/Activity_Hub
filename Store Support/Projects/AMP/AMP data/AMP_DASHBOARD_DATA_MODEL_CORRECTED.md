# AMP Dashboard Data Model - Corrected Architecture

**Owner:** Kendall Rush  
**Last Updated:** February 12, 2026

---

## Data Connection Information

### BigQuery Project
- **Project:** `wmt-assetprotection-prod`
- **Dataset:** `Store_Support_Dev`

### Primary AMP Data
| Table Name | Purpose |
|------------|----------|
| `Output - AMP ALL 2` | Main AMP event data (95 columns, all business logic applied) |

### Store Dimension Data
| Table Name | Purpose |
|------------|----------|
| `Store Cur Data` | All stores - Division, Region, Market |
| `Store Cur Div 1 Data` | Division 1 stores (Alignment = "Store") |
| `Store Cur Div 10 Data` | Division 10 stores (Alignment = "H&W") |

### Click Engagement Data
| Table Name | Purpose |
|------------|----------|
| `Audience Breakdown Cur` | Current click data by employee type (Hourly/Salaried) |
| `Audience Breakdown Historical` | Historical click data by employee type |
| `Device Types Cur` | Current click data by device (Mobile/Desktop) |
| `Device Types Historical` | Historical click data by device |
| `Time Spent Cur` | Current click data by time duration |
| `Time Spent Historical` | Historical click data by time duration |

### Location Catalog Source
| Table Name | Purpose |
|------------|----------|
| `wmt-loc-cat-prod.catalog_location_views.businessunit_view` | Store BU geographic data |
| `wmt-loc-cat-prod.catalog_location_views.division_view` | Store division data (Div 1, Div 10) |

---

## Data Source Summary

### Primary AMP Data Source
**Table:** `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
- **Description:** Refined, production-ready AMP event data with all business logic applied
- **Contains:** 95 columns including all dashboard requirements
- **Pre-filters Applied:** Message Type = "Store Updates", Status = "Published"

### Store Dimension Sources

#### 1. Store Current Data (All Stores)
**Table:** `wmt-assetprotection-prod.Store_Support_Dev.Store Cur Data`
**Source:** `wmt-loc-cat-prod.catalog_location_views.businessunit_view`
- **Purpose:** Geographic location data (Division, Region, Market)
- **Filters:** US stores, open status, WAL-MART STORES INC.

#### 2. Store Division 1 Data (WM US Stores)
**Table:** `wmt-assetprotection-prod.Store_Support_Dev.Store Cur Div 1 Data`
**Source:** `wmt-loc-cat-prod.catalog_location_views.division_view` (division_nbr = 1)
- **Purpose:** Store alignment data
- **Alignment Value:** "Store"

#### 3. Store Division 10 Data (Health & Wellness)
**Table:** `wmt-assetprotection-prod.Store_Support_Dev.Store Cur Div 10 Data`
**Source:** `wmt-loc-cat-prod.catalog_location_views.division_view` (division_nbr = 10)
- **Purpose:** H&W alignment data
- **Alignment Value:** "H&W"

### Click Engagement Sources (Current + Historical)

#### 1. Audience Breakdown
- **Current:** `wmt-assetprotection-prod.Store_Support_Dev.Audience Breakdown Cur`
- **Historical:** `wmt-assetprotection-prod.Store_Support_Dev.Audience Breakdown Historical`
- **Purpose:** Click data by audience segment

#### 2. Device Types
- **Current:** `wmt-assetprotection-prod.Store_Support_Dev.Device Types Cur`
- **Historical:** `wmt-assetprotection-prod.Store_Support_Dev.Device Types Historical`
- **Purpose:** Click data by device type (mobile, desktop, etc.)

#### 3. Time Spent
- **Current:** `wmt-assetprotection-prod.Store_Support_Dev.Time Spent Cur`
- **Historical:** `wmt-assetprotection-prod.Store_Support_Dev.Time Spent Historical`
- **Purpose:** Click data by time range duration

---

## Understanding "Division" - Three Different Contexts

### Context 1: Alignment (Business Division Filter)
**Column:** `Alignment` (from store dimension tables)
**Values:** 
- `Store` = Division 1 (WM US Stores business)
- `H&W` = Division 10 (Health & Wellness/Pharmacy business)

**Purpose:** Filter dashboard to show Store-focused vs H&W-focused messages

**Source:**
```sql
CASE division_name
  WHEN 'WAL-MART STORES INC.' THEN 'Store'
  WHEN 'PHARMACY' THEN 'H&W'
  ELSE division_name
END AS Alignment
```

---

### Context 2: Division (Geographic Business Unit)
**Column:** `Division` (from store dimension SUBDIV_NAME)
**Values:**
- `EAST BU` (East Business Unit)
- `WEST BU` (West Business Unit)  
- `NORTH BU` (North Business Unit)
- `SOUTHEAST BU` (Southeast Business Unit)
- `SOUTHWEST BU` (Southwest Business Unit)
- `NHM BU` (Neighborhood Market Business Unit)
- Other regional divisions

**Purpose:** Filter dashboard by geographic store division (what the dashboard "Division" filter uses)

**Source:**
```sql
CASE subdivision_code
  WHEN 'A' THEN 'SOUTHEAST BU'
  WHEN 'B' THEN 'SOUTHWEST BU'
  WHEN 'E' THEN 'NORTH BU'
  WHEN 'F' THEN 'EAST BU'
  WHEN 'M' THEN 'WEST BU'
  WHEN 'O' THEN 'NHM BU'
  -- etc.
END AS SUBDIV_NAME  -- This becomes "Division" in dashboard
```

---

### Context 3: Store Format Division
**Column:** `Division` or `Store_Type` (from Output - AMP ALL 2)
**Values:**
- `DIV 1` = Division 1 format stores
- Different from SC (Supercenter) and NHM (Neighborhood Market)

**Purpose:** Store format classification (not used in dashboard filters)

---

## Dashboard Field Mapping

### Complete Field List (19 Required + Additional)

| # | Dashboard Field | Source Column | Source Table | Data Type | Example Value |
|---|----------------|---------------|--------------|-----------|---------------|
| 1 | Event_ID | event_id | Output - AMP ALL 2 | STRING | 5b635469-... |
| 2 | Title | Title | Output - AMP ALL 2 | STRING | Your Week 2 Messages... |
| 3 | FY | FY | Output - AMP ALL 2 | INTEGER | 2027 |
| 4 | Week | Week | Output - AMP ALL 2 | INTEGER | 2 |
| 5 | Message Type | Message_Type | Output - AMP ALL 2 | STRING | Store Updates |
| 6 | Activity Type | Activity_Type | Output - AMP ALL 2 | STRING | Inform |
| 7 | Status | Status | Output - AMP ALL 2 | STRING | Published - Published |
| 8 | **Division** | SUBDIV_NAME | Store Dimension | STRING | **EAST BU** |
| 9 | Region | REGION_NBR | Store Dimension | STRING | 99 |
| 10 | Market | MARKET_AREA_NBR | Store Dimension | STRING | 999 |
| 11 | Store | store | Output - AMP ALL 2 | FLOAT | 545.0 |
| 12 | Edit Link | Edit_Link | Output - AMP ALL 2 | STRING | https://amp2-cms... |
| 13 | Preview Link | Web_Preview | Output - AMP ALL 2 | STRING | https://amp2-cms... |
| 14 | Store Count | Store_Cnt | Output - AMP ALL 2 | INTEGER | 4601 |
| 15 | Verification Status | Verification_Status | Output - AMP ALL 2 | STRING | Inform Only |
| 16 | Store Area | Store_Area | Output - AMP ALL 2 | STRING | Total Store |
| 17 | Audience | Target_Audience | Output - AMP ALL 2 | STRING | Hourly and Salary |
| 18 | Business Area | Business_Area | Output - AMP ALL 2 | STRING | Marketing |
| 19 | **Alignment** | Alignment (Store_Alignment) | Store Dimension Div 1/10 | STRING | **H&W** or **Store** |

### Click Engagement Fields (Aggregated from Click Tables)

| # | Dashboard Field | Source Table | Aggregation | Example |
|---|----------------|--------------|-------------|---------|
| 20 | Audience Clicks | Audience Breakdown Cur/Historical | SUM(Clicks) by Audience | 1,808 Hourly clicks |
| 21 | Device Clicks | Device Types Cur/Historical | SUM(Clicks) by Device_Type | 1,200 Mobile, 608 Desktop |
| 22 | Time Spent Clicks | Time Spent Cur/Historical | SUM(Clicks) by Time_Range | 500 (0-30s), 300 (30s-1m) |

---

## Data Join Strategy

### Join Pattern Overview
```
Output - AMP ALL 2 (Primary)
    ↓
LEFT JOIN Store Cur Data (for Division/Region/Market)
    ON store = STORE_NBR
    ↓
LEFT JOIN Store Cur Div 1 Data (for Store alignment)
    ON store = STORE_NBR AND division_nbr = 1
    ↓
LEFT JOIN Store Cur Div 10 Data (for H&W alignment)
    ON store = STORE_NBR AND division_nbr = 10
    ↓
LEFT JOIN Audience Breakdown (Cur + Historical)
    ON event_id = Event_ID AND FY = FY AND Week = Week
    ↓
LEFT JOIN Device Types (Cur + Historical)
    ON event_id = Event_ID AND FY = FY AND Week = Week
    ↓
LEFT JOIN Time Spent (Cur + Historical)
    ON event_id = Event_ID AND FY = FY AND Week = Week
```

### Composite Key for Click Data Joins
**Join Keys:** `event_id + FY + Week`
- Prevents duplicate records when same event appears in current + historical
- Ensures click data aligns with correct event time period

---

## Data Quality Notes

### Null/Placeholder Values Observed

1. **Division = NULL** in Output - AMP ALL 2
   - **Solution:** Join with Store Cur Data to populate SUBDIV_NAME
   
2. **Region = 99, Market = 999** (possible placeholders for "all stores")
   - **Solution:** Join with Store Cur Data for actual store-specific values
   
3. **Store = 545.0** (single store shown, but Store_Cnt = 4601)
   - **Interpretation:** May be primary store or first store in array
   - **Note:** Full store array not exposed in Output - AMP ALL 2

### Click Data Deduplication

Both Current and Historical tables exist for:
- Audience Breakdown
- Device Types
- Time Spent

**Strategy:** UNION ALL both tables, then GROUP BY to deduplicate and sum clicks

---

## Dashboard Filter Implementation

### 11 Required Filters

| Filter Name | Source Column | Filter Type | Example Values |
|------------|---------------|-------------|----------------|
| 1. Division | SUBDIV_NAME (from store dimension) | Multi-select | East BU, West BU, North BU |
| 2. Region | REGION_NBR (from store dimension) | Multi-select | 01, 02, 03, ... 99 |
| 3. Market | MARKET_AREA_NBR (from store dimension) | Multi-select | 101, 142, 999 |
| 4. Store | store | Multi-select | 1, 2, 545, 4567 |
| 5. Title | Title | Text search | "Week 2 Messages" |
| 6. Activity Type | Activity_Type | Multi-select | Inform, Verification |
| 7. Store Area | Store_Area | Multi-select | Total Store, Front End, Fresh |
| 8. **Alignment** | Alignment (Store_Alignment) | Multi-select | **Store, H&W** |
| 9. WM Week | Week | Range slider | 1-52 |
| 10. FY | FY | Multi-select | 2025, 2026, 2027 |
| 11. Keyword Search | Keyword_Tags | Text search | valentines, inventory |

### Admin Pre-Filters (Not User-Controllable)

Applied at query level:
- Message_Type = "Store Updates"
- Status LIKE "%Published%"

---

## Output Schema - Final Dashboard Table

**Table Name:** `Dashboard_AMP_Analysis_Final`

### Column List (30+ fields)

```sql
event_id                STRING
Title                   STRING
FY                      INTEGER
Week                    INTEGER
Message_Type            STRING
Activity_Type           STRING
Status                  STRING
Division                STRING      -- Geographic (East BU, West BU, etc)
Region                  STRING
Market                  STRING
store                   FLOAT
Store_Cnt               INTEGER
Edit_Link               STRING
Preview_Link            STRING
Verification_Status     STRING
Store_Area              STRING
Audience                STRING
Business_Area           STRING
Store_Alignment         STRING      -- "Store" or "H&W"
Start_Date              DATE
End_Date                DATE
Created_Date            DATE
Last_Updated            TIMESTAMP
Audience_Breakdown      STRING      -- Comma-separated audience types
Total_Audience_Clicks   INTEGER
Device_Types            STRING      -- Comma-separated device types
Total_Device_Clicks     INTEGER
Time_Ranges             STRING      -- Comma-separated time ranges
Total_Time_Clicks       INTEGER
Author                  STRING
QTR                     STRING
Priority                STRING
High_Impact             STRING
Refresh_Timestamp       TIMESTAMP
```

---

## Data Refresh Strategy

### Recommended Schedule
- **Output - AMP ALL 2**: Refreshed daily (managed by source system)
- **Store Dimension Tables**: Refreshed daily (managed by location catalog)
- **Click Data (Current)**: Refreshed hourly (near real-time)
- **Click Data (Historical)**: Refreshed daily

### Dashboard ETL Refresh
- **Frequency:** Daily at 6:00 AM UTC
- **Total Runtime:** ~10-15 minutes
- **Dependencies:** All source tables must complete first

---

## Validation Rules

### Data Quality Checks

1. **Event ID Uniqueness**: Each event_id should be unique per FY + Week
2. **Store Count Match**: Store_Cnt should match actual store array length
3. **Division Not Null**: After store join, Division (SUBDIV_NAME) should be populated
4. **Date Coherence**: Start_Date <= End_Date
5. **Click Data Integrity**: Total clicks should be non-negative
6. **Alignment Completeness**: Each store should have Store or H&W alignment

### Expected Row Counts (Example)
- **Output - AMP ALL 2**: ~50,000 events
- **Dashboard Final View**: ~50,000 rows (1:1 after joins and aggregation)
- **Click Data Rows**: ~500,000 (many:1 to events)

---

## Future Enhancements

### Potential Additions
1. **Store Array Expansion**: Unnest store arrays to show per-store metrics
2. **Historical Trending**: Compare week-over-week click performance
3. **Geo Mapping**: Map events by latitude/longitude
4. **Author Analytics**: Track message creation by author
5. **Keyword Tagging**: Parse and filter by keyword tags

---

## Contact & Support

**Data Owners:**
- **AMP Data**: Enterprise Store Communications Team
- **Store Dimension**: Location Catalog Team
- **Click Data**: Analytics & Engagement Team

**BigQuery Project:** `wmt-assetprotection-prod`
**Dataset:** `Store_Support_Dev`
