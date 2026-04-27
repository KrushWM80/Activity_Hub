from google.cloud import bigquery
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.expanduser('~') + r'\AppData\Roaming\gcloud\application_default_credentials.json'

client = bigquery.Client(project='wmt-assetprotection-prod')

# Restore Tour Guides from source
restore_query = """
DELETE FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE project_id = '18049';

INSERT INTO `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
(project_id, title, owner, owner_id, health, store_area, business_organization, project_update, created_date, last_updated, project_update_date, project_update_by)
SELECT
  Intake_Card_Nbr as project_id,
  Project_Title as title,
  Owner as owner,
  Owner_ID as owner_id,
  Health_Update as health,
  Store_Area as store_area,
  Store_Area as business_organization,
  Project_Update as project_update,
  CURRENT_TIMESTAMP() as created_date,
  CURRENT_TIMESTAMP() as last_updated,
  CURRENT_TIMESTAMP() as project_update_date,
  'System Restore' as project_update_by
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
WHERE Intake_Card_Nbr = '18049'
"""

try:
    # Execute as a script with multiple statements
    job_config = bigquery.QueryJobConfig(use_legacy_sql=False)
    query_job = client.query(restore_query, job_config=job_config)
    query_job.result()
    print('✓ Tour Guides restored successfully!')
    
    # Verify the restoration
    verify_query = """
    SELECT project_id, title, owner, owner_id, health, store_area, project_update
    FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
    WHERE project_id = '18049'
    """
    
    results = client.query(verify_query).result()
    print('\nVerification - Tour Guides in AH_Projects:')
    for row in results:
        print(f'  ID: {row.project_id}')
        print(f'  Title: {row.title}')
        print(f'  Owner: {row.owner}')
        print(f'  Owner ID: {row.owner_id}')
        print(f'  Health: {row.health}')
        print(f'  Area: {row.store_area}')
        print(f'  Update: {row.project_update}')
        
except Exception as e:
    print(f'Error: {e}')
