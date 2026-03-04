#!/usr/bin/env python3
"""Check sample data from TDA Report table"""

import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Query to get sample data
query = """
SELECT 
  Topic, 
  Facility,
  Health_Update,
  Phase,
  Dallas_POC,
  Deployment,
  Intake_n_Testing,
  COUNT(*) as store_count
FROM `wmt-assetprotection-prod.Store_Support_Dev.`Output- TDA Report``
GROUP BY Topic, Facility, Health_Update, Phase, Dallas_POC, Deployment, Intake_n_Testing
LIMIT 5
"""

try:
    results = client.query(query)
    print('=' * 100)
    print('Sample Data from Output- TDA Report:')
    print('=' * 100)
    for row in results:
        print(f'Topic: {row.Topic}')
        print(f'Facility: {row.Facility}')
        print(f'Health: {row.Health_Update}')
        print(f'Phase: {row.Phase}')
        print(f'POC: {row.Dallas_POC}')
        print(f'Deploy: {row.Deployment}')
        print(f'Intake: {row.Intake_n_Testing}')
        print(f'Stores: {row.store_count}')
        print('-' * 100)
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
