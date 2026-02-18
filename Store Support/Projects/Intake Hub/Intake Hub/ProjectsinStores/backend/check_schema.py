# Quick Schema Check
from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Get table schema
table = client.get_table('wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data')

print("Table Schema:")
print("=" * 60)
for field in table.schema:
    print(f"{field.name:30} {field.field_type:15}")

print("\n" + "=" * 60)
print("\nFetching sample row...")

query = """
SELECT *
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Status = 'Active'
LIMIT 1
"""

result = list(client.query(query).result())
if result:
    row = result[0]
    print("\nSample Data:")
    print("=" * 60)
    for key in row.keys():
        value = row[key]
        if value is not None and str(value).strip():
            print(f"{key:30} {value}")
