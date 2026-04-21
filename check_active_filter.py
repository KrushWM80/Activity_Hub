#!/usr/bin/env python3
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

from google.cloud import bigquery

client = bigquery.Client()

# Check distinct projects by Status and ARCHIVED
sql = r"""
SELECT Status, ARCHIVED, COUNT(DISTINCT PROJECT_ID) as cnt
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
GROUP BY Status, ARCHIVED
ORDER BY cnt DESC
"""

results = client.query(sql).result()
print('Projects by Status and ARCHIVED:')
print(f"{'Status':<15} {'ARCHIVED':<15} {'Count':>10}")
print('-' * 45)
for row in results:
    arch = str(row.ARCHIVED) if row.ARCHIVED is not None else 'NULL'
    print(f'{str(row.Status):<15} {arch:<15} {row.cnt:>10}')

# Count with different filters
print('\n\nDifferent Filter Options:')

sql1 = r"""SELECT COUNT(DISTINCT PROJECT_ID) FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data` WHERE Status = 'Active'"""
r1 = list(client.query(sql1).result())[0][0]
print(f'  WHERE Status = "Active": {r1}')

sql2 = r"""SELECT COUNT(DISTINCT PROJECT_ID) FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data` WHERE ARCHIVED = False"""
r2 = list(client.query(sql2).result())[0][0]
print(f'  WHERE ARCHIVED = False: {r2}')

sql3 = r"""SELECT COUNT(DISTINCT PROJECT_ID) FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data` WHERE ARCHIVED IS NULL OR ARCHIVED = False"""
r3 = list(client.query(sql3).result())[0][0]
print(f'  WHERE ARCHIVED IS NULL OR ARCHIVED = False: {r3}')

sql4 = r"""SELECT COUNT(DISTINCT PROJECT_ID) FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data` WHERE ARCHIVED != True"""
r4 = list(client.query(sql4).result())[0][0]
print(f'  WHERE ARCHIVED != True: {r4}')

sql5 = r"""SELECT COUNT(DISTINCT PROJECT_ID) FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data` WHERE Status = 'Active' AND ARCHIVED != True"""
r5 = list(client.query(sql5).result())[0][0]
print(f'  WHERE Status = "Active" AND ARCHIVED != True: {r5}')
