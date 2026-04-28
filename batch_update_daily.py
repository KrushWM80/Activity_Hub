#!/usr/bin/env python3
"""
Daily Batch Update - Sync projects with hierarchy data
Runs daily at 5:05 AM (after hierarchy sync completes)
Updates projects with director/sr_director from AH_Hierarchy table
"""

from google.cloud import bigquery
import logging
import sys
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

client = bigquery.Client('wmt-assetprotection-prod')

BQ_PROJECT = 'wmt-assetprotection-prod'
BQ_DATASET = 'Store_Support_Dev'

def main():
    logger.info("=" * 80)
    logger.info("BATCH UPDATE: Projects with Hierarchy Data")
    logger.info("=" * 80)
    
    # Check current state
    logger.info("\nStep 1: Checking projects that need hierarchy data...")
    check_query = f"""
    SELECT COUNT(*) as missing_director,
           COUNT(DISTINCT owner) as unique_owners
    FROM `{BQ_PROJECT}.{BQ_DATASET}.AH_Projects`
    WHERE (director_id IS NULL OR sr_director_id IS NULL)
      AND owner IS NOT NULL
      AND TRIM(owner) != ''
      AND TRIM(owner) != 'Unknown'
    """
    
    try:
        result = list(client.query(check_query).result())[0]
        logger.info(f"  Found {result.missing_director} projects with missing hierarchy")
        logger.info(f"  Across {result.unique_owners} unique owners")
    except Exception as e:
        logger.error(f"  Error checking projects: {e}")
        return False
    
    # Check how many owners are in hierarchy
    logger.info("\nStep 2: Checking which owners are in AH_Hierarchy...")
    owner_check = f"""
    SELECT DISTINCT LOWER(TRIM(ap.owner)) as owner_lower,
           COUNT(*) as project_count,
           MAX(h.director) as director,
           MAX(h.sr_director) as sr_director
    FROM `{BQ_PROJECT}.{BQ_DATASET}.AH_Projects` ap
    LEFT JOIN `{BQ_PROJECT}.{BQ_DATASET}.AH_Hierarchy` h
        ON LOWER(TRIM(ap.owner)) = LOWER(TRIM(h.person_name))
    WHERE (ap.director_id IS NULL OR ap.sr_director_id IS NULL)
      AND ap.owner IS NOT NULL
      AND TRIM(ap.owner) != ''
      AND TRIM(ap.owner) != 'Unknown'
    GROUP BY owner_lower
    HAVING director IS NOT NULL OR sr_director IS NOT NULL
    ORDER BY project_count DESC
    """
    
    try:
        results = list(client.query(owner_check).result())
        updatable = sum(r.project_count for r in results)
        logger.info(f"  {len(results)} owners can be updated")
        logger.info(f"  {updatable} projects can receive hierarchy data")
    except Exception as e:
        logger.error(f"  Error checking updatable owners: {e}")
        return False
    
    if len(results) == 0:
        logger.info("\n  No updatable projects found. All hierarchy data is current.")
        return True
    
    # Prepare UPDATE statement using deduplicated hierarchy
    logger.info("\nStep 3: Building update query (deduplicating hierarchy)...")
    
    update_query = f"""
    UPDATE `{BQ_PROJECT}.{BQ_DATASET}.AH_Projects` ap
    SET
        ap.director_id = COALESCE(h.director, ap.director_id),
        ap.sr_director_id = COALESCE(h.sr_director, ap.sr_director_id),
        ap.last_updated = CURRENT_TIMESTAMP()
    FROM (
        SELECT DISTINCT
            LOWER(TRIM(person_name)) as person_name_lower,
            FIRST_VALUE(director) OVER (PARTITION BY LOWER(TRIM(person_name)) ORDER BY director DESC NULLS LAST) as director,
            FIRST_VALUE(sr_director) OVER (PARTITION BY LOWER(TRIM(person_name)) ORDER BY sr_director DESC NULLS LAST) as sr_director
        FROM `{BQ_PROJECT}.{BQ_DATASET}.AH_Hierarchy`
    ) h
    WHERE LOWER(TRIM(ap.owner)) = h.person_name_lower
      AND (ap.director_id IS NULL OR ap.sr_director_id IS NULL)
      AND ap.owner IS NOT NULL
      AND TRIM(ap.owner) != ''
      AND TRIM(ap.owner) != 'Unknown'
    """
    
    logger.info("  Query prepared successfully")
    logger.info("\nStep 4: Attempting to execute update...")
    
    try:
        job = client.query(update_query)
        job.result()
        logger.info("  ✓ Update executed successfully!")
        
        # Verify results
        logger.info("\nStep 5: Verifying updates...")
        verify_query = f"""
        SELECT 
            COUNTIF(director_id IS NOT NULL AND sr_director_id IS NOT NULL) as fully_populated,
            COUNTIF(director_id IS NOT NULL AND sr_director_id IS NULL) as director_only,
            COUNTIF(director_id IS NULL AND sr_director_id IS NOT NULL) as sr_director_only,
            COUNT(*) as total_projects
        FROM `{BQ_PROJECT}.{BQ_DATASET}.AH_Projects`
        """
        
        verify_result = list(client.query(verify_query).result())[0]
        logger.info(f"  ✓ Total projects: {verify_result.total_projects}")
        logger.info(f"    - With both Director + Sr.Director: {verify_result.fully_populated}")
        logger.info(f"    - Director only: {verify_result.director_only}")
        logger.info(f"    - Sr.Director only: {verify_result.sr_director_only}")
        
        logger.info("\n" + "=" * 80)
        logger.info("✓ BATCH UPDATE COMPLETE")
        logger.info("=" * 80)
        return True
        
    except Exception as e:
        logger.error(f"  ✗ Error executing update: {e}")
        logger.error(f"  Details: {str(e)}")
        
        # Check if it's a VPC issue
        if "VPC Service Controls" in str(e):
            logger.info("\n  Note: VPC Service Controls policy blocks write operations.")
            logger.info("  Contact DBA to execute the update query directly.")
        
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
