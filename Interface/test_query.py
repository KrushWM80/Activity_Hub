from google.cloud import bigquery

bq_client = bigquery.Client(project='wmt-assetprotection-prod')

# Check for duplicates
sql = """
SELECT 
    project_id,
    title,
    COUNT(*) as count
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
GROUP BY project_id, title
ORDER BY count DESC
LIMIT 20
"""

print("Checking for duplicate projects...")
results = bq_client.query(sql).result()
for row in results:
    print(f'Project {row.project_id}: {row.title} - appears {row.count} times')

# Also check total count
total_sql = "SELECT COUNT(*) as total FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`"
total = list(bq_client.query(total_sql).result())[0].total
print(f'\nTotal rows in AH_Projects: {total}')

# Check distinct project IDs
distinct_sql = "SELECT COUNT(DISTINCT project_id) as distinct_count FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`"
distinct = list(bq_client.query(distinct_sql).result())[0].distinct_count
print(f'Distinct project IDs: {distinct}')
