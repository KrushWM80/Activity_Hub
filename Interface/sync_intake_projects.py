#!/usr/bin/env python3
"""
Sync Intake Hub projects to AH_Projects table
Pulls from 'Output - Intake Accel Council Data' and syncs to AH_Projects
"""
from google.cloud import bigquery
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BQ_PROJECT = 'wmt-assetprotection-prod'
BQ_DATASET = 'Store_Support_Dev'

def sync_intake_projects():
    """Sync all Intake Hub projects to AH_Projects table using MERGE"""
    client = bigquery.Client(project=BQ_PROJECT)
    
    logger.info("Starting Intake Hub project sync (batch)...")
    
    # Use MERGE to efficiently upsert all projects at once
    merge_sql = """
    MERGE `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects` t
    USING (
        SELECT DISTINCT
            CAST(Intake_Card_Nbr AS STRING) as project_id,
            Project_Title as title,
            Owner as owner,
            PROJECT_OWNERID as owner_id,
            Business_Owner_Area as business_organization,
            Project_Update as project_update,
            Project_Update_Date as project_update_date,
            PROJECT_DIRECTOR_ID as director_id,
            PROJECT_SR_DIRECTOR_ID as sr_director_id,
            Health_Update as health,
            Status as status
        FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
        WHERE Intake_Card_Nbr IS NOT NULL
    ) s
    ON t.project_id = s.project_id
    WHEN MATCHED THEN
        UPDATE SET
            title = s.title,
            owner = s.owner,
            owner_id = s.owner_id,
            business_organization = s.business_organization,
            health = s.health,
            status = s.status,
            last_updated = CURRENT_TIMESTAMP(),
            project_update = s.project_update,
            project_update_date = s.project_update_date,
            director_id = s.director_id,
            sr_director_id = s.sr_director_id
    WHEN NOT MATCHED THEN
        INSERT (project_id, title, owner, owner_id, business_organization, 
                project_source, health, status, created_date, last_updated,
                project_update, project_update_date, director_id, sr_director_id)
        VALUES (s.project_id, s.title, s.owner, s.owner_id, s.business_organization,
                'Intake', s.health, s.status, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(),
                s.project_update, s.project_update_date, s.director_id, s.sr_director_id)
    """
    
    logger.info("Executing MERGE to sync all projects...")
    try:
        job = client.query(merge_sql)
        job.result()
        logger.info(f"✓ Sync complete! Rows modified: {job.total_bytes_processed}")
        return True
    except Exception as e:
        logger.error(f"Sync failed: {e}")
        return False

if __name__ == '__main__':
    sync_intake_projects()
