"""Check what fields are available for Realty projects"""
from google.cloud import bigquery

client = bigquery.Client(project="wmt-assetprotection-prod")

# Check a specific Realty project (store 5425)
query1 = """
SELECT *
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Project_Source = 'Realty' 
AND Facility = 5425
LIMIT 1
"""

print("=== Sample Realty Project (Store 5425) ===")
result1 = client.query(query1).result()
for row in result1:
    for key, value in row.items():
        if value is not None and value != '':
            print(f"  {key}: {value}")

# Check for Project_Type and Initiative_Type columns
query2 = """
SELECT 
    Project_Type,
    Initiative_Type,
    Title,
    PROJECT_TITLE,
    COUNT(*) as count
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Project_Source = 'Realty'
GROUP BY Project_Type, Initiative_Type, Title, PROJECT_TITLE
LIMIT 20
"""

print("\n=== Realty Project Types and Initiative Types ===")
try:
    result2 = client.query(query2).result()
    for row in result2:
        print(f"  Project_Type: {row.Project_Type}, Initiative_Type: {row.Initiative_Type}, Title: {row.Title}, PROJECT_TITLE: {row.PROJECT_TITLE}, Count: {row.count}")
except Exception as e:
    print(f"  Error: {e}")
    # Try to find what columns exist
    query3 = """
    SELECT column_name
    FROM `wmt-assetprotection-prod.Store_Support_Dev.INFORMATION_SCHEMA.COLUMNS`
    WHERE table_name = 'IH_Intake_Data'
    ORDER BY column_name
    """
    print("\n=== Available Columns ===")
    result3 = client.query(query3).result()
    for row in result3:
        print(f"  {row.column_name}")
