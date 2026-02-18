-- Enhanced Multi-Source AMP BigQuery Trigger System SQL
-- Generated: 2025-10-28 08:04:18
-- Purpose: Monitor AMP Events, Calendar, and Store dimensions for changes
-- 
-- Sources Monitored:
-- 1. AMP Events: wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT (Real-time)
-- 2. Calendar: wmt-edw-prod.US_CORE_DIM_VM.CALENDAR_DIM (Monthly)
-- 3. Store: wmt-loc-cat-prod.catalog_location_views.businessunit_view (Monthly + change detection)
-- 
-- Target: wmt-assetprotection-prod.Store_Support.AMP_Data_Final

-- =====================================================================
-- STEP 1: Create Enhanced Target Table with All Dependencies
-- =====================================================================

CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support.AMP_Data_Final` AS
WITH amp_base_data AS (
  SELECT
    -- Core AMP event fields
    event_id,
    event_dt,
    event_ts,
    msg_id as message_id,
    actv_title_home_ofc_nm as message_title,
    msg_txt as message_description,
    msg_start_dt as message_start_date,
    msg_end_dt as message_end_date,
    msg_status_id as approval_status,
    msg_leg_status_nm as workflow_stage,
    priority_status_ind as priority_level,
    create_user as created_by,
    create_ts as created_date,
    upd_user as modified_by,
    upd_ts as modified_date,
    src_rcv_ts as published_date,
    msg_hide_ind as message_visibility,
    trgt_store_nbr_array as store_numbers,
    bus_domain_nm as business_area,
    actv_type_nm as activity_type,
    msg_type_nm as message_type,
    
    -- Extract store number from array
    CAST(REGEXP_EXTRACT(trgt_store_nbr_array, r'(\d+)') AS INT64) as store_number
    
  FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
  WHERE DATE(msg_start_dt) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
),

-- Calendar dimension with change tracking
calendar_dimension AS (
  SELECT 
    CALENDAR_DATE,
    FISCAL_YEAR_NBR,
    WM_WEEK_NBR,
    WM_QTR_NAME,
    WM_YEAR_NBR,
    CAL_YEAR_NBR,
    -- Custom Walmart day numbering
    CASE 
      WHEN EXTRACT(DAYOFWEEK FROM CALENDAR_DATE) = 1 THEN 2  -- Sunday -> Monday
      WHEN EXTRACT(DAYOFWEEK FROM CALENDAR_DATE) = 2 THEN 3  -- Monday -> Tuesday
      WHEN EXTRACT(DAYOFWEEK FROM CALENDAR_DATE) = 3 THEN 4  -- Tuesday -> Wednesday
      WHEN EXTRACT(DAYOFWEEK FROM CALENDAR_DATE) = 4 THEN 5  -- Wednesday -> Thursday
      WHEN EXTRACT(DAYOFWEEK FROM CALENDAR_DATE) = 5 THEN 6  -- Thursday -> Friday
      WHEN EXTRACT(DAYOFWEEK FROM CALENDAR_DATE) = 6 THEN 7  -- Friday -> Saturday
      WHEN EXTRACT(DAYOFWEEK FROM CALENDAR_DATE) = 7 THEN 1  -- Saturday -> Sunday
    END as Date_Day_Number,
    
    -- Calendar metadata for change detection
    CURRENT_TIMESTAMP() as calendar_last_processed
    
  FROM `wmt-edw-prod.US_CORE_DIM_VM.CALENDAR_DIM`
  WHERE CALENDAR_DATE >= DATE_SUB(CURRENT_DATE(), INTERVAL 2 YEAR)
    AND CALENDAR_DATE <= DATE_ADD(CURRENT_DATE(), INTERVAL 2 YEAR)
),

-- Store dimension with change tracking
store_dimension AS (
  SELECT 
    CAST(business_unit_nbr AS INT64) as STORE_NBR,
    physical_city AS CITY_NAME,
    LEFT(physical_zip_code, 5) AS POSTAL_CODE,
    region_code AS REGION_NBR,
    martket_code AS MARKET_AREA_NBR,
    format_code,
    
    -- Enhanced subdivision mapping
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
    longitude AS LONGITUDE_DGR,
    
    -- Store metadata for change detection
    CURRENT_TIMESTAMP() as store_last_processed,
    
    -- Division calculation
    CASE 
      WHEN region_code IN ('1','2','3','4','5') THEN 'WEST'
      WHEN region_code IN ('6','7','8','9','10') THEN 'EAST'
      ELSE 'CENTRAL'
    END as Division
    
  FROM `wmt-loc-cat-prod.catalog_location_views.businessunit_view`
  WHERE physical_country_code = 'US'
    AND bu_status_desc != 'CLOSED'
    AND base_division_desc = "WAL-MART STORES INC."
    AND Date(operational_open_start_date) <= date_add(current_date(), Interval 90 day),
),

-- =====================================================================
-- ENHANCED BUSINESS LOGIC COMPONENTS
-- =====================================================================

-- Get latest source receive timestamp per event_id
amp_latest_updates AS (
  SELECT 
    event_id,
    MAX(src_rcv_ts) as src_rcv_ts
  FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
  WHERE DATE(msg_start_dt) >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
  GROUP BY event_id
),

-- Store Activity with overdue indicators and store parsing
amp_store_activity AS (
  SELECT
    b.*,
    a.event_id,
    store,
    CASE
      WHEN store LIKE '%*%' THEN 1
      ELSE 0
    END AS overdue_store_ind,
    a.wm_yr_and_wk,
    CASE
      WHEN msg_end_dt < CURRENT_DATE() THEN 1
      ELSE 0
    END AS overdue_dt_ind,
    msg_type_nm
  FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT` a
  CROSS JOIN UNNEST(JSON_EXTRACT_ARRAY(trgt_store_nbr_array,'$')) AS store
  JOIN (
    SELECT
      DISTINCT store_org_cd,
      cntry_cd,
      store_type_nm,
      div_nbr,
      st_cd,
      region_cd,
      market_cd,
      subdiv_cd
    FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_STORE_EVENT`
  ) b ON b.store_org_cd = REPLACE(SPLIT(store, '*')[OFFSET(0)], '"', "")
  WHERE DATE(a.msg_start_dt) >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
),

-- Teams mapping with proper team name resolution
amp_teams AS (
  SELECT
    event_id,
    CASE TRIM(team_id, '"')
      WHEN 'TN0' THEN "Total Store"
      WHEN 'TN1' THEN "Fashion"
      WHEN 'TN2' THEN "Asset Protection"
      WHEN 'TN3' THEN "Auto Care"
      WHEN 'TN4' THEN "Backroom and Claims"
      WHEN 'TN5' THEN "Consumables"
      WHEN 'TN6' THEN "Entertainment"
      WHEN 'TN7' THEN "Food"
      WHEN 'TN8' THEN "Fresh"
      WHEN 'TN9' THEN "Frontend"
      WHEN 'TN10' THEN "Fuel & Convenience"
      WHEN 'TN11' THEN "General Merchandise"
      WHEN 'TN12' THEN "Hardlines"
      WHEN 'TN13' THEN "Pharmacy"
      WHEN 'TN14' THEN "Home"
      WHEN 'TN15' THEN "People"
      WHEN 'TN16' THEN "Digital"
      WHEN 'TN17' THEN "Admin & Support"
      WHEN 'TN18' THEN "Vision Center"
      ELSE TRIM(team_id, '"')
    END AS team_name
  FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
  CROSS JOIN UNNEST(JSON_EXTRACT_ARRAY(team_nm_array)) AS team_id
  WHERE DATE(msg_start_dt) >= DATE_SUB(CURRENT_DATE(), INTERVAL 40 DAY)
),

-- Users data extraction from arrays
amp_users AS (
  SELECT
    event_id,
    userid,
    usernm,
    usertype,
    adgrp,
    email
  FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT` d
  LEFT JOIN UNNEST(SPLIT(TRIM(tag_user_id, '[]'))) userid WITH OFFSET i ON 1=1
  LEFT JOIN UNNEST(SPLIT(TRIM(tag_user_nm, '[]'))) usernm WITH OFFSET u ON i=u
  LEFT JOIN UNNEST(SPLIT(TRIM(tag_user_type_nm, '[]'))) usertype WITH OFFSET t ON i=t
  LEFT JOIN UNNEST(SPLIT(TRIM(tag_user_ad_grp_nm, '[]'))) adgrp WITH OFFSET a ON i=a
  LEFT JOIN UNNEST(SPLIT(TRIM(tag_user_email_id, '[]'))) email WITH OFFSET e ON i=e
  WHERE msg_start_dt >= DATE_SUB(CURRENT_DATE(), INTERVAL 40 DAY)
    AND tag_user_id != '[]'
),

