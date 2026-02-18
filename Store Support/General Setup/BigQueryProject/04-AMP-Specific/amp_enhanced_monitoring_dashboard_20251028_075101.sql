-- Enhanced Multi-Source AMP Data Sync Monitoring Dashboard
-- Generated: October 28, 2025
-- Purpose: Monitor AMP Events, Calendar, and Store dimension synchronization

-- =====================================================================
-- 1. OVERALL SYNC STATUS DASHBOARD
-- =====================================================================

-- Current sync status across all data sources
SELECT 
  'CURRENT_STATUS' as dashboard_section,
  CURRENT_TIMESTAMP() as check_time,
  
  -- AMP Data freshness
  DATETIME_DIFF(
    CURRENT_DATETIME(), 
    MAX(PARSE_DATETIME('%m/%d/%Y %l:%M:%S %p', `Last Updated`)), 
    MINUTE
  ) as minutes_since_last_amp_update,
  
  -- Record counts
  COUNT(*) as total_records,
  COUNT(DISTINCT `event_id`) as unique_events,
  COUNT(DISTINCT `store`) as unique_stores,
  COUNT(DISTINCT `WM Week`) as weeks_covered,
  
  -- Data quality checks
  COUNTIF(`state` IS NULL) as missing_state_records,
  COUNTIF(`store` IS NULL) as missing_store_records,
  COUNTIF(`WM Year` IS NULL) as missing_calendar_records

FROM `wmt-assetprotection-prod.Store_Support.AMP_Data_Final`;

-- =====================================================================
-- 2. MULTI-SOURCE SYNC SUMMARY
-- =====================================================================

-- Recent sync activity by source type
SELECT 
  DATE(update_timestamp) as sync_date,
  trigger_type,
  COUNT(*) as sync_runs,
  SUM(records_updated) as total_records_updated,
  AVG(records_updated) as avg_records_per_run,
  SUM(CASE WHEN success THEN 1 ELSE 0 END) as successful_runs,
  SUM(CASE WHEN NOT success THEN 1 ELSE 0 END) as failed_runs,
  ROUND(AVG(execution_duration_seconds), 2) as avg_duration_seconds,
  
  -- Parse additional info for dimension details
  COUNTIF(JSON_EXTRACT_SCALAR(additional_info, '$.calendar_refresh') = 'true') as calendar_refreshes,
  COUNTIF(JSON_EXTRACT_SCALAR(additional_info, '$.store_refresh') = 'true') as store_refreshes

FROM `wmt-assetprotection-prod.Store_Support.AMP_Data_Update_Log`
WHERE update_timestamp >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY DATE(update_timestamp), trigger_type
ORDER BY sync_date DESC, trigger_type;

-- =====================================================================
-- 3. DATA SOURCE MONITORING
-- =====================================================================

-- Monitor each data source for freshness and issues
WITH source_monitoring AS (
  SELECT 
    'AMP_EVENTS' as source_name,
    'wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT' as source_table,
    'Real-time (15 min)' as expected_frequency,
    DATETIME_DIFF(
      CURRENT_DATETIME(), 
      MAX(PARSE_DATETIME('%m/%d/%Y %l:%M:%S %p', `Last Updated`)), 
      MINUTE
    ) as minutes_since_update,
    CASE 
      WHEN DATETIME_DIFF(CURRENT_DATETIME(), MAX(PARSE_DATETIME('%m/%d/%Y %l:%M:%S %p', `Last Updated`)), MINUTE) <= 30 THEN 'FRESH'
      WHEN DATETIME_DIFF(CURRENT_DATETIME(), MAX(PARSE_DATETIME('%m/%d/%Y %l:%M:%S %p', `Last Updated`)), MINUTE) <= 120 THEN 'STALE'
      ELSE 'VERY_STALE'
    END as freshness_status
  FROM `wmt-assetprotection-prod.Store_Support.AMP_Data_Final`
  
  UNION ALL
  
  SELECT 
    'CALENDAR_DIM' as source_name,
    'wmt-edw-prod.US_CORE_DIM_VM.CALENDAR_DIM' as source_table,
    'Monthly' as expected_frequency,
    CASE 
      WHEN MAX(calendar_last_processed) IS NOT NULL 
      THEN DATETIME_DIFF(CURRENT_DATETIME(), MAX(calendar_last_processed), HOUR)
      ELSE NULL
    END as hours_since_calendar_update,
    CASE 
      WHEN EXTRACT(DAY FROM CURRENT_DATE()) <= 5 AND MAX(calendar_last_processed) IS NULL THEN 'NEEDS_UPDATE'
      WHEN MAX(calendar_last_processed) IS NOT NULL THEN 'UPDATED'
      ELSE 'OK'
    END as freshness_status
  FROM `wmt-assetprotection-prod.Store_Support.AMP_Data_Final`
  
  UNION ALL
  
  SELECT 
    'STORE_DIM' as source_name,
    'wmt-loc-cat-prod.catalog_location_views.businessunit_view' as source_table,
    'Monthly' as expected_frequency,
    CASE 
      WHEN MAX(store_last_processed) IS NOT NULL 
      THEN DATETIME_DIFF(CURRENT_DATETIME(), MAX(store_last_processed), HOUR)
      ELSE NULL
    END as hours_since_store_update,
    CASE 
      WHEN EXTRACT(DAY FROM CURRENT_DATE()) <= 5 AND MAX(store_last_processed) IS NULL THEN 'NEEDS_UPDATE'
      WHEN MAX(store_last_processed) IS NOT NULL THEN 'UPDATED'
      ELSE 'OK'
    END as freshness_status
  FROM `wmt-assetprotection-prod.Store_Support.AMP_Data_Final`
)

