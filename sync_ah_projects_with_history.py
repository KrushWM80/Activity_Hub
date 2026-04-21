#!/usr/bin/env python3
"""
Sync AH_Projects from Intake Accel Council Data every 30 minutes.
Smart merge: Keep most recent note (by timestamp), preserve history.

Logic:
- Intake Hub projects: Compare project_update_date timestamps
  - If source is newer: Update note, move current note to history
  - If user-edited is newer: Keep user edit, don't overwrite
- Manual Upload projects: Never touch
- All: Append to previous_updates JSON array for audit trail
"""

from google.cloud import bigquery
from datetime import datetime
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

client = bigquery.Client(project='wmt-assetprotection-prod')


def fetch_source_projects():
    """Fetch all latest project records from Intake Hub source (ranked by most recent update)"""
    sql = """
    WITH ranked_projects AS (
        SELECT 
            CAST(Intake_Card_Nbr AS STRING) as project_id,
            Project_Title as title,
            Business_Owner_Area as business_organization,
            COALESCE(Owner, Initiative_Lead, 'Unknown') as owner,
            COALESCE(PROJECT_OWNERID, CREATED_BY_ID, '') as owner_id,
            COALESCE(PROJECT_HEALTH_DESC, 'Unknown') as health,
            COALESCE(Status, '') as status,
            COALESCE(Project_Update_Date, CURRENT_TIMESTAMP()) as project_update_date,
            COALESCE(CAST(Project_Update AS STRING), CAST(Project_Updates AS STRING), '') as source_update_text,
            ROW_NUMBER() OVER (PARTITION BY Intake_Card_Nbr ORDER BY COALESCE(Project_Update_Date, CURRENT_TIMESTAMP()) DESC) as rn
        FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
        WHERE Intake_Card_Nbr IS NOT NULL
          AND COALESCE(Is_Duplicate_Row, 'No') = 'No'
    )
    SELECT * EXCEPT(rn)
    FROM ranked_projects
    WHERE rn = 1
    ORDER BY project_id
    """
    try:
        projects = list(client.query(sql).result())
        logger.info(f"Fetched {len(projects)} unique projects from Intake Hub source")
        return projects
    except Exception as e:
        logger.error(f"Error fetching source projects: {e}")
        return []


def fetch_existing_projects():
    """Fetch all projects from AH_Projects"""
    sql = """
    SELECT 
        project_id,
        title,
        owner,
        owner_id,
        health,
        status,
        business_organization,
        project_source,
        project_update,
        project_update_date,
        project_update_by,
        previous_updates,
        last_updated
    FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
    ORDER BY project_id
    """
    try:
        projects = {row.project_id: row for row in client.query(sql).result()}
        logger.info(f"Loaded {len(projects)} existing projects from AH_Projects")
        return projects
    except Exception as e:
        logger.error(f"Error fetching existing projects: {e}")
        return {}


def archive_note(existing_project):
    """
    Move current note to previous_updates history
    Returns JSON string of historical notes (or '[]' if no history yet)
    """
    history = []
    
    # Parse existing history if present
    if existing_project.previous_updates:
        try:
            if isinstance(existing_project.previous_updates, str):
                history = json.loads(existing_project.previous_updates)
            else:
                history = existing_project.previous_updates
        except:
            history = []
    
    # Add current note to history if it exists
    if existing_project.project_update:
        history.append({
            "note": existing_project.project_update,
            "timestamp": existing_project.project_update_date.isoformat() 
                         if existing_project.project_update_date else None,
            "updated_by": existing_project.project_update_by or "Unknown"
        })
    
    return json.dumps(history)


