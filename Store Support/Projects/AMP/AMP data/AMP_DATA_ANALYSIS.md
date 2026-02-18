# AMP BigQuery Data Integration Architecture

## Enterprise Data Sources

### Primary AMP Data Source
**Production Table**: `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
- Core enterprise table for all AMP (Activity Management Plan) message events
- Contains complete store operations application activity management plan message events
- Requires inner joins with calendar and store dimension tables for comprehensive analysis
- Production-grade data source with enterprise-level data quality and consistency

### Walmart Calendar Dimension Source  
**Production Table**: `wmt-edw-prod.US_CORE_DIM_VM.CALENDAR_DIM`
- Enterprise calendar dimension with Walmart-specific fiscal calendar structure
- Provides fiscal year, WM week, quarter alignment, and custom day numbering
- Supports multi-year analysis with proper date range filtering
- Essential for aligning AMP events with Walmart business calendar

### Store Business Unit Dimension Source
**Production Table**: `wmt-loc-cat-prod.catalog_location_views.businessunit_view`
- Complete store business unit dimension with geographic and operational data
- Includes subdivision mapping, regional breakdown, and store status information
- Provides geographic coordinates, city/state data, and store format classification
- Critical for store-level analysis and geographic reporting

### Schema Reference Framework
**Reference File**: `AMP Data.tflx` (Tableau Packaged Data Source, 966KB)
- Contains authoritative schema definitions and field mappings for AMP BigQuery table
- Provides calculated field definitions and complex data relationships
- Includes proven join patterns and data integration best practices
- Serves as the definitive reference for field definitions and data transformation logic

## Approaches to Extract Information

### ✅ COMPLETED: Schema Integration Analysis
Based on extracted Tableau schema from `AMP Data.tflx`, here's the complete field mapping:

#### Tableau Schema Analysis Results:
- **Total Fields Identified**: 311 unique business fields
- **AMP Event Fields**: 35 fields (message data, status, priorities)
- **Calendar/Time Fields**: 28 fields (WM weeks, fiscal years, dates)
- **Store/Business Fields**: 24 fields (store numbers, locations, audiences)
- **System/Other Fields**: 224 fields (internal IDs, user data, workflow)

#### Data Sources Identified in Tableau:
1. **AMP2 Data** → Maps to `STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
2. **Cal_Dim_Data** → Maps to `CALENDAR_DIM` 
3. **Store Cur Data** → Maps to `businessunit_view`
4. **AMP2 Users, Comments, Verification** → Additional workflow tables

### BigQuery Integration Schema Mapping

#### Primary AMP Event Fields (Tableau → BigQuery):
```sql
-- Core AMP message events from Tableau to BigQuery mapping
SELECT 
    event_id,                    -- Tableau: event_id
    msg_id as message_id,        -- Tableau: AMPID, AMP_ID
    actv_title_home_ofc_nm as message_title,  -- Tableau: Title, Activity_Title
    msg_txt as message_description,           -- Tableau: message content
    msg_start_dt as message_start_date,       -- Tableau: Start_Date, event_dt
    msg_end_dt as message_end_date,           -- Tableau: End_Date
    msg_start_dt::date as message_date,       -- Tableau: Date
    bus_domain_nm as business_area,           -- Tableau: Business_Area, Store_Area
    actv_type_nm as activity_type,            -- Tableau: Activity_Type, Event_Type
    msg_type_nm as message_type,              -- Tableau: Message_Type, Prim_Message_Type
    msg_status_id as message_status,          -- Tableau: Message_Status, Status
    priority_status_ind as priority_level,    -- Tableau: Priority, high_priority
    trgt_store_nbr_array as store_number,     -- Tableau: Store, STORE_NBR, StoreNumber
    create_user as created_by,                -- Tableau: Author, create_user
    create_ts as created_date,                -- Tableau: Created_TS, Created_Date
    upd_user as modified_by,                  -- Tableau: upd_user
    upd_ts as modified_date,                  -- Tableau: upd_ts, Last_Updated
    src_rcv_ts as published_date,             -- Tableau: src_rcv_ts
    msg_hide_ind as approval_status,          -- Tableau: Hidden_Status, Verification_Status
    msg_leg_status_nm as workflow_stage       -- Tableau: Legal_Status, Sub_Category_Message_Status
FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
```

