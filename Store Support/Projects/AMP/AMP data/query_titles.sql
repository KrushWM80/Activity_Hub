-- Get distinct Titles for FY 2027
SELECT DISTINCT Title 
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2` 
WHERE Message_Type = 'Store Updates' 
  AND Status LIKE '%Published%'
  AND FY = 2027
ORDER BY Title
LIMIT 50;
