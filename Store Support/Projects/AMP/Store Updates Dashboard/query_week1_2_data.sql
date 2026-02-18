-- Fix: Pre-aggregate audience and time data to avoid Cartesian product multiplication
WITH audience_agg AS (
    SELECT 
        message_id,
        SUM(CAST(unique_users AS INT64)) as unique_users,
        SUM(CAST(total_opens AS INT64)) as total_opens
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Audience Breakdown Cur`
    GROUP BY message_id
),
time_agg AS (
    SELECT
        message_id,
        AVG(avg_time_seconds) as avg_time_seconds
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Time Spent Cur`
    GROUP BY message_id
),
amp_dedup AS (
    SELECT 
        WM_Week,
        Title,
        Activity_Type,
        Store_Area,
        MAX(CAST(Store_Cnt AS INT64)) as Store_Cnt,
        Status,
        event_id
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
    WHERE FY = 2027
        AND WM_Week IN ('1', '2')
        AND Status = 'Published - Published'
        AND Message_Type LIKE '%Store Updates%'
    GROUP BY WM_Week, Title, Activity_Type, Store_Area, Status, event_id
)
SELECT 
    amp.WM_Week,
    amp.Title,
    amp.Activity_Type,
    amp.Store_Area,
    amp.Store_Cnt,
    amp.Status,
    amp.event_id,
    COALESCE(aud.unique_users, 0) as unique_users,
    COALESCE(aud.total_opens, 0) as total_opens,
    ROUND(COALESCE(ts.avg_time_seconds, 0), 1) as avg_time_seconds
FROM amp_dedup amp
LEFT JOIN audience_agg aud ON amp.event_id = aud.message_id
LEFT JOIN time_agg ts ON amp.event_id = ts.message_id
ORDER BY amp.WM_Week, amp.Title
LIMIT 200
