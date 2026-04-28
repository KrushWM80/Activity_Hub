#!/usr/bin/env python3
from google.cloud import bigquery

client = bigquery.Client('wmt-assetprotection-prod')

# 1. Check Kendall's hierarchy
print("=" * 80)
print("KENDALL RUSH'S HIERARCHY")
print("=" * 80)

query = """
SELECT person_name, director, sr_director, vp
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Hierarchy`
WHERE LOWER(TRIM(person_name)) = LOWER('Kendall Rush')
"""

results = list(client.query(query).result())
kendall_director = None
kendall_sr_director = None

if results:
    row = results[0]
    print(f"Person: {row.person_name}")
    print(f"Director: {row.director}")
    print(f"Sr Director: {row.sr_director}")
    print(f"VP: {row.vp or 'NULL'}")
    kendall_director = row.director
    kendall_sr_director = row.sr_director
else:
    print("Kendall Rush not found in hierarchy!")

# 2. Find projects with Kendall as owner
print("\n" + "=" * 80)
print("KENDALL'S PROJECTS - CHECKING DIRECTOR INFO")
print("=" * 80)

query2 = """
SELECT 
    project_id,
    title,
    owner,
    director_id,
    sr_director_id,
    project_source
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE LOWER(TRIM(owner)) = LOWER('Kendall Rush')
ORDER BY project_id
"""

results2 = list(client.query(query2).result())
print(f"\nFound {len(results2)} projects where Kendall is owner:\n")

missing_projects = []
for row in results2:
    has_director = "✓" if row.director_id else "✗"
    has_sr_director = "✓" if row.sr_director_id else "✗"
    print(f"  {row.project_id:5} | {has_director} {has_sr_director} | {row.title:35} ({row.project_source})")
    if not row.director_id or not row.sr_director_id:
        missing_projects.append(row)

print(f"\n{len(missing_projects)} projects missing director/sr_director info:")
for row in missing_projects:
    print(f"  - {row.project_id}: {row.title} ({row.project_source})")

# 3. If we have Kendall's hierarchy, update the missing projects
if kendall_director or kendall_sr_director:
    print("\n" + "=" * 80)
    print("UPDATING MISSING PROJECTS WITH KENDALL'S HIERARCHY")
    print("=" * 80)
    
    if missing_projects:
        # Build update statement
        project_ids = [f"'{row.project_id}'" for row in missing_projects]
        update_sql = f"""
        UPDATE `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
        SET
            director_id = {f"'{kendall_director}'" if kendall_director else "NULL"},
            sr_director_id = {f"'{kendall_sr_director}'" if kendall_sr_director else "NULL"},
            last_updated = CURRENT_TIMESTAMP()
        WHERE project_id IN ({','.join(project_ids)})
        """
        
        print(f"\nUpdating {len(missing_projects)} projects:")
        print(f"  Setting director_id = {kendall_director or 'NULL'}")
        print(f"  Setting sr_director_id = {kendall_sr_director or 'NULL'}")
        
        try:
            job = client.query(update_sql)
            job.result()
            print(f"\n✓ Updated {len(missing_projects)} projects successfully!")
        except Exception as e:
            print(f"\n✗ Error updating projects: {e}")
    else:
        print("\nNo missing projects to update!")
