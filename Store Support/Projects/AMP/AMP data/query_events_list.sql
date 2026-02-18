-- Get recent events from Output - AMP ALL 2 for dashboard
SELECT 
    event_id,
    Title,
    FY,
    Week,
    Activity_Type,
    Store_Area,
    Status,
    Store_Cnt,
    Web_Preview
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE Message_Type = 'Store Updates'
  AND Status LIKE '%Published%'
  AND FY = 2027
ORDER BY Week DESC, Title
LIMIT 20