#### Calendar Dimension Fields (Tableau → BigQuery):
```sql
-- Calendar integration with Walmart-specific calculations
SELECT 
    CALENDAR_DATE,
    FISCAL_YEAR_NBR,             -- Tableau: FISCAL_YEAR_NBR, FY
    WM_WEEK_NBR,                 -- Tableau: WM_WEEK_NBR, WM_Week, Week
    WM_QTR_NAME,                 -- Tableau: WM_QTR_NAME, QTR
    WM_YEAR_NBR,                 -- Tableau: WM_YEAR_NBR, WM_Year
    CAL_YEAR_NBR,                -- Tableau: CAL_YEAR_NBR
    -- Custom Walmart day numbering from Tableau
    CASE 
        WHEN extract(dayofweek from CALENDAR_DATE)=1 THEN 2  -- Sunday=1 → Monday=2
        WHEN extract(dayofweek from CALENDAR_DATE)=2 THEN 3  -- Monday=2 → Tuesday=3
        WHEN extract(dayofweek from CALENDAR_DATE)=3 THEN 4  -- Tuesday=3 → Wednesday=4
        WHEN extract(dayofweek from CALENDAR_DATE)=4 THEN 5  -- Wednesday=4 → Thursday=5
        WHEN extract(dayofweek from CALENDAR_DATE)=5 THEN 6  -- Thursday=5 → Friday=6
        WHEN extract(dayofweek from CALENDAR_DATE)=6 THEN 7  -- Friday=6 → Saturday=7
        WHEN extract(dayofweek from CALENDAR_DATE)=7 THEN 1  -- Saturday=7 → Sunday=1
    END as Date_Day_Number       -- Tableau: Date_Day_Number, Week_Day
FROM `wmt-edw-prod.US_CORE_DIM_VM.CALENDAR_DIM`
```

#### Store Business Unit Fields (Tableau → BigQuery):
```sql
-- Store dimension with subdivision mapping from Tableau
SELECT
    CAST(business_unit_nbr AS NUMERIC) AS STORE_NBR,    -- Tableau: STORE_NBR, Store
    physical_city AS CITY_NAME,                         -- Tableau: CITY_NAME
    LEFT(physical_zip_code,5) AS POSTAL_CODE,          -- Tableau: POSTAL_CODE
    region_code AS REGION_NBR,                          -- Tableau: REGION_NBR, Region
    martket_code AS MARKET_AREA_NBR,                    -- Tableau: MARKET_AREA_NBR, Market
    format_code,                                        -- Tableau: format_code, Store_Type
    -- Subdivision mapping extracted from Tableau business logic
    CASE subdivision_code
        WHEN 'A' THEN 'SOUTHEAST BU'        -- Tableau: SUBDIV_NAME patterns
        WHEN 'B' THEN 'SOUTHWEST BU'
        WHEN 'C' THEN 'FORMAT DEVELOPMENT'
        WHEN 'D' THEN 'STORE NO 8'
        WHEN 'E' THEN 'NORTH BU'
        WHEN 'F' THEN 'EAST BU'
        WHEN 'G' THEN 'RETAIL SUBDIVISION G'
        WHEN 'M' THEN 'WEST BU'
        WHEN 'O' THEN 'NHM BU'
        WHEN 'X' THEN 'US Retail SD X'
        WHEN 'I' THEN 'PR BU'
        WHEN 'Z' THEN 'RX Facilities'
        ELSE subdivision_code
    END AS SUBDIV_NAME,                                 -- Tableau: SUBDIV_NAME
    banner_code AS BANNER_CODE,                         -- Tableau: BANNER_CODE
    banner_desc AS BANNER_DESC,                         -- Tableau: BANNER_DESC
    STORE_TYPE_CODE,                                    -- Tableau: STORE_TYPE_CODE
    STORE_TYPE_DESC,                                    -- Tableau: STORE_TYPE_DESC  
    bu_status_code AS OPEN_STATUS_CODE,                 -- Tableau: OPEN_STATUS_CODE
    bu_status_desc AS OPEN_STATUS_DESC,                 -- Tableau: OPEN_STATUS_DESC
    physical_county AS COUNTY_NAME,                     -- Tableau: COUNTY_NAME
    physical_state_code AS STATE_PROV_CODE,             -- Tableau: STATE_PROV_CODE
    LATITUDE AS LATITUDE_DGR,                           -- Tableau: LATITUDE_DGR
    longitude AS LONGITUDE_DGR                          -- Tableau: LONGITUDE_DGR
FROM `wmt-loc-cat-prod.catalog_location_views.businessunit_view`
```

