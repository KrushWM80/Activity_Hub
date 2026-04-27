from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Check for any "Activity Hub" titled projects
query = """
SELECT project_id, title, owner, owner_id, business_organization
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE title = 'Activity Hub'
ORDER BY created_date DESC
"""

results = list(client.query(query).result())

if results:
    print(f"✓ Found {len(results)} 'Activity Hub' project(s):\n")
    for i, row in enumerate(results, 1):
        print(f"  [{i}] project_id: {row.project_id}")
        print(f"      title: {row.title}")
        print(f"      owner: {row.owner} (ID: {row.owner_id})")
        print(f"      business_area: {row.business_organization}\n")
else:
    print("✗ No 'Activity Hub' projects found in the database")
    print("   (All duplicates were deleted earlier)")
