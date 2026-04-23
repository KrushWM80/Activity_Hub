#!/usr/bin/env python3
"""
Remove artificial sync timestamps (April 23 @ 14:05) from 30 projects
Set them back to NULL to match source (which has no update date for these projects)
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

# The 30 project IDs that got artificial timestamps
artificial_project_ids = [
    '12574', '13780', '16824', '16841', '16848', '17897', '17929', '17955', 
    '17963', '17971', '17975', '17984', '17996', '17997', '17999', '18005', 
    '18006', '18020', '18021', '18022', '18024', '18029', '18038', '18044', 
    '18045', '18046', '18051', '18055', '18066', '18072'
]

def cleanup_artificial_dates():
    logger.info("\n" + "="*80)
    logger.info("CLEANUP: Removing artificial sync timestamps")
    logger.info("="*80)
    logger.info(f"Projects to update: {len(artificial_project_ids)}")
    
    # Build the IN clause for the project IDs
    id_list = ','.join([f"'{pid}'" for pid in artificial_project_ids])
    
    cleanup_sql = f"""
    UPDATE `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
    SET project_update_date = NULL
    WHERE project_id IN ({id_list})
      AND project_source = 'Intake Hub'
    """
    
    try:
        logger.info("Executing cleanup query...")
        job = client.query(cleanup_sql)
        result = job.result()
        logger.info(f"✅ Cleanup executed")
        logger.info(f"These 30 projects now have NULL project_update_date (matching source)")
        
        # Verify the cleanup
        verify_sql = f"""
        SELECT 
            project_id,
            title,
            project_update_date,
            project_source
        FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
        WHERE project_id IN ({id_list})
        ORDER BY project_id
        """
        
        logger.info("\n" + "="*80)
        logger.info("VERIFICATION: Projects after cleanup")
        logger.info("="*80)
        
        query_job = client.query(verify_sql)
        rows = query_job.result()
        
        for row in rows:
            status = "✅ NULL" if row.project_update_date is None else f"⚠️ {row.project_update_date}"
            logger.info(f"  {row.project_id:6} | {row.title[:40]:40} | {status}")
        
        logger.info("\n✅ CLEANUP COMPLETE")
        
    except Exception as e:
        logger.error(f"Cleanup error: {e}")
        return False
    
    return True

if __name__ == '__main__':
    cleanup_artificial_dates()
