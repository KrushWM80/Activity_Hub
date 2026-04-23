#!/usr/bin/env python3
"""
Find which source projects are missing from synced for WK12
"""

from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Get source project IDs in WK12
source_query = """
SELECT DISTINCT CAST(Intake_Card_Nbr AS STRING) as source_id,
       Project_Update_Date,
       Project_Title
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
WHERE Project_Update_Date >= TIMESTAMP('2026-04-18') AND Project_Update_Date < TIMESTAMP('2026-04-25')
ORDER BY Project_Update_Date DESC
"""

source_results = list(client.query(source_query).result())
source_ids = {row.source_id for row in source_results}

# Get synced project IDs in WK12
synced_query = """
SELECT DISTINCT project_id,
       project_update_date,
       title
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE project_update_date >= TIMESTAMP('2026-04-18') AND project_update_date < TIMESTAMP('2026-04-25')
ORDER BY project_update_date DESC
"""

synced_results = list(client.query(synced_query).result())
synced_ids = {row.project_id for row in synced_results}

# Find difference
in_source_not_synced = source_ids - synced_ids
in_synced_not_source = synced_ids - source_ids

print("\n" + "="*80)
print("WM WEEK 12 - SOURCE vs SYNCED COMPARISON")
print("="*80)

if in_source_not_synced:
    print(f"\n❌ IN SOURCE BUT NOT SYNCED ({len(in_source_not_synced)} projects):")
    for source_id in sorted(in_source_not_synced):
        for row in source_results:
            if row.source_id == source_id:
                print(f"   {source_id:6} | {row.Project_Title[:45]:45} | {row.Project_Update_Date}")
                break

if in_synced_not_source:
    print(f"\n❌ IN SYNCED BUT NOT SOURCE ({len(in_synced_not_source)} projects):")
    for synced_id in sorted(in_synced_not_source):
        for row in synced_results:
            if row.project_id == synced_id:
                print(f"   {synced_id:6} | {row.title[:45]:45} | {row.project_update_date}")
                break

if not in_source_not_synced and not in_synced_not_source:
    print("\n✅ PERFECT MATCH - All source projects are synced for WK12")

print("="*80)
