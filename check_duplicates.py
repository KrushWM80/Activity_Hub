from google.cloud import bigquery
import json

client = bigquery.Client(project='wmt-assetprotection-prod')

# Check what we have
print("=== CHECKING CURRENT PROJECTS ===\n")

# Find Activity Hub projects
query = """
SELECT project_id, title, owner, owner_id, business_organization, health, project_source, created_date
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE title = 'Activity Hub'
ORDER BY created_date DESC
"""

results = list(client.query(query).result())
print(f"Found {len(results)} 'Activity Hub' projects:")
for i, row in enumerate(results, 1):
    print(f"  [{i}] ID: {row.project_id}")
    print(f"      Title: {row.title}")
    print(f"      Owner: {row.owner} (ID: {row.owner_id})")
    print(f"      Area: {row.business_organization}")
    print(f"      Health: {row.health}")
    print(f"      Source: {row.project_source}")
    print(f"      Created: {row.created_date}\n")

# Find Total Store projects
print("\n=== CHECKING 'TOTAL STORE' PROJECTS ===\n")
query2 = """
SELECT project_id, title, owner, business_organization
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE business_organization = 'Total Store'
ORDER BY created_date DESC
LIMIT 10
"""

results2 = list(client.query(query2).result())
print(f"Found {len(results2)} 'Total Store' projects")
for i, row in enumerate(results2, 1):
    print(f"  [{i}] {row.project_id}: {row.title} (Owner: {row.owner})")
