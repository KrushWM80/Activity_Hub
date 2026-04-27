from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Get all columns from source table
query = """
SELECT column_name 
FROM `wmt-assetprotection-prod.Store_Support_Dev.INFORMATION_SCHEMA.COLUMNS` 
WHERE table_name = 'Output - Intake Accel Council Data'
ORDER BY ordinal_position
LIMIT 200
"""

results = list(client.query(query).result())
print("All columns in source table:")
for i, row in enumerate(results, 1):
    col_name = row.column_name.lower()
    if 'business' in col_name or 'area' in col_name or 'org' in col_name or 'department' in col_name or 'category' in col_name:
        print(f"  [{i}] {row.column_name} **")
    else:
        print(f"  [{i}] {row.column_name}")
