from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

print("Checking current data for project 18049:\n")

sql = """
SELECT 
    project_id,
    title,
    store_area,
    business_organization,
    owner,
    health,
    status,
    last_updated,
    project_update_date,
    project_update
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE project_id = '18049'
"""

try:
    results = list(client.query(sql).result())
    
    if results:
        row = results[0]
        print("Current AH_Projects state for project 18049:")
        print(f"  project_id: {row.project_id}")
        print(f"  title: {row.title if row.title else 'NULL'}")
        print(f"  store_area: {row.store_area if row.store_area else 'NULL'}")
        print(f"  business_organization: {row.business_organization if row.business_organization else 'NULL'}")
        print(f"  owner: {row.owner if row.owner else 'NULL'}")
        print(f"  health: {row.health if row.health else 'NULL'}")
        print(f"  status: {row.status if row.status else 'NULL'}")
        print(f"  last_updated: {row.last_updated}")
        print(f"  project_update_date: {row.project_update_date if row.project_update_date else 'NULL'}")
        print(f"  project_update: {row.project_update if row.project_update else 'NULL'}")
        
        print("\n" + "="*80)
        
        # Now check if the project shows up in the API query
        print("\nChecking if project would be visible with current WHERE clause:\n")
        print("API WHERE clause: WHERE TRIM(business_organization) != ''")
        print(f"Current business_organization value: '{row.business_organization}'")
        print(f"TRIM of that value: '{row.business_organization.strip() if row.business_organization else ''}'")
        
        if row.business_organization and row.business_organization.strip():
            print("✓ Project WOULD BE VISIBLE")
        else:
            print("✗ Project would be HIDDEN")
        
except Exception as e:
    print(f"Error: {str(e)}")

print("\n" + "="*80)
print("Source data from Intake Hub for comparison:\n")

sql2 = """
SELECT 
    Intake_Card_Nbr,
    Project_Title,
    Business_Owner_Area,
    Store_Area,
    Owner
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
WHERE Intake_Card_Nbr = 18049
"""

try:
    results = list(client.query(sql2).result())
    
    if results:
        row = results[0]
        print("Source data from Intake Hub:")
        print(f"  Intake_Card_Nbr: {row.Intake_Card_Nbr}")
        print(f"  Project_Title: {row.Project_Title if row.Project_Title else 'NULL'}")
        print(f"  Business_Owner_Area: '{row.Business_Owner_Area if row.Business_Owner_Area else 'NULL'}'")
        print(f"  Store_Area: {row.Store_Area if row.Store_Area else 'NULL'}")
        print(f"  Owner: {row.Owner if row.Owner else 'NULL'}")
        
except Exception as e:
    print(f"Error: {str(e)}")