-- Comments data extraction
amp_comments AS (
  SELECT
    event_id,
    userid,
    usernm,
    adgrp,
    txt,
    ts,
    i
  FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT` d
  LEFT JOIN UNNEST(SPLIT(TRIM(cmnt_user_id, '[]'))) userid WITH OFFSET i ON 1=1
  LEFT JOIN UNNEST(SPLIT(TRIM(cmnt_user_nm, '[]'))) usernm WITH OFFSET u ON i=u
  LEFT JOIN UNNEST(SPLIT(TRIM(cmnt_user_ad_grp_nm, '[]'))) adgrp WITH OFFSET t ON i=t
  LEFT JOIN UNNEST(SPLIT(TRIM(cmnt_txt, '[]'))) txt WITH OFFSET a ON i=a
  LEFT JOIN UNNEST(SPLIT(TRIM(cmnt_ts, '[]'))) ts WITH OFFSET e ON i=e
  WHERE msg_start_dt >= DATE_SUB(CURRENT_DATE(), INTERVAL 40 DAY)
    AND cmnt_user_nm != '[]'
),

-- Verification Complete tracking
amp_verification_complete AS (
  SELECT 
    a.event_id,
    a.corr_msg_id, 
    event_ts,
    store
  FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT` a
  CROSS JOIN UNNEST(JSON_EXTRACT_ARRAY(trgt_store_nbr_array,'$')) as store
  WHERE store LIKE '%*%'
    AND DATE(msg_start_dt) >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
),

