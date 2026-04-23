#!/usr/bin/env python3
"""
Compare SOURCE vs SYNCED counts for WM WK 12
"""

from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Count from SOURCE
source_query = """
SELECT COUNT(DISTINCT Intake_Card_Nbr) as source_count
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
WHERE Project_Update_Date >= TIMESTAMP('2026-04-18') AND Project_Update_Date < TIMESTAMP('2026-04-25')
"""

source_results = list(client.query(source_query).result())

# Count from SYNCED
synced_query = """
SELECT COUNT(DISTINCT project_id) as synced_count
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE project_update_date >= TIMESTAMP('2026-04-18') AND project_update_date < TIMESTAMP('2026-04-25')
"""

synced_results = list(client.query(synced_query).result())

print("\n" + "="*80)
print("WM WEEK 12 COMPARISON (April 18-24, 2026) - AFTER CLEANUP")
print("="*80)
print(f"SOURCE (Intake Accel Council Data): {source_results[0].source_count} projects")
print(f"SYNCED (AH_Projects):                {synced_results[0].synced_count} projects")

diff = synced_results[0].synced_count - source_results[0].source_count
if diff == 0:
    print(f"\n✅ MATCH - Data integrity restored!")
else:
    print(f"\n⚠️  DISCREPANCY: {diff} extra projects in synced")
print("="*80)
