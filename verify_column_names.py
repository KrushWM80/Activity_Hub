from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Get full schema
sql = """
SELECT column_name, data_type
FROM `wmt-assetprotection-prod.Store_Support_Dev.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'AH_Projects'
ORDER BY ordinal_position
"""

print("All AH_Projects columns:\n")
cols = []
try:
    for row in client.query(sql).result():
        cols.append(row.column_name)
        print(f"  {row.column_name}")
        
    print("\n" + "="*80)
    if 'business_area' in cols:
        print("✓ business_area column EXISTS")
    else:
        print("✗ business_area column NOT FOUND")
        
    if 'business_organization' in cols:
        print("✓ business_organization column EXISTS")
    else:
        print("✗ business_organization column NOT FOUND")
        
except Exception as e:
    print(f"Error: {str(e)}")
