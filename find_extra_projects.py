#!/usr/bin/env python3
"""
Find which projects got CURRENT_TIMESTAMP during sync (April 23 @ 14:05)
"""
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

print('\n' + '='*120)
print('IDENTIFYING EXTRA PROJECTS (Got April 23 timestamp from sync)')
print('='*120)

# Get projects with April 23 @ 14:05 timestamp (sync ran at this time)
extra_sql = """
SELECT 
    project_id,
    title,
    project_update_date,
    project_source
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE CAST(project_update_date AS DATE) = '2026-04-23'
  AND EXTRACT(HOUR FROM project_update_date) = 14
ORDER BY project_id
LIMIT 30
"""

results = list(client.query(extra_sql).result())
print('\nProjects with April 23 @ 14:05 timestamp (sync time):')
print('Count: {}'.format(len(results)))
print('-'*120)
print('Project ID | Title | Source')
print('-'*120)

for row in results:
    title = str(row.title)[:50] if row.title else 'N/A'
    print('{:<10} | {:<50} | {}'.format(row.project_id, title, row.project_source))

print('\n' + '='*120)
print('VERIFICATION: Check if these 28 extra projects exist in SOURCE')
print('='*120)

# Check if first 10 of these exist in source
if len(results) >= 10:
    project_ids = [str(row.project_id) for row in results[:10]]
    project_ids_str = "', '".join(project_ids)
    
    check_sql = """
    SELECT COUNT(DISTINCT Intake_Card_Nbr) as found_in_source
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
    WHERE Intake_Card_Nbr IN ('{}')
    """.format(project_ids_str)
    
    check_results = list(client.query(check_sql).result())
    for row in check_results:
        print('These 10 project IDs exist in SOURCE: {} out of 10'.format(row.found_in_source))
        if row.found_in_source < 10:
            print('  ** These are new projects inserted without source dates **')

print('\n' + '='*120)
print('ROOT CAUSE: INSERT statement used CURRENT_TIMESTAMP() for project_update_date')
print('Fix: Only insert projects that have NULL/empty project_update_date in source')
print('='*120)
