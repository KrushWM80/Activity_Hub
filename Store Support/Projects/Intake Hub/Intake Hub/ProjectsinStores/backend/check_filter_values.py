# Check more columns for Partners data
from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Check specific values
search_terms = ['Activity Team', 'Intake', 'Validation', 'Implement']

# First, let's search across multiple text columns
query = """
SELECT 
    DISTINCT 
    COALESCE(Business_Area, '') as business_area,
    COALESCE(Business_Type, '') as business_type,
    COALESCE(Store_Area, '') as store_area,
    COALESCE(Health, '') as health,
    COALESCE(PROJECT_HEALTH, '') as project_health,
    COALESCE(ASSOCIATE_IMPACT, '') as associate_impact,
    COALESCE(CUSTOMER_IMPACT, '') as customer_impact,
    COALESCE(Owner, '') as owner,
    COALESCE(PROJECT_OWNER, '') as project_owner
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Status = 'Active'
LIMIT 5
"""

print("Sample of key columns:")
print("="*80)
results = list(client.query(query).result())
for row in results:
    print(f"Business Area: {row.business_area}")
    print(f"Business Type: {row.business_type}")
    print(f"Store Area: {row.store_area}")
    print(f"Health: {row.health}")
    print(f"Project Health: {row.project_health}")
    print(f"Associate Impact: {row.associate_impact}")
    print(f"Customer Impact: {row.customer_impact}")
    print(f"Owner: {row.owner}")
    print(f"Project Owner: {row.project_owner}")
    print("-"*40)

# Get distinct values for each filter column
print("\n\nDISTINCT VALUES FOR EACH FILTER:")

columns = {
    'Business_Type': 'Business Type',
    'Store_Area': 'Store Area', 
    'Health': 'Health',
    'PROJECT_HEALTH': 'Project Health',
    'ASSOCIATE_IMPACT': 'Associate Impact',
    'CUSTOMER_IMPACT': 'Customer Impact'
}

for col, label in columns.items():
    query = f"""
    SELECT DISTINCT {col} as value, COUNT(*) as cnt
    FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
    WHERE Status = 'Active' AND {col} IS NOT NULL AND TRIM({col}) != ''
    GROUP BY {col}
    ORDER BY cnt DESC
    LIMIT 20
    """
    print(f"\n{'='*60}")
    print(f"{label} ({col}):")
    print('='*60)
    try:
        results = list(client.query(query).result())
        if not results:
            print("  (no data)")
        for row in results:
            print(f"  {row.value}: {row.cnt}")
    except Exception as e:
        print(f"  Error: {e}")