SELECT * FROM source_monitoring;

-- =====================================================================
-- 4. ERROR ANALYSIS DASHBOARD
-- =====================================================================

-- Recent errors and their patterns
SELECT 
  DATE(update_timestamp) as error_date,
  trigger_type,
  error_message,
  COUNT(*) as error_count,
  MIN(update_timestamp) as first_occurrence,
  MAX(update_timestamp) as last_occurrence,
  
  -- Extract additional error context
  ARRAY_AGG(DISTINCT JSON_EXTRACT_SCALAR(additional_info, '$.amp_changes')) as amp_change_counts,
  ARRAY_AGG(DISTINCT JSON_EXTRACT_SCALAR(additional_info, '$.calendar_refresh')) as calendar_refresh_attempts,
  ARRAY_AGG(DISTINCT JSON_EXTRACT_SCALAR(additional_info, '$.store_refresh')) as store_refresh_attempts

FROM `wmt-assetprotection-prod.Store_Support.AMP_Data_Update_Log`
WHERE NOT success
  AND update_timestamp >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY DATE(update_timestamp), trigger_type, error_message
ORDER BY error_date DESC, error_count DESC;

-- =====================================================================
-- 5. PERFORMANCE METRICS DASHBOARD
-- =====================================================================

-- Sync performance by trigger type
SELECT 
  trigger_type,
  COUNT(*) as total_executions,
  AVG(records_updated) as avg_records_per_sync,
  MAX(records_updated) as max_records_per_sync,
  MIN(records_updated) as min_records_per_sync,
  AVG(execution_duration_seconds) as avg_duration_seconds,
  MAX(execution_duration_seconds) as max_duration_seconds,
  
  -- Success rates
  ROUND(SUM(CASE WHEN success THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as success_rate_percent,
  
  -- Performance trends
  AVG(CASE WHEN update_timestamp >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY) 
           THEN execution_duration_seconds END) as recent_avg_duration,
  AVG(CASE WHEN update_timestamp < DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY) 
           THEN execution_duration_seconds END) as historical_avg_duration

FROM `wmt-assetprotection-prod.Store_Support.AMP_Data_Update_Log`
WHERE update_timestamp >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
  AND execution_duration_seconds IS NOT NULL
GROUP BY trigger_type
ORDER BY avg_duration_seconds DESC;

-- =====================================================================
-- 6. MONTHLY DIMENSION REFRESH TRACKING
-- =====================================================================

-- Track monthly dimension refreshes
SELECT 
  EXTRACT(YEAR FROM update_timestamp) as year,
  EXTRACT(MONTH FROM update_timestamp) as month,
  EXTRACT(DAY FROM update_timestamp) as day_of_month,
  
  -- Dimension refresh summary
  COUNTIF(trigger_type = 'FULL_REFRESH') as full_refreshes,
  COUNTIF(trigger_type = 'DIMENSION_REFRESH') as dimension_refreshes,
  COUNTIF(JSON_EXTRACT_SCALAR(additional_info, '$.calendar_refresh') = 'true') as calendar_updates,
  COUNTIF(JSON_EXTRACT_SCALAR(additional_info, '$.store_refresh') = 'true') as store_updates,
  
  -- Performance for dimension updates
  AVG(CASE WHEN trigger_type IN ('FULL_REFRESH', 'DIMENSION_REFRESH') 
           THEN execution_duration_seconds END) as avg_dimension_sync_duration,
  SUM(CASE WHEN trigger_type IN ('FULL_REFRESH', 'DIMENSION_REFRESH') 
           THEN records_updated ELSE 0 END) as total_dimension_records_updated

