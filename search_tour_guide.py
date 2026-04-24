from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Search for tour/guide anywhere in the database
sql = """
SELECT 
    project_id,
    title,
    owner,
    project_update_date,
    last_updated
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE LOWER(title) LIKE '%tour%'
   OR LOWER(title) LIKE '%guide%'
ORDER BY last_updated DESC
"""

print("All 'tour' or 'guide' projects in database:\n")
results = list(client.query(sql).result())
print(f"Found {len(results)} projects\n")

if results:
    for row in results:
        print(f"Title: {row.title}")
        print(f"  Owner: {row.owner}")
        print(f"  Last Updated: {row.last_updated}")
        print()
else:
    print("No 'tour' or 'guide' projects found\n")

# Also check for recently updated projects in last 24 hours
print("\n\nProjects updated in last 24 hours:\n")
sql2 = """
SELECT 
    project_id,
    title,
    owner,
    last_updated
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE last_updated >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)
ORDER BY last_updated DESC
LIMIT 20
"""

results2 = list(client.query(sql2).result())
print(f"Found {len(results2)} recently updated projects:\n")
for row in results2:
    print(f"  - {row.title} (Owner: {row.owner})")
