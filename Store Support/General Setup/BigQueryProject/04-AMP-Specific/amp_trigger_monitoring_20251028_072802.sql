-- AMP Data Sync Monitoring Dashboard Queries
-- Use these queries to monitor the trigger system performance

-- 1. Recent Updates Summary
SELECT 
  DATE(update_timestamp) as update_date,
  COUNT(*) as sync_runs,
  SUM(records_updated) as total_records_updated,
  AVG(records_updated) as avg_records_per_run,
  SUM(CASE WHEN success THEN 1 ELSE 0 END) as successful_runs,
  SUM(CASE WHEN NOT success THEN 1 ELSE 0 END) as failed_runs
FROM `wmt-assetprotection-prod.Store_Support.AMP_Data_Update_Log`
WHERE update_timestamp >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
GROUP BY DATE(update_timestamp)
ORDER BY update_date DESC;

-- 2. Current Table Status
SELECT 
  COUNT(*) as total_records,
  COUNT(DISTINCT `event_id`) as unique_events,
  MIN(PARSE_DATETIME('%m/%d/%Y %l:%M:%S %p', `Last Updated`)) as oldest_update,
  MAX(PARSE_DATETIME('%m/%d/%Y %l:%M:%S %p', `Last Updated`)) as newest_update,
  COUNT(DISTINCT `WM Week`) as weeks_covered,
  COUNT(DISTINCT `store`) as stores_covered
FROM `wmt-assetprotection-prod.Store_Support.AMP_Data_Final`;

-- 3. Error Analysis
SELECT 
  DATE(update_timestamp) as error_date,
  trigger_type,
  error_message,
  COUNT(*) as error_count
FROM `wmt-assetprotection-prod.Store_Support.AMP_Data_Update_Log`
WHERE NOT success
  AND update_timestamp >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY DATE(update_timestamp), trigger_type, error_message
ORDER BY error_date DESC, error_count DESC;

-- 4. Data Freshness Check
SELECT 
  CASE 
    WHEN DATETIME_DIFF(CURRENT_DATETIME(), MAX(PARSE_DATETIME('%m/%d/%Y %l:%M:%S %p', `Last Updated`)), MINUTE) <= 30 THEN 'FRESH'
    WHEN DATETIME_DIFF(CURRENT_DATETIME(), MAX(PARSE_DATETIME('%m/%d/%Y %l:%M:%S %p', `Last Updated`)), MINUTE) <= 120 THEN 'STALE'
    ELSE 'VERY_STALE'
  END as data_freshness,
  MAX(PARSE_DATETIME('%m/%d/%Y %l:%M:%S %p', `Last Updated`)) as last_data_update,
  DATETIME_DIFF(CURRENT_DATETIME(), MAX(PARSE_DATETIME('%m/%d/%Y %l:%M:%S %p', `Last Updated`)), MINUTE) as minutes_since_update
FROM `wmt-assetprotection-prod.Store_Support.AMP_Data_Final`;

-- 5. Performance Metrics
SELECT 
  trigger_type,
  AVG(records_updated) as avg_records_per_run,
  MAX(records_updated) as max_records_per_run,
  MIN(records_updated) as min_records_per_run,
  COUNT(*) as total_runs,
  SUM(CASE WHEN success THEN 1 ELSE 0 END) / COUNT(*) * 100 as success_rate_percent
FROM `wmt-assetprotection-prod.Store_Support.AMP_Data_Update_Log`
WHERE update_timestamp >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY trigger_type
ORDER BY avg_records_per_run DESC;

-- 6. Weekly Sync Pattern Analysis
SELECT 
  EXTRACT(DAYOFWEEK FROM update_timestamp) as day_of_week,
  EXTRACT(HOUR FROM update_timestamp) as hour_of_day,
  COUNT(*) as sync_count,
  AVG(records_updated) as avg_records,
  SUM(CASE WHEN success THEN 1 ELSE 0 END) / COUNT(*) * 100 as success_rate
FROM `wmt-assetprotection-prod.Store_Support.AMP_Data_Update_Log`
WHERE update_timestamp >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
GROUP BY EXTRACT(DAYOFWEEK FROM update_timestamp), EXTRACT(HOUR FROM update_timestamp)
ORDER BY day_of_week, hour_of_day;
