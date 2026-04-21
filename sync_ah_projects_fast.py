#!/usr/bin/env python3
"""
Fast sync: AH_Projects from Intake Accel Council Data - Batch processing version.

Uses direct SQL with PARSE_JSON to avoid parameterized query overhead.
Processes in smaller batches for maintainability and reliability.
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


def sync_intake_hub_projects():
    """
    Sync all projects from Intake Hub source to AH_Projects.
    Smart merge: Compares timestamps and preserves the most recent note.
    """
    
    logger.info("\n" + "="*80)
    logger.info("STARTING FAST SYNC: Intake Hub -> AH_Projects (batch processing)")
    logger.info("="*80)
    
    # Step 1: Update existing Intake Hub projects where source is newer
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
        ap.project_update_date = sl.source_update_date,
        ap.project_update_by = 'Intake Hub',
        ap.previous_updates = PARSE_JSON(
            CASE 
                WHEN ap.project_update IS NOT NULL AND ap.project_update != sl.source_update_text
                THEN TO_JSON_STRING(
                    ARRAY_CONCAT(
                        CASE 
                            WHEN ap.previous_updates IS NOT NULL 
                            THEN SAFE.PARSE_JSON_ARRAY(TO_JSON_STRING(ap.previous_updates))
                            ELSE []
                        END,
                        [STRUCT(
                            ap.project_update as note,
                            ap.project_update_date as timestamp,
                            COALESCE(ap.project_update_by, 'Unknown') as updated_by
                        )]
                    )
                )
                ELSE TO_JSON_STRING(
                    CASE 
                        WHEN ap.previous_updates IS NOT NULL 
                        THEN SAFE.PARSE_JSON_ARRAY(TO_JSON_STRING(ap.previous_updates))
                        ELSE []
                    END
                )
            END
        ),
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
            COALESCE(Project_Update_Date, CURRENT_TIMESTAMP()) as source_update_date,
            COALESCE(CAST(Project_Update AS STRING), CAST(Project_Updates AS STRING), '') as source_update_text
        FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
        WHERE Intake_Card_Nbr IS NOT NULL
          AND COALESCE(Is_Duplicate_Row, 'No') = 'No'
        QUALIFY ROW_NUMBER() OVER (PARTITION BY Intake_Card_Nbr ORDER BY COALESCE(Project_Update_Date, CURRENT_TIMESTAMP()) DESC) = 1
    ) sl
    WHERE ap.project_id = sl.source_project_id
      AND ap.project_source = 'Intake Hub'
      AND sl.source_update_date > COALESCE(ap.project_update_date, TIMESTAMP('1970-01-01'))
    """
    
    try:
        logger.info("Step 1: Updating existing Intake Hub projects where source is newer...")
        job = client.query(update_sql)
        result = job.result()
        logger.info(f"  Updates complete: {result.total_rows} rows affected")
    except Exception as e:
        logger.error(f"Update error: {e}")
        raise
    
    # Step 2: Insert new projects from source that don't exist in AH_Projects
    insert_sql = """
    INSERT INTO `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
    (project_id, title, owner, owner_id, health, status, business_organization,
     project_source, created_date, last_updated,
     project_update, project_update_date, project_update_by, previous_updates)
    
    SELECT 
        source_project_id as project_id,
        source_title as title,
        source_owner as owner,
        source_owner_id as owner_id,
        source_health as health,
        source_status as status,
        source_business_org as business_organization,
        'Intake Hub' as project_source,
        CURRENT_TIMESTAMP() as created_date,
        CURRENT_TIMESTAMP() as last_updated,
        source_update_text as project_update,
        source_update_date as project_update_date,
        'Intake Hub' as project_update_by,
        JSON '[]' as previous_updates
    FROM (
        SELECT 
            CAST(Intake_Card_Nbr AS STRING) as source_project_id,
            Project_Title as source_title,
            Business_Owner_Area as source_business_org,
            COALESCE(Owner, Initiative_Lead, 'Unknown') as source_owner,
            COALESCE(PROJECT_OWNERID, CREATED_BY_ID, '') as source_owner_id,
            COALESCE(PROJECT_HEALTH_DESC, 'Unknown') as source_health,
            COALESCE(Status, '') as source_status,
            COALESCE(Project_Update_Date, CURRENT_TIMESTAMP()) as source_update_date,
            COALESCE(CAST(Project_Update AS STRING), CAST(Project_Updates AS STRING), '') as source_update_text
        FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
        WHERE Intake_Card_Nbr IS NOT NULL
          AND COALESCE(Is_Duplicate_Row, 'No') = 'No'
        QUALIFY ROW_NUMBER() OVER (PARTITION BY Intake_Card_Nbr ORDER BY COALESCE(Project_Update_Date, CURRENT_TIMESTAMP()) DESC) = 1
    ) sl
    WHERE source_project_id NOT IN (
        SELECT project_id FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
    )
    """
    
    try:
        logger.info("Step 2: Inserting new projects from Intake Hub source...")
        job = client.query(insert_sql)
        result = job.result()
        logger.info(f"  Inserts complete: {result.total_rows} rows affected")
    except Exception as e:
        logger.error(f"Insert error: {e}")
        raise
    
    # Get sync summary
    summary_sql = """
    SELECT 
        COUNT(*) as total_projects,
        COUNTIF(project_source = 'Intake Hub') as intake_hub_projects,
        COUNTIF(project_source = 'Manual Upload') as manual_projects,
        COUNT(DISTINCT business_organization) as distinct_business_areas,
        COUNTIF(project_update_date IS NOT NULL) as projects_with_note_date
    FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
    """
    
    summary = list(client.query(summary_sql).result())[0]
    
    logger.info("\n" + "="*80)
    logger.info("SYNC COMPLETE")
    logger.info(f"  Total Projects: {summary.total_projects}")
    logger.info(f"  Intake Hub Projects: {summary.intake_hub_projects}")
    logger.info(f"  Manual Projects: {summary.manual_projects}")
    logger.info(f"  Distinct Business Areas: {summary.distinct_business_areas}")
    logger.info(f"  Projects with Note Timestamp: {summary.projects_with_note_date}")
    logger.info("="*80 + "\n")


if __name__ == '__main__':
    sync_intake_hub_projects()
