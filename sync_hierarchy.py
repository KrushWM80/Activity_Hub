#!/usr/bin/env python3
"""
Sync Organizational Hierarchy from Intake Hub -> AH_Hierarchy Table
Extracts Director, Sr Director, VP relationships for all project owners/leaders
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
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS `{BQ_PROJECT}.{BQ_DATASET}.AH_Hierarchy`
    (
        person_name STRING NOT NULL,
        director STRING,
        sr_director STRING,
        vp STRING,
        source STRING,  -- 'Intake Hub' or 'Manual'
        last_updated TIMESTAMP,
        is_active BOOLEAN DEFAULT TRUE
    )
    PARTITION BY DATE(last_updated)
    CLUSTER BY person_name
    """
    
    try:
        logger.info(f"Creating AH_Hierarchy table...")
        job = client.query(create_table_sql)
        job.result()
        logger.info("✓ AH_Hierarchy table created/verified")
        return True
    except Exception as e:
        logger.error(f"Error creating table: {e}")
        return False


def sync_hierarchy_from_intake():
    """
    Extract hierarchy relationships from Intake Hub and sync to AH_Hierarchy
    Builds multi-level hierarchy for each person
    """
    
    # Query: Extract all unique people with their hierarchy info
    query_sql = f"""
    WITH intake_hierarchy AS (
        SELECT 
            -- Primary person
            COALESCE(TRIM(Owner), TRIM(Initiative_Lead), 'Unknown') as person_name,
            -- Their direct manager/director
            TRIM(PROJECT_DIRECTOR) as direct_director,
            -- Sr Director above that
            TRIM(PROJECT_SR_DIRECTOR) as sr_director_level,
            -- Look for VP info if available
            COALESCE(
                TRIM(VP_Name),  -- Try VP_Name column if exists
                TRIM(VP),       -- Try VP column if exists
                NULL
            ) as vp_level,
            Project_Title,
            Intake_Card_Nbr
        FROM `{BQ_PROJECT}.{BQ_DATASET}.Output - Intake Accel Council Data`
        WHERE COALESCE(Is_Duplicate_Row, 'No') = 'No'
          AND Intake_Card_Nbr IS NOT NULL
          AND COALESCE(TRIM(Owner), TRIM(Initiative_Lead)) IS NOT NULL
            
        UNION ALL
        
        -- Also include directors as primary people (looking at their hierarchy)
        SELECT 
            TRIM(PROJECT_DIRECTOR) as person_name,
            NULL as direct_director,
            TRIM(PROJECT_SR_DIRECTOR) as sr_director_level,
            COALESCE(
                TRIM(VP_Name),
                TRIM(VP),
                NULL
            ) as vp_level,
            Project_Title,
            Intake_Card_Nbr
        FROM `{BQ_PROJECT}.{BQ_DATASET}.Output - Intake Accel Council Data`
        WHERE COALESCE(Is_Duplicate_Row, 'No') = 'No'
          AND Intake_Card_Nbr IS NOT NULL
          AND TRIM(PROJECT_DIRECTOR) IS NOT NULL
            
        UNION ALL
        
        -- Include Sr Directors as primary people too
        SELECT 
            TRIM(PROJECT_SR_DIRECTOR) as person_name,
            NULL as direct_director,
            NULL as sr_director_level,
            COALESCE(
                TRIM(VP_Name),
                TRIM(VP),
                NULL
            ) as vp_level,
            Project_Title,
            Intake_Card_Nbr
        FROM `{BQ_PROJECT}.{BQ_DATASET}.Output - Intake Accel Council Data`
        WHERE COALESCE(Is_Duplicate_Row, 'No') = 'No'
          AND Intake_Card_Nbr IS NOT NULL
          AND TRIM(PROJECT_SR_DIRECTOR) IS NOT NULL
    )
    
    -- Deduplicate and aggregate
    SELECT DISTINCT
        person_name,
        MAX(direct_director) as director,           -- Most common director
        MAX(sr_director_level) as sr_director,       -- Most common sr director
        MAX(vp_level) as vp,                         -- Most common vp
        'Intake Hub' as source,
        CURRENT_TIMESTAMP() as last_updated
    FROM intake_hierarchy
    WHERE person_name IS NOT NULL 
      AND person_name != 'Unknown'
      AND TRIM(person_name) != ''
    GROUP BY person_name
    ORDER BY person_name ASC
    """
    
    try:
        logger.info("Querying Intake Hub hierarchy...")
        results = client.query(query_sql).result()
        hierarchy_data = list(results)
        logger.info(f"Found {len(hierarchy_data)} unique people in Intake Hub")
        return hierarchy_data
    except Exception as e:
        logger.error(f"Error querying hierarchy: {e}")
        logger.error("Note: VP_Name/VP columns may not exist in Intake Hub. Proceeding without VP data.")
        
        # Fallback query without VP columns
        query_sql_fallback = f"""
        WITH intake_hierarchy AS (
            SELECT 
                COALESCE(TRIM(Owner), TRIM(Initiative_Lead), 'Unknown') as person_name,
                TRIM(PROJECT_DIRECTOR) as direct_director,
                TRIM(PROJECT_SR_DIRECTOR) as sr_director_level,
                Project_Title,
                Intake_Card_Nbr
            FROM `{BQ_PROJECT}.{BQ_DATASET}.Output - Intake Accel Council Data`
            WHERE COALESCE(Is_Duplicate_Row, 'No') = 'No'
              AND Intake_Card_Nbr IS NOT NULL
              AND COALESCE(TRIM(Owner), TRIM(Initiative_Lead)) IS NOT NULL
                
            UNION ALL
            
            SELECT 
                TRIM(PROJECT_DIRECTOR) as person_name,
                NULL as direct_director,
                TRIM(PROJECT_SR_DIRECTOR) as sr_director_level,
                Project_Title,
                Intake_Card_Nbr
            FROM `{BQ_PROJECT}.{BQ_DATASET}.Output - Intake Accel Council Data`
            WHERE COALESCE(Is_Duplicate_Row, 'No') = 'No'
              AND Intake_Card_Nbr IS NOT NULL
              AND TRIM(PROJECT_DIRECTOR) IS NOT NULL
                
            UNION ALL
            
            SELECT 
                TRIM(PROJECT_SR_DIRECTOR) as person_name,
                NULL as direct_director,
                NULL as sr_director_level,
                Project_Title,
                Intake_Card_Nbr
            FROM `{BQ_PROJECT}.{BQ_DATASET}.Output - Intake Accel Council Data`
            WHERE COALESCE(Is_Duplicate_Row, 'No') = 'No'
              AND Intake_Card_Nbr IS NOT NULL
              AND TRIM(PROJECT_SR_DIRECTOR) IS NOT NULL
        )
        
        SELECT DISTINCT
            person_name,
            MAX(direct_director) as director,
            MAX(sr_director_level) as sr_director,
            NULL as vp,
            'Intake Hub' as source,
            CURRENT_TIMESTAMP() as last_updated
        FROM intake_hierarchy
        WHERE person_name IS NOT NULL 
          AND person_name != 'Unknown'
          AND TRIM(person_name) != ''
        GROUP BY person_name
        ORDER BY person_name ASC
        """
        
        try:
            logger.info("Running fallback query without VP columns...")
            results = client.query(query_sql_fallback).result()
            hierarchy_data = list(results)
            logger.info(f"Found {len(hierarchy_data)} unique people in Intake Hub")
            return hierarchy_data
        except Exception as e2:
            logger.error(f"Fallback query also failed: {e2}")
            return []


