#!/usr/bin/env python3
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

from google.cloud import bigquery

client = bigquery.Client()

# Check ARCHIVED field values
sql = r"""
SELECT ARCHIVED, COUNT(*) as cnt
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
GROUP BY ARCHIVED
"""

results = client.query(sql).result()
print('ARCHIVED field values:')
for row in results:
    print(f'  ARCHIVED={row.ARCHIVED}: {row.cnt} records')

# Check status field
print('\nStatus field sample values:')
sql2 = r"""
SELECT DISTINCT Status
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
LIMIT 20
"""
results2 = client.query(sql2).result()
for row in results2:
    print(f'  {repr(row.Status)}')

# Count active vs archived
print('\nActive vs Archived (DISTINCT projects):')
sql3 = r"""
SELECT ARCHIVED, COUNT(DISTINCT PROJECT_ID) as cnt
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
GROUP BY ARCHIVED
"""
results3 = client.query(sql3).result()
for row in results3:
    status = 'Active' if row.ARCHIVED == False else 'Archived'
    print(f'  {status}: {row.cnt} projects')