### Complete Integration Query with Tableau Field Alignment

```sql
-- Production BigQuery query aligned with Tableau schema structure
SELECT 
    -- AMP Event Core Data (from Tableau AMP2 Data source)
    amp.event_id,
    amp.msg_id as message_id,
    amp.actv_title_home_ofc_nm as message_title,
    amp.msg_txt as message_description,
    amp.msg_start_dt as message_start_date,
    amp.msg_end_dt as message_end_date,
    DATE(amp.msg_start_dt) as message_date,
    amp.bus_domain_nm as business_area,
    amp.actv_type_nm as activity_type,
    amp.msg_type_nm as message_type,
    amp.msg_status_id as message_status,
    amp.priority_status_ind as priority_level,
    amp.trgt_store_nbr_array as store_number,
    amp.create_user as created_by,
    amp.create_ts as created_date,
    amp.upd_user as modified_by,
    amp.upd_ts as modified_date,
    amp.src_rcv_ts as published_date,
    amp.msg_hide_ind as approval_status,
    amp.msg_leg_status_nm as workflow_stage,
    
    -- Calendar Dimension Data (from Tableau Cal_Dim_Data source)
    cal.FISCAL_YEAR_NBR,
    cal.WM_WEEK_NBR,
    cal.WM_QTR_NAME,
    cal.WM_YEAR_NBR,
    cal.CAL_YEAR_NBR,
    cal.Date_Day_Number,
    cal.THE_DAY,
    CURRENT_DATE() as Today,
    EXTRACT(DAYOFWEEK FROM CURRENT_DATE()) as Week_Day,
    
    -- Store Business Unit Data (from Tableau Store Cur Data source)
    store.STORE_NBR,
    store.CITY_NAME,
    store.POSTAL_CODE,
    store.REGION_NBR,
    store.MARKET_AREA_NBR,
    store.format_code,
    store.SUBDIV_NAME,
    store.BANNER_CODE,
    store.BANNER_DESC,
    store.STORE_TYPE_CODE,
    store.STORE_TYPE_DESC,
    store.OPEN_STATUS_CODE,
    store.OPEN_STATUS_DESC,
    store.COUNTY_NAME,
    'US' as COUNTRY_CODE,
    store.STATE_PROV_CODE,
    store.LATITUDE_DGR,
    store.LONGITUDE_DGR

FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT` amp

-- Calendar integration (matches Tableau Cal_Dim_Data logic)
INNER JOIN (
    SELECT 
        CALENDAR_DATE, 
        FISCAL_YEAR_NBR, 
        WM_WEEK_NBR, 
        WM_QTR_NAME, 
        WM_YEAR_NBR, 
        CAL_YEAR_NBR,
        CASE 
            WHEN EXTRACT(DAYOFWEEK FROM CALENDAR_DATE)=1 THEN 2
            WHEN EXTRACT(DAYOFWEEK FROM CALENDAR_DATE)=2 THEN 3
            WHEN EXTRACT(DAYOFWEEK FROM CALENDAR_DATE)=3 THEN 4
            WHEN EXTRACT(DAYOFWEEK FROM CALENDAR_DATE)=4 THEN 5
            WHEN EXTRACT(DAYOFWEEK FROM CALENDAR_DATE)=5 THEN 6
            WHEN EXTRACT(DAYOFWEEK FROM CALENDAR_DATE)=6 THEN 7
            WHEN EXTRACT(DAYOFWEEK FROM CALENDAR_DATE)=7 THEN 1
        END as Date_Day_Number,
        DATE_SUB(CURRENT_DATE(), INTERVAL (Date_Day_Number - 1) DAY) as THE_DAY
    FROM `wmt-edw-prod.US_CORE_DIM_VM.CALENDAR_DIM`
    WHERE CALENDAR_DATE >= DATE_SUB(CURRENT_DATE(), INTERVAL 7*365 DAY)
      AND CALENDAR_DATE <= DATE_ADD(CURRENT_DATE(), INTERVAL 4*365 DAY)
) cal ON DATE(amp.msg_start_dt) = cal.CALENDAR_DATE