def sync_projects():
    """Main sync logic: compare source vs existing, keep most recent notes"""
    source_projects = fetch_source_projects()
    existing_projects = fetch_existing_projects()
    
    if not source_projects:
        logger.error("No source projects to sync!")
        return
    
    updates_to_apply = []
    updates_count = 0
    inserts_count = 0
    skips_count = 0
    
    logger.info("\n" + "="*80)
    logger.info("STARTING SYNC: Intake Hub -> AH_Projects (30-minute merge)")
    logger.info("="*80)
    
    for source in source_projects:
        project_id = source.project_id
        
        if project_id in existing_projects:
            existing = existing_projects[project_id]
            
            # Only sync Intake Hub projects, never touch Manual Upload
            if existing.project_source != 'Intake Hub':
                skips_count += 1
                continue
            
            # Compare timestamps: source vs user-edited
            source_ts = source.project_update_date
            existing_ts = existing.project_update_date
            
            # Determine which note is newer
            if source_ts and existing_ts and source_ts > existing_ts:
                # SOURCE IS NEWER: Update note, preserve history
                logger.info(f"  UPDATE {project_id}: Source is newer ({source_ts} > {existing_ts})")
                
                history = archive_note(existing)
                previous_updates_json = history
                
                update_sql = f"""
                UPDATE `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
                SET 
                    title = @title,
                    owner = @owner,
                    owner_id = @owner_id,
                    health = @health,
                    status = @status,
                    business_organization = @business_organization,
                    project_update = @source_update_text,
                    project_update_date = @project_update_date,
                    project_update_by = 'Intake Hub',
                    previous_updates = PARSE_JSON(@previous_updates_json),
                    last_updated = CURRENT_TIMESTAMP()
                WHERE project_id = @project_id
                """
                
                job_config = bigquery.QueryJobConfig(query_parameters=[
                    bigquery.ScalarQueryParameter("project_id", "STRING", project_id),
                    bigquery.ScalarQueryParameter("title", "STRING", source.title),
                    bigquery.ScalarQueryParameter("owner", "STRING", source.owner),
                    bigquery.ScalarQueryParameter("owner_id", "STRING", source.owner_id),
                    bigquery.ScalarQueryParameter("health", "STRING", source.health),
                    bigquery.ScalarQueryParameter("status", "STRING", source.status),
                    bigquery.ScalarQueryParameter("business_organization", "STRING", source.business_organization),
                    bigquery.ScalarQueryParameter("source_update_text", "STRING", source.source_update_text),
                    bigquery.ScalarQueryParameter("project_update_date", "TIMESTAMP", source.project_update_date),
                    bigquery.ScalarQueryParameter("previous_updates_json", "STRING", previous_updates_json),
                ])
                
                try:
                    job = client.query(update_sql, job_config=job_config)
                    job.result()
                    updates_count += 1
                except Exception as e:
                    logger.error(f"  ERROR updating {project_id}: {e}")
            
            elif not existing_ts or not source_ts:
                # One is NULL: use whichever is available
                if source_ts:
                    logger.info(f"  UPDATE {project_id}: Existing has no timestamp, using source")
                    history = archive_note(existing)
                    previous_updates_json = history
                    
                    update_sql = f"""
                    UPDATE `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
                    SET 
                        project_update = @source_update_text,
                        project_update_date = @project_update_date,
                        project_update_by = 'Intake Hub',
                        previous_updates = PARSE_JSON(@previous_updates_json),
                        last_updated = CURRENT_TIMESTAMP()
                    WHERE project_id = @project_id
                    """
                    
                    job_config = bigquery.QueryJobConfig(query_parameters=[
                        bigquery.ScalarQueryParameter("project_id", "STRING", project_id),
                        bigquery.ScalarQueryParameter("source_update_text", "STRING", source.source_update_text),
                        bigquery.ScalarQueryParameter("project_update_date", "TIMESTAMP", source.project_update_date),
                        bigquery.ScalarQueryParameter("previous_updates_json", "STRING", previous_updates_json),
                    ])
                    
                    try:
                        job = client.query(update_sql, job_config=job_config)
                        job.result()
                        updates_count += 1
                    except Exception as e:
                        logger.error(f"  ERROR updating {project_id}: {e}")
            else:
                # Existing is newer or same: KEEP AS-IS
                logger.info(f"  SKIP {project_id}: Existing is newer or same (user edit preserved)")
                skips_count += 1
        
        else:
            # NEW PROJECT: Insert from source
            logger.info(f"  INSERT {project_id}: New project from Intake Hub")
            
            insert_sql = """
            INSERT INTO `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
            (project_id, title, owner, owner_id, health, status, business_organization,
             project_source, created_date, last_updated, 
             project_update, project_update_date, project_update_by, previous_updates)
            VALUES 
            (@project_id, @title, @owner, @owner_id, @health, @status, @business_organization,
             'Intake Hub', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(),
             @source_update_text, @project_update_date, 'Intake Hub', PARSE_JSON(@previous_updates_json))
            """
            
            job_config = bigquery.QueryJobConfig(query_parameters=[
                bigquery.ScalarQueryParameter("project_id", "STRING", source.project_id),
                bigquery.ScalarQueryParameter("title", "STRING", source.title),
                bigquery.ScalarQueryParameter("owner", "STRING", source.owner),
                bigquery.ScalarQueryParameter("owner_id", "STRING", source.owner_id),
                bigquery.ScalarQueryParameter("health", "STRING", source.health),
                bigquery.ScalarQueryParameter("status", "STRING", source.status),
                bigquery.ScalarQueryParameter("business_organization", "STRING", source.business_organization),
                bigquery.ScalarQueryParameter("source_update_text", "STRING", source.source_update_text),
                bigquery.ScalarQueryParameter("project_update_date", "TIMESTAMP", source.project_update_date),
                bigquery.ScalarQueryParameter("previous_updates_json", "STRING", json.dumps([])),
            ])
            
            try:
                job = client.query(insert_sql, job_config=job_config)
                job.result()
                inserts_count += 1
            except Exception as e:
                logger.error(f"  ERROR inserting {source.project_id}: {e}")
    
    # Summary
    logger.info("\n" + "="*80)
    logger.info("SYNC COMPLETE")
    logger.info(f"  Updates: {updates_count} (source notes newer than user edits)")
    logger.info(f"  Inserts: {inserts_count} (new projects from Intake Hub)")
    logger.info(f"  Skipped: {skips_count} (user edits preserved, manual projects untouched)")
    logger.info("="*80 + "\n")


if __name__ == '__main__':
    sync_projects()
