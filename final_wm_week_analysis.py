#!/usr/bin/env python3
"""
Correct Analysis: WM Week validation using Cal_Dim_Cur for exact date boundaries
"""
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

print("WALMART WEEK PROJECT UPDATE ANALYSIS")
print("="*110)

# Step 1: Get exact dates for WM WK 11 and 12 from Cal_Dim_Cur
print("\nStep 1: Get WM Week 11 & 12 Boundaries from Cal_Dim_Cur")
print("-"*110)

cal_query = """
SELECT 
    MIN(CAL_DT) as week_start,
    MAX(CAL_DT) as week_end,
    WM_WK_NBR,
    WM_YR_NBR
FROM `polaris-analytics-prod.us_walmart.Cal_Dim_Cur`
WHERE WM_YR_NBR = 2026
  AND WM_WK_NBR IN (11, 12)
GROUP BY WM_WK_NBR, WM_YR_NBR
ORDER BY WM_WK_NBR
"""

cal_results = list(client.query(cal_query).result())

wk11_info = None
wk12_info = None

for row in cal_results:
    if row.WM_WK_NBR == 11:
        wk11_info = row
        print(f"WM WK 11: {row.week_start} to {row.week_end}")
    elif row.WM_WK_NBR == 12:
        wk12_info = row
        print(f"WM WK 12: {row.week_start} to {row.week_end}")

if not wk12_info:
    print("ERROR: Could not find WM WK 12 in calendar")
    exit(1)

wk12_start = wk12_info.week_start
wk12_end = wk12_info.week_end

# Step 2: Query source table with exact date range
print("\nStep 2: Count Projects in SOURCE (Intake Accel Council Data)")
print("-"*110)

source_query = """
SELECT COUNT(DISTINCT Intake_Card_Nbr) as count_wk12
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
WHERE Project_Update_Date >= CAST('{start}' AS TIMESTAMP)
  AND Project_Update_Date < DATE_ADD(CAST('{end}' AS DATE), INTERVAL 1 DAY)
  AND Project_Update_Date IS NOT NULL
""".format(start=wk12_start, end=wk12_end)

source_count = list(client.query(source_query).result())[0].count_wk12
print(f"Projects in WM WK 12 (source): {source_count}")

# Step 3: Query synced table with exact date range
print("\nStep 3: Count Projects in SYNCED (AH_Projects)")
print("-"*110)

synced_query = """
SELECT COUNT(DISTINCT project_id) as count_wk12
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE project_update_date >= CAST('{start}' AS TIMESTAMP)
  AND project_update_date < DATE_ADD(CAST('{end}' AS DATE), INTERVAL 1 DAY)
  AND project_update_date IS NOT NULL
""".format(start=wk12_start, end=wk12_end)

synced_count = list(client.query(synced_query).result())[0].count_wk12
print(f"Projects in WM WK 12 (synced): {synced_count}")

# Summary
print("\n" + "="*110)
print("SUMMARY")
print("="*110)
print(f"WM WK 12 Date Range: {wk12_start} to {wk12_end}")
print(f"Projects in SOURCE data: {source_count}")
print(f"Projects in SYNCED table: {synced_count}")

if source_count != synced_count:
    print(f"\nWARNING: Mismatch of {abs(synced_count - source_count)} projects")
    print("  This indicates sync issue or data quality problem")
else:
    print(f"\n✓ Source and synced counts match!")

print("\nConclusion: {0} projects have been updated in WM Week 12".format(source_count))
