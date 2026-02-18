SELECT 
    SUM(total_views) as total_device_views, 
    SUM(unique_users) as unique_device_users
FROM `wmt-assetprotection-prod.Store_Support_Dev.Device Types Cur`
WHERE message_id = '5b635469-0694-4a39-bbe8-ee873d3d22b5'
