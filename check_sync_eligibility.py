from google.cloud import bigquery
from datetime import datetime

client = bigquery.Client(project='wmt-assetprotection-prod')

print("Checking sync eligibility for project 18049:\n")

# Get source data
sql_source = """
SELECT 
    CAST(Intake_Card_Nbr AS STRING) as project_id,
    Project_Title as title,
    Business_Owner_Area as business_organization,
    Owner as owner,
    PROJECT_OWNERID as owner_id,
    PROJECT_HEALTH_DESC as health,
    Status as status,
    CAST(Last_Updated AS TIMESTAMP) as last_updated,
    Project_Update as project_update
FROM (
    SELECT 
        *,
        ROW_NUMBER() OVER (PARTITION BY Intake_Card_Nbr ORDER BY Last_Updated DESC) as rn
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
    WHERE ARCHIVED != True AND Intake_Card_Nbr = 18049
)
WHERE rn = 1
"""

print("Source data:")
try:
    source = list(client.query(sql_source).result())
    if source:
        row = source[0]
        print(f"  project_id: {row.project_id}")
        print(f"  title: {row.title}")
        print(f"  business_organization: {row.business_organization}")
        print(f"  owner: {row.owner}")
        print(f"  last_updated: {row.last_updated}")
        print(f"  project_update: {row.project_update[:50]}...")
        src_timestamp = row.last_updated
    else:
        print("  NOT FOUND in source")
        src_timestamp = None
except Exception as e:
    print(f"  Error: {e}")
    src_timestamp = None

print("\n" + "="*80)
print("Current AH_Projects data:\n")

sql_existing = """
SELECT 
    project_id,
    title,
    business_organization,
    owner,
    last_updated
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE project_id = '18049'
"""

try:
    existing = list(client.query(sql_existing).result())
    if existing:
        row = existing[0]
        print(f"  project_id: {row.project_id}")
        print(f"  title: {row.title if row.title else 'NULL'}")
        print(f"  business_organization: {row.business_organization if row.business_organization else 'NULL'}")
        print(f"  owner: {row.owner if row.owner else 'NULL'}")
        print(f"  last_updated: {row.last_updated}")
        existing_timestamp = row.last_updated
    else:
        print("  NOT FOUND")
        existing_timestamp = None
except Exception as e:
    print(f"  Error: {e}")
    existing_timestamp = None

print("\n" + "="*80)
print("Sync comparison:\n")

if src_timestamp and existing_timestamp:
    print(f"Source last_updated:     {src_timestamp}")
    print(f"AH_Projects last_updated: {existing_timestamp}")
    print(f"\nComparison: src > existing? {src_timestamp > existing_timestamp}")
    
    if src_timestamp > existing_timestamp:
        print("✓ SOURCE IS NEWER - Should be synced!")
    else:
        print("✗ Existing is newer or equal - Won't sync")
else:
    print("Cannot compare timestamps")
