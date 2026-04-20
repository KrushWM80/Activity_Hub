from google.cloud import bigquery

bq_client = bigquery.Client(project='wmt-assetprotection-prod')

# Get schema and sample data
schema_sql = """
SELECT column_name, data_type
FROM `wmt-assetprotection-prod.Store_Support_Dev.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'AH_Projects'
ORDER BY ordinal_position
"""

print("=== AH_Projects Schema ===\n")
results = bq_client.query(schema_sql).result()
for row in results:
    print(f"  {row.column_name}: {row.data_type}")

# Get sample row with all data
sample_sql = """
SELECT *
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
LIMIT 1
"""

print("\n=== Sample Data ===\n")
sample = list(bq_client.query(sample_sql).result())
if sample:
    row = sample[0]
    for key in row.keys():
        value = row[key]
        if value is not None:
            print(f"  {key}: {value}")
