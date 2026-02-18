-- Query to retrieve specific event_id with all related data
-- Execute this in BigQuery Console: https://console.cloud.google.com/bigquery

-- Event ID to retrieve: 5b635469-0694-4a39-bbe8-ee873d3d22b5

SELECT 
  -- Event Core Information
  e.event_id,
  e.msg_id as message_id,
  e.actv_title_home_ofc_nm as message_title,
  e.msg_txt as message_description,
  e.msg_start_dt as message_start_date,
  e.msg_end_dt as message_end_date,
  
  -- Classification
  e.bus_domain_nm as business_area,
  e.actv_type_nm as activity_type,
  e.msg_type_nm as message_type,
  e.msg_status_id as message_status,
  e.priority_status_ind as priority_level,
  
  -- Store & Location
  e.trgt_store_nbr_array as store_array,
  s.store_number as STORE_NBR,
  s.store_name,
  s.city_name as CITY_NAME,
  s.postal_code as POSTAL_CODE,
  s.state_prov_code as STATE_PROV_CODE,
  s.region_nbr as REGION_NBR,
  s.market_area_nbr as MARKET_AREA_NBR,
  s.subdiv_name as SUBDIV_NAME,
  s.latitude_dgr as LATITUDE_DGR,
  s.longitude_dgr as LONGITUDE_DGR,
  
  -- Calendar Information
  c.FISCAL_YEAR_NBR as FY,
  c.WM_WEEK_NBR as WM_WEEK,
  c.WM_QTR_NAME as QUARTER,
  c.CALENDAR_DATE,
  
  -- Audit Fields
  e.create_user as created_by,
  e.create_ts as created_datetime,
  e.upd_user as modified_by,
  e.upd_ts as modified_datetime,
  e.src_rcv_ts as published_datetime,
  e.msg_hide_ind as hidden_status,
  
  -- System Fields
  e.approval_status,
  e.workflow_stage

FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT` e

-- Join with Calendar Dimension for date/week info
LEFT JOIN `wmt-edw-prod.US_CORE_DIM_VM.CALENDAR_DIM` c
  ON CAST(e.msg_start_dt AS DATE) = c.CALENDAR_DATE

-- Join with Store Dimension for location details
LEFT JOIN `wmt-loc-cat-prod.catalog_location_views.businessunit_view` s
  ON e.trgt_store_nbr_array CONTAINS s.store_number

WHERE e.event_id = '5b635469-0694-4a39-bbe8-ee873d3d22b5'

ORDER BY e.create_ts DESC;
