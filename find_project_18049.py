from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Search for project ID 18049
sql = """
SELECT 
    project_id,
    title,
    owner,
    business_organization,
    health,
    project_update,
    project_update_date,
    last_updated,
    project_source
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE project_id = '18049'
"""

print("Searching for Project ID 18049...\n")
results = list(client.query(sql).result())

if results:
    for row in results:
        print(f"✓ FOUND!")
        print(f"  Title: {row.title}")
        print(f"  ID: {row.project_id}")
        print(f"  Owner: {row.owner}")
        print(f"  Business Org: {row.business_organization}")
        print(f"  Health: {row.health}")
        print(f"  Source: {row.project_source}")
        print(f"  Last Updated: {row.last_updated}")
        print(f"  Project Update Date: {row.project_update_date}")
        print(f"  Note: {row.project_update[:100] if row.project_update else 'None'}...\n")
else:
    print("✗ Project 18049 NOT found in AH_Projects table\n")

# Now search by project title
print("Searching by title 'Tour Guides'...\n")
sql2 = """
SELECT 
    project_id,
    title,
    owner,
    business_organization,
    project_update_date,
    last_updated
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE LOWER(title) LIKE '%tour%guide%'
   OR LOWER(title) LIKE '%guide%development%'
"""

results2 = list(client.query(sql2).result())
if results2:
    print(f"Found {len(results2)} matching projects:")
    for row in results2:
        print(f"  - {row.title} (ID: {row.project_id}, Owner: {row.owner})")
else:
    print("No projects found with 'tour guides' in title")
