"""Debug: Check what fields are populated for Realty records"""
from google.cloud import bigquery

client = bigquery.Client(project="wmt-assetprotection-prod")

# Check which fields are NOT NULL for Realty records to find a suitable project_id
query = """
SELECT 
    COUNT(*) as total_realty,
    COUNT(DISTINCT Intake_Card) as intake_card_count,
    COUNT(DISTINCT PROJECT_ID) as project_id_count,
    COUNT(DISTINCT Unique_Key) as unique_key_count,
    COUNT(DISTINCT Facility) as facility_count,
    COUNT(DISTINCT Realty_Source) as realty_source_count,
    COUNT(DISTINCT Possession_Date) as possession_date_count,
    COUNT(CASE WHEN Intake_Card IS NOT NULL THEN 1 END) as nonnull_intake_card,
    COUNT(CASE WHEN PROJECT_ID IS NOT NULL THEN 1 END) as nonnull_project_id,
    COUNT(CASE WHEN Unique_Key IS NOT NULL THEN 1 END) as nonnull_unique_key,
    COUNT(CASE WHEN Facility IS NOT NULL THEN 1 END) as nonnull_facility,
    COUNT(CASE WHEN Title IS NOT NULL THEN 1 END) as nonnull_title,
    COUNT(CASE WHEN Realty_Source IS NOT NULL THEN 1 END) as nonnull_realty_source
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Project_Source = 'Realty'
  AND Status = 'Active'
"""

print("Checking what fields are populated for active Realty records...\n")
result = list(client.query(query).result())[0]

for field, value in result.items():
    print(f"{field:<30} = {value}")

print("\n" + "="*60 + "\n")

# Show a sample of actual data
print("Sample Realty records (first 10):")
sample_query = """
SELECT 
    Intake_Card,
    PROJECT_ID,
    Unique_Key,
    Facility,
    Title,
    Realty_Source,
    Status,
    Project_Source
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Project_Source = 'Realty'
  AND Status = 'Active'
LIMIT 10
"""

for i, row in enumerate(client.query(sample_query).result(), 1):
    print(f"\n{i}. Intake_Card={row.Intake_Card}, PROJECT_ID={row.PROJECT_ID}, Unique_Key={row.Unique_Key}, "
          f"Facility={row.Facility}, Title='{row.Title[:30] if row.Title else None}'")