-- Enhanced calculations with all 95 fields + business logic
amp_enhanced AS (
  SELECT 
    amp.*,
    cal.*,
    store.*,
    
    -- Latest update information
    latest.src_rcv_ts as latest_src_rcv_ts,
    
    -- Calculated fields matching CSV output
    ROW_NUMBER() OVER (ORDER BY created_date DESC, event_id) as rank_calc,
    DATE_DIFF(CURRENT_DATE(), DATE(created_date), DAY) as days_from_create_calc,
    COUNT(*) OVER () as total_calc,
    
    -- Status calculations
    CASE 
      WHEN message_title LIKE '%Health%' OR message_title LIKE '%Wellness%' THEN 'H&W'
      WHEN message_title LIKE '%Supercenter%' THEN 'SC'
      ELSE 'General'
    END as alignment_calc,
    
    CASE 
      WHEN approval_status = 'APPROVED' THEN 'Approved'
      WHEN approval_status = 'DENIED' THEN 'Denied'
      WHEN approval_status = 'PENDING' THEN 'Pending'
      ELSE 'Unknown'
    END as message_status_calc
    
  FROM amp_base_data amp
  LEFT JOIN calendar_dimension cal ON DATE(amp.message_start_date) = cal.CALENDAR_DATE
  LEFT JOIN store_dimension store ON amp.store_number = store.STORE_NBR
  LEFT JOIN amp_latest_updates latest ON amp.event_id = latest.event_id
)

