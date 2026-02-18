# Check which column contains Partners data
from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Columns that might contain "Activity Team", "Intake & Test", etc.
columns_to_check = [
    'STRATEGY_GROUP', 'PILLAR', 'tribe', 'INITIATIVE', 
    'Business_Area', 'SC_STRATEGIC_LEVEL', 'Category_Source',
    'Program_Name', 'ROLES'
]

for col in columns_to_check:
    query = f"""
    SELECT DISTINCT {col} as value, COUNT(*) as cnt
    FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
    WHERE Status = 'Active' AND {col} IS NOT NULL AND {col} != ''
    GROUP BY {col}
    ORDER BY cnt DESC
    LIMIT 15
    """
    try:
        print(f"\n{'='*60}")
        print(f"Column: {col}")
        print('='*60)
        results = list(client.query(query).result())
        for row in results:
            print(f"  {row.value}: {row.cnt}")
    except Exception as e:
        print(f"  Error: {e}")
