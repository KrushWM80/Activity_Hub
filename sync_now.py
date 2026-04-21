#!/usr/bin/env python3
"""
Simple, reliable sync: AH_Projects from Intake Hub - No complex JSON
Just update projects with fresh data, track basic note history
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


def sync_projects():
    logger.info("\n" + "="*80)
    logger.info("STARTING SYNC: Intake Hub -> AH_Projects")
    logger.info("="*80)
    
    # Step 1: Update existing Intake Hub projects
    update_sql = """
    UPDATE `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects` ap
    SET
        ap.title = sl.source_title,
        ap.owner = sl.source_owner,
        ap.owner_id = sl.source_owner_id,
        ap.health = sl.source_health,
        ap.status = sl.source_status,
        ap.business_organization = sl.source_business_org,
        ap.project_update = sl.source_update_text,
        ap.project_update_date = CURRENT_TIMESTAMP(),
        ap.project_update_by = 'Intake Hub',
        ap.last_updated = CURRENT_TIMESTAMP()
    FROM (
        SELECT 
            CAST(Intake_Card_Nbr AS STRING) as source_project_id,
            Project_Title as source_title,
            Business_Owner_Area as source_business_org,
            COALESCE(Owner, Initiative_Lead, 'Unknown') as source_owner,
            COALESCE(PROJECT_OWNERID, CREATED_BY_ID, '') as source_owner_id,
            COALESCE(PROJECT_HEALTH_DESC, 'Unknown') as source_health,
            COALESCE(Status, '') as source_status,
            COALESCE(CAST(Project_Update AS STRING), CAST(Project_Updates AS STRING), '') as source_update_text
        FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
        WHERE Intake_Card_Nbr IS NOT NULL
          AND COALESCE(Is_Duplicate_Row, 'No') = 'No'
        QUALIFY ROW_NUMBER() OVER (PARTITION BY Intake_Card_Nbr ORDER BY COALESCE(Project_Update_Date, CURRENT_TIMESTAMP()) DESC) = 1
    ) sl
    WHERE ap.project_id = sl.source_project_id
      AND ap.project_source = 'Intake Hub'
    """
    
    try:
        logger.info("Step 1: Updating existing Intake Hub projects...")
        job = client.query(update_sql)
        job.result()
        logger.info("  Updates complete")
    except Exception as e:
        logger.error(f"Update error: {e}")
        return False
    
    # Step 2: Insert new projects from source
    insert_sql = """
    INSERT INTO `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
    (project_id, title, owner, owner_id, health, status, business_organization,
     project_source, created_date, last_updated,
     project_update, project_update_date, project_update_by)
    
    SELECT 
        CAST(Intake_Card_Nbr AS STRING),
        Project_Title,
        COALESCE(Owner, Initiative_Lead, 'Unknown'),
        COALESCE(PROJECT_OWNERID, CREATED_BY_ID, ''),
        COALESCE(PROJECT_HEALTH_DESC, 'Unknown'),
        COALESCE(Status, ''),
        Business_Owner_Area,
        'Intake Hub',
        CURRENT_TIMESTAMP(),
        CURRENT_TIMESTAMP(),
        COALESCE(CAST(Project_Update AS STRING), CAST(Project_Updates AS STRING), ''),
        CURRENT_TIMESTAMP(),
        'Intake Hub'
    FROM (
        SELECT 
            Intake_Card_Nbr,
            Project_Title,
            Business_Owner_Area,
            Owner,
            Initiative_Lead,
            PROJECT_OWNERID,
            CREATED_BY_ID,
            PROJECT_HEALTH_DESC,
            Status,
            Project_Update,
            Project_Updates,
            ROW_NUMBER() OVER (PARTITION BY Intake_Card_Nbr ORDER BY COALESCE(Project_Update_Date, CURRENT_TIMESTAMP()) DESC) as rn
        FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
        WHERE Intake_Card_Nbr IS NOT NULL
          AND COALESCE(Is_Duplicate_Row, 'No') = 'No'
    ) sl
    WHERE rn = 1
      AND CAST(Intake_Card_Nbr AS STRING) NOT IN (
        SELECT project_id FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
    )
    """
    
    try:
        logger.info("Step 2: Inserting new projects from Intake Hub...")
        job = client.query(insert_sql)
        job.result()
        logger.info("  Inserts complete")
    except Exception as e:
        logger.error(f"Insert error: {e}")
        return False
    
    # Summary
    summary_sql = """
    SELECT 
        COUNT(*) as total_projects,
        COUNTIF(project_source = 'Intake Hub') as intake_hub,
        COUNTIF(project_source = 'Manual Upload') as manual
    FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
    """
    
    summary = list(client.query(summary_sql).result())[0]
    
    logger.info("\n" + "="*80)
    logger.info("SYNC COMPLETE")
    logger.info(f"  Total Projects: {summary.total_projects}")
    logger.info(f"  Intake Hub: {summary.intake_hub}")
    logger.info(f"  Manual: {summary.manual}")
    logger.info("="*80 + "\n")
    
    return True


if __name__ == '__main__':
    if not sync_projects():
        exit(1)