-- Store integration (matches Tableau Store Cur Data logic)  
INNER JOIN (
    SELECT
        CAST(business_unit_nbr AS NUMERIC) AS STORE_NBR,
        physical_city AS CITY_NAME,
        LEFT(physical_zip_code,5) AS POSTAL_CODE,
        region_code AS REGION_NBR,
        martket_code AS MARKET_AREA_NBR,
        format_code,
        CASE subdivision_code
            WHEN 'A' THEN 'SOUTHEAST BU'
            WHEN 'B' THEN 'SOUTHWEST BU'
            WHEN 'C' THEN 'FORMAT DEVELOPMENT'
            WHEN 'D' THEN 'STORE NO 8'
            WHEN 'E' THEN 'NORTH BU'
            WHEN 'F' THEN 'EAST BU'
            WHEN 'G' THEN 'RETAIL SUBDIVISION G'
            WHEN 'M' THEN 'WEST BU'
            WHEN 'O' THEN 'NHM BU'
            WHEN 'X' THEN 'US Retail SD X'
            WHEN 'I' THEN 'PR BU'
            WHEN 'Z' THEN 'RX Facilities'
            ELSE subdivision_code
        END AS SUBDIV_NAME,
        banner_code AS BANNER_CODE,
        banner_desc AS BANNER_DESC,
        STORE_TYPE_CODE,
        STORE_TYPE_DESC,
        bu_status_code AS OPEN_STATUS_CODE,
        bu_status_desc AS OPEN_STATUS_DESC,
        physical_county AS COUNTY_NAME,
        physical_state_code AS STATE_PROV_CODE,
        LATITUDE AS LATITUDE_DGR,
        longitude AS LONGITUDE_DGR
    FROM `wmt-loc-cat-prod.catalog_location_views.businessunit_view`
    WHERE physical_country_code = 'US'
      AND base_division_desc = "WAL-MART STORES INC."
      AND bu_status_desc != 'CLOSED'
      AND DATE(operational_open_start_date) <= DATE_ADD(CURRENT_DATE(), INTERVAL 90 DAY)
) store ON CAST(REGEXP_EXTRACT(amp.trgt_store_nbr_array, r'(\d+)') AS NUMERIC) = store.STORE_NBR

