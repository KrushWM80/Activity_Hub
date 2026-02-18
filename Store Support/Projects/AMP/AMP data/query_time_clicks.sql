SELECT 
    SUM(verification_count) as total_verifications,
    AVG(avg_time_seconds) as avg_time_seconds
FROM `wmt-assetprotection-prod.Store_Support_Dev.Time Spent Cur`
WHERE message_id = '5b635469-0694-4a39-bbe8-ee873d3d22b5'
