from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

print("Project 18049 - Verifying field values:\n")

sql = """
SELECT 
    project_id,
    title,
    owner,
    business_organization,
    store_area,
    last_updated
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE project_id = '18049'
"""

try:
    results = list(client.query(sql).result())
    
    if results:
        row = results[0]
        print("Current AH_Projects state:")
        print(f"  project_id: {row.project_id}")
        print(f"  title: {row.title if row.title else 'NULL'}")
        print(f"  owner: {row.owner if row.owner else 'NULL'}")
        print(f"  business_organization: '{row.business_organization if row.business_organization else 'NULL'}'")
        print(f"  store_area: {row.store_area if row.store_area else 'NULL'}")
        print(f"  last_updated: {row.last_updated}")
        
except Exception as e:
    print(f"Error: {str(e)}")

print("\n" + "="*80)
print("Intake Hub source for comparison:\n")

sql2 = """
SELECT 
    Intake_Card_Nbr,
    Project_Title,
    Owner,
    Business_Owner_Area,
    Store_Area
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
WHERE Intake_Card_Nbr = 18049
LIMIT 1
"""

try:
    results = list(client.query(sql2).result())
    
    if results:
        row = results[0]
        print("Intake Hub source:")
        print(f"  Intake_Card_Nbr: {row.Intake_Card_Nbr}")
        print(f"  Project_Title: {row.Project_Title if row.Project_Title else 'NULL'}")
        print(f"  Owner: {row.Owner if row.Owner else 'NULL'}")
        print(f"  Business_Owner_Area: '{row.Business_Owner_Area if row.Business_Owner_Area else 'NULL'}'")
        print(f"  Store_Area: {row.Store_Area if row.Store_Area else 'NULL'}")
        
except Exception as e:
    print(f"Error: {str(e)}")
