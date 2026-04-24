from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

print("=" * 80)
print("COMPARISON: AH_Projects vs Intake Hub SOURCE")
print("=" * 80)

# Check Intake Hub source for project 18049
print("\n1. INTAKE HUB SOURCE DATA (Project Card 18049):\n")
sql_intake = """
SELECT 
    Intake_Card_Nbr,
    Project_Name,
    Project_Lead,
    Project_Lead_Manager,
    Store_Area,
    Health_Status,
    Project_Status,
    Latest_Update,
    Last_Updated
FROM `wmt-assetprotection-prod.Store_Support_Dev.`Output - Intake Accel Council Data``
WHERE Intake_Card_Nbr = 18049
"""

try:
    results_intake = list(client.query(sql_intake).result())
    if results_intake:
        row = results_intake[0]
        print("✓ Found in Intake Hub SOURCE!\n")
        print(f"  Intake_Card_Nbr: {row.Intake_Card_Nbr}")
        print(f"  Project_Name: {row.Project_Name if row.Project_Name else 'NULL'}")
        print(f"  Project_Lead: {row.Project_Lead if row.Project_Lead else 'NULL'}")
        print(f"  Project_Lead_Manager: {row.Project_Lead_Manager if row.Project_Lead_Manager else 'NULL'}")
        print(f"  Store_Area: {row.Store_Area if row.Store_Area else 'NULL'}")
        print(f"  Health_Status: {row.Health_Status if row.Health_Status else 'NULL'}")
        print(f"  Latest_Update: {row.Latest_Update if row.Latest_Update else 'NULL'}")
        print(f"  Last_Updated: {row.Last_Updated}")
    else:
        print("✗ Not found in Intake Hub source")
except Exception as e:
    print(f"✗ Error: {str(e)}")

# Now show current AH_Projects state
print("\n\n2. CURRENT AH_PROJECTS STATE (Project 18049):\n")
sql_ah = """
SELECT 
    project_id,
    title,
    owner,
    business_organization,
    health,
    project_update,
    last_updated
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE project_id = '18049'
"""

results_ah = list(client.query(sql_ah).result())
if results_ah:
    row = results_ah[0]
    print(f"  project_id: {row.project_id}")
    print(f"  title: {row.title if row.title else 'NULL'}")
    print(f"  owner: {row.owner if row.owner else 'NULL'}")
    print(f"  business_organization: '{row.business_organization if row.business_organization else 'EMPTY'}'")
    print(f"  health: {row.health if row.health else 'NULL'}")
    print(f"  project_update: {row.project_update if row.project_update else 'NULL/EMPTY'}")
    print(f"  last_updated: {row.last_updated}")

print("\n\n3. ROOT CAUSE ANALYSIS:\n")
print("  Observations:")
print("  - last_updated timestamp: 2026-04-23 17:45:07 (Yesterday, when you edited)")
print("  - AH_Projects has NULL values for title, owner, health")
print("  - project_source shows 'Intake Hub'")
print("  - business_organization is EMPTY (filtered out by API)")
print("\n  Likely causes:")
print("  1. Your edit cleared the title/owner fields (submitted empty values)")
print("  2. The business_organization should have been populated but wasn't")
print("  3. The API filters out projects with empty business_organization")
print("\n  Solution:")
print("  - Populate missing fields (title, owner, health, business_organization)")
print("  - Then the project will be visible again in Activity Hub")
