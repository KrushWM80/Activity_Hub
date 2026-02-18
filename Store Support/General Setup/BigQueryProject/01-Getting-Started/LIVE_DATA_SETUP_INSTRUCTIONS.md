# Live BigQuery Data Setup Instructions

Since we encountered network connectivity issues with the Python BigQuery library, here's how to get live data working:

## Method 1: Manual BigQuery Export (Recommended)

### Step 1: Export Data from BigQuery Console
1. Go to [BigQuery Console](https://console.cloud.google.com/bigquery)
2. Navigate to project: `wmt-assetprotection-prod`
3. Open dataset: `Store_Support_Dev`
4. Open table: `AMP_Data_Prep`

### Step 2: Run This Query
```sql
SELECT 
    actv_title_home_ofc_nm as title,
    division,
    region,
    market,
    store_nbr,
    store_name,
    week,
    created_date,
    preview_link,
    status,
    verification_status
FROM `wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Prep`
WHERE week = 39 
  AND status = 'Published'
ORDER BY created_date DESC
```

### Step 3: Export Results
1. Click "SAVE RESULTS" 
2. Choose "JSON (newline delimited)"
3. Save as `live_amp_data.json`
4. Place the file in this folder: `C:\Users\krush\Documents\VSCode\AMP\Store Updates Dashboard\`

## Method 2: Quick Test with Sample Live Data

I'll create a sample file with the correct structure that mimics live BigQuery data:

### File: `live_amp_data.json`
This file will contain realistic data with proper preview links that work.

## Dashboard Integration

The dashboard is already set up to:
1. ✅ Look for `live_amp_data.json` first
2. ✅ Fall back to embedded sample data if file not found
3. ✅ Show data status indicator
4. ✅ Handle both real and sample preview links

## Testing Live Data

Once you have the `live_amp_data.json` file:
1. Refresh the dashboard (F5)
2. Look for "📊 Data Status: Live BigQuery Data" indicator
3. Test preview links - they should all work with real GUIDs
4. Use browser console command: `showAllPreviewLinks()` to verify

## Troubleshooting

### If Preview Links Don't Work:
- Check that preview_link column contains full URLs with GUIDs
- Format should be: `https://amp2-cms.prod.walmart.com/preview/{GUID}`
- GUIDs look like: `029a6006-5b63-4d7f-872a-45ffca6bf10d`

### If No Data Shows:
- Check browser console (F12) for errors
- Verify `live_amp_data.json` is in the correct folder
- Make sure JSON format is valid (use JSONLint.com to check)

## Next Steps

1. Export the live data using Method 1
2. Test the dashboard functionality
3. Verify all 75+ activities show up
4. Confirm preview links work properly