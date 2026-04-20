from google.cloud import bigquery

bq_client = bigquery.Client(project='wmt-assetprotection-prod')

# Check the source table columns
source_sql = """
SELECT column_name, data_type
FROM `wmt-assetprotection-prod.Store_Support_Dev.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'Output___Intake_Accel_Council_Data'
ORDER BY ordinal_position
LIMIT 50
"""

print("=== Source Table Columns (First 50) ===\n")
results = list(bq_client.query(source_sql).result())
for i, row in enumerate(results, 1):
    print(f"  {i}. {row.column_name}: {row.data_type}")

# Get sample row
sample_sql = """
SELECT project_id, project_name, impact, business_area, business_organization, department, owner
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output___Intake_Accel_Council_Data`
LIMIT 1
"""

print("\n=== Checking for Business Organization ===\n")
try:
    sample = list(bq_client.query(sample_sql).result())
    if sample:
        row = sample[0]
        for key in row.keys():
            value = row[key]
            print(f"  {key}: {value}")
except Exception as e:
    print(f"Error: {e}")
    print("Trying alternative query...")
    # Try to see what columns are available
    alt_sql = """
    SELECT *
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Output___Intake_Accel_Council_Data`
    LIMIT 1
    """
    sample = list(bq_client.query(alt_sql).result())
    if sample:
        row = sample[0]
        print("Available columns in first row:")
        for key in list(row.keys())[:20]:  # Show first 20
            try:
                value = row[key]
                print(f"  {key}: {value}")
            except:
                pass