WHERE DATE(amp.msg_start_dt) >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY);
```

### Field Validation Based on Tableau Schema

#### Key Tableau Fields Successfully Mapped:
✅ **Event Identification**: `event_id`, `AMPID` → `event_id`, `message_id`  
✅ **Message Content**: `Title`, `Activity_Title` → `message_title`  
✅ **Timing**: `Start_Date`, `End_Date`, `event_dt` → `message_start_date`, `message_end_date`  
✅ **Business Context**: `Business_Area`, `Store_Area` → `business_area`  
✅ **Status Tracking**: `Message_Status`, `Status` → `message_status`  
✅ **Priority Management**: `Priority`, `high_priority` → `priority_level`  
✅ **Store Targeting**: `Store`, `STORE_NBR` → `store_number`  
✅ **Calendar Integration**: `WM_WEEK_NBR`, `FISCAL_YEAR_NBR` → Calendar dimension  
✅ **Geographic Data**: `CITY_NAME`, `STATE_PROV_CODE`, `SUBDIV_NAME` → Store dimension

### Implementation Steps Using Tableau Schema

1. **Field Alignment Verification**: Use `tableau_schema_extracted.json` for complete field reference
2. **Data Type Mapping**: Apply proper BigQuery data types based on Tableau field usage
3. **Join Key Validation**: Verify store number extraction from `trgt_store_nbr_array` 
4. **Calendar Logic Implementation**: Apply Tableau's custom day numbering logic
5. **Business Rule Implementation**: Apply subdivision mapping and status filtering from Tableau

### Option 1: Manual Tableau Inspection ✅ COMPLETED
- Schema extracted programmatically from .tflx contents
- 311 unique fields identified and categorized
- Data source relationships mapped to BigQuery tables

### Option 2: Extract Data Source Information ✅ COMPLETED  
```powershell
# Already completed - AMP_Data_contents directory contains:
# - displaySettings: Field definitions and ordinals
# - flow: Complete data flow and transformation logic  
# - maestroMetadata: Tableau version and feature information
```

## BigQuery Data Integration Architecture

### Core AMP Table Structure
**Table**: `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`

The AMP Data.tflx file provides schema guidance for extracting:
- **Message/Event Identifiers**: Event IDs, message IDs, activity identifiers
- **Store Operations Context**: Store numbers, operational areas, message types
- **Timing Information**: Message start/end dates, activity periods
- **Status Tracking**: Message status, publication status, workflow states
- **Content Details**: Message titles, descriptions, target audiences

### Required Inner Joins

#### 1. Walmart Calendar Dimension
**Table**: `wmt-edw-prod.US_CORE_DIM_VM.CALENDAR_DIM`
- **Purpose**: Fiscal year, WM week alignment, date calculations
- **Join Key**: Date fields from AMP events to CALENDAR_DATE
- **Custom Logic**: Walmart-specific day numbering and fiscal periods

#### 2. Store Business Unit Dimension  
**Table**: `wmt-loc-cat-prod.catalog_location_views.businessunit_view`
- **Purpose**: Store geographic data, subdivision mapping, operational status
- **Join Key**: Store numbers from AMP events to business_unit_nbr
- **Filters**: US stores only, active/open status, WAL-MART STORES INC. division

## Recommended Integration Steps

### Step 1: Document Current AMP Structure
Create a file documenting what's in your Tableau data source:

```yaml
amp_data_structure:
  tables:
    - name: "main_activity_table"
      fields: 
        - activity_id: "Primary key for activities"
        - store_nbr: "Links to store operations data"
        - planned_dt: "Aligns with calendar dimension"
  
  calculated_fields:
    - name: "performance_variance"
      formula: "actual - planned"
  
  relationships:
    - table1: "activities"
      table2: "stores" 
      join_key: "store_nbr"
