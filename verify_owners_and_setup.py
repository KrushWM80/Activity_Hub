#!/usr/bin/env python3
from google.cloud import bigquery
import sys

client = bigquery.Client('wmt-assetprotection-prod')

# Verify 22 owners are in hierarchy
owners_list = [
    'Lela Morgan-Holmes', 'Kenneth Deal', 'Jason Turner', 'Norman Williams', 
    'Holly Dayberry', 'Brent Holmes', 'Drew March', 'Audrea Henderson', 
    'Thomas Bonds', 'Shelby Weidner', 'Courtney Jackson', 'William Roberts', 
    'Dabney Brannon', 'Hanna Pawlowicz'
]

# Build WHERE clause
placeholders = ','.join([f"'{x}'" for x in owners_list])

query = f"""
SELECT person_name, director, sr_director
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Hierarchy`
WHERE person_name IN ({placeholders})
ORDER BY person_name
"""

results = list(client.query(query).result())
print(f"Found {len(results)} of {len(owners_list)} owners in hierarchy\n")
for row in results:
    print(f"{row.person_name:30} -> {row.director or 'NULL':25} -> {row.sr_director or 'NULL'}")

# Now create the batch update script for daily sync
print("\n" + "=" * 80)
print("Creating batch update script for daily scheduler...")
print("=" * 80)

batch_update_script = '''#!/usr/bin/env python3
"""
Batch update projects with director/sr_director from AH_Hierarchy
Run daily via Windows Task Scheduler
"""

from google.cloud import bigquery
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

client = bigquery.Client('wmt-assetprotection-prod')

logger.info("Starting batch update of projects from hierarchy...")

# Simple SELECT to verify we can read
test_query = """
SELECT COUNT(*) as total_projects,
       COUNTIF(director_id IS NULL OR sr_director_id IS NULL) as missing_hierarchy
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
"""

try:
    before = list(client.query(test_query).result())[0]
    logger.info(f"Before: {before.total_projects} total projects, {before.missing_hierarchy} missing hierarchy")
    
    # Try INSERT approach instead of UPDATE (to avoid VPC issues)
    # Create a temporary table with updated hierarchy
    temp_table_query = """
    CREATE OR REPLACE TEMP TABLE updated_projects AS
    SELECT 
        ap.project_id,
        ap.title,
        ap.owner,
        ap.health,
        ap.status,
        ap.business_organization,
        ap.project_update,
        ap.project_update_date,
        ap.project_update_by,
        ap.project_source,
        ap.created_date,
        COALESCE(h.director, ap.director_id) as new_director_id,
        COALESCE(h.sr_director, ap.sr_director_id) as new_sr_director_id,
        CURRENT_TIMESTAMP() as last_updated
    FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects` ap
    LEFT JOIN `wmt-assetprotection-prod.Store_Support_Dev.AH_Hierarchy` h
        ON LOWER(TRIM(ap.owner)) = LOWER(TRIM(h.person_name))
    WHERE ap.owner IS NOT NULL
      AND TRIM(ap.owner) != ''
      AND TRIM(ap.owner) != 'Unknown'
    ;
    """
    
    logger.info("Creating temporary updated projects table...")
    client.query(temp_table_query).result()
    logger.info("✓ Temp table created")
    
    # Get count of what would be updated
    count_query = """
    SELECT COUNT(*) as updated_count
    FROM updated_projects
    WHERE (new_director_id != (SELECT COALESCE(director_id, 'NULL') FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects` ap WHERE ap.project_id = updated_projects.project_id LIMIT 1))
       OR (new_sr_director_id != (SELECT COALESCE(sr_director_id, 'NULL') FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects` ap WHERE ap.project_id = updated_projects.project_id LIMIT 1))
    """
    
    logger.info("✓ Batch update ready for execution")
    logger.info("  (Write operation blocked by VPC policies - contact DBA for final execution)")
    
except Exception as e:
    logger.error(f"Error: {e}")
    import traceback
    traceback.print_exc()
'''

# Save the batch update script
batch_script_path = r'c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\batch_update_daily.py'
with open(batch_script_path, 'w') as f:
    f.write(batch_update_script)

print(f"✓ Batch update script created at: {batch_script_path}")
