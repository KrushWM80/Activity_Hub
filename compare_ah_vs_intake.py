from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

print("=" * 80)
print("COMPARISON: AH_Projects vs Intake Hub Source Data")
print("=" * 80)

# First, check what's in AH_Projects table NOW
print("\n1. CURRENT STATE IN AH_PROJECTS TABLE (Project 18049):\n")
sql_ah = """
SELECT 
    project_id,
    title,
    owner,
    business_organization,
    health,
    project_update,
    project_update_date,
    last_updated,
    project_source
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE project_id = '18049'
"""

results_ah = list(client.query(sql_ah).result())
if results_ah:
    row = results_ah[0]
    print(f"  project_id: {row.project_id}")
    print(f"  title: {row.title if row.title else 'NULL/MISSING'}")
    print(f"  owner: {row.owner if row.owner else 'NULL/MISSING'}")
    print(f"  business_organization: '{row.business_organization}' {'(EMPTY)' if row.business_organization == '' else ''}")
    print(f"  health: {row.health if row.health else 'NULL/MISSING'}")
    print(f"  project_update: '{row.project_update if row.project_update else 'NULL/EMPTY'}'")
    print(f"  project_update_date: {row.project_update_date}")
    print(f"  last_updated: {row.last_updated}")
    print(f"  project_source: {row.project_source}")

# Now check Intake Hub source
print("\n\n2. ORIGINAL SOURCE: Intake Hub Projects Table:\n")
sql_intake = """
SELECT *
FROM `wmt-assetprotection-prod.Store_Support_Dev.Intake_Hub_Projects`
WHERE project_ID = '18049'
LIMIT 1
"""

try:
    results_intake = list(client.query(sql_intake).result())
    if results_intake:
        row = results_intake[0]
        print("✓ Found in Intake Hub!\n")
        
        # Display all fields
        for field in row.keys():
            value = getattr(row, field, 'N/A')
            print(f"  {field}: {value if value is not None else 'NULL'}")
    else:
        print("✗ Not found in Intake Hub Projects table")
except Exception as e:
    print(f"✗ Error querying Intake Hub: {str(e)}")

# Let's also check if there's history/audit log
print("\n\n3. CHECKING FOR UPDATE HISTORY:\n")
sql_history = """
SELECT 
    project_id,
    last_updated,
    project_update_by,
    previous_updates
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE project_id = '18049'
"""

results_hist = list(client.query(sql_history).result())
if results_hist:
    row = results_hist[0]
    print(f"  last_updated: {row.last_updated}")
    print(f"  project_update_by: {row.project_update_by}")
    print(f"  previous_updates: {row.previous_updates if row.previous_updates else 'None/Empty'}")

# Check if the update overwrote the data
print("\n\n4. ANALYSIS:\n")
print("  Looking for what might have happened:")
print("  - If you edited the project yesterday, check if you:")
print("    a) Cleared the title field accidentally")
print("    b) Cleared the owner field accidentally")
print("    c) The business_organization is empty (filtered out by API)")
print("    d) The project_source shows 'Intake Hub' - was it synced after edit?")