FROM `wmt-assetprotection-prod.Store_Support.AMP_Data_Update_Log`
WHERE update_timestamp >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH)
  AND EXTRACT(DAY FROM update_timestamp) <= 5  -- Focus on early month activity
GROUP BY year, month, day_of_month
ORDER BY year DESC, month DESC, day_of_month;

-- =====================================================================
-- 7. DATA QUALITY MONITORING
-- =====================================================================

-- Monitor data quality across all sources
WITH data_quality_metrics AS (
  SELECT 
    COUNT(*) as total_records,
    
    -- AMP Events data quality
    COUNTIF(`event_id` IS NULL OR `event_id` = '') as missing_event_ids,
    COUNTIF(`Activity Title` IS NULL OR `Activity Title` = '') as missing_titles,
    COUNTIF(`Author` IS NULL OR `Author` = '') as missing_authors,
    COUNTIF(`Created Date` IS NULL OR `Created Date` = '') as missing_created_dates,
    
    -- Calendar data quality
    COUNTIF(`WM Year` IS NULL) as missing_wm_year,
    COUNTIF(`WM Week` IS NULL) as missing_wm_week,
    COUNTIF(`FY` IS NULL) as missing_fiscal_year,
    
    -- Store data quality
    COUNTIF(`store` IS NULL) as missing_store_numbers,
    COUNTIF(`state` IS NULL OR `state` = '') as missing_states,
    COUNTIF(`Region` IS NULL) as missing_regions,
    COUNTIF(`Division` IS NULL OR `Division` = '') as missing_divisions,
    
    -- Data freshness
    MIN(PARSE_DATETIME('%m/%d/%Y %l:%M:%S %p', `Last Updated`)) as oldest_record,
    MAX(PARSE_DATETIME('%m/%d/%Y %l:%M:%S %p', `Last Updated`)) as newest_record
    
  FROM `wmt-assetprotection-prod.Store_Support.AMP_Data_Final`
)

SELECT 
  *,
  -- Calculate data quality percentages
  ROUND(missing_event_ids * 100.0 / total_records, 2) as missing_event_ids_percent,
  ROUND(missing_store_numbers * 100.0 / total_records, 2) as missing_stores_percent,
  ROUND(missing_states * 100.0 / total_records, 2) as missing_states_percent,
  
  -- Data freshness assessment
  DATETIME_DIFF(CURRENT_DATETIME(), newest_record, MINUTE) as minutes_since_newest,
  DATETIME_DIFF(newest_record, oldest_record, DAY) as data_age_span_days

FROM data_quality_metrics;

-- =====================================================================
-- 8. SYNC FREQUENCY ANALYSIS
-- =====================================================================

-- Analyze sync patterns by hour of day and day of week
SELECT 
  EXTRACT(DAYOFWEEK FROM update_timestamp) as day_of_week,
  CASE EXTRACT(DAYOFWEEK FROM update_timestamp)
    WHEN 1 THEN 'Sunday'
    WHEN 2 THEN 'Monday'
    WHEN 3 THEN 'Tuesday'
    WHEN 4 THEN 'Wednesday'
    WHEN 5 THEN 'Thursday'
    WHEN 6 THEN 'Friday'
    WHEN 7 THEN 'Saturday'
  END as day_name,
  EXTRACT(HOUR FROM update_timestamp) as hour_of_day,
  
  -- Sync activity
  COUNT(*) as sync_count,
  AVG(records_updated) as avg_records,
  SUM(CASE WHEN success THEN 1 ELSE 0 END) / COUNT(*) * 100 as success_rate,
  
  -- Trigger type distribution
  COUNTIF(trigger_type = 'INCREMENTAL') as incremental_syncs,
  COUNTIF(trigger_type = 'FULL_REFRESH') as full_refreshes,
  COUNTIF(trigger_type = 'DIMENSION_REFRESH') as dimension_syncs

FROM `wmt-assetprotection-prod.Store_Support.AMP_Data_Update_Log`
WHERE update_timestamp >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY day_of_week, day_name, hour_of_day
ORDER BY day_of_week, hour_of_day;

-- =====================================================================
-- 9. ALERT CONDITIONS
-- =====================================================================

