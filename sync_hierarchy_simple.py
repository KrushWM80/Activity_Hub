#!/usr/bin/env python3
"""
Simple hierarchy sync: Extract unique people from Intake Hub
Build basic director/sr_director/vp relationships
"""

from google.cloud import bigquery
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

client = bigquery.Client(project='wmt-assetprotection-prod')

BQ_PROJECT = 'wmt-assetprotection-prod'
BQ_DATASET = 'Store_Support_Dev'


def create_hierarchy_table():
    """Create AH_Hierarchy table if it doesn't exist"""
    try:
        logger.info("Creating/verifying AH_Hierarchy table...")
        
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS `{BQ_PROJECT}.{BQ_DATASET}.AH_Hierarchy` (
            person_name STRING NOT NULL,
            director STRING,
            sr_director STRING,
            vp STRING,
            source STRING DEFAULT 'Manual',
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
            is_active BOOLEAN DEFAULT TRUE
        )
        PARTITION BY DATE(last_updated)
        CLUSTER BY person_name
        """
        
        client.query(create_table_sql).result()
        logger.info("✓ AH_Hierarchy table created/verified")
        return True
    except Exception as e:
        logger.error(f"Error creating table: {e}")
        return False


def sync_hierarchy():
    """Simple sync: Extract all unique people and store them"""
    
    logger.info("\n" + "="*80)
    logger.info("STARTING HIERARCHY SYNC")
    logger.info("="*80 + "\n")
    
    if not create_hierarchy_table():
        return False
    
    # Step 1: Debug - check what columns exist
    logger.info("Step 1: Checking Intake Hub table structure...")
    check_sql = f"""
    SELECT column_name, data_type 
    FROM `{BQ_PROJECT}.{BQ_DATASET}.INFORMATION_SCHEMA.COLUMNS`
    WHERE table_name = 'Output - Intake Accel Council Data'
    AND column_name IN ('Owner', 'Initiative_Lead', 'PROJECT_DIRECTOR', 'PROJECT_SR_DIRECTOR', 'VP_Name', 'VP', 'Intake_Card_Nbr')
    ORDER BY column_name
    """
    
    try:
        cols = list(client.query(check_sql).result())
        logger.info(f"Found {len(cols)} hierarchy-related columns:")
        for col in cols:
            logger.info(f"  - {col.column_name}: {col.data_type}")
    except Exception as e:
        logger.warning(f"Could not check columns: {e}")
    
    # Step 2: Extract all unique people WITH their hierarchy relationships
    logger.info("\nStep 2: Extracting unique people and hierarchy from Intake Hub...")
    
    extract_sql = f"""
    WITH all_people AS (
        -- Owners and their direct hierarchy
        SELECT 
            TRIM(Owner) as person_name,
            TRIM(PROJECT_DIRECTOR) as direct_director,
            TRIM(PROJECT_SR_DIRECTOR) as direct_sr_director
        FROM `{BQ_PROJECT}.{BQ_DATASET}.Output - Intake Accel Council Data`
        WHERE TRIM(Owner) IS NOT NULL AND TRIM(Owner) != '' AND TRIM(Owner) != 'Unknown'
        
        UNION ALL
        
        -- Initiative leads and their direct hierarchy
        SELECT 
            TRIM(Initiative_Lead) as person_name,
            TRIM(PROJECT_DIRECTOR) as direct_director,
            TRIM(PROJECT_SR_DIRECTOR) as direct_sr_director
        FROM `{BQ_PROJECT}.{BQ_DATASET}.Output - Intake Accel Council Data`
        WHERE TRIM(Initiative_Lead) IS NOT NULL AND TRIM(Initiative_Lead) != '' AND TRIM(Initiative_Lead) != 'Unknown'
        
        UNION ALL
        
        -- Project directors and their hierarchy (director below them, sr_director above)
        SELECT 
            TRIM(PROJECT_DIRECTOR) as person_name,
            NULL as direct_director,
            TRIM(PROJECT_SR_DIRECTOR) as direct_sr_director
        FROM `{BQ_PROJECT}.{BQ_DATASET}.Output - Intake Accel Council Data`
        WHERE TRIM(PROJECT_DIRECTOR) IS NOT NULL AND TRIM(PROJECT_DIRECTOR) != '' AND TRIM(PROJECT_DIRECTOR) != 'Unknown'
        
        UNION ALL
        
        -- Sr directors (top of hierarchy in our data)
        SELECT 
            TRIM(PROJECT_SR_DIRECTOR) as person_name,
            NULL as direct_director,
            NULL as direct_sr_director
        FROM `{BQ_PROJECT}.{BQ_DATASET}.Output - Intake Accel Council Data`
        WHERE TRIM(PROJECT_SR_DIRECTOR) IS NOT NULL AND TRIM(PROJECT_SR_DIRECTOR) != '' AND TRIM(PROJECT_SR_DIRECTOR) != 'Unknown'
    )
    
    SELECT DISTINCT
        person_name,
        CASE 
            WHEN direct_director IS NOT NULL AND direct_director != 'Unknown' THEN direct_director
            ELSE NULL 
        END as director,
        CASE 
            WHEN direct_sr_director IS NOT NULL AND direct_sr_director != 'Unknown' THEN direct_sr_director
            ELSE NULL 
        END as sr_director,
        CAST(NULL AS STRING) as vp,
        'Intake Hub' as source,
        CURRENT_TIMESTAMP() as last_updated,
        TRUE as is_active
    FROM all_people
    WHERE person_name IS NOT NULL AND person_name != 'Unknown' AND person_name != ''
    ORDER BY person_name ASC
    """
    
    try:
        results = list(client.query(extract_sql).result())
        logger.info(f"Found {len(results)} unique people")
        
        if len(results) > 0:
            logger.info("First 10 people:")
            for i, row in enumerate(results[:10]):
                logger.info(f"  {i+1}. {row.person_name}")
        
        # Step 3: Clear old Intake Hub entries and insert new ones
        logger.info("\nStep 3: Updating AH_Hierarchy...")
        
        delete_sql = f"""
        DELETE FROM `{BQ_PROJECT}.{BQ_DATASET}.AH_Hierarchy`
        WHERE source = 'Intake Hub'
        """
        
        client.query(delete_sql).result()
        logger.info(f"  Cleared old Intake Hub entries")
        
        # Build insert statement with actual values and hierarchy
        if len(results) > 0:
            values_list = []
            for row in results:
                person_name_escaped = row.person_name.replace("'", "''")
                director = f"'{row.director.replace(chr(39), chr(39)+chr(39))}'" if row.director else "NULL"
                sr_director = f"'{row.sr_director.replace(chr(39), chr(39)+chr(39))}'" if row.sr_director else "NULL"
                
                values_list.append(f"('{person_name_escaped}', {director}, {sr_director}, NULL, 'Intake Hub', CURRENT_TIMESTAMP(), TRUE)")
            
            insert_sql = f"""
            INSERT INTO `{BQ_PROJECT}.{BQ_DATASET}.AH_Hierarchy`
            (person_name, director, sr_director, vp, source, last_updated, is_active)
            VALUES
            {','.join(values_list)}
            """
            
            client.query(insert_sql).result()
            logger.info(f"  Inserted {len(results)} people with hierarchy")
        
        # Summary
        summary_sql = f"""
        SELECT 
            COUNT(*) as total_people,
            COUNTIF(source = 'Intake Hub') as intake_hub_people,
            COUNTIF(source = 'Manual') as manual_people
        FROM `{BQ_PROJECT}.{BQ_DATASET}.AH_Hierarchy`
        """
        
        summary = list(client.query(summary_sql).result())[0]
        
        logger.info("\n" + "="*80)
        logger.info("✓ HIERARCHY SYNC COMPLETE")
        logger.info(f"  Total people: {summary.total_people}")
        logger.info(f"  From Intake Hub: {summary.intake_hub_people}")
        logger.info(f"  Manual entries: {summary.manual_people}")
        logger.info("="*80 + "\n")
        
        return True
        
    except Exception as e:
        logger.error(f"Sync error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = sync_hierarchy()
    exit(0 if success else 1)
