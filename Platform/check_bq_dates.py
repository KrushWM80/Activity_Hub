#!/usr/bin/env python3
"""
Check latest available dates in BigQuery for Store Refresh data
"""

from google.cloud import bigquery
from datetime import datetime

client = bigquery.Client(project='athena-gateway-prod')

# Query to find latest dates in the table
query = '''
SELECT 
  DISTINCT DATE(exportDate) as export_date,
  COUNT(*) as record_count,
  COUNT(DISTINCT businessUnitNumber) as store_count,
  COUNT(DISTINCT checklistQuestionId) as question_count
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
GROUP BY
  DATE(exportDate)
ORDER BY
  export_date DESC
LIMIT 20
'''

print('📊 BIGQUERY DATA AVAILABILITY REPORT')
print('=' * 100)
print()

try:
    results = client.query(query).result()
    
    print('Latest 20 Snapshots in BigQuery:')
    print('-' * 100)
    print()
    
    for idx, row in enumerate(results, 1):
        date_str = row.export_date.strftime('%Y-%m-%d') if row.export_date else 'NULL'
        print(f'{idx:2d}. Date: {date_str}  |  Records: {row.record_count:>12,}  |  Stores: {row.store_count:>6,}  |  Questions: {row.question_count:>6,}')
    
    print()
    print('=' * 100)
    
except Exception as e:
    print(f'ERROR: {e}')
    print('This may mean you need to authenticate with Google Cloud.')
