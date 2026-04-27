#!/usr/bin/env python3
from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

sql = """
SELECT DISTINCT health, COUNT(*) as count
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
GROUP BY health
ORDER BY count DESC
"""

results = client.query(sql).result()
print('Distinct health values in AH_Projects:')
for row in results:
    print(f'  "{row.health}" - {row.count} projects')
