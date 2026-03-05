#!/usr/bin/env python3
"""
Find all available dates with data in BigQuery
"""

from google.cloud import bigquery
from datetime import datetime

client = bigquery.Client(project='athena-gateway-prod')

print('\n' + '=' * 100)
print('CHECKING AVAILABLE DATES IN BIGQUERY')
print('=' * 100 + '\n')

query = '''
SELECT DISTINCT
  DATE(exportDate) as export_date,
  COUNT(DISTINCT businessUnitNumber) as store_count,
  COUNT(*) as total_records
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) >= '2026-01-15'
GROUP BY
  DATE(exportDate)
ORDER BY
  export_date ASC
'''

try:
    results = list(client.query(query).result())
    
    print(f"Found {len(results)} dates with data:\n")
    print(f"{'Date':<12} {'Stores':<10} {'Total Records':<15}")
    print('-' * 40)
    
    for row in results:
        print(f"{str(row.export_date):<12} {row.store_count:<10,} {row.total_records:<15,}")
    
    print(f"\nLatest date: {results[-1].export_date}")
    print(f"Earliest date: {results[0].export_date}")
    
except Exception as e:
    print(f"Error: {e}")

print()
