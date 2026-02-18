# BigQuery Export Instructions for Complete AMP Data

## Problem: Dashboard only shows 20 sample records instead of 75+ Week 39 published titles

## Solution: Export complete dataset from BigQuery

### Step 1: Run this BigQuery Query (NO LIMITS!)

```sql
SELECT 
    week_number,
    actv_title_home_ofc_nm as activity_title,
    division,
    store_nbr as site,
    preview_link,
    published,
    -- Add other fields as needed
    region,
    market,
    activity_type,
    store_area,
    create_ts,
    msg_start_dt,
    msg_end_dt
FROM `wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Prep`
WHERE published = true
ORDER BY week_number DESC, actv_title_home_ofc_nm
```

### Step 2: Export Results

1. Click "Save Results" 
2. Choose "JSON (newline delimited)" or "JSON"
3. Save as `bigquery-complete-export.json`
4. Place file in dashboard folder

### Step 3: Update Dashboard

The dashboard will automatically load the complete dataset with:
- All 75+ Week 39 published titles
- Real preview links from the database
- Accurate division and store data
- Complete activity information

### Current Issue:
- Dashboard shows: ~20 sample records
- BigQuery table has: 75+ published titles in Week 39
- Missing: Real preview links and complete dataset

### Expected Result:
- Dashboard will show: ALL published activities
- Real preview links from database
- Complete activity details for all weeks
- Accurate counts and verification data

### Alternative: Direct BigQuery Connection

If JSON export doesn't work, use direct BigQuery API:
1. Set up service account authentication
2. Configure CORS for amp2-cms.prod.walmart.com
3. Use BigQuery REST API directly in browser

### Verification:

After loading complete data, you should see:
- 75+ activities for Week 39
- Real preview links (not sample URLs)
- Accurate division counts
- Complete store and activity information