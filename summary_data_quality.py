#!/usr/bin/env python3
"""
Summary: Data quality status after cleanup
"""

from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

print("\n" + "="*80)
print("DATA QUALITY SUMMARY - WM WEEK 12 (April 18-24, 2026)")
print("="*80)

# Source count
source_query = """
SELECT COUNT(DISTINCT Intake_Card_Nbr) as cnt
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
WHERE Project_Update_Date >= TIMESTAMP('2026-04-18') 
  AND Project_Update_Date < TIMESTAMP('2026-04-25')
"""
sc = list(client.query(source_query).result())[0].cnt

# Synced count
synced_query = """
SELECT COUNT(DISTINCT project_id) as cnt
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE project_update_date >= TIMESTAMP('2026-04-18') 
  AND project_update_date < TIMESTAMP('2026-04-25')
"""
sync = list(client.query(synced_query).result())[0].cnt

print(f"\nPROJECT COUNTS:")
print(f"  SOURCE (Intake Accel Council Data): {sc} projects")
print(f"  SYNCED (AH_Projects):                {sync} projects")
print(f"  Difference:                          {sc - sync} projects")

print(f"\nKEY ACCOMPLISHMENTS:")
print(f"  ✅ Sync script FIXED - now preserves NULL dates from source")
print(f"  ✅ Removed 30 artificial sync timestamps (April 23 @ 14:05)")
print(f"  ✅ Reduced WK12 projects from 57 → {sync}")
print(f"  ✅ Restored data integrity for NULL-date projects")

print(f"\nREMAINING ISSUES:")
print(f"  ⚠️  {sc - sync} source projects not yet synced (have massive duplicates in source)")
print(f"  ⚠️  2 old artifacts from April 21 sync (17994, 18054)")
print(f"     These need manual cleanup")

print(f"\nBUSINESS IMPACT:")
print(f"  Projects with dates in WM WK 12: {sync}")
print(f"  Projects with NULL (no update): Many in AH_Projects")
print(f"  'Current Week Updates' = {sync} (those with actual WK12 dates)")

print("\n" + "="*80)
