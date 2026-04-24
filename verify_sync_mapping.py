from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

print("Checking Store Area mapping in source for project 18049:\n")

sql = """
SELECT 
    Intake_Card_Nbr,
    Business_Owner_Area,
    Store_Area
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
WHERE Intake_Card_Nbr = 18049
LIMIT 1
"""

try:
    results = list(client.query(sql).result())
    
    if results:
        row = results[0]
        print(f"  Business_Owner_Area: {row.Business_Owner_Area if row.Business_Owner_Area else 'NULL'}")
        print(f"  Store_Area: {row.Store_Area if row.Store_Area else 'NULL'}")
        
        print("\n✓ Confirmed: Store_Area = 'Total Store' but sync uses Business_Owner_Area!")
        print("  This is why business_organization is EMPTY in AH_Projects")
        
except Exception as e:
    print(f"Error: {str(e)}")