```

### Step 2: Create AMP Integration Pipeline
Production BigQuery integration with proper inner joins:

```python
def create_amp_integration_pipeline():
    amp_config = {
        "name": "AMP Store Operations Integration",
        "primary_query": '''
            SELECT 
                amp.*,
                cal.FISCAL_YEAR_NBR,
                cal.WM_WEEK_NBR, 
                cal.WM_QTR_NAME,
                cal.WM_YEAR_NBR,
                store.SUBDIV_NAME,
                store.BANNER_DESC as STORE_TYPE_DESC,
                store.CITY_NAME,
                store.STATE_PROV_CODE,
                store.LATITUDE_DGR,
                store.LONGITUDE_DGR
            FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT` amp
            INNER JOIN (
                SELECT CALENDAR_DATE, CAL_YEAR_NBR, FISCAL_YEAR_NBR, WM_WEEK_NBR, WM_QTR_NAME, WM_YEAR_NBR,
                       current_date() as Today, extract(dayofweek from current_date) as Week_Day,
                       CASE 
                           WHEN extract(dayofweek from current_date)=7 THEN 1
                           WHEN extract(dayofweek from current_date)=1 THEN 2
                           WHEN extract(dayofweek from current_date)=2 THEN 3
                           WHEN extract(dayofweek from current_date)=3 THEN 4
                           WHEN extract(dayofweek from current_date)=4 THEN 5
                           WHEN extract(dayofweek from current_date)=5 THEN 6
                           WHEN extract(dayofweek from current_date)=6 THEN 7
                       END as Date_Day_Number,
                       date_add(current_date(), INTERVAL -(CASE 
                           WHEN extract(dayofweek from current_date)=7 THEN 1
                           WHEN extract(dayofweek from current_date)=1 THEN 2
                           WHEN extract(dayofweek from current_date)=2 THEN 3
                           WHEN extract(dayofweek from current_date)=3 THEN 4
                           WHEN extract(dayofweek from current_date)=4 THEN 5
                           WHEN extract(dayofweek from current_date)=5 THEN 6
                           WHEN extract(dayofweek from current_date)=6 THEN 7
                       END) DAY) as THE_DAY
                FROM `wmt-edw-prod.US_CORE_DIM_VM.CALENDAR_DIM`
                WHERE CALENDAR_DATE >= DATE_ADD(current_date, interval -7 YEAR)
                  AND CALENDAR_DATE < DATE_ADD(current_date, interval 4 YEAR)
            ) cal ON DATE(amp.message_start_date) = cal.CALENDAR_DATE
            INNER JOIN (
                SELECT
                    CAST(business_unit_nbr AS NUMERIC) AS STORE_NBR,
                    physical_city AS CITY_NAME,
                    LEFT(physical_zip_code,5) AS POSTAL_CODE,
                    region_code AS REGION_NBR,
                    martket_code AS MARKET_AREA_NBR,
                    format_code,
                    CASE subdivision_code
                        WHEN 'A' THEN 'SOUTHEAST BU'
                        WHEN 'B' THEN 'SOUTHWEST BU'
                        WHEN 'C' THEN 'FORMAT DEVELOPMENT'
                        WHEN 'D' THEN 'STORE NO 8'
                        WHEN 'E' THEN 'NORTH BU'
                        WHEN 'F' THEN 'EAST BU'
                        WHEN 'G' THEN 'RETAIL SUBDIVISION G'
                        WHEN 'M' THEN 'WEST BU'
                        WHEN 'O' THEN 'NHM BU'
                        WHEN 'X' THEN 'US Retail SD X'
                        WHEN 'I' THEN 'PR BU'
                        WHEN 'Z' THEN 'RX Facilities'
                        ELSE subdivision_code
                    END AS SUBDIV_NAME,
                    banner_code AS BANNER_CODE,
                    banner_desc AS BANNER_DESC,
                    bu_status_code AS OPEN_STATUS_CODE,
                    bu_status_desc AS OPEN_STATUS_DESC,
                    physical_county AS COUNTY_NAME,
                    physical_state_code AS STATE_PROV_CODE,
                    LATITUDE AS LATITUDE_DGR,
                    longitude AS LONGITUDE_DGR
                FROM `wmt-loc-cat-prod.catalog_location_views.businessunit_view`
                WHERE physical_country_code = 'US'
                  AND base_division_desc = "WAL-MART STORES INC."
                  AND bu_status_desc != 'CLOSED'
                  AND Date(operational_open_start_date) <= date_add(current_date(), Interval 90 day)
            ) store ON amp.store_number = store.STORE_NBR
            WHERE amp.message_date >= DATE_ADD(CURRENT_DATE(), INTERVAL -90 DAY)
        '''
    }
```

## Potential Pipeline Enhancements

### 1. Activity Status Mapping
```sql
CASE 
    WHEN activity_status = 'PLANNED' THEN 'Scheduled'
    WHEN activity_status = 'IN_PROGRESS' THEN 'Active' 
    WHEN activity_status = 'COMPLETED' THEN 'Finished'
    WHEN activity_status = 'CANCELLED' THEN 'Cancelled'
    WHEN activity_status = 'ON_HOLD' THEN 'Paused'
    ELSE 'Unknown'
END as activity_status_desc
```

### 2. Performance Calculations
```sql
SELECT *,
    CASE 
        WHEN actual_start_dt <= planned_start_dt THEN 'On Time'
        WHEN actual_start_dt > planned_start_dt THEN 'Delayed'
        ELSE 'Not Started'
    END as timing_status,
    
    DATE_DIFF(actual_start_dt, planned_start_dt, DAY) as days_variance,
    
    CASE 
        WHEN completion_pct >= 100 THEN 'Complete'
        WHEN completion_pct >= 75 THEN 'Nearly Complete'
        WHEN completion_pct >= 50 THEN 'In Progress'
        WHEN completion_pct > 0 THEN 'Started'
        ELSE 'Not Started'
    END as progress_status
