from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

print("Checking column names in Intake Hub source table...\n")

# First, let's see the schema
sql = """
SELECT column_name, data_type
FROM `wmt-assetprotection-prod.Store_Support_Dev.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'Output - Intake Accel Council Data'
ORDER BY ordinal_position
"""

try:
    results = list(client.query(sql).result())
    
    print("Available columns in 'Output - Intake Accel Council Data':\n")
    for row in results:
        print(f"  {row.column_name:<40} {row.data_type}")
        
except Exception as e:
    print(f"Error: {str(e)}")
