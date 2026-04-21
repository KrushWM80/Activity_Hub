#!/usr/bin/env python3
"""
Fresh sync of AH_Projects from Output - Intake Accel Council Data.
This clears existing projects and repopulates with all ACTIVE projects from Intake Hub.
"""

from google.cloud import bigquery
from datetime import datetime

client = bigquery.Client()

print("\n" + "="*80)
print("FRESH SYNC: AH_Projects from Intake Accel Council Data")
print("="*80)

# Step 1: Clear existing data
print("\n[Step 1] Clearing existing AH_Projects data...")
try:
    clear_sql = "DELETE FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects` WHERE 1=1"
    job = client.query(clear_sql)
    job.result()
    print("✓ AH_Projects cleared")
except Exception as e:
    print(f"✗ Error clearing table: {e}")
    exit(1)

# Step 2: Fetch all ACTIVE projects from Intake Hub
print("\n[Step 2] Fetching ACTIVE projects from Intake Hub...")
source_sql = """
SELECT 
    CAST(Intake_Card_Nbr AS STRING) as project_id,
    Project_Title as title,
    Business_Owner_Area as business_organization,
    Project_Lead_Name as owner,
    Project_Lead_ID as owner_id,
    Health_Status as health,
    Status as status,
    'Intake Hub' as project_source,
    Created_Date as created_date,
    Project_Update_Date as last_updated,
    Project_Update_Date as project_update
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
WHERE Status NOT IN ('Complete', 'Removed')
ORDER BY Business_Owner_Area, Project_Title
"""

try:
    source_projects = list(client.query(source_sql).result())
    print(f"✓ Found {len(source_projects)} active projects")
except Exception as e:
    print(f"✗ Error fetching source data: {e}")
    exit(1)

# Step 3: Insert all projects into AH_Projects
print("\n[Step 3] Inserting projects into AH_Projects...")

batch_size = 500
total_inserted = 0

for batch_idx in range(0, len(source_projects), batch_size):
    batch = source_projects[batch_idx:batch_idx + batch_size]
    
    insert_sql = """
    INSERT INTO `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
    (project_id, title, business_organization, owner, owner_id, health, status, project_source,
     created_date, last_updated, project_update)
    VALUES 
    """
    
    using_params = []
    
    for i, row in enumerate(batch):
        if i > 0:
            insert_sql += ", "
        
        params = [
            bigquery.ScalarQueryParameter(f"p{i}_project_id", "STRING", row.project_id),
            bigquery.ScalarQueryParameter(f"p{i}_title", "STRING", row.title),
            bigquery.ScalarQueryParameter(f"p{i}_business_organization", "STRING", row.business_organization),
            bigquery.ScalarQueryParameter(f"p{i}_owner", "STRING", row.owner),
            bigquery.ScalarQueryParameter(f"p{i}_owner_id", "STRING", row.owner_id),
            bigquery.ScalarQueryParameter(f"p{i}_health", "STRING", row.health),
            bigquery.ScalarQueryParameter(f"p{i}_status", "STRING", row.status),
            bigquery.ScalarQueryParameter(f"p{i}_project_source", "STRING", row.project_source),
            bigquery.ScalarQueryParameter(f"p{i}_created_date", "TIMESTAMP", row.created_date),
            bigquery.ScalarQueryParameter(f"p{i}_last_updated", "TIMESTAMP", row.last_updated),
            bigquery.ScalarQueryParameter(f"p{i}_project_update", "STRING", row.project_update),
        ]
        
        using_params.extend(params)
        insert_sql += f"""(@p{i}_project_id, @p{i}_title, @p{i}_business_organization, @p{i}_owner, 
                      @p{i}_owner_id, @p{i}_health, @p{i}_status, @p{i}_project_source,
                      @p{i}_created_date, @p{i}_last_updated, @p{i}_project_update)"""
    
    try:
        job_config = bigquery.QueryJobConfig(query_parameters=using_params)
        job = client.query(insert_sql, job_config=job_config)
        job.result()
        total_inserted += len(batch)
        print(f"  ✓ Batch {batch_idx + len(batch)}/{len(source_projects)} inserted")
    except Exception as e:
        print(f"✗ Error inserting batch: {e}")
        exit(1)

# Step 4: Verify
print("\n[Step 4] Verifying data...")
verify_sql = """
SELECT 
    COUNT(*) as total_projects,
    COUNT(DISTINCT business_organization) as distinct_business_areas,
    COUNT(DISTINCT project_source) as distinct_sources
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
"""

results = client.query(verify_sql).result()
for row in results:
    print(f"✓ Total Projects: {row.total_projects}")
    print(f"✓ Distinct Business Areas: {row.distinct_business_areas}")
    print(f"✓ Distinct Project Sources: {row.distinct_sources}")

# Step 5: Show business area distribution
print("\n[Step 5] Business Area Distribution:")
print("-" * 60)
dist_sql = """
SELECT 
    business_organization,
    COUNT(*) as count
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
GROUP BY business_organization
ORDER BY count DESC
"""

results = client.query(dist_sql).result()
for row in results:
    print(f"  {row.business_organization:40} | {row.count:5} projects")

print("\n" + "="*80)
print(f"SYNC COMPLETE: {total_inserted} projects synced at {datetime.now().isoformat()}")
print("="*80 + "\n")