```

### 3. Production Calendar Integration Query
```sql
-- Walmart-specific calendar integration with custom day numbering
SELECT 
    CALENDAR_DATE, 
    CAL_YEAR_NBR, 
    FISCAL_YEAR_NBR, 
    WM_WEEK_NBR, 
    WM_QTR_NAME, 
    WM_YEAR_NBR, 
    current_date() as Today,
    extract(dayofweek from current_date) as Week_Day,
    CASE 
        WHEN extract(dayofweek from current_date)=7 THEN 1
        WHEN extract(dayofweek from current_date)=1 THEN 2
        WHEN extract(dayofweek from current_date)=2 THEN 3
        WHEN extract(dayofweek from current_date)=3 THEN 4
        WHEN extract(dayofweek from current_date)=4 THEN 5
        WHEN extract(dayofweek from current_date)=5 THEN 6
        WHEN extract(dayofweek from current_date)=6 THEN 7
    END as Date_Day_Number,
    date_add(current_date(), INTERVAL -(Date_Day_Number) DAY) as THE_DAY
FROM `wmt-edw-prod.US_CORE_DIM_VM.CALENDAR_DIM`
WHERE CALENDAR_DATE >= DATE_ADD(current_date, interval -7 YEAR)
  AND CALENDAR_DATE < DATE_ADD(current_date, interval 4 YEAR)
```

## Next Steps

### Immediate Actions:
1. **Review AMP Data.tflx** to understand field mappings and calculated fields
2. **Map Tableau schema** to BigQuery table `STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
3. **Identify key join fields** between AMP events and store/calendar dimensions
4. **Extract field definitions** for proper data type handling

### Integration Planning:
1. **Implement inner joins** with calendar and store business unit tables
2. **Apply Walmart-specific logic** for subdivision codes and day numbering
3. **Create comprehensive queries** combining all three data sources
4. **Add proper filtering** for active stores and relevant date ranges

### Production Implementation Requirements:
- **BigQuery Access**: Ensure permissions to all three production tables
- **Inner Join Strategy**: All joins must be inner joins for data integrity
- **Date Range Filtering**: Apply appropriate date filters for performance
- **Store Status Filtering**: Exclude closed stores and non-US locations
- **Field Mapping**: Use AMP Data.tflx to properly map and transform fields

## Production Data Architecture

### Confirmed BigQuery Tables:

```yaml
amp_data_architecture:
  connection_type: "BigQuery"
  main_tables: 
    - "wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT"
  dimension_tables:
    - "wmt-edw-prod.US_CORE_DIM_VM.CALENDAR_DIM"  
    - "wmt-loc-cat-prod.catalog_location_views.businessunit_view"
  
  key_join_fields:
    calendar_join: "DATE(message_start_date) = CALENDAR_DATE"
    store_join: "store_number = CAST(business_unit_nbr AS NUMERIC)"
  
  date_fields:
    - "message_start_date"
    - "message_end_date" 
    - "CALENDAR_DATE"
    - "operational_open_start_date"
  
  required_filters:
    calendar: "CALENDAR_DATE >= DATE_ADD(current_date, interval -7 YEAR)"
    stores: "physical_country_code = 'US' AND bu_status_desc != 'CLOSED'"
    amp_data: "message_date >= DATE_ADD(CURRENT_DATE(), INTERVAL -90 DAY)"
  
  walmart_specific_logic:
    subdivision_mapping: "12 subdivision codes (A-Z) to business unit names"
    day_numbering: "Custom Walmart day of week numbering (Sunday=1, Monday=2, etc.)"
    fiscal_calendar: "WM_WEEK_NBR, WM_QTR_NAME, FISCAL_YEAR_NBR alignment"
```

### AMP Data.tflx Usage:
- **Schema Reference**: Use to understand field names and data types in main AMP table
- **Calculated Fields**: Extract any custom business logic or derived fields
- **Join Patterns**: Understand how fields should be related across tables
- **Sample Data**: Validate data quality and expected values