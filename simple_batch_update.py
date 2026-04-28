#!/usr/bin/env python3
from google.cloud import bigquery

client = bigquery.Client('wmt-assetprotection-prod')

print("=" * 80)
print("UPDATING PROJECTS FROM HIERARCHY DATA")
print("=" * 80)

# Simpler: Update statement
update_sql = """
UPDATE `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects` ap
SET
    ap.director_id = COALESCE(h.director, ap.director_id),
    ap.sr_director_id = COALESCE(h.sr_director, ap.sr_director_id),
    ap.last_updated = CURRENT_TIMESTAMP()
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Hierarchy` h
WHERE LOWER(TRIM(ap.owner)) = LOWER(TRIM(h.person_name))
  AND (ap.director_id IS NULL OR ap.sr_director_id IS NULL)
  AND ap.owner IS NOT NULL
  AND TRIM(ap.owner) != ''
  AND TRIM(ap.owner) != 'Unknown'
"""

print("\nExecuting batch update...")
try:
    job = client.query(update_sql)
    result = job.result()
    print("✓ Update complete!")
    
    # Check results
    summary_query = """
    SELECT COUNT(*) as total_projects,
           COUNTIF(director_id IS NOT NULL AND sr_director_id IS NOT NULL) as fully_populated
    FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
    """
    summary = list(client.query(summary_query).result())[0]
    print(f"\nResults:")
    print(f"  Total projects in AH_Projects: {summary.total_projects}")
    print(f"  With both director + sr_director: {summary.fully_populated}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