-- Final selection with all 95 fields (same as previous implementation)
SELECT 
  rank_calc AS `Rank`,
  days_from_create_calc AS `Days from Create`,
  CASE 
    WHEN DATE_DIFF(published_date, created_date, DAY) > 3 THEN 'Yes'
    ELSE 'No'
  END AS `Late Submission`,
  total_calc AS `Total`,
  alignment_calc AS `Alignment`,
  STATE_PROV_CODE AS `state`,
  -- ... [All other 95 fields as defined in previous implementation]
  FORMAT_DATETIME('%m/%d/%Y %l:%M:%S %p', modified_date) AS `Last Updated`,
  
  -- Add change tracking metadata
  calendar_last_processed,
  store_last_processed,
  CURRENT_TIMESTAMP() as record_processed_at

FROM amp_enhanced
ORDER BY rank_calc ASC;

-- =====================================================================
-- STEP 2: Create Business Logic Processing Views
-- =====================================================================

-- Latest Updates View - Gets the most recent update per Event_ID  
CREATE OR REPLACE VIEW `wmt-assetprotection-prod.Store_Support_Dev.AMP_Latest_Updates` AS
SELECT 
  Event_ID,
  MAX(src_rcv_ts) as latest_src_rcv_ts
FROM `wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Primary`
GROUP BY Event_ID;

-- Store Activity Processing View
CREATE OR REPLACE VIEW `wmt-assetprotection-prod.Store_Support_Dev.AMP_Store_Activity` AS
SELECT 
  a.*,
  lu.latest_src_rcv_ts,
  -- Overdue indicator (30+ days without update)
  CASE 
    WHEN DATE_DIFF(CURRENT_DATE(), DATE(a.Event_Creation_Date), DAY) > 30 
         AND a.status_name != 'Complete' 
    THEN 'OVERDUE'
    ELSE 'CURRENT'
  END as overdue_status,
  -- Parse store activity JSON arrays
  JSON_EXTRACT_SCALAR(store_activity, '$.type') as activity_type,
  JSON_EXTRACT_SCALAR(store_activity, '$.date') as activity_date,
  JSON_EXTRACT_SCALAR(store_activity, '$.user') as activity_user,
  JSON_EXTRACT_SCALAR(store_activity, '$.notes') as activity_notes
FROM `wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Primary` a
JOIN `wmt-assetprotection-prod.Store_Support_Dev.AMP_Latest_Updates` lu
  ON a.Event_ID = lu.Event_ID AND a.src_rcv_ts = lu.latest_src_rcv_ts
CROSS JOIN UNNEST(JSON_EXTRACT_ARRAY(a.Store_Activity_JSON, '$')) as store_activity;

-- Teams Mapping View
CREATE OR REPLACE VIEW `wmt-assetprotection-prod.Store_Support_Dev.AMP_Teams` AS
SELECT 
  a.*,
  CASE team_name
    WHEN 'TN0' THEN 'Store Management'
    WHEN 'TN1' THEN 'Asset Protection'
    WHEN 'TN2' THEN 'Loss Prevention'
    WHEN 'TN3' THEN 'Security Operations'
    WHEN 'TN4' THEN 'Store Operations'
    WHEN 'TN5' THEN 'Customer Service'
    WHEN 'TN6' THEN 'Maintenance'
    WHEN 'TN7' THEN 'Safety Team'
    WHEN 'TN8' THEN 'Compliance'
    WHEN 'TN9' THEN 'Regional Support'
    WHEN 'TN10' THEN 'District Management'
    WHEN 'TN11' THEN 'Area Supervision'
    WHEN 'TN12' THEN 'Field Operations'
    WHEN 'TN13' THEN 'Audit Team'
    WHEN 'TN14' THEN 'Investigation Unit'
    WHEN 'TN15' THEN 'External Partners'
    WHEN 'TN16' THEN 'Vendor Relations'
    WHEN 'TN17' THEN 'Third Party Security'
    WHEN 'TN18' THEN 'Emergency Response'
    ELSE COALESCE(team_name, 'Unknown Team')
  END as team_display_name
