#!/usr/bin/env python3
from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

sql = """
SELECT project_id, title, health
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE owner = 'Kendall Rush'
ORDER BY title
"""

results = client.query(sql).result()
print('Kendall Rush projects:')
for row in results:
    print(f'  {row.project_id}: "{row.title}" - Health: "{row.health}"')
