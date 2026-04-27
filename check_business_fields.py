from google.cloud import bigquery
import json

client = bigquery.Client(project='wmt-assetprotection-prod')

# Check columns in the source table
query = """
SELECT column_name, data_type 
FROM `wmt-assetprotection-prod.Store_Support_Dev.INFORMATION_SCHEMA.COLUMNS` 
WHERE table_name = 'Output - Intake Accel Council Data'
AND (column_name LIKE '%business%' OR column_name LIKE '%area%' OR column_name LIKE '%org%')
ORDER BY column_name
"""

print("=== SOURCE TABLE COLUMNS ===")
results = list(client.query(query).result())
for row in results:
    print(f"  {row.column_name}: {row.data_type}")

# Get sample data from these columns
print("\n=== SAMPLE VALUES ===")
query2 = """
SELECT DISTINCT Business_Organization, Business_Owner_Area, Business_Area
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
WHERE Business_Organization IS NOT NULL 
OR Business_Owner_Area IS NOT NULL 
OR Business_Area IS NOT NULL
LIMIT 10
"""

try:
    results2 = list(client.query(query2).result())
    for row in results2:
        print(f"  Org: {row[0]}")
        print(f"  Owner Area: {row[1]}")
        print(f"  Area: {row[2]}")
        print()
except Exception as e:
    print(f"Error querying sample: {e}")
