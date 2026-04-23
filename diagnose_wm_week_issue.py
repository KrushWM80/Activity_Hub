#!/usr/bin/env python3
"""
Get correct WM WK 12 dates from Cal_Dim_Cur and verify source vs synced data
"""
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

from google.cloud import bigquery
from datetime import datetime

client = bigquery.Client(project='wmt-assetprotection-prod')

# Get WM WK 12 from calendar
print('Step 1: Get WM WK 12 Date Range from Cal_Dim_Cur')
print('='*100)

# Try to access the calendar table
cal_sql = '''
SELECT DISTINCT
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
'''

try:
    cal_results = list(client.query(cal_sql).result())
    print('Calendar Results:')
    for row in cal_results:
        print('  WM WK {}: {} to {} ({} days)'.format(
            row.WM_WK_NBR,
            row.week_start.strftime('%Y-%m-%d'),
            row.week_end.strftime('%Y-%m-%d'),
            row.days_in_week
        ))
except Exception as e:
    print('  Error accessing Cal_Dim_Cur: {}'.format(e))
    print('  (May not have permission to this table)')

print('\n' + '='*100)
print('Step 2: Count Projects in SOURCE Table (Intake Accel Council Data)')
print('='*100)

# Query source table directly
source_sql = '''
SELECT 
    COUNT(DISTINCT Intake_Card_Nbr) as count_wk12,
    MIN(Project_Update_Date) as earliest,
    MAX(Project_Update_Date) as latest
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
WHERE Project_Update_Date > '2026-04-18'
  AND Project_Update_Date IS NOT NULL
'''

source_results = list(client.query(source_sql).result())
for row in source_results:
    print('  Total projects > 2026-04-18: {}'.format(row.count_wk12))
    print('  Earliest date: {}'.format(row.earliest.strftime('%Y-%m-%d %H:%M') if row.earliest else 'N/A'))
    print('  Latest date: {}'.format(row.latest.strftime('%Y-%m-%d %H:%M') if row.latest else 'N/A'))

print('\n' + '='*100)
print('Step 3: Count Projects in AH_Projects (After Sync)')
print('='*100)

synced_sql = '''
SELECT 
    COUNT(DISTINCT project_id) as count_synced,
    MIN(project_update_date) as earliest,
    MAX(project_update_date) as latest
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE project_update_date > '2026-04-18'
  AND project_update_date IS NOT NULL
'''

synced_results = list(client.query(synced_sql).result())
for row in synced_results:
    print('  Total projects > 2026-04-18: {}'.format(row.count_synced))
    print('  Earliest date: {}'.format(row.earliest.strftime('%Y-%m-%d %H:%M') if row.earliest else 'N/A'))
    print('  Latest date: {}'.format(row.latest.strftime('%Y-%m-%d %H:%M') if row.latest else 'N/A'))

print('\n' + '='*100)
print('Step 4: Sample Data Comparison')
print('='*100)

# Show sample from source
print('\nTop 10 from SOURCE (Intake Accel Council Data):')
sample_source = '''
SELECT Distinct 
    Intake_Card_Nbr,
    Project_Update,
    Project_Update_Date
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
WHERE Project_Update_Date > '2026-04-18'
ORDER BY Project_Update_Date DESC
LIMIT 10
'''

sample_results = list(client.query(sample_source).result())
for row in sample_results:
    date_str = row.Project_Update_Date.strftime('%Y-%m-%d %H:%M') if row.Project_Update_Date else 'N/A'
    print('  Card {}: {}'.format(row.Intake_Card_Nbr, date_str))

print('\nTop 10 from SYNCED (AH_Projects):')
sample_synced = '''
SELECT 
    project_id,
    title,
    project_update_date
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE project_update_date > '2026-04-18'
ORDER BY project_update_date DESC
LIMIT 10
'''

sample_results = list(client.query(sample_synced).result())
for row in sample_results:
    date_str = row.project_update_date.strftime('%Y-%m-%d %H:%M') if row.project_update_date else 'N/A'
    print('  Project {}: {}'.format(row.project_id, date_str))
