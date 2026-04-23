#!/usr/bin/env python3
"""
Investigate why 5 source projects aren't being synced
"""

from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Check if these 5 exist in AH_Projects but with NULL dates
missing_ids = ['11466', '13767', '14798', '17919', '18056']

id_list = ','.join([f"'{pid}'" for pid in missing_ids])

query = f"""
SELECT 
    project_id,
    title,
    project_update_date,
    project_source,
    created_date,
    last_updated
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE project_id IN ({id_list})
"""

results = list(client.query(query).result())

print("\n" + "="*80)
print("STATUS OF 5 'MISSING' PROJECTS IN AH_Projects")
print("="*80)

if results:
    print(f"Found {len(results)} of these projects already in AH_Projects:\n")
    for row in results:
        date_status = "✅ HAS DATE" if row.project_update_date else "❌ NULL DATE"
        print(f"{row.project_id:6} | {row.title[:40]:40} | {date_status}")
        print(f"       Source: {row.project_source}, Created: {row.created_date}")
else:
    print("None of these 5 projects exist in AH_Projects")
    print("They should be inserted as new projects on next sync")

print("\n" + "="*80)
