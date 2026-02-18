"""Check store 728 projects and all project sources"""
from google.cloud import bigquery

client = bigquery.Client(project="wmt-assetprotection-prod")

# Check store 728
query1 = """
SELECT DISTINCT Title, Project_Source
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Status = 'Active' AND CAST(Facility AS STRING) = '728'
ORDER BY Title
LIMIT 20
"""
print("=== STORE 728 PROJECTS ===")
for row in client.query(query1).result():
    print(f"{row.Title}: {row.Project_Source}")

# Check all project sources
query2 = """
SELECT DISTINCT Project_Source, COUNT(*) as count
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Status = 'Active'
GROUP BY Project_Source
"""
print("\n=== ALL PROJECT SOURCES ===")
for row in client.query(query2).result():
    print(f"{row.Project_Source}: {row.count}")
    
# Check if source filter is working
query3 = """
SELECT ARRAY_AGG(DISTINCT Project_Source IGNORE NULLS ORDER BY Project_Source) as sources
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Status = 'Active'
"""
print("\n=== SOURCES FOR FILTER ===")
result = list(client.query(query3).result())[0]
print(result.sources)
