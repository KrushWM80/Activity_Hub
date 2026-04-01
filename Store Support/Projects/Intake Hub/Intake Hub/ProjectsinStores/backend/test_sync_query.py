"""Test the exact sync query to see project_id values"""
from google.cloud import bigquery

client = bigquery.Client(project="wmt-assetprotection-prod")

query = """
    SELECT 
        COALESCE(CAST(Intake_Card AS STRING), CAST(PROJECT_ID AS STRING), Unique_Key, CONCAT('FAC-', CAST(Facility AS STRING))) as project_id,
        Intake_Card,
        PROJECT_ID,
        Unique_Key,
        Facility,
        Project_Source,
        Title
    FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
    WHERE Status = 'Active'
      AND Project_Source = 'Realty'
    LIMIT 10
"""

print("Testing sync query for Realty records:\n")
for i, row in enumerate(client.query(query).result(), 1):
    print(f"{i}. project_id={row.project_id}, Facility={row.Facility}, Title='{row.Title[:20] if row.Title else None}'")

print("\n" + "="*60 + "\n")

# Check for NULL project_id in result
null_query = """
    SELECT COUNT(*) as null_count
    FROM (
        SELECT 
            COALESCE(CAST(Intake_Card AS STRING), CAST(PROJECT_ID AS STRING), Unique_Key, CONCAT('FAC-', CAST(Facility AS STRING))) as project_id
        FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
        WHERE Status = 'Active'
          AND Project_Source = 'Realty'
    )
    WHERE project_id IS NULL
"""

result = list(client.query(null_query).result())[0]
print(f"Realty records with NULL project_id in query result: {result.null_count}")
