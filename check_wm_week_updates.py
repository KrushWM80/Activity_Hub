#!/usr/bin/env python3
"""
Check which projects have update dates in the current WM Week
Based on Walmart Fiscal Year calendar (FY starts Feb 1)
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

print(f'Current Date: {today.strftime("%Y-%m-%d")}')
print(f'Fiscal Year Start: {fiscal_year_start.strftime("%Y-%m-%d")}')
print(f'Days Since FY Start: {days_since_fy}')
print(f'Current WM Week: WK{current_wm_week}\n')

# Query ALL projects with project_update_date
sql = '''
SELECT 
    project_id,
    title,
    project_update_date,
    project_update_by,
    health,
    status
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE project_update_date IS NOT NULL
ORDER BY project_update_date DESC
'''

results = client.query(sql).result()

print('='*170)
print(f"{'Project ID':<12} {'Title':<45} {'Update Date':<25} {'Update WK':<12} {'In WK'+str(current_wm_week)+'?':<12} {'Health':<10}")
print('='*170)

in_current_week = []
not_in_current_week = []

for row in results:
    if row.project_update_date:
        update_date = row.project_update_date
        fy_start = datetime(update_date.year if update_date.month >= 2 else update_date.year - 1, 2, 1)
        days_since = (update_date.replace(tzinfo=None) - fy_start).days
        update_wm_week = (days_since // 7) + 1
    else:
        update_date = None
        update_wm_week = None
    
    is_this_week = update_wm_week == current_wm_week if update_wm_week else False
    
    if is_this_week:
        in_current_week.append(row.project_id)
        indicator = 'YES ✓'
    else:
        not_in_current_week.append(row.project_id)
        indicator = 'NO'
    
    date_str = update_date.strftime('%Y-%m-%d %H:%M:%S') if update_date else 'N/A'
    wk_str = f'WK{update_wm_week}' if update_wm_week else 'N/A'
    title_str = row.title[:43] if row.title else 'N/A'
    health_str = row.health[:8] if row.health else 'N/A'
    
    print(f'{str(row.project_id):<12} {title_str:<45} {date_str:<25} {wk_str:<12} {indicator:<12} {health_str:<10}')

print('='*170)
print(f'\nSUMMARY:')
print(f'  ✓ Projects Updated IN current WM Week {current_wm_week}: {len(in_current_week)} projects')
print(f'  ✗ Projects Updated BEFORE current WK: {len(not_in_current_week)} projects')
print(f'  Total with update dates: {len(in_current_week) + len(not_in_current_week)} projects\n')

if in_current_week:
    print(f'Project IDs Updated THIS WEEK (WK{current_wm_week}):')
    print(f'  {", ".join(map(str, in_current_week[:20]))}')
    if len(in_current_week) > 20:
        print(f'  ... and {len(in_current_week) - 20} more')
