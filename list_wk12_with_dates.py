#!/usr/bin/env python3
"""
Show which projects still have dates in WM WK 12
"""

from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

query = """
SELECT 
    project_id,
    title,
    project_update_date,
    project_source
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE project_update_date >= TIMESTAMP('2026-04-18') AND project_update_date < TIMESTAMP('2026-04-25')
ORDER BY project_update_date DESC
LIMIT 50
"""

results = client.query(query).result()

print("\n" + "="*80)
print("Projects with dates in WM WK 12 (April 18-24, 2026)")
print("="*80)

for row in results:
    print(f"{row.project_id:6} | {row.title[:45]:45} | {row.project_update_date}")

print("="*80)
