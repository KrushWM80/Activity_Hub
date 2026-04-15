#!/usr/bin/env python
"""Check where form submission went - query BigQuery logic_requests table"""

import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.expandvars(r'%APPDATA%\gcloud\application_default_credentials.json')

from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Query logic_requests table
query = '''
SELECT request_id, name, trigger_type, custom_trigger_text, approval_status, created_at
FROM `wmt-assetprotection-prod.Store_Support_Dev.logic_requests`
ORDER BY created_at DESC
LIMIT 10
'''

print('=== Last 10 Logic Requests in BigQuery ===\n')
try:
    results = client.query(query).result()
    if results.total_rows == 0:
        print('No logic requests found in database.')
    else:
        for row in results:
            print(f'ID: {row.request_id}')
            print(f'Name: {row.name}')
            print(f'Trigger Type: {row.trigger_type}')
            print(f'Custom Text: {row.custom_trigger_text}')
            print(f'Approval Status: {row.approval_status}')
            print(f'Created: {row.created_at}')
            print('---')
except Exception as e:
    print(f'Error: {e}')
