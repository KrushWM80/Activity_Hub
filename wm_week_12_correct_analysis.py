#!/usr/bin/env python3
"""
Correct WM Week 12 Analysis
1. Get WM WK 12 exact dates from Cal_Dim_Cur
2. Compare source (Intake Accel Council Data) vs synced (AH_Projects)
"""
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

from google.cloud import bigquery
from datetime import datetime

client = bigquery.Client(project='wmt-assetprotection-prod')

print('\n' + '='*120)
print('STEP 1: Get WM WK 12 Exact Date Range from Cal_Dim_Cur')
print('='*120)

cal_sql = """
SELECT 
    WM_WK_NBR,
    WM_YR_NBR,
    MIN(CAL_DT) as week_start,
    MAX(CAL_DT) as week_end,
    COUNT(*) as days_in_week
FROM `polaris-analytics-prod.us_walmart.Cal_Dim_Cur`
WHERE WM_WK_NBR IN (11, 12)
  AND WM_YR_NBR = 2026
GROUP BY WM_WK_NBR, WM_YR_NBR
ORDER BY WM_WK_NBR
"""

try:
    cal_results = list(client.query(cal_sql).result())
    for row in cal_results:
        print('WM WK {}: {} to {} ({} days)'.format(
            row.WM_WK_NBR,
            row.week_start.strftime('%Y-%m-%d'),
            row.week_end.strftime('%Y-%m-%d'),
            row.days_in_week
        ))
    
    # Extract WK12 dates
    wk12_row = [r for r in cal_results if r.WM_WK_NBR == 12][0]
    wk12_start = wk12_row.week_start
    wk12_end = wk12_row.week_end
    
except Exception as e:
    print('Error: {}'.format(e))
    print('Proceeding with estimate...')
    from datetime import timedelta
    # If we can't access Cal_Dim_Cur, estimate based on Feb 1 start
    fy_start = datetime(2026, 2, 1)
    wk12_start = fy_start + timedelta(days=77)  # Week 12 starts at day 77
    wk12_end = wk12_start + timedelta(days=6)

print('\nUsing WK12 range: {} to {}\n'.format(
    wk12_start.strftime('%Y-%m-%d'),
    wk12_end.strftime('%Y-%m-%d')
))

print('='*120)
print('STEP 2: Count Projects in SOURCE Table (Intake Accel Council Data)')
print('='*120)

source_sql = """
SELECT 
    COUNT(DISTINCT Intake_Card_Nbr) as count_wk12,
    MIN(Project_Update_Date) as earliest,
    MAX(Project_Update_Date) as latest
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
WHERE Project_Update_Date >= CAST('{} 00:00:00' AS TIMESTAMP)
  AND Project_Update_Date <= CAST('{} 23:59:59' AS TIMESTAMP)
  AND Project_Update_Date IS NOT NULL
""".format(wk12_start.strftime('%Y-%m-%d'), wk12_end.strftime('%Y-%m-%d'))

source_results = list(client.query(source_sql).result())
for row in source_results:
    print('Total projects in SOURCE for WK12: {}'.format(row.count_wk12))
    print('  Earliest: {}'.format(row.earliest.strftime('%Y-%m-%d %H:%M') if row.earliest else 'N/A'))
    print('  Latest: {}'.format(row.latest.strftime('%Y-%m-%d %H:%M') if row.latest else 'N/A'))
    source_wk12_count = row.count_wk12

print('\n' + '='*120)
print('STEP 3: Count Projects in AH_Projects (After Sync)')
print('='*120)

synced_sql = """
SELECT 
    COUNT(DISTINCT project_id) as count_synced,
    MIN(project_update_date) as earliest,
    MAX(project_update_date) as latest
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE project_update_date >= CAST('{} 00:00:00' AS TIMESTAMP)
  AND project_update_date <= CAST('{} 23:59:59' AS TIMESTAMP)
  AND project_update_date IS NOT NULL
""".format(wk12_start.strftime('%Y-%m-%d'), wk12_end.strftime('%Y-%m-%d'))

synced_results = list(client.query(synced_sql).result())
for row in synced_results:
    print('Total projects in AH_Projects for WK12: {}'.format(row.count_synced))
    print('  Earliest: {}'.format(row.earliest.strftime('%Y-%m-%d %H:%M') if row.earliest else 'N/A'))
    print('  Latest: {}'.format(row.latest.strftime('%Y-%m-%d %H:%M') if row.latest else 'N/A'))
    synced_wk12_count = row.count_synced

# Check for discrepancy
if source_wk12_count != synced_wk12_count:
    print('\n*** DISCREPANCY DETECTED ***')
    print('Source count: {}, Synced count: {}'.format(source_wk12_count, synced_wk12_count))

print('\n' + '='*120)
print('STEP 4: Sample Data - Top 15 from SOURCE')
print('='*120)

sample_source = """
SELECT DISTINCT
    Intake_Card_Nbr,
    Project_Update,
    Project_Update_Date
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
WHERE Project_Update_Date >= CAST('{} 00:00:00' AS TIMESTAMP)
  AND Project_Update_Date <= CAST('{} 23:59:59' AS TIMESTAMP)
ORDER BY Project_Update_Date DESC
LIMIT 15
""".format(wk12_start.strftime('%Y-%m-%d'), wk12_end.strftime('%Y-%m-%d'))

sample_results = list(client.query(sample_source).result())
print('Card # | Date | Update Text')
print('-'*120)
for row in sample_results:
    date_str = row.Project_Update_Date.strftime('%Y-%m-%d %H:%M') if row.Project_Update_Date else 'N/A'
    update_text = str(row.Project_Update)[:60] if row.Project_Update else 'N/A'
    print('{:<8} | {:<19} | {}'.format(row.Intake_Card_Nbr, date_str, update_text))

print('\n' + '='*120)
print('SUMMARY')
print('='*120)
print('WM WK 12 Date Range: {} to {}'.format(
    wk12_start.strftime('%Y-%m-%d'),
    wk12_end.strftime('%Y-%m-%d')
))
print('Projects in SOURCE (Intake Accel Council Data): {}'.format(source_wk12_count))
print('Projects in SYNCED (AH_Projects): {}'.format(synced_wk12_count))
print('Match: {}'.format('YES' if source_wk12_count == synced_wk12_count else 'NO - INVESTIGATE'))
