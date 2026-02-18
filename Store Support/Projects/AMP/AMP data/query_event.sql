SELECT 
  -- Event Core Information
  event_id,
  actv_title_home_ofc_nm as message_title,
  msg_subj_nm.array as message_subject_array,
  msg_txt.array as message_text_array,
  msg_start_dt as message_start_date,
  msg_end_dt as message_end_date,
  
  -- Classification
  bus_domain_nm as business_area,
  msg_type_nm as message_type,
  msg_status_id as message_status,
  msg_scndry_status_id as message_secondary_status,
  priority_status_ind as priority_level,
  impct_status_ind as impact_status,
  urgent_ind as urgent_indicator,
  
  -- Store & Location
  trgt_store_nbr_array as store_array,
  trgt_all_store_ind as all_stores_indicator,
  geo_region_cd as geographic_region,
  
  -- Calendar/Week Information
  wm_yr_and_wk as walmart_year_week,
  event_dt as event_date,
  EXTRACT(YEAR FROM msg_start_dt) as fiscal_year,
  EXTRACT(WEEK FROM msg_start_dt) as week_number,
  
  -- Workflow & Status
  msg_hide_ind as hidden_status,
  msg_leg_status_nm as legal_status,
  cmpltd_sts_ind as completed_status,
  store_uncmpltd_cnt as stores_uncompleted_count,
  
  -- Auto Feed Info
  auto_feed_id,
  auto_feed_title_nm as auto_feed_title,
  reltv_wk_nbr as relative_week_number,
  
  -- Audit Fields
  create_user as created_by,
  create_ts as created_datetime,
  upd_user as modified_by,
  upd_ts as modified_datetime,
  src_rcv_ts as source_received_datetime,
  
  -- Keywords & Attachments
  msg_kw_array as keyword_array,
  msg_atch_loc_nm as attachment_location,
  atch_loc_id as attachment_location_id,
  
  -- Team & User Targets
  trgt_user_id_array as target_user_array,
  team_id_array,
  team_nm_array as team_name_array,
  
  -- Platform & Translation
  msg_pltf_type_array as platform_type_array,
  msg_spanish_translate_ind as spanish_translation_indicator,
  
  -- Technical Fields
  data_src_cd as data_source_code,
  op_cmpny_cd as operating_company_code,
  tz_cd as timezone_code

FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`

WHERE event_id = '5b635469-0694-4a39-bbe8-ee873d3d22b5'

LIMIT 1
