from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Search for calendar dimension tables
query = """
SELECT table_name
FROM `wmt-assetprotection-prod.Store_Support_Dev.INFORMATION_SCHEMA.TABLES`
WHERE LOWER(table_name) LIKE '%calendar%'
  OR LOWER(table_name) LIKE '%cal_dim%'
  OR LOWER(table_name) LIKE '%date%'
ORDER BY table_name
"""

results = list(client.query(query).result())

print("Available Calendar/Date tables:")
for row in results:
    print(f"  - {row.table_name}")