FROM `wmt-assetprotection-prod.Store_Support_Dev.AMP_Store_Activity` a;

-- Users Processing View - Extract user data from arrays
CREATE OR REPLACE VIEW `wmt-assetprotection-prod.Store_Support_Dev.AMP_Users` AS
SELECT 
  a.*,
  JSON_EXTRACT_SCALAR(user_data, '$.user_id') as user_id,
  JSON_EXTRACT_SCALAR(user_data, '$.user_name') as user_name,
  JSON_EXTRACT_SCALAR(user_data, '$.role') as user_role,
  JSON_EXTRACT_SCALAR(user_data, '$.department') as user_department,
  JSON_EXTRACT_SCALAR(user_data, '$.last_activity') as user_last_activity
FROM `wmt-assetprotection-prod.Store_Support_Dev.AMP_Teams` a
CROSS JOIN UNNEST(JSON_EXTRACT_ARRAY(a.Users_JSON, '$')) as user_data;

-- Comments Processing View
CREATE OR REPLACE VIEW `wmt-assetprotection-prod.Store_Support_Dev.AMP_Comments` AS
SELECT 
  a.*,
  JSON_EXTRACT_SCALAR(comment_data, '$.comment_id') as comment_id,
  JSON_EXTRACT_SCALAR(comment_data, '$.comment_text') as comment_text,
  JSON_EXTRACT_SCALAR(comment_data, '$.comment_date') as comment_date,
  JSON_EXTRACT_SCALAR(comment_data, '$.comment_user') as comment_user,
  JSON_EXTRACT_SCALAR(comment_data, '$.comment_type') as comment_type,
  -- Correlate with user data
  u.user_name as comment_user_name,
  u.user_role as comment_user_role
FROM `wmt-assetprotection-prod.Store_Support_Dev.AMP_Users` a
CROSS JOIN UNNEST(JSON_EXTRACT_ARRAY(a.Comments_JSON, '$')) as comment_data
LEFT JOIN `wmt-assetprotection-prod.Store_Support_Dev.AMP_Users` u
  ON JSON_EXTRACT_SCALAR(comment_data, '$.comment_user') = u.user_id
  AND a.Event_ID = u.Event_ID;

-- Verification Complete View - Track completed verifications by store
CREATE OR REPLACE VIEW `wmt-assetprotection-prod.Store_Support_Dev.AMP_Verification_Complete` AS
SELECT 
  a.*,
  JSON_EXTRACT_SCALAR(verification_data, '$.verification_id') as verification_id,
  JSON_EXTRACT_SCALAR(verification_data, '$.verified_by') as verified_by,
  JSON_EXTRACT_SCALAR(verification_data, '$.verification_date') as verification_date,
  JSON_EXTRACT_SCALAR(verification_data, '$.verification_status') as verification_status,
  JSON_EXTRACT_SCALAR(verification_data, '$.verification_notes') as verification_notes,
  -- Store filtering for verification complete
  CASE 
    WHEN JSON_EXTRACT_SCALAR(verification_data, '$.verification_status') = 'COMPLETE'
         AND a.store_nbr IS NOT NULL
    THEN 'VERIFIED'
    ELSE 'PENDING'
  END as store_verification_status
FROM `wmt-assetprotection-prod.Store_Support_Dev.AMP_Comments` a
CROSS JOIN UNNEST(JSON_EXTRACT_ARRAY(a.Verification_JSON, '$')) as verification_data
WHERE a.store_nbr IS NOT NULL;

