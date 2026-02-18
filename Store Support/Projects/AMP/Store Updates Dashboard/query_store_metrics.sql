-- Store-Level Event Count Aggregation
-- Purpose: Calculate Store High/Low/Avg from store uniqueness of events
-- Data Source: wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2

WITH store_event_summary AS (
  SELECT
    store,
    wm_week,
    fy,
    COUNT(DISTINCT event_id) as event_count
  FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
  WHERE fy = 2027 
    AND wm_week = 2
    AND store IS NOT NULL
    AND store != ''
  GROUP BY store, wm_week, fy
)
SELECT
  wm_week,
  fy,
  MAX(event_count) as store_high,
  MIN(event_count) as store_low,
  ROUND(AVG(event_count), 2) as store_avg,
  COUNT(DISTINCT store) as total_unique_stores,
  SUM(event_count) as total_store_event_touchpoints
FROM store_event_summary
GROUP BY wm_week, fy
