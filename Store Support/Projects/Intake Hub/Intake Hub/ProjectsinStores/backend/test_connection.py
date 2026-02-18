"""Quick test to verify BigQuery connection and data"""
from google.cloud import bigquery

client = bigquery.Client(project="wmt-assetprotection-prod")

# Test 1: Check project sources
query1 = """
SELECT DISTINCT Project_Source, COUNT(*) as count
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Status = 'Active'
GROUP BY Project_Source
"""
print("=== PROJECT SOURCES ===")
for row in client.query(query1).result():
    print(f"{row.Project_Source}: {row.count}")

# Test 2: Check if simple query works
query2 = """
SELECT 
    CAST(Intake_Card AS STRING) as project_id,
    Project_Source,
    Title,
    Division,
    CAST(39.0 + MOD(CAST(Facility AS INT64), 15) AS FLOAT64) as latitude,
    CAST(-95.0 + MOD(CAST(Facility AS INT64), 30) AS FLOAT64) as longitude
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Status = 'Active'
LIMIT 3
"""
print("\n=== SAMPLE RECORDS WITH COORDINATES ===")
for row in client.query(query2).result():
    print(f"{row.project_id}: {row.Title[:40]} | {row.Project_Source} | Lat: {row.latitude}, Lon: {row.longitude}")