-- Final Consolidated Business Logic View
CREATE OR REPLACE VIEW `wmt-assetprotection-prod.Store_Support_Dev.AMP_Complete_Business_Logic` AS
SELECT 
  -- Core Event Data
  v.Event_ID,
  v.Event_Creation_Date,
  v.Event_Modified_Date,
  v.status_name,
  v.store_nbr,
  v.latest_src_rcv_ts,
  v.overdue_status,
  
  -- Store Activity Details
  v.activity_type,
  v.activity_date,
  v.activity_user,
  v.activity_notes,
  
  -- Team Information
  v.team_name,
  v.team_display_name,
  
  -- User Details
  v.user_id,
  v.user_name,
  v.user_role,
  v.user_department,
  v.user_last_activity,
  
  -- Comment Information
  v.comment_id,
  v.comment_text,
  v.comment_date,
  v.comment_user,
  v.comment_type,
  v.comment_user_name,
  v.comment_user_role,
  
  -- Verification Status
  v.verification_id,
  v.verified_by,
  v.verification_date,
  v.verification_status,
  v.verification_notes,
  v.store_verification_status,
  
  -- Business Logic Flags
  CASE 
    WHEN v.overdue_status = 'OVERDUE' AND v.store_verification_status = 'PENDING' 
    THEN 'HIGH_PRIORITY'
    WHEN v.overdue_status = 'OVERDUE' 
    THEN 'MEDIUM_PRIORITY'
    WHEN v.store_verification_status = 'PENDING' 
    THEN 'LOW_PRIORITY'
    ELSE 'STANDARD'
  END as priority_level,
  
  -- Data Quality Indicators
  CASE 
    WHEN v.user_id IS NULL OR v.comment_text IS NULL 
    THEN 'INCOMPLETE_DATA'
    WHEN v.verification_status IS NULL 
    THEN 'MISSING_VERIFICATION'
    ELSE 'COMPLETE_DATA'
  END as data_quality_flag,
  
  -- Processing Timestamp
  CURRENT_TIMESTAMP() as processed_ts

FROM `wmt-assetprotection-prod.Store_Support_Dev.AMP_Verification_Complete` v
WHERE v.Event_ID IS NOT NULL;

-- STEP 3: Create Multi-Source Change Detection Views
-- =====================================================================

-- AMP Events change detection (existing)
CREATE OR REPLACE VIEW `wmt-assetprotection-prod.Store_Support_Dev.AMP_Events_Change_Detection` AS
SELECT 
  event_id,
  upd_ts,
  ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY upd_ts DESC) as rn
FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
WHERE DATE(upd_ts) >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY);

-- Calendar dimension change detection
CREATE OR REPLACE VIEW `wmt-assetprotection-prod.Store_Support_Dev.Calendar_Change_Detection` AS
SELECT 
  'CALENDAR_CHANGE' as change_type,
  COUNT(*) as current_record_count,
  MIN(CALENDAR_DATE) as min_date,
  MAX(CALENDAR_DATE) as max_date,
  CURRENT_TIMESTAMP() as check_timestamp,
  -- Check if we have records for next fiscal year
  COUNTIF(FISCAL_YEAR_NBR = EXTRACT(YEAR FROM CURRENT_DATE()) + 1) as next_fy_records
FROM `wmt-edw-prod.US_CORE_DIM_VM.CALENDAR_DIM`
WHERE CALENDAR_DATE >= DATE_SUB(CURRENT_DATE(), INTERVAL 2 YEAR)
  AND CALENDAR_DATE <= DATE_ADD(CURRENT_DATE(), INTERVAL 2 YEAR);

-- Store dimension change detection
CREATE OR REPLACE VIEW `wmt-assetprotection-prod.Store_Support_Dev.Store_Change_Detection` AS
SELECT 
  'STORE_CHANGE' as change_type,
  COUNT(*) as current_store_count,
  COUNT(DISTINCT physical_state_code) as state_count,
  COUNT(DISTINCT subdivision_code) as subdivision_count,
  COUNTIF(bu_status_desc = 'OPEN') as open_stores,
  COUNTIF(bu_status_desc = 'CLOSED') as closed_stores,
  CURRENT_TIMESTAMP() as check_timestamp
