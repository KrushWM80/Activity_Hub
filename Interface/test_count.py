from google.cloud import bigquery

bq_client = bigquery.Client(project='wmt-assetprotection-prod')

# Test COUNT query
count_sql = """
SELECT COUNT(*) as total
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE 1=1
"""

result = list(bq_client.query(count_sql).result())
print(f"Total count from database: {result[0].total}")

# Test paginated query
data_sql = """
SELECT project_id, title
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE 1=1
ORDER BY last_updated DESC
LIMIT 10 OFFSET 0
"""

data_result = list(bq_client.query(data_sql).result())
print(f"Returned rows: {len(data_result)}")
for i, row in enumerate(data_result, 1):
    print(f"  {i}. {row.project_id} - {row.title}")