-- Conditions that should trigger alerts
WITH alert_conditions AS (
  -- Data freshness alerts
  SELECT 
    'DATA_FRESHNESS' as alert_type,
    'HIGH' as priority,
    CASE 
      WHEN DATETIME_DIFF(CURRENT_DATETIME(), MAX(PARSE_DATETIME('%m/%d/%Y %l:%M:%S %p', `Last Updated`)), MINUTE) > 60 
      THEN CONCAT('Data is stale - last update was ', 
                  DATETIME_DIFF(CURRENT_DATETIME(), MAX(PARSE_DATETIME('%m/%d/%Y %l:%M:%S %p', `Last Updated`)), MINUTE),
                  ' minutes ago')
      ELSE NULL
    END as alert_message,
    CURRENT_TIMESTAMP() as check_time
  FROM `wmt-assetprotection-prod.Store_Support.AMP_Data_Final`
  
  UNION ALL
  
  -- Error rate alerts
  SELECT 
    'ERROR_RATE' as alert_type,
    'MEDIUM' as priority,
    CASE 
      WHEN error_rate > 20 
      THEN CONCAT('High error rate: ', ROUND(error_rate, 1), '% of syncs failed in last 24 hours')
      ELSE NULL
    END as alert_message,
    CURRENT_TIMESTAMP() as check_time
  FROM (
    SELECT 
      (SUM(CASE WHEN NOT success THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as error_rate
    FROM `wmt-assetprotection-prod.Store_Support.AMP_Data_Update_Log`
    WHERE update_timestamp >= DATE_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)
  )
  
  UNION ALL
  
  -- Monthly dimension update check
  SELECT 
    'DIMENSION_UPDATE' as alert_type,
    'MEDIUM' as priority,
    CASE 
      WHEN EXTRACT(DAY FROM CURRENT_DATE()) <= 5 
           AND dimension_updates_this_month = 0
      THEN 'Monthly dimension update has not occurred yet this month'
      ELSE NULL
    END as alert_message,
    CURRENT_TIMESTAMP() as check_time
  FROM (
    SELECT 
      COUNTIF(
        trigger_type IN ('FULL_REFRESH', 'DIMENSION_REFRESH') 
        AND EXTRACT(MONTH FROM update_timestamp) = EXTRACT(MONTH FROM CURRENT_DATE())
        AND EXTRACT(YEAR FROM update_timestamp) = EXTRACT(YEAR FROM CURRENT_DATE())
      ) as dimension_updates_this_month
    FROM `wmt-assetprotection-prod.Store_Support.AMP_Data_Update_Log`
  )
)

SELECT * FROM alert_conditions WHERE alert_message IS NOT NULL;

-- =====================================================================
-- 10. SUMMARY DASHBOARD QUERY
-- =====================================================================

-- Single query for executive summary
SELECT 
  'AMP_MULTI_SOURCE_SYNC_SUMMARY' as dashboard_name,
  CURRENT_TIMESTAMP() as report_time,
  
  -- Overall status
  (SELECT COUNT(*) FROM `wmt-assetprotection-prod.Store_Support.AMP_Data_Final`) as total_records_in_target,
  
  -- Freshness
  (SELECT DATETIME_DIFF(CURRENT_DATETIME(), MAX(PARSE_DATETIME('%m/%d/%Y %l:%M:%S %p', `Last Updated`)), MINUTE)
   FROM `wmt-assetprotection-prod.Store_Support.AMP_Data_Final`) as minutes_since_last_update,
  
  -- Today's sync activity
  (SELECT COUNT(*) FROM `wmt-assetprotection-prod.Store_Support.AMP_Data_Update_Log`
   WHERE DATE(update_timestamp) = CURRENT_DATE()) as syncs_today,
  
  -- Success rate last 24 hours
  (SELECT ROUND(SUM(CASE WHEN success THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1)
   FROM `wmt-assetprotection-prod.Store_Support.AMP_Data_Update_Log`
   WHERE update_timestamp >= DATE_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)) as success_rate_24h,
  
  -- Dimension refresh status
  (SELECT MAX(update_timestamp) FROM `wmt-assetprotection-prod.Store_Support.AMP_Data_Update_Log`
   WHERE trigger_type IN ('FULL_REFRESH', 'DIMENSION_REFRESH')
   AND EXTRACT(MONTH FROM update_timestamp) = EXTRACT(MONTH FROM CURRENT_DATE())) as last_dimension_refresh_this_month;