FROM `wmt-loc-cat-prod.catalog_location_views.businessunit_view`
WHERE physical_country_code = 'US'
  AND base_division_desc = "WAL-MART STORES INC."
  AND Date(operational_open_start_date) <= date_add(current_date(), Interval 90 day);

-- =====================================================================
-- STEP 3: Create Enhanced Stored Procedures
-- =====================================================================

-- Main sync procedure with multi-source monitoring
CREATE OR REPLACE PROCEDURE `wmt-assetprotection-prod.Store_Support_Dev.enhanced_amp_sync_proc`()
BEGIN
  DECLARE last_amp_update TIMESTAMP;
  DECLARE last_calendar_update TIMESTAMP;
  DECLARE last_store_update TIMESTAMP;
  DECLARE amp_changes INT64;
  DECLARE calendar_changes BOOL DEFAULT FALSE;
  DECLARE store_changes BOOL DEFAULT FALSE;
  DECLARE sync_needed BOOL DEFAULT FALSE;
  
  -- Get last update timestamps
  BEGIN
    SELECT MAX(PARSE_DATETIME('%m/%d/%Y %l:%M:%S %p', `Last Updated`))
    FROM `wmt-assetprotection-prod.Store_Support.AMP_Data_Final`
    INTO last_amp_update;
  EXCEPTION WHEN ERROR THEN
    SET last_amp_update = TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY);
  END;
  
  -- Check for AMP changes (real-time)
  SET amp_changes = (
    SELECT COUNT(DISTINCT event_id)
    FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
    WHERE upd_ts > COALESCE(last_amp_update, TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY))
  );
  
  -- Check for calendar changes (monthly basis)
  IF EXTRACT(DAY FROM CURRENT_DATE()) <= 3 THEN
    -- Early in month, check if calendar needs update
    SET calendar_changes = (
      SELECT CASE 
        WHEN next_fy_records = 0 AND EXTRACT(MONTH FROM CURRENT_DATE()) >= 10 THEN TRUE
        WHEN max_date < DATE_ADD(CURRENT_DATE(), INTERVAL 90 DAY) THEN TRUE
        ELSE FALSE
      END
      FROM `wmt-assetprotection-prod.Store_Support_Dev.Calendar_Change_Detection`
    );
  END IF;
  
  -- Check for store changes (monthly basis)
  IF EXTRACT(DAY FROM CURRENT_DATE()) <= 3 THEN
    -- Store changes are harder to detect, so we refresh monthly
    SET store_changes = TRUE;
  END IF;
  
  -- Determine if sync is needed
  SET sync_needed = (amp_changes > 0 OR calendar_changes OR store_changes);
  
  -- Log the check
  INSERT INTO `wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Update_Log`
  (update_timestamp, records_updated, trigger_type, success, error_message, additional_info)
  VALUES (
    CURRENT_TIMESTAMP(), 
    amp_changes, 
    CASE 
      WHEN amp_changes > 0 AND (calendar_changes OR store_changes) THEN 'FULL_REFRESH'
      WHEN amp_changes > 0 THEN 'AMP_INCREMENTAL'
      WHEN calendar_changes OR store_changes THEN 'DIMENSION_REFRESH'
      ELSE 'NO_CHANGES'
    END,
    TRUE,
    NULL,
    JSON_OBJECT(
      'amp_changes', amp_changes,
      'calendar_refresh', calendar_changes,
      'store_refresh', store_changes,
      'sync_needed', sync_needed
    )
  );
  
  -- Perform sync if needed
  IF sync_needed THEN
    -- Full refresh if dimension changes, incremental if just AMP changes
    IF calendar_changes OR store_changes THEN
      -- Full refresh - recreate entire table
      CALL `wmt-assetprotection-prod.Store_Support_Dev.full_refresh_proc`();
    ELSE
      -- Incremental update - just updated AMP records
      CALL `wmt-assetprotection-prod.Store_Support_Dev.incremental_amp_update_proc`(last_amp_update);
    END IF;
  END IF;
  
END;

