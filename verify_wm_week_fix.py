#!/usr/bin/env python3
"""
Verify that project_update_date values are now preserved
"""
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

from google.cloud import bigquery
from datetime import datetime

client = bigquery.Client(project='wmt-assetprotection-prod')

# Calculate current WM week
today = datetime.now()
fiscal_year_start = datetime(today.year if today.month >= 2 else today.year - 1, 2, 1)
days_since_fy = (today - fiscal_year_start).days
current_wm_week = (days_since_fy // 7) + 1

print('Current Date:', today.strftime('%Y-%m-%d'))
print('Current WM Week: WK{}\n'.format(current_wm_week))

# Query with WM week calculation
sql = '''
SELECT 
    project_id,
    title,
    project_update_date,
    COUNT(*) OVER () as total_projects
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE project_update_date IS NOT NULL
ORDER BY project_update_date DESC
LIMIT 25
'''

results = client.query(sql).result()

print('SAMPLE DATA - Top 25 Projects:')
print('='*110)
print('Project ID | Update Date         | WK | Health | Title')
print('='*110)

total_projects = 0
for row in results:
    if row.project_update_date:
        update_date = row.project_update_date
        fy_start = datetime(update_date.year if update_date.month >= 2 else update_date.year - 1, 2, 1)
        days_since = (update_date.replace(tzinfo=None) - fy_start).days
        update_wm_week = (days_since // 7) + 1
    else:
        update_date = None
        update_wm_week = None
    
    if row.total_projects:
        total_projects = row.total_projects
    
    date_str = update_date.strftime('%Y-%m-%d %H:%M') if update_date else 'N/A'
    wk_str = 'WK{}'.format(update_wm_week) if update_wm_week else 'N/A'
    title_str = str(row.title)[:45] if row.title else 'N/A'
    
    print('{:<10} | {:<19} | {:5} | {:35}'.format(str(row.project_id), date_str, wk_str, title_str))

print('='*110)

# Count by WM week
count_sql = '''
WITH weekly_breakdown AS (
  SELECT 
    project_id,
    project_update_date,
    CAST(FLOOR(DATE_DIFF(DATE(project_update_date), DATE('2026-02-01'), DAY) / 7) + 1 AS INT64) as update_wk
  FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
  WHERE project_update_date IS NOT NULL
)
SELECT 
  update_wk as wm_week,
  COUNT(*) as project_count,
  MIN(project_update_date) as earliest_date,
  MAX(project_update_date) as latest_date
FROM weekly_breakdown
GROUP BY update_wk
ORDER BY update_wk DESC
LIMIT 5
'''

print('\nPROJECT COUNT BY WM WEEK (Top 5 weeks):')
print('='*100)
print('WM Week | Count | Date Range')
print('='*100)

count_results = list(client.query(count_sql).result())

wk12_count = 0
wk11_count = 0
other_count = 0

for row in count_results:
    min_date = row.earliest_date.strftime('%Y-%m-%d') if row.earliest_date else 'N/A'
    max_date = row.latest_date.strftime('%Y-%m-%d') if row.latest_date else 'N/A'
    print('WK{:<4} | {:5} | {} to {}'.format(row.wm_week, row.project_count, min_date, max_date))
    
    if row.wm_week == current_wm_week:
        wk12_count = row.project_count
    elif row.wm_week == current_wm_week - 1:
        wk11_count = row.project_count
    else:
        other_count += row.project_count

print('='*100)
print('\nSUMMARY:')
print('  Total projects analyzed: {}'.format(total_projects))
print('  Updated in Current WK{}: {} projects'.format(current_wm_week, wk12_count))
print('  Updated in WK{}: {} projects'.format(current_wm_week - 1, wk11_count))
print('  Updated in earlier weeks: {} projects'.format(other_count))
print('\n  Current Week Percentage: {:.1f}%'.format((wk12_count / total_projects * 100) if total_projects > 0 else 0))
