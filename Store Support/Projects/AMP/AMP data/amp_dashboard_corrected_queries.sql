-- ============================================================================
-- AMP ANALYSIS DASHBOARD - CORRECTED DATA MODEL
-- Primary Source: wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2
-- ============================================================================

-- ============================================================================
-- QUERY 1: Get AMP Events with Store Location Data
-- Joins AMP data with store dimension for Division/Region/Market
-- ============================================================================
CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support_Dev.Dashboard_AMP_With_Stores` AS

WITH amp_events AS (
  -- Get all AMP events from refined table
  SELECT
    event_id,
    Title,
    Activity_Title,
    FY,
    Week,
    WM_Week,
    WM_Year,
    Message_Type,
    Prim_Message_Type,
    Activity_Type,
    Status,
    Message_Status,
    store,
    Facility,
    Store_Cnt,
    Verification_Status,
    Store_Area,
    Target_Audience,
    Business_Area,
    Edit_Link,
    Web_Preview,
    Alignment,
    Division as Store_Format_Division,  -- This is the format (Div 1, etc)
    Region as AMP_Region,               -- May be placeholder
    Market as AMP_Market,               -- May be placeholder
    Store_Type,
    Author,
    Author_email,
    Created_Date,
    Last_Updated,
    Start_Date,
    End_Date,
    Keyword_Tags,
    Category,
    Hidden_Status,
    Legal_Status,
    Urgent_Activity,
    Priority,
    High_Impact,
    QTR
  FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
  WHERE Message_Type = 'Store Updates'
    AND Status LIKE '%Published%'
),

-- Join with Store Current Data for location info
store_locations AS (
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
    END AS SUBDIV_NAME,  -- This is the GEOGRAPHIC DIVISION for dashboard
    banner_code AS BANNER_CODE,
    banner_desc AS BANNER_DESC,
    bu_status_code AS OPEN_STATUS_CODE,
    bu_status_desc AS OPEN_STATUS_DESC,
    physical_county AS COUNTY_NAME,
    physical_country_code AS COUNTRY_CODE,
    physical_state_code AS STATE_PROV_CODE,
    LATITUDE AS LATITUDE_DGR,
    longitude AS LONGITUDE_DGR
  FROM `wmt-loc-cat-prod.catalog_location_views.businessunit_view`
  WHERE physical_country_code = 'US'
    AND base_division_desc = "WAL-MART STORES INC."
    AND bu_status_desc != 'CLOSED'
    AND Date(operational_open_start_date) <= date_add(current_date(), Interval 90 day)
),

-- Join AMP events with store locations
amp_with_stores AS (
  SELECT
    a.*,
    s.SUBDIV_NAME as Division,      -- Geographic division for dashboard
    s.REGION_NBR as Region,           -- Actual region number
    s.MARKET_AREA_NBR as Market,      -- Actual market number
    s.CITY_NAME,
    s.STATE_PROV_CODE,
    s.POSTAL_CODE,
    s.BANNER_DESC,
    s.format_code,
    s.LATITUDE_DGR,
    s.LONGITUDE_DGR
  FROM amp_events a
  LEFT JOIN store_locations s
    ON CAST(a.store AS NUMERIC) = s.STORE_NBR
)

SELECT * FROM amp_with_stores;


-- ============================================================================
-- QUERY 2: Join with Alignment-Specific Store Data (Div 1 + Div 10)
-- For filtering by Store vs H&W alignment
-- ============================================================================
CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support_Dev.Dashboard_AMP_With_Alignment` AS

WITH store_div1 AS (
  -- Division 1 - WM US Stores
  SELECT
    CAST(business_unit_nbr AS NUMERIC) AS STORE_NBR,
    'Store' AS Alignment,
    division_nbr,
    division_name,
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
    region_code AS REGION_NBR,
    martket_code AS MARKET_AREA_NBR
  FROM `wmt-loc-cat-prod.catalog_location_views.division_view`
  WHERE physical_country_code = 'US'
    AND base_division_desc = "WAL-MART STORES INC."
    AND division_nbr = 1
    AND bu_status_desc != 'CLOSED'
    AND Date(new_bu_start_date) <= date_add(current_date(), Interval 90 day)
),

