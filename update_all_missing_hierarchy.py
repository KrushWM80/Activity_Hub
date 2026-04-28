#!/usr/bin/env python3
from google.cloud import bigquery

client = bigquery.Client('wmt-assetprotection-prod')

# 1. Find all projects with missing director/sr_director info
print("=" * 80)
print("FINDING PROJECTS WITH MISSING DIRECTOR/SR_DIRECTOR INFO")
print("=" * 80)

query = """
SELECT 
    project_id,
    title,
    owner,
    director_id,
    sr_director_id,
    project_source
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE (director_id IS NULL OR sr_director_id IS NULL)
  AND owner IS NOT NULL
  AND TRIM(owner) != ''
  AND TRIM(owner) != 'Unknown'
ORDER BY owner, project_id
"""

results = list(client.query(query).result())
print(f"\nFound {len(results)} projects with missing director/sr_director info:\n")

# Group by owner
by_owner = {}
for row in results:
    owner = row.owner
    if owner not in by_owner:
        by_owner[owner] = []
    by_owner[owner].append(row)

# Show summary
for owner in sorted(by_owner.keys()):
    projects = by_owner[owner]
    print(f"{owner}: {len(projects)} projects")
    for row in projects:
        print(f"  - {row.project_id:5} | {row.title:40} ({row.project_source})")

# 2. Try to update from hierarchy
print("\n" + "=" * 80)
print("ATTEMPTING TO UPDATE FROM HIERARCHY")
print("=" * 80)

updates_made = 0
updates_by_owner = {}

for owner in sorted(by_owner.keys()):
    # Look up owner in hierarchy
    hierarchy_query = """
    SELECT director, sr_director
    FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Hierarchy`
    WHERE LOWER(TRIM(person_name)) = LOWER(TRIM(@owner_name))
    LIMIT 1
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("owner_name", "STRING", owner)
        ]
    )
    
    hierarchy_results = list(client.query(hierarchy_query, job_config=job_config).result())
    
    if hierarchy_results:
        h_row = hierarchy_results[0]
        director = h_row.director
        sr_director = h_row.sr_director
        
        if director or sr_director:
            # Found hierarchy info - update projects for this owner
            projects = by_owner[owner]
            project_ids = [f"'{p.project_id}'" for p in projects]
            
            update_sql = f"""
            UPDATE `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
            SET
                director_id = {f"'{director}'" if director else "director_id"},
                sr_director_id = {f"'{sr_director}'" if sr_director else "sr_director_id"},
                last_updated = CURRENT_TIMESTAMP()
            WHERE project_id IN ({','.join(project_ids)})
            """
            
            try:
                client.query(update_sql).result()
                updates_made += len(projects)
                updates_by_owner[owner] = {
                    'count': len(projects),
                    'director': director,
                    'sr_director': sr_director
                }
                print(f"\n✓ {owner}")
                print(f"  Updated {len(projects)} projects")
                print(f"  Director: {director or 'NULL'}")
                print(f"  Sr Director: {sr_director or 'NULL'}")
            except Exception as e:
                print(f"\n✗ Error updating projects for {owner}: {e}")
        else:
            print(f"\n○ {owner}: Found in hierarchy but no director/sr_director info")
    else:
        print(f"\n○ {owner}: Not found in hierarchy")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Total projects updated: {updates_made}")
if updates_by_owner:
    print(f"\nUpdated owners:")
    for owner, info in sorted(updates_by_owner.items()):
        print(f"  - {owner}: {info['count']} projects -> {info['director'] or 'NULL'} / {info['sr_director'] or 'NULL'}")
