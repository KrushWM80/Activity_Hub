"""Check the position of GMD Tote Divider in the sorted list"""
from google.cloud import bigquery

client = bigquery.Client(project="wmt-assetprotection-prod")

# Get the 10,000th project by Last_Updated DESC
query = """
WITH ranked AS (
    SELECT 
        Title,
        Last_Updated,
        Status,
        ROW_NUMBER() OVER (ORDER BY Last_Updated DESC) as row_num
    FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
    WHERE Status = 'Active'
)
SELECT Title, Last_Updated, row_num
FROM ranked
WHERE Title = 'GMD Tote Divider POC Test with Volumetrics'
   OR row_num = 10000
ORDER BY row_num
"""

results = client.query(query).result()

print("Results:")
for row in results:
    print(f"  Row #{row.row_num}: {row.Title}")
    print(f"  Last Updated: {row.Last_Updated}")
    print()
