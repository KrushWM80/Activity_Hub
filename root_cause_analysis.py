from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

print("Checking Intake Hub source for project 18049 with CORRECT column names...\n")

# Using actual column names from schema
sql = """
SELECT 
    Intake_Card_Nbr,
    Project_Title,
    Owner,
    Store_Area,
    PROJECT_HEALTH_DESC,
    Last_Updated
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
WHERE Intake_Card_Nbr = 18049
LIMIT 1
"""

try:
    results = list(client.query(sql).result())
    
    if results:
        row = results[0]
        print("✓ Found in Intake Hub Source!\n")
        print(f"  Intake_Card_Nbr: {row.Intake_Card_Nbr}")
        print(f"  Project_Title: {row.Project_Title if row.Project_Title else 'NULL'}")
        print(f"  Owner: {row.Owner if row.Owner else 'NULL'}")
        print(f"  Store_Area: {row.Store_Area if row.Store_Area else 'NULL'}")
        print(f"  PROJECT_HEALTH_DESC: {row.PROJECT_HEALTH_DESC if row.PROJECT_HEALTH_DESC else 'NULL'}")
        print(f"  Last_Updated: {row.Last_Updated}")
        
        print("\n" + "=" * 80)
        print("ROOT CAUSE ANALYSIS")
        print("=" * 80 + "\n")
        
        print("Why Tour Guides is INVISIBLE:\n")
        print("In AH_Projects (Activity Hub database):")
        print(f"  ✗ business_organization is EMPTY (filtered out by WHERE TRIM(business_organization) != '')\n")
        print(f"Correct value should be: {row.Store_Area if row.Store_Area else 'NULL (also missing in source!)'}\n")
        
        if row.Project_Title:
            print(f"✓ Project_Title MATCHES: '{row.Project_Title}'")
        else:
            print(f"✗ Project_Title is also NULL in source!")
            
        if row.Owner:
            print(f"✓ Owner EXISTS in source: '{row.Owner}'")
        else:
            print(f"✗ Owner is NULL in source!")
            
        print("\n" + "=" * 80)
        print("FIELD MAPPING (Source → AH_Projects)")
        print("=" * 80 + "\n")
        
        print(f"Intake_Card_Nbr: {row.Intake_Card_Nbr}")
        print(f"  └→ project_id in AH_Projects: 18049 ✓ MATCHES\n")
        
        print(f"Project_Title: {row.Project_Title if row.Project_Title else 'NULL'}")
        print(f"  └→ title in AH_Projects: NULL ✗ MISMATCH\n")
        
        print(f"Owner: {row.Owner if row.Owner else 'NULL'}")
        print(f"  └→ owner in AH_Projects: NULL ✗ MISMATCH\n")
        
        print(f"Store_Area: {row.Store_Area if row.Store_Area else 'NULL'}")
        print(f"  └→ business_organization in AH_Projects: EMPTY ✗ MISMATCH\n")
        
        print(f"PROJECT_HEALTH_DESC: {row.PROJECT_HEALTH_DESC if row.PROJECT_HEALTH_DESC else 'NULL'}")
        print(f"  └→ health in AH_Projects: NULL ✗ MISMATCH\n")
        
        print("\n" + "=" * 80)
        print("CONCLUSION")
        print("=" * 80 + "\n")
        
        print("The data exists in Intake Hub source but wasn't synced to AH_Projects.")
        print("When you edited the project on April 23, it updated last_updated timestamp")
        print("but the sync didn't populate the missing fields.")
        print("\nThe project is hidden because business_organization is empty,")
        print("which triggers the filtering WHERE clause in the API.")
        
    else:
        print("✗ Project 18049 not found in Intake Hub source")
        
except Exception as e:
    print(f"Error: {str(e)}")
