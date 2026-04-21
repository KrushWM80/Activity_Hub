#!/usr/bin/env python3
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

from google.cloud import bigquery
from datetime import datetime
import pandas as pd

client = bigquery.Client()

# Calculate current WM week
today = datetime.now()
fiscal_year_start = datetime(today.year if today.month >= 2 else today.year - 1, 2, 1)
days_since_fy = (today - fiscal_year_start).days
current_wm_week = (days_since_fy // 7) + 1

print(f'Current Date: {today.strftime("%Y-%m-%d")}')
print(f'Fiscal Year Start: {fiscal_year_start.strftime("%Y-%m-%d")}')
print(f'Current WM Week: WK{current_wm_week}\n')

# Query all projects with their update dates
sql = """
SELECT 
    project_id,
    title,
    last_updated,
    owner
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE title IS NOT NULL AND TRIM(title) != ''
ORDER BY last_updated DESC
LIMIT 100
"""

results = client.query(sql).result()
data = []

for row in results:
    if row.last_updated:
        update_date = row.last_updated
        fy_start = datetime(update_date.year if update_date.month >= 2 else update_date.year - 1, 2, 1)
        days_since = (update_date.replace(tzinfo=None) - fy_start).days
        update_wm_week = (days_since // 7) + 1
    else:
        update_date = None
        update_wm_week = None
    
    data.append({
        'Project Title': row.title[:50] if row.title else 'N/A',
        'Owner': row.owner,
        'Update Date': update_date.strftime('%Y-%m-%d %H:%M') if update_date else 'N/A',
        'Update WK': f'WK{update_wm_week}' if update_wm_week else 'N/A',
        'Current WK': f'WK{current_wm_week}',
        'This Week?': 'YES' if update_wm_week == current_wm_week else 'NO'
    })

df = pd.DataFrame(data)

print('=' * 140)
print('PROJECT UPDATE DATE & WM WEEK ANALYSIS')
print('=' * 140)
print(df.to_string(index=False))
print('=' * 140)

# Summary
this_week = df[df['This Week?'] == 'YES']
not_this_week = df[df['This Week?'] == 'NO']
print(f'\nSummary (Top 100 projects):')
print(f'  Updated THIS week (WK{current_wm_week}): {len(this_week)} projects')
print(f'  Updated BEFORE this week: {len(not_this_week)} projects')

# Show "Tour Guides" if it exists
print(f'\n--- Checking for "Tour Guides" project ---')
sql_tour = """
SELECT title, last_updated, owner
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE LOWER(title) LIKE '%tour%guide%'
"""
results_tour = client.query(sql_tour).result()
found_tour = False
for row in results_tour:
    found_tour = True
    if row.last_updated:
        update_date = row.last_updated
        fy_start = datetime(update_date.year if update_date.month >= 2 else update_date.year - 1, 2, 1)
        days_since = (update_date.replace(tzinfo=None) - fy_start).days
        update_wm_week = (days_since // 7) + 1
        print(f'Title: {row.title}')
        print(f'Owner: {row.owner}')
        print(f'Update Date: {update_date.strftime("%Y-%m-%d %H:%M")}')
        print(f'Update WK: WK{update_wm_week}')
        print(f'Current WK: WK{current_wm_week}')
        print(f'Expected: Last week (WK{current_wm_week - 1}), Actual: WK{update_wm_week}')

if not found_tour:
    print('Tour Guides project not found')
