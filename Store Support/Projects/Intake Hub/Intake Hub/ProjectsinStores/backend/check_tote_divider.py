"""Check if GMD Tote Divider project exists in BigQuery"""
from google.cloud import bigquery

client = bigquery.Client(project="wmt-assetprotection-prod")

query = """
SELECT 
    Title,
    COUNT(*) as store_count,
    MAX(Last_Updated) as last_updated,
    Phase,
    Status
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE LOWER(Title) LIKE '%gmd%tote%divider%'
GROUP BY Title, Phase, Status
ORDER BY last_updated DESC
"""

results = client.query(query).result()

print("GMD Tote Divider projects:")
for row in results:
    print(f"  Title: {row.Title}")
    print(f"  Stores: {row.store_count}")
    print(f"  Last Updated: {row.last_updated}")
    print(f"  Phase: {row.Phase}")
    print(f"  Status: {row.Status}")
    print()