store_div10 AS (
  -- Division 10 - H&W (Pharmacy)
  SELECT
    CAST(business_unit_nbr AS NUMERIC) AS STORE_NBR,
    'H&W' AS Alignment,
    division_nbr,
    division_name,
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
    region_code AS REGION_NBR,
    martket_code AS MARKET_AREA_NBR
  FROM `wmt-loc-cat-prod.catalog_location_views.division_view`
  WHERE physical_country_code = 'US'
    AND base_division_desc = "WAL-MART STORES INC."
    AND division_nbr = 10
    AND bu_status_desc != 'CLOSED'
    AND Date(new_bu_start_date) <= date_add(current_date(), Interval 90 day)
),

combined_alignment AS (
  SELECT * FROM store_div1
  UNION ALL
  SELECT * FROM store_div10
)

SELECT
  a.*,
  s.Alignment as Store_Alignment,  -- Store vs H&W for filtering
  s.division_nbr,
  s.division_name
FROM `wmt-assetprotection-prod.Store_Support_Dev.Dashboard_AMP_With_Stores` a
LEFT JOIN combined_alignment s
  ON CAST(a.store AS NUMERIC) = s.STORE_NBR;


-- ============================================================================
-- QUERY 3: Aggregate Click Data - Audience Breakdown
-- Join Current + Historical audience click data
-- ============================================================================
CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support_Dev.Click_Data_Audience_Agg` AS

WITH audience_current AS (
  SELECT
    Event_ID,
    FY,
    Week,
    Audience,
    SUM(Clicks) as Total_Clicks
  FROM `wmt-assetprotection-prod.Store_Support_Dev.Audience Breakdown Cur`
  GROUP BY Event_ID, FY, Week, Audience
),

audience_historical AS (
  SELECT
    Event_ID,
    FY,
    Week,
    Audience,
    SUM(Clicks) as Total_Clicks
  FROM `wmt-assetprotection-prod.Store_Support_Dev.Audience Breakdown Historical`
  GROUP BY Event_ID, FY, Week, Audience
)

SELECT
  Event_ID,
  FY,
  Week,
  Audience,
  SUM(Total_Clicks) as Audience_Total_Clicks
FROM (
  SELECT * FROM audience_current
  UNION ALL
  SELECT * FROM audience_historical
)
GROUP BY Event_ID, FY, Week, Audience;


-- ============================================================================
-- QUERY 4: Aggregate Click Data - Device Types
-- Join Current + Historical device click data
-- ============================================================================
CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support_Dev.Click_Data_Devices_Agg` AS

WITH devices_current AS (
  SELECT
    Event_ID,
    FY,
    Week,
    Device_Type,
    SUM(Clicks) as Total_Clicks
  FROM `wmt-assetprotection-prod.Store_Support_Dev.Device Types Cur`
  GROUP BY Event_ID, FY, Week, Device_Type
),

devices_historical AS (
  SELECT
    Event_ID,
    FY,
    Week,
    Device_Type,
    SUM(Clicks) as Total_Clicks
  FROM `wmt-assetprotection-prod.Store_Support_Dev.Device Types Historical`
  GROUP BY Event_ID, FY, Week, Device_Type
)

SELECT
  Event_ID,
  FY,
  Week,
  Device_Type,
  SUM(Total_Clicks) as Device_Total_Clicks
FROM (
  SELECT * FROM devices_current
  UNION ALL
  SELECT * FROM devices_historical
)
GROUP BY Event_ID, FY, Week, Device_Type;


-- ============================================================================
-- QUERY 5: Aggregate Click Data - Time Spent
-- Join Current + Historical time spent data
-- ============================================================================
CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support_Dev.Click_Data_TimeSpent_Agg` AS

WITH time_current AS (
  SELECT
    Event_ID,
    FY,
    Week,
    Time_Range,
    SUM(Clicks) as Total_Clicks
  FROM `wmt-assetprotection-prod.Store_Support_Dev.Time Spent Cur`
  GROUP BY Event_ID, FY, Week, Time_Range
),

time_historical AS (
  SELECT
    Event_ID,
    FY,
    Week,
    Time_Range,
    SUM(Clicks) as Total_Clicks
  FROM `wmt-assetprotection-prod.Store_Support_Dev.Time Spent Historical`
  GROUP BY Event_ID, FY, Week, Time_Range
)

SELECT
  Event_ID,
  FY,
  Week,
  Time_Range,
  SUM(Total_Clicks) as Time_Total_Clicks
FROM (
  SELECT * FROM time_current
  UNION ALL
  SELECT * FROM time_historical
)
GROUP BY Event_ID, FY, Week, Time_Range;


-- ============================================================================
-- QUERY 6: FINAL DASHBOARD VIEW
-- Combines AMP events + stores + alignment + click data
-- ============================================================================
CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support_Dev.Dashboard_AMP_Analysis_Final` AS