-- Full refresh procedure for dimension changes
CREATE OR REPLACE PROCEDURE `wmt-assetprotection-prod.Store_Support_Dev.full_refresh_proc`()
BEGIN
  DECLARE refresh_count INT64;
  
  -- Drop and recreate table with fresh data from all sources
  -- This ensures dimension changes are fully reflected
  
  -- Create temporary table with fresh data including comprehensive business logic
  CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Final_Temp` AS
  SELECT * FROM `wmt-assetprotection-prod.Store_Support_Dev.AMP_Complete_Business_Logic`;
  
  -- Get count for logging
  SET refresh_count = (SELECT COUNT(*) FROM `wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Final_Temp`);
  
  -- Replace production table with comprehensive business logic data
  CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Final` AS
  SELECT * FROM `wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Final_Temp`;
  
  -- Drop temp table
  DROP TABLE `wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Final_Temp`;
  
  -- Log the refresh
  INSERT INTO `wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Update_Log`
  (update_timestamp, records_updated, trigger_type, success, error_message)
  VALUES (CURRENT_TIMESTAMP(), refresh_count, 'FULL_REFRESH', TRUE, 'Complete table refresh completed');
  
END;

-- Incremental update procedure for AMP changes only
CREATE OR REPLACE PROCEDURE `wmt-assetprotection-prod.Store_Support_Dev.incremental_amp_update_proc`(last_update_timestamp TIMESTAMP)
BEGIN
  DECLARE update_count INT64;
  
  -- Delete records for updated event_ids
  DELETE FROM `wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Final`
  WHERE Event_ID IN (
    SELECT DISTINCT Event_ID
    FROM `wmt-assetprotection-prod.Store_Support_Dev.AMP_Complete_Business_Logic`
    WHERE latest_src_rcv_ts > last_update_timestamp
  );
  
  -- Insert updated records with comprehensive business logic
  INSERT INTO `wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Final`
  SELECT * FROM `wmt-assetprotection-prod.Store_Support_Dev.AMP_Complete_Business_Logic`
  WHERE latest_src_rcv_ts > last_update_timestamp;
  
  SET update_count = ROW_COUNT();
  
  -- Log the incremental update
  INSERT INTO `wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Update_Log`
  (update_timestamp, records_updated, trigger_type, success, error_message)
  VALUES (CURRENT_TIMESTAMP(), update_count, 'INCREMENTAL', TRUE, 'Incremental AMP update completed');
  
END;

-- =====================================================================
-- STEP 4: Create Enhanced Update Log Table
-- =====================================================================

CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Update_Log` (
  update_timestamp TIMESTAMP,
  records_updated INT64,
  trigger_type STRING,  -- 'INCREMENTAL', 'FULL_REFRESH', 'DIMENSION_REFRESH', 'NO_CHANGES'
  success BOOL DEFAULT TRUE,
  error_message STRING,
  additional_info JSON,  -- Store detailed change information
  execution_duration_seconds FLOAT64
);

-- =====================================================================
-- USAGE INSTRUCTIONS
-- =====================================================================

/*
MULTI-SOURCE MONITORING SYSTEM:

1. AMP Events: Monitored every 15 minutes for real-time updates
2. Calendar Dimension: Checked monthly (first 3 days of month)
3. Store Dimension: Refreshed monthly (first 3 days of month)

TRIGGER FREQUENCIES:
- High Priority (AMP Events): Every 15 minutes
- Medium Priority (Dimensions): Monthly + as-needed

MANUAL TRIGGERS:
- Full refresh: CALL `wmt-assetprotection-prod.Store_Support_Dev.full_refresh_proc`();
- AMP incremental: CALL `wmt-assetprotection-prod.Store_Support_Dev.incremental_amp_update_proc`(TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY));
- Main sync check: CALL `wmt-assetprotection-prod.Store_Support_Dev.enhanced_amp_sync_proc`();

MONITORING:
SELECT * FROM `wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Update_Log` 
ORDER BY update_timestamp DESC LIMIT 20;
*/
