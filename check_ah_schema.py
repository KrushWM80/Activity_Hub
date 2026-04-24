from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

print("Checking AH_Projects schema:\n")

sql = """
SELECT column_name, data_type
FROM `wmt-assetprotection-prod.Store_Support_Dev.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'AH_Projects'
ORDER BY ordinal_position
"""

try:
    results = list(client.query(sql).result())
    
    print("Available columns in AH_Projects:\n")
    for row in results:
        print(f"  {row.column_name:<40} {row.data_type}")
        
except Exception as e:
    print(f"Error: {str(e)}")
