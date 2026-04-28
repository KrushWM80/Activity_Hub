#!/usr/bin/env python3
from google.cloud import bigquery

client = bigquery.Client('wmt-assetprotection-prod')

# Find projects with missing director info and check who is in hierarchy
query = """
WITH missing_projects AS (
    SELECT 
        project_id,
        title,
        owner,
        project_source
    FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
    WHERE (director_id IS NULL OR sr_director_id IS NULL)
      AND owner IS NOT NULL
      AND TRIM(owner) != ''
      AND TRIM(owner) != 'Unknown'
),
owners_in_hierarchy AS (
    SELECT DISTINCT LOWER(TRIM(person_name)) as owner_lower
    FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Hierarchy`
)
SELECT 
    mp.owner,
    COUNT(*) as project_count,
    CASE WHEN oih.owner_lower IS NOT NULL THEN 'YES' ELSE 'NO' END as in_hierarchy
FROM missing_projects mp
LEFT JOIN owners_in_hierarchy oih ON LOWER(TRIM(mp.owner)) = oih.owner_lower
GROUP BY mp.owner, oih.owner_lower
ORDER BY in_hierarchy DESC, project_count DESC
"""

results = list(client.query(query).result())

print("=" * 80)
print("PROJECTS WITH MISSING DIRECTOR/SR_DIRECTOR INFO - CAN BE UPDATED?")
print("=" * 80)

can_update = [r for r in results if r.in_hierarchy == 'YES']
cannot_update = [r for r in results if r.in_hierarchy == 'NO']

print(f"\nCAN UPDATE (Owner in Hierarchy): {sum(r.project_count for r in can_update)} projects")
print("─" * 80)
for row in can_update:
    print(f"  {row.owner:30} {row.project_count:3} projects")

print(f"\nCANNOT UPDATE (Owner NOT in Hierarchy): {sum(r.project_count for r in cannot_update)} projects")
print("─" * 80)
for row in cannot_update:
    print(f"  {row.owner:30} {row.project_count:3} projects")

# Now do a batch update for all that CAN be updated
if can_update:
    print(f"\n" + "=" * 80)
    print("BATCH UPDATING ALL PROJECTS WHERE OWNER IS IN HIERARCHY")
    print("=" * 80)
    
    # Single UPDATE statement using hierarchy join
    batch_update = """
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
    
    try:
        job = client.query(batch_update)
        job.result()
        print(f"\n✓ Batch update complete!")
        
        # Count how many were actually updated
        count_query = """
        SELECT COUNT(*) as updated_count
        FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
        WHERE owner IN ({})
          AND director_id IS NOT NULL
          AND sr_director_id IS NOT NULL
        """.format(','.join([f"'{r.owner}'" for r in can_update]))
        
        count = list(client.query(count_query).result())[0].updated_count
        print(f"  Updated {count} projects total")
        
    except Exception as e:
        print(f"✗ Error: {e}")
