
-- AMP Store Operations BigQuery Integration
-- Aligned with Tableau schema from AMP Data.tflx
-- Combines AMP events, calendar dimension, and store business unit data

WITH amp_events AS (
  -- Primary AMP event data with Tableau field alignment
  SELECT 
    event_id,                              -- Tableau: event_id
    COALESCE(msg_id, auto_feed_id) as message_id,  -- Tableau: AMPID, AMP_ID
    COALESCE(actv_title_home_ofc_nm, auto_feed_title_nm) as message_title,  -- Tableau: Title, Activity_Title
    msg_txt as message_description,        -- Tableau: message content fields
    msg_start_dt as message_start_date,    -- Tableau: Start_Date, event_dt
    msg_end_dt as message_end_date,        -- Tableau: End_Date
    DATE(msg_start_dt) as message_date,    -- Tableau: Date
    bus_domain_nm as business_area,        -- Tableau: Business_Area, Store_Area
    actv_type_nm as activity_type,         -- Tableau: Activity_Type, Event_Type
    msg_type_nm as message_type,           -- Tableau: Message_Type, Prim_Message_Type
    CASE 
      WHEN msg_status_id = 1 THEN 'Draft'
      WHEN msg_status_id = 2 THEN 'Pending Approval'
      WHEN msg_status_id = 3 THEN 'Approved'
      WHEN msg_status_id = 4 THEN 'Published'
      WHEN msg_status_id = 5 THEN 'Archived'
      ELSE 'Unknown'
    END as message_status,                 -- Tableau: Message_Status, Status
    COALESCE(priority_status_ind, 0) as priority_level,  -- Tableau: Priority, high_priority
    trgt_store_nbr_array as store_number_array,  -- Tableau: Store, STORE_NBR, StoreNumber
    -- Extract first store number for join
    CAST(REGEXP_EXTRACT(trgt_store_nbr_array, r'(\d+)') AS NUMERIC) as store_number,
    create_user as created_by,             -- Tableau: Author, create_user
    create_ts as created_date,             -- Tableau: Created_TS, Created_Date
    upd_user as modified_by,               -- Tableau: upd_user
    upd_ts as modified_date,               -- Tableau: upd_ts, Last_Updated
    src_rcv_ts as published_date,          -- Tableau: src_rcv_ts
    CASE 
      WHEN msg_hide_ind = 1 THEN 'Hidden'
      WHEN msg_leg_status_nm = 'APPROVED' THEN 'Approved'
      WHEN msg_leg_status_nm = 'PENDING' THEN 'Pending'
      ELSE 'Active'
    END as approval_status,                -- Tableau: Hidden_Status, Verification_Status
    COALESCE(msg_leg_status_nm, 'Published') as workflow_stage,  -- Tableau: Legal_Status
    -- Additional Tableau-identified fields
    urgent_ind as urgent_activity,         -- Tableau: Urgent_Activity
    impct_status_ind as high_impact,       -- Tableau: High_Impact
    trgt_all_store_ind as all_stores_target  -- Tableau: All_Stores_Ind
  FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
  WHERE DATE(msg_start_dt) >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
    AND del_ind = 0  -- Exclude deleted records
),

walmart_calendar AS (
  -- Calendar dimension with Tableau-specific calculations
  SELECT 
    CALENDAR_DATE,
    FISCAL_YEAR_NBR,                       -- Tableau: FISCAL_YEAR_NBR, FY
    WM_WEEK_NBR,                           -- Tableau: WM_WEEK_NBR, WM_Week, Week
    WM_QTR_NAME,                           -- Tableau: WM_QTR_NAME, QTR
    WM_YEAR_NBR,                           -- Tableau: WM_YEAR_NBR, WM_Year
    CAL_YEAR_NBR,                          -- Tableau: CAL_YEAR_NBR
    -- Tableau custom day numbering logic
    CASE 
      WHEN EXTRACT(DAYOFWEEK FROM CALENDAR_DATE) = 1 THEN 2  -- Sunday → Monday
      WHEN EXTRACT(DAYOFWEEK FROM CALENDAR_DATE) = 2 THEN 3  -- Monday → Tuesday
      WHEN EXTRACT(DAYOFWEEK FROM CALENDAR_DATE) = 3 THEN 4  -- Tuesday → Wednesday
      WHEN EXTRACT(DAYOFWEEK FROM CALENDAR_DATE) = 4 THEN 5  -- Wednesday → Thursday
      WHEN EXTRACT(DAYOFWEEK FROM CALENDAR_DATE) = 5 THEN 6  -- Thursday → Friday
      WHEN EXTRACT(DAYOFWEEK FROM CALENDAR_DATE) = 6 THEN 7  -- Friday → Saturday
      WHEN EXTRACT(DAYOFWEEK FROM CALENDAR_DATE) = 7 THEN 1  -- Saturday → Sunday
    END as Date_Day_Number,                -- Tableau: Date_Day_Number, Week_Day
    -- Reference day calculation from Tableau logic
    DATE_SUB(CURRENT_DATE(), INTERVAL (
      CASE 
        WHEN EXTRACT(DAYOFWEEK FROM CURRENT_DATE()) = 1 THEN 1
        WHEN EXTRACT(DAYOFWEEK FROM CURRENT_DATE()) = 2 THEN 2
        WHEN EXTRACT(DAYOFWEEK FROM CURRENT_DATE()) = 3 THEN 3
        WHEN EXTRACT(DAYOFWEEK FROM CURRENT_DATE()) = 4 THEN 4
        WHEN EXTRACT(DAYOFWEEK FROM CURRENT_DATE()) = 5 THEN 5
        WHEN EXTRACT(DAYOFWEEK FROM CURRENT_DATE()) = 6 THEN 6
        WHEN EXTRACT(DAYOFWEEK FROM CURRENT_DATE()) = 7 THEN 0
      END
    ) DAY) as THE_DAY,                     -- Tableau: THE_DAY
    -- Additional Tableau calendar fields
    CURRENT_DATE() as Today,               -- Tableau: Today
    EXTRACT(DAYOFWEEK FROM CURRENT_DATE()) as Week_Day  -- Tableau: Week_Day
  FROM `wmt-edw-prod.US_CORE_DIM_VM.CALENDAR_DIM`
  WHERE CALENDAR_DATE >= DATE_SUB(CURRENT_DATE(), INTERVAL 7*365 DAY)
    AND CALENDAR_DATE <= DATE_ADD(CURRENT_DATE(), INTERVAL 4*365 DAY)
),

