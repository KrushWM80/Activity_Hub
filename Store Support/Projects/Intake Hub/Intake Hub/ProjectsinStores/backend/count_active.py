"""Check total count of active projects in BigQuery"""
from google.cloud import bigquery

client = bigquery.Client(project="wmt-assetprotection-prod")

query = """
SELECT COUNT(*) as total_count
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Status = 'Active'
"""

results = client.query(query).result()

for row in results:
    print(f"Total Active Projects: {row.total_count:,}")
