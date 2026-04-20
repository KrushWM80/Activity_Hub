from google.cloud import bigquery

bq_client = bigquery.Client(project='wmt-assetprotection-prod')

print("Fixing duplicates in AH_Projects table...")
print("This will keep only the latest version of each project.\n")

# Step 1: Backup the old table
backup_sql = """
CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects_backup` AS
SELECT * FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
"""

print("Step 1: Creating backup...")
job = bq_client.query(backup_sql)
job.result()
print("✓ Backup created\n")

# Step 2: Delete current table and recreate with deduplicated data
recreate_sql = """
CREATE OR REPLACE TABLE `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects` AS
SELECT 
    project_id,
    title,
    store_area,
    owner,
    owner_id,
    health,
    status,
    created_date,
    last_updated,
    project_update,
    project_source,
    director_id,
    sr_director_id,
    ho_impact,
    impact,
    store_count,
    projected_start_date
FROM (
    SELECT 
        *,
        ROW_NUMBER() OVER (PARTITION BY project_id ORDER BY last_updated DESC) as rn
    FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects_backup`
)
WHERE rn = 1
"""

print("Step 2: Recreating table with deduplicated data...")
job = bq_client.query(recreate_sql)
job.result()
print("✓ Table recreated\n")

# Step 3: Verify
verify_sql = """
SELECT 
    COUNT(*) as total_rows,
    COUNT(DISTINCT project_id) as distinct_projects
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
"""

print("Step 3: Verifying results...")
results = list(bq_client.query(verify_sql).result())
row = results[0]
print(f"✓ Total rows: {row.total_rows}")
print(f"✓ Distinct projects: {row.distinct_projects}")
print(f"✓ Duplicates removed: {962548 - row.total_rows}\n")

print("✅ Fix complete! The table now contains only unique projects.")
