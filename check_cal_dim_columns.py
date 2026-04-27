from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Get column info
query = """
SELECT column_name, data_type
FROM `wmt-assetprotection-prod.Store_Support_Dev.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'Cal_Dim_Data'
ORDER BY ordinal_position
"""

results = list(client.query(query).result())

print("Cal_Dim_Data columns:")
for row in results:
    print(f"  - {row.column_name:30} {row.data_type}")
