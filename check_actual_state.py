from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

print("Checking actual field names and values in AH_Projects for project 18049:\n")

sql = """
SELECT 
    project_id,
    title,
    business_area,
    business_organization,
    owner,
    health,
    store_area,
    last_updated,
    project_update_date,
    last_edited_timestamp
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
        print(f"  business_area: {row.business_area if row.business_area else 'NULL'}")
        print(f"  business_organization: {row.business_organization if row.business_organization else 'NULL'}")
        print(f"  owner: {row.owner if row.owner else 'NULL'}")
        print(f"  health: {row.health if row.health else 'NULL'}")
        print(f"  store_area: {row.store_area if row.store_area else 'NULL'}")
        print(f"  last_updated: {row.last_updated}")
        print(f"  project_update_date: {row.project_update_date if row.project_update_date else 'NULL'}")
        print(f"  last_edited_timestamp: {row.last_edited_timestamp if row.last_edited_timestamp else 'NULL'}")
        
        print("\n" + "="*80)
        print("Now checking what field is being used for filtering in the API query:\n")
        
except Exception as e:
    print(f"Error querying AH_Projects: {str(e)}")

print("\nAlso checking Intake Hub source for comparison:")
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
        print(f"  Business_Owner_Area: {row.Business_Owner_Area if row.Business_Owner_Area else 'NULL'}")
        print(f"  Store_Area: {row.Store_Area if row.Store_Area else 'NULL'}")
        print(f"  Owner: {row.Owner if row.Owner else 'NULL'}")
        
except Exception as e:
    print(f"Error querying source: {str(e)}")
