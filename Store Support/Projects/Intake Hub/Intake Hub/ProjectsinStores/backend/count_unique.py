"""Check unique project titles vs total records"""
from google.cloud import bigquery

client = bigquery.Client(project="wmt-assetprotection-prod")

query = """
SELECT 
    COUNT(*) as total_records,
    COUNT(DISTINCT Title) as unique_titles,
    COUNT(DISTINCT CAST(Intake_Card AS STRING)) as unique_projects
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Status = 'Active'
"""

results = client.query(query).result()

for row in results:
    print(f"Total Active Records: {row.total_records:,}")
    print(f"Unique Project Titles: {row.unique_titles:,}")
    print(f"Unique Project IDs: {row.unique_projects:,}")
    print(f"\nAverage stores per project: {row.total_records / row.unique_titles:.1f}")
