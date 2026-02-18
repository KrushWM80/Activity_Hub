-- =====================================================
-- AMP Analysis Dashboard - Data Integration Queries
-- Purpose: Join AMP event data with click engagement data
-- Last Updated: February 11, 2026
-- =====================================================

-- =====================================================
-- 1. PRIMARY AMP DATA INTEGRATION
-- Join Current and Historical AMP data, deduplicated by Event_ID, FY, Week
-- =====================================================

CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support_Dev.AMP_Combined_Events` AS
WITH current_events AS (
  SELECT
    event_id,
    activity_title,
    fy,
    wm_week,
    message_type,
    activity_type,
    message_status,
    division,
    region,
    market,
    store,
    edit_link,
    preview_link,
    count_of_stores,
    status,
    store_area,
    audience,
    business_area,
    created_date,
    modified_date,
    'Current' AS data_source,
    ROW_NUMBER() OVER (PARTITION BY event_id, fy, wm_week ORDER BY modified_date DESC) AS rn
  FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
  WHERE event_id IS NOT NULL
),
historical_events AS (
  SELECT
    event_id,
    activity_title,
    fy,
    wm_week,
    message_type,
    activity_type,
    message_status,
    division,
    region,
    market,
    store,
    edit_link,
    preview_link,
    count_of_stores,
    status,
    store_area,
    audience,
    business_area,
    created_date,
    modified_date,
    'Historical' AS data_source,
    ROW_NUMBER() OVER (PARTITION BY event_id, fy, wm_week ORDER BY modified_date DESC) AS rn
  FROM `wmt-edw-prod.{TABLEAU_PREP_PROD_SCHEMA}.Output - AMP 2.0 Historic`
  WHERE event_id IS NOT NULL
),
combined AS (
  SELECT * FROM current_events WHERE rn = 1
  UNION ALL
  SELECT * FROM historical_events WHERE rn = 1
    AND CONCAT(event_id, '-', fy, '-', wm_week) 
    NOT IN (SELECT CONCAT(event_id, '-', fy, '-', wm_week) FROM current_events WHERE rn = 1)
)
SELECT
  DISTINCT
  event_id,
  activity_title,
  fy,
  wm_week,
  message_type,
  activity_type,
  message_status,
  division,
  region,
  market,
  store,
  edit_link,
  preview_link,
  count_of_stores,
  status,
  store_area,
  audience,
  business_area,
  created_date,
  modified_date,
  data_source
FROM combined
WHERE message_type = 'Store Update'
  AND message_status = 'Published';

-- =====================================================
-- 2. CLICK DATA AGGREGATION - AUDIENCE BREAKDOWN
-- Aggregate audience breakdown data by Event_ID
-- =====================================================

CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support_Dev.Click_Data_Audience_Agg` AS
WITH audience_current AS (
  SELECT
    event_id,
    audience_segment,
    click_count,
    view_count,
    fy,
    wm_week,
    'Current' AS data_source
  FROM `wmt-assetprotection-prod.Store_Support_Dev.Audience Breakdown Cur`
),
audience_historical AS (
  SELECT
    event_id,
    audience_segment,
    click_count,
    view_count,
    fy,
    wm_week,
    'Historical' AS data_source
  FROM `wmt-assetprotection-prod.Store_Support_Dev.Audience Breakdown Historical`
),
combined_audience AS (
  SELECT * FROM audience_current
  UNION ALL
  SELECT * FROM audience_historical
)
SELECT
  event_id,
  fy,
  wm_week,
  SUM(click_count) AS total_audience_clicks,
  SUM(view_count) AS total_audience_views,
  COUNT(DISTINCT audience_segment) AS audience_segment_count,
  STRING_AGG(DISTINCT audience_segment, ', ' ORDER BY audience_segment) AS audience_segments
FROM combined_audience
WHERE event_id IS NOT NULL
GROUP BY event_id, fy, wm_week;

-- =====================================================
-- 3. CLICK DATA AGGREGATION - DEVICE TYPES
-- Aggregate device type data by Event_ID
-- =====================================================

CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support_Dev.Click_Data_Devices_Agg` AS
WITH devices_current AS (
  SELECT
    event_id,
    device_type,
    click_count,
    view_count,
    fy,
    wm_week,
    'Current' AS data_source
  FROM `wmt-assetprotection-prod.Store_Support_Dev.Device Types Cur`
),
devices_historical AS (
  SELECT
    event_id,
    device_type,
    click_count,
    view_count,
    fy,
    wm_week,
    'Historical' AS data_source
  FROM `wmt-assetprotection-prod.Store_Support_Dev.Device Types Historical`
),
combined_devices AS (
  SELECT * FROM devices_current
  UNION ALL
  SELECT * FROM devices_historical
)
SELECT
  event_id,
  fy,
  wm_week,
  SUM(click_count) AS total_device_clicks,
  SUM(view_count) AS total_device_views,
  COUNT(DISTINCT device_type) AS device_type_count,
  STRING_AGG(DISTINCT device_type, ', ' ORDER BY device_type) AS device_types
FROM combined_devices
WHERE event_id IS NOT NULL
GROUP BY event_id, fy, wm_week;

-- =====================================================
-- 4. CLICK DATA AGGREGATION - TIME SPENT
-- Aggregate time spent data by Event_ID
-- =====================================================

CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support_Dev.Click_Data_TimeSpent_Agg` AS
WITH timespent_current AS (
  SELECT
    event_id,
    duration_seconds,
    click_count,
    view_count,
    fy,
    wm_week,
    'Current' AS data_source
  FROM `wmt-assetprotection-prod.Store_Support_Dev.Time Spent Cur`
),
timespent_historical AS (
  SELECT
    event_id,
    duration_seconds,
    click_count,
    view_count,
    fy,
    wm_week,
    'Historical' AS data_source
  FROM `wmt-assetprotection-prod.Store_Support_Dev.Time Spent Historical`
),
combined_timespent AS (
  SELECT * FROM timespent_current
  UNION ALL
  SELECT * FROM timespent_historical
)
SELECT
  event_id,
  fy,
  wm_week,
  SUM(click_count) AS total_time_clicks,
  SUM(view_count) AS total_time_views,
  AVG(duration_seconds) AS avg_duration_seconds,
  MAX(duration_seconds) AS max_duration_seconds,
  MIN(duration_seconds) AS min_duration_seconds
FROM combined_timespent
WHERE event_id IS NOT NULL
GROUP BY event_id, fy, wm_week;

-- =====================================================
-- 5. COMPLETE ANALYSIS DASHBOARD VIEW
-- Final joined dataset for dashboard consumption
-- =====================================================

CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support_Dev.Dashboard_AMP_Analysis` AS
SELECT
  -- Event Identifiers
  e.event_id,
  e.fy,
  e.wm_week,
  
  -- Event Details
  e.activity_title,
  e.message_type,
  e.activity_type,
  e.message_status,
  e.status,
  
  -- Location/Business Hierarchy
  e.division,
  e.region,
  e.market,
  e.store,
  e.store_area,
  e.audience,
  e.business_area,
  
  -- Store Counts
  e.count_of_stores AS total_store_count,
  
  -- Click Engagement Metrics
  COALESCE(aud.total_audience_clicks, 0) AS total_audience_clicks,
  COALESCE(aud.total_audience_views, 0) AS total_audience_views,
  COALESCE(aud.audience_segment_count, 0) AS audience_segment_count,
  aud.audience_segments,
  
  COALESCE(dev.total_device_clicks, 0) AS total_device_clicks,
  COALESCE(dev.total_device_views, 0) AS total_device_views,
  COALESCE(dev.device_type_count, 0) AS device_type_count,
  dev.device_types,
  
  COALESCE(ts.total_time_clicks, 0) AS total_time_clicks,
  COALESCE(ts.total_time_views, 0) AS total_time_views,
  COALESCE(ts.avg_duration_seconds, 0) AS avg_duration_seconds,
  COALESCE(ts.max_duration_seconds, 0) AS max_duration_seconds,
  
  -- Total Clicks Across All Sources
  COALESCE(aud.total_audience_clicks, 0) + 
  COALESCE(dev.total_device_clicks, 0) + 
  COALESCE(ts.total_time_clicks, 0) AS total_clicks,
  
  -- Links
  e.edit_link,
  e.preview_link,
  
  -- Metadata
  e.created_date,
  e.modified_date,
  e.data_source,
  CURRENT_TIMESTAMP() AS dashboard_refresh_timestamp
  
FROM `wmt-assetprotection-prod.Store_Support_Dev.AMP_Combined_Events` e
LEFT JOIN `wmt-assetprotection-prod.Store_Support_Dev.Click_Data_Audience_Agg` aud
  ON e.event_id = aud.event_id 
  AND e.fy = aud.fy 
  AND e.wm_week = aud.wm_week
LEFT JOIN `wmt-assetprotection-prod.Store_Support_Dev.Click_Data_Devices_Agg` dev
  ON e.event_id = dev.event_id 
  AND e.fy = dev.fy 
  AND e.wm_week = dev.wm_week
LEFT JOIN `wmt-assetprotection-prod.Store_Support_Dev.Click_Data_TimeSpent_Agg` ts
  ON e.event_id = ts.event_id 
  AND e.fy = ts.fy 
  AND e.wm_week = ts.wm_week
WHERE e.message_type = 'Store Update'
  AND e.message_status = 'Published';

-- =====================================================
-- 6. VERIFICATION STATUS AGGREGATION (if applicable)
-- Count Complete vs Incomplete verification status
-- =====================================================

CREATE OR REPLACE VIEW `wmt-assetprotection-prod.Store_Support_Dev.Verification_Status_Summary` AS
SELECT
  event_id,
  fy,
  wm_week,
  COUNTIF(status = 'Complete') AS complete_count,
  COUNTIF(status = 'Incomplete') AS incomplete_count,
  COUNT(*) AS total_status_records,
  ROUND(COUNTIF(status = 'Complete') / COUNT(*) * 100, 2) AS complete_percentage
FROM `wmt-assetprotection-prod.Store_Support_Dev.Dashboard_AMP_Analysis`
WHERE status IN ('Complete', 'Incomplete')
GROUP BY event_id, fy, wm_week;

-- =====================================================
-- 7. Admin Query - Pre-filter Status Check
-- View current pre-filter configuration
-- =====================================================

CREATE OR REPLACE VIEW `wmt-assetprotection-prod.Store_Support_Dev.Admin_Prefilter_Status` AS
SELECT
  'Message Type: Store Update' AS prefilter_type,
  COUNT(DISTINCT event_id) AS record_count,
  MIN(modified_date) AS earliest_record,
  MAX(modified_date) AS latest_record
FROM `wmt-assetprotection-prod.Store_Support_Dev.Dashboard_AMP_Analysis`
WHERE message_type = 'Store Update'
UNION ALL
SELECT
  'Status: Published' AS prefilter_type,
  COUNT(DISTINCT event_id) AS record_count,
  MIN(modified_date) AS earliest_record,
  MAX(modified_date) AS latest_record
FROM `wmt-assetprotection-prod.Store_Support_Dev.Dashboard_AMP_Analysis`
WHERE message_status = 'Published'
UNION ALL
SELECT
  'Combined Prefilter' AS prefilter_type,
  COUNT(DISTINCT event_id) AS record_count,
  MIN(modified_date) AS earliest_record,
  MAX(modified_date) AS latest_record
FROM `wmt-assetprotection-prod.Store_Support_Dev.Dashboard_AMP_Analysis`
WHERE message_type = 'Store Update' 
  AND message_status = 'Published';

-- =====================================================
-- NOTES FOR DASHBOARD QUERIES
-- =====================================================
-- Replace {TABLEAU_PREP_PROD_SCHEMA} with actual schema path from Tableau Prep Prod
-- All queries join on: event_id, fy (FY), wm_week (Week)
-- Pre-filter applied: message_type = 'Store Update' AND message_status = 'Published'
-- Time-based deduplication: Uses most recent modified_date for ties
-- All click data aggregation handles both Current and Historical sources