store_business_units AS (
  -- Store dimension with Tableau subdivision mapping
  SELECT
    CAST(business_unit_nbr AS NUMERIC) AS STORE_NBR,     -- Tableau: STORE_NBR, Store
    physical_city AS CITY_NAME,                          -- Tableau: CITY_NAME
    LEFT(physical_zip_code, 5) AS POSTAL_CODE,           -- Tableau: POSTAL_CODE
    region_code AS REGION_NBR,                           -- Tableau: REGION_NBR, Region
    martket_code AS MARKET_AREA_NBR,                     -- Tableau: MARKET_AREA_NBR, Market
    format_code,                                         -- Tableau: format_code, Store_Type
    division_nbr,                                        -- Tableau: Division, Division_Code
    -- Tableau subdivision mapping logic
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
      ELSE CONCAT('SUBDIVISION_', subdivision_code)
    END AS SUBDIV_NAME,                                  -- Tableau: SUBDIV_NAME
    banner_code AS BANNER_CODE,                          -- Tableau: BANNER_CODE
    banner_desc AS BANNER_DESC,                          -- Tableau: BANNER_DESC
    STORE_TYPE_CODE,                                     -- Tableau: STORE_TYPE_CODE
    STORE_TYPE_DESC,                                     -- Tableau: STORE_TYPE_DESC
    bu_status_code AS OPEN_STATUS_CODE,                  -- Tableau: OPEN_STATUS_CODE
    bu_status_desc AS OPEN_STATUS_DESC,                  -- Tableau: OPEN_STATUS_DESC
    physical_county AS COUNTY_NAME,                      -- Tableau: COUNTY_NAME
    'US' as COUNTRY_CODE,                                -- Tableau: COUNTRY_CODE
    physical_state_code AS STATE_PROV_CODE,              -- Tableau: STATE_PROV_CODE
    LATITUDE AS LATITUDE_DGR,                            -- Tableau: LATITUDE_DGR
    longitude AS LONGITUDE_DGR                           -- Tableau: LONGITUDE_DGR
  FROM `wmt-loc-cat-prod.catalog_location_views.businessunit_view`
  WHERE physical_country_code = 'US'
    AND base_division_desc = "WAL-MART STORES INC."
    AND bu_status_desc != 'CLOSED'
    AND DATE(operational_open_start_date) <= DATE_ADD(CURRENT_DATE(), INTERVAL 90 DAY)
)

-- Final integrated result set with complete Tableau schema alignment
SELECT 
  -- AMP Event Core Fields (22 fields from Tableau schema)
  amp.event_id,
  amp.message_id,
  amp.message_title,
  amp.message_description,
  amp.message_start_date,
  amp.message_end_date,
  amp.message_date,
  amp.business_area,
  amp.activity_type,
  amp.message_type,
  amp.message_status,
  amp.priority_level,
  amp.store_number,
  amp.store_number_array,
  amp.created_by,
  amp.created_date,
  amp.modified_by,
  amp.modified_date,
  amp.published_date,
  amp.approval_status,
  amp.workflow_stage,
  amp.urgent_activity,
  amp.high_impact,
  amp.all_stores_target,
  
  -- Calendar Dimension Fields (9 fields from Tableau schema)
  cal.FISCAL_YEAR_NBR,
  cal.WM_WEEK_NBR,
  cal.WM_QTR_NAME,
  cal.WM_YEAR_NBR,
  cal.CAL_YEAR_NBR,
  cal.Date_Day_Number,
  cal.THE_DAY,
  cal.Today,
  cal.Week_Day,
  
  -- Store Business Unit Fields (17 fields from Tableau schema)
  store.STORE_NBR,
  store.CITY_NAME,
  store.POSTAL_CODE,
  store.REGION_NBR,
  store.MARKET_AREA_NBR,
  store.format_code,
  store.division_nbr,
  store.SUBDIV_NAME,
  store.BANNER_CODE,
  store.BANNER_DESC,
  store.STORE_TYPE_CODE,
  store.STORE_TYPE_DESC,
  store.OPEN_STATUS_CODE,
  store.OPEN_STATUS_DESC,
  store.COUNTY_NAME,
  store.COUNTRY_CODE,
  store.STATE_PROV_CODE,
  store.LATITUDE_DGR,
  store.LONGITUDE_DGR

FROM amp_events amp

-- Inner join with calendar dimension (Tableau Cal_Dim_Data logic)
INNER JOIN walmart_calendar cal 
  ON amp.message_date = cal.CALENDAR_DATE

-- Inner join with store business units (Tableau Store Cur Data logic)
INNER JOIN store_business_units store 
  ON amp.store_number = store.STORE_NBR

-- Additional filters based on Tableau business logic
WHERE amp.message_date IS NOT NULL
  AND amp.store_number IS NOT NULL
  AND amp.business_area IS NOT NULL

ORDER BY 
  amp.message_date DESC,
  cal.WM_WEEK_NBR DESC,
  store.SUBDIV_NAME,
  amp.priority_level DESC;
