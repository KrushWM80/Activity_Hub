from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

print("Checking Intake Hub source for project 18049...\n")

# Correct syntax for table name with special characters
sql = """
SELECT 
    Intake_Card_Nbr,
    Project_Name,
    Project_Lead,
    Store_Area,
    Health_Status,
    Last_Updated
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
WHERE Intake_Card_Nbr = 18049
"""

try:
    results = list(client.query(sql).result())
    
    if results:
        row = results[0]
        print("✓ Found in Intake Hub Source!\n")
        print(f"  Intake_Card_Nbr: {row.Intake_Card_Nbr}")
        print(f"  Project_Name: {row.Project_Name if row.Project_Name else 'NULL'}")
        print(f"  Project_Lead: {row.Project_Lead if row.Project_Lead else 'NULL'}")
        print(f"  Store_Area: {row.Store_Area if row.Store_Area else 'NULL'}")
        print(f"  Health_Status: {row.Health_Status if row.Health_Status else 'NULL'}")
        print(f"  Last_Updated: {row.Last_Updated}")
        
        print("\n\nCOMPARISON WITH AH_PROJECTS:\n")
        print(f"Source => AH_Projects Mapping:")
        print(f"  Intake_Card_Nbr (18049) => project_id (18049) ✓")
        print(f"  Project_Name ({row.Project_Name if row.Project_Name else 'NULL'}) => title (NULL) ✗")
        print(f"  Project_Lead ({row.Project_Lead if row.Project_Lead else 'NULL'}) => owner (NULL) ✗")
        print(f"  Store_Area ({row.Store_Area if row.Store_Area else 'NULL'}) => business_organization (EMPTY) ✗")
        
    else:
        print("✗ Not found in Intake Hub source")
        
except Exception as e:
    print(f"Error: {str(e)}")
