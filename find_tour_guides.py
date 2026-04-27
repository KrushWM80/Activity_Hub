from google.cloud import bigquery
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.expanduser('~') + r'\AppData\Roaming\gcloud\application_default_credentials.json'

client = bigquery.Client(project='wmt-assetprotection-prod')

# Find Tour Guides in the SOURCE (Intake Hub)
query = """
SELECT
  Intake_Card_Nbr as project_id,
  Project_Title as title,
  Owner as owner,
  Store_Area as store_area,
  Project_Update as project_update,
  Health_Update as health
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
WHERE Project_Title LIKE '%Tour%Guide%'
LIMIT 1
"""

try:
    results = client.query(query).result()
    print('Tour Guides in SOURCE (Intake Hub):')
    found = False
    for row in results:
        found = True
        print(f'Project ID: {row.project_id}')
        print(f'Title: {row.title}')
        print(f'Owner: {row.owner}')
        print(f'Area: {row.store_area}')
        print(f'Update: {row.project_update}')
        print(f'Health: {row.health}')
    
    if not found:
        print('Tour Guides NOT found in Intake Hub source!')
except Exception as e:
    print(f'Error: {e}')
