from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Get all columns from IH_Intake_Data table
query = """
SELECT column_name, data_type 
FROM `wmt-assetprotection-prod.Store_Support_Dev.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'IH_Intake_Data'
ORDER BY ordinal_position
"""

result = client.query(query).result()
print("Columns in IH_Intake_Data:")
print("-" * 50)
for row in result:
    # Highlight if it might be related to branch/partner
    marker = " <-- BRANCH/PARTNER?" if 'branch' in row.column_name.lower() or 'partner' in row.column_name.lower() else ""
    print(f"{row.column_name}: {row.data_type}{marker}")
