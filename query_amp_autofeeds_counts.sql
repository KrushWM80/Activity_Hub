-- AMP AutoFeeds Missing Daily - Store Counts by Dimensions and Status
-- Table: wmt-assetprotection-prod.Store_Support_Dev.AMP AutoFeeds Missing Daily
-- Purpose: Count of Stores grouped by Series_Title, Auto_Feed_ID, WM_WEEK_NBR, Published_Date, broken out by Status

-- PRIMARY QUERY: Detail view with Status breakdown
SELECT 
  Series_Title,
  Auto_Feed_ID,
  WM_WEEK_NBR,
  Published_Date,
  Status,
  COUNT(DISTINCT Store) as Store_Count
FROM 
  `wmt-assetprotection-prod.Store_Support_Dev.AMP AutoFeeds Missing Daily`
GROUP BY 
  Series_Title,
  Auto_Feed_ID,
  WM_WEEK_NBR,
  Published_Date,
  Status
ORDER BY 
  Published_Date DESC,
  Series_Title,
  Auto_Feed_ID,
  WM_WEEK_NBR,
  Status;

-- ALTERNATIVE QUERY: Pivot view with Status as columns
-- Uncomment to use instead of primary query
/*
SELECT 
  Series_Title,
  Auto_Feed_ID,
  WM_WEEK_NBR,
  Published_Date,
  COUNTIF(Status = 'Active') as Active_Count,
  COUNTIF(Status = 'Inactive') as Inactive_Count,
  COUNTIF(Status = 'Pending') as Pending_Count,
  COUNT(DISTINCT Store) as Total_Store_Count
FROM 
  `wmt-assetprotection-prod.Store_Support_Dev.AMP AutoFeeds Missing Daily`
GROUP BY 
  Series_Title,
  Auto_Feed_ID,
  WM_WEEK_NBR,
  Published_Date
ORDER BY 
  Published_Date DESC,
  Series_Title,
  Auto_Feed_ID,
  WM_WEEK_NBR;
*/

-- SUMMARY: Total stores by Status across all dimensions
-- Uncomment to use for quick summary
/*
SELECT 
  Status,
  COUNT(DISTINCT Store) as Total_Store_Count,
  COUNT(*) as Total_Records
FROM 
  `wmt-assetprotection-prod.Store_Support_Dev.AMP AutoFeeds Missing Daily`
GROUP BY 
  Status
ORDER BY 
  Total_Store_Count DESC;
*/