SELECT
  -- Event Core Info
  a.event_id,
  a.Title,
  a.FY,
  a.Week,
  a.Message_Type,
  a.Activity_Type,
  a.Status,
  
  -- Location Info (from store dimension)
  a.Division,              -- Geographic division (East BU, West BU, etc)
  a.Region,                -- Region number
  a.Market,                -- Market number
  a.store,
  a.Store_Cnt,
  
  -- Links
  a.Edit_Link,
  a.Web_Preview as Preview_Link,
  
  -- Additional Fields
  a.Verification_Status,
  a.Store_Area,
  a.Target_Audience as Audience,
  a.Business_Area,
  a.Store_Alignment,       -- Store vs H&W alignment filter
  
  -- Dates
  a.Start_Date,
  a.End_Date,
  a.Created_Date,
  a.Last_Updated,
  
  -- Click Data (aggregated)
  STRING_AGG(DISTINCT aud.Audience, ', ') as Audience_Breakdown,
  SUM(aud.Audience_Total_Clicks) as Total_Audience_Clicks,
  
  STRING_AGG(DISTINCT dev.Device_Type, ', ') as Device_Types,
  SUM(dev.Device_Total_Clicks) as Total_Device_Clicks,
  
  STRING_AGG(DISTINCT tm.Time_Range, ', ') as Time_Ranges,
  SUM(tm.Time_Total_Clicks) as Total_Time_Clicks,
  
  -- Metadata
  a.Author,
  a.QTR,
  a.Priority,
  a.High_Impact,
  CURRENT_TIMESTAMP() as Refresh_Timestamp

FROM `wmt-assetprotection-prod.Store_Support_Dev.Dashboard_AMP_With_Alignment` a

-- Join click data
LEFT JOIN `wmt-assetprotection-prod.Store_Support_Dev.Click_Data_Audience_Agg` aud
  ON a.event_id = aud.Event_ID 
  AND CAST(a.FY AS STRING) = CAST(aud.FY AS STRING)
  AND CAST(a.Week AS STRING) = CAST(aud.Week AS STRING)

LEFT JOIN `wmt-assetprotection-prod.Store_Support_Dev.Click_Data_Devices_Agg` dev
  ON a.event_id = dev.Event_ID
  AND CAST(a.FY AS STRING) = CAST(dev.FY AS STRING)
  AND CAST(a.Week AS STRING) = CAST(dev.Week AS STRING)

LEFT JOIN `wmt-assetprotection-prod.Store_Support_Dev.Click_Data_TimeSpent_Agg` tm
  ON a.event_id = tm.Event_ID
  AND CAST(a.FY AS STRING) = CAST(tm.FY AS STRING)
  AND CAST(a.Week AS STRING) = CAST(tm.Week AS STRING)

GROUP BY
  a.event_id, a.Title, a.FY, a.Week, a.Message_Type, a.Activity_Type, a.Status,
  a.Division, a.Region, a.Market, a.store, a.Store_Cnt,
  a.Edit_Link, a.Web_Preview, a.Verification_Status, a.Store_Area,
  a.Target_Audience, a.Business_Area, a.Store_Alignment,
  a.Start_Date, a.End_Date, a.Created_Date, a.Last_Updated,
  a.Author, a.QTR, a.Priority, a.High_Impact;


-- ============================================================================
-- QUERY 7: Dashboard Summary Stats
-- Provides counts and metrics for dashboard filters
-- ============================================================================
CREATE OR REPLACE VIEW `wmt-assetprotection-prod.Store_Support_Dev.Dashboard_Summary_Stats` AS

SELECT
  COUNT(DISTINCT event_id) as Total_Events,
  COUNT(DISTINCT Division) as Total_Divisions,
  COUNT(DISTINCT Region) as Total_Regions,
  COUNT(DISTINCT Market) as Total_Markets,
  SUM(Store_Cnt) as Total_Store_Impacts,
  COUNT(DISTINCT CASE WHEN Store_Alignment = 'Store' THEN event_id END) as Store_Events,
  COUNT(DISTINCT CASE WHEN Store_Alignment = 'H&W' THEN event_id END) as HW_Events,
  SUM(Total_Audience_Clicks) as Total_Audience_Clicks,
  SUM(Total_Device_Clicks) as Total_Device_Clicks,
  SUM(Total_Time_Clicks) as Total_Time_Clicks,
  MAX(Refresh_Timestamp) as Last_Refresh
FROM `wmt-assetprotection-prod.Store_Support_Dev.Dashboard_AMP_Analysis_Final`;