def sync_hierarchy_table():
    """Update AH_Hierarchy with dedup logic: Intake Hub overwrites Manual entries"""
    
    logger.info("\n" + "="*80)
    logger.info("STARTING HIERARCHY SYNC: Intake Hub -> AH_Hierarchy")
    logger.info("="*80 + "\n")
    
    # Step 1: Create table if needed
    if not create_hierarchy_table():
        return False
    
    # Step 2: Get hierarchy data from Intake Hub
    hierarchy_data = sync_hierarchy_from_intake()
    if not hierarchy_data:
        logger.warning("No hierarchy data found, aborting sync")
        return False
    
    # Step 3: Merge into AH_Hierarchy (Intake Hub overwrites Manual on name match)
    merge_sql = f"""
    MERGE INTO `{BQ_PROJECT}.{BQ_DATASET}.AH_Hierarchy` h
    USING (
        SELECT 
            person_name,
            director,
            sr_director,
            vp,
            source,
            last_updated
        FROM UNNEST(@hierarchy_data) AS data
    ) incoming
    ON h.person_name = incoming.person_name
        AND (incoming.source = 'Intake Hub' OR h.source = 'Manual')  -- Intake Hub always overwrites
    WHEN MATCHED AND incoming.source = 'Intake Hub' THEN
        UPDATE SET
            director = incoming.director,
            sr_director = incoming.sr_director,
            vp = incoming.vp,
            source = incoming.source,
            last_updated = incoming.last_updated,
            is_active = TRUE
    WHEN NOT MATCHED THEN
        INSERT (person_name, director, sr_director, vp, source, last_updated, is_active)
        VALUES (incoming.person_name, incoming.director, incoming.sr_director, incoming.vp, 
                incoming.source, incoming.last_updated, TRUE)
    """
    
    # Convert hierarchy data to list of dicts for parameterized query
    hierarchy_list = [
        {
            'person_name': row['person_name'],
            'director': row['director'],
            'sr_director': row['sr_director'],
            'vp': row.get('vp'),
            'source': row['source'],
            'last_updated': row['last_updated']
        }
        for row in hierarchy_data
    ]
    
    try:
        logger.info(f"Step 1: Syncing {len(hierarchy_list)} people into AH_Hierarchy...")
        
        # Delete previous Intake Hub entries
        delete_sql = f"""
        DELETE FROM `{BQ_PROJECT}.{BQ_DATASET}.AH_Hierarchy`
        WHERE source = 'Intake Hub'
        """
        
        logger.info("  Clearing previous Intake Hub entries...")
        client.query(delete_sql).result()
        
        # Build insert from hierarchy data
        insert_sql = f"""
        INSERT INTO `{BQ_PROJECT}.{BQ_DATASET}.AH_Hierarchy`
        (person_name, director, sr_director, vp, source, last_updated, is_active)
        VALUES
        """
        
        values_list = []
        for row in hierarchy_list:
            person_name_escaped = row['person_name'].replace("'", "''")
            director = f"'{row['director']}'" if row['director'] else "NULL"
            sr_director = f"'{row['sr_director']}'" if row['sr_director'] else "NULL"
            vp = f"'{row['vp']}'" if row['vp'] else "NULL"
            
            values_list.append(f"('{person_name_escaped}', {director}, {sr_director}, {vp}, 'Intake Hub', CURRENT_TIMESTAMP(), TRUE)")
        
        if values_list:
            insert_sql += ",\n".join(values_list)
            logger.info("  Inserting new Intake Hub hierarchy...")
            client.query(insert_sql).result()
            logger.info(f"✓ Inserted {len(hierarchy_list)} hierarchy records")
        
        logger.info("\n" + "="*80)
        logger.info("✓ HIERARCHY SYNC COMPLETE")
        logger.info(f"  Total people synced: {len(hierarchy_list)}")
        logger.info("="*80 + "\n")
        
        return True
        
    except Exception as e:
        logger.error(f"Sync error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = sync_hierarchy_table()
    exit(0 if success else 1)
