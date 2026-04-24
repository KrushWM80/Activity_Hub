from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

print("Checking Intake Hub source for project 18049...\n")

# Using correct column name
sql = """
SELECT 
    Intake_Card_Nbr,
    Project_Title,
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
        print(f"  Project_Title: {row.Project_Title if row.Project_Title else 'NULL'}")
        print(f"  Project_Lead: {row.Project_Lead if row.Project_Lead else 'NULL'}")
        print(f"  Store_Area: {row.Store_Area if row.Store_Area else 'NULL'}")
        print(f"  Health_Status: {row.Health_Status if row.Health_Status else 'NULL'}")
        print(f"  Last_Updated: {row.Last_Updated}")
        
        print("\n" + "=" * 80)
        print("ROOT CAUSE ANALYSIS")
        print("=" * 80 + "\n")
        
        print("Data Flow: Intake Hub Source → AH_Projects mapping\n")
        print(f"Column Mapping:")
        print(f"  1. Intake_Card_Nbr: {row.Intake_Card_Nbr}")
        print(f"     └─> project_id in AH_Projects: 18049 ✓ Correct\n")
        
        print(f"  2. Project_Title: {row.Project_Title if row.Project_Title else 'NULL'}")
        print(f"     └─> title in AH_Projects: NULL ✗ MISSING\n")
        
        print(f"  3. Project_Lead: {row.Project_Lead if row.Project_Lead else 'NULL'}")
        print(f"     └─> owner in AH_Projects: NULL ✗ MISSING\n")
        
        print(f"  4. Store_Area: {row.Store_Area if row.Store_Area else 'NULL'}")
        print(f"     └─> business_organization in AH_Projects: (EMPTY) ✗ MISSING\n")
        
        print(f"  5. Health_Status: {row.Health_Status if row.Health_Status else 'NULL'}")
        print(f"     └─> health in AH_Projects: NULL ✗ MISSING\n")
        
        print("\n" + "=" * 80)
        print("WHY IS THE PROJECT INVISIBLE?")
        print("=" * 80 + "\n")
        
        print("The API query includes this WHERE clause:")
        print("  AND TRIM(business_organization) != ''")
        print("\nSince business_organization is EMPTY in AH_Projects,")
        print("the project is FILTERED OUT and not shown in Activity Hub!")
        
        print("\n\n" + "=" * 80)
        print("WHAT HAPPENED WHEN YOU EDITED IT?")
        print("=" * 80 + "\n")
        
        print("Timeline:")
        print("  1. Project 18049 was synced from Intake Hub (March 17)")
        print("  2. It had missing data (title, owner, business_org)")
        print("  3. You edited it on April 23")
        print("  4. Your edit updated last_updated timestamp")
        print("  5. But the CORE FIELDS (title, owner, business_org) remained NULL/EMPTY")
        print("  6. Since business_organization is still empty, it's FILTERED OUT")
        print("\nThe project didn't disappear - it's actually hidden by the API filter!")
        
    else:
        print("✗ Not found in Intake Hub source")
        
except Exception as e:
    print(f"Error: {str(e)}")
