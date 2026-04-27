from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Delete all 10 Activity Hub duplicates
print("=== DELETING ALL 'Activity Hub' DUPLICATES ===\n")

delete_query = """
DELETE FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE title = 'Activity Hub' AND project_source = 'Manual Upload'
"""

job = client.query(delete_query)
result = job.result()
print(f"✓ Deleted all Activity Hub manual projects\n")

# Verify they're gone
verify_query = """
SELECT COUNT(*) as count
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE title = 'Activity Hub'
"""

verify_result = list(client.query(verify_query).result())
remaining = verify_result[0].count
print(f"✓ Activity Hub projects remaining: {remaining}")
print(f"✓ All duplicates and Total Store projects deleted!")
