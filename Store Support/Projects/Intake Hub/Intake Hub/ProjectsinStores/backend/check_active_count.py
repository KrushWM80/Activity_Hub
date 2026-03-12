from google.cloud import bigquery
client = bigquery.Client(project='wmt-assetprotection-prod')

# Count all active
query = """
SELECT COUNT(*) as total
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Status = 'Active'
"""
result = list(client.query(query).result())
print(f"Total Active records in BigQuery: {result[0]['total']}")

# Count by project source
query2 = """
SELECT Project_Source, COUNT(*) as count
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Status = 'Active'
GROUP BY Project_Source
ORDER BY count DESC
"""
result = list(client.query(query2).result())
print("\nBreakdown by Project_Source:")
for row in result:
    print(f"  {row['Project_Source']}: {row['count']}")
