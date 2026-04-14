#!/usr/bin/env python3
import os
from google.cloud import bigquery

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
    os.environ.get('APPDATA', ''), 'gcloud', 'application_default_credentials.json'
)

client = bigquery.Client(project='wmt-assetprotection-prod')

# Check table exists and has data
print("\n=== Checking AH_Projects Table ===")
try:
    result = list(client.query('SELECT COUNT(*) as cnt FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`').result())
    count = result[0]['cnt']
    print(f"✓ Total records in AH_Projects: {count}")
    
    if count > 0:
        print("\nSample records:")
        records = list(client.query('SELECT title, owner_name, business_area, health_status FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects` LIMIT 5').result())
        for r in records:
            print(f"  - {r['title']} | Owner: {r['owner_name']} | Area: {r['business_area']} | Health: {r['health_status']}")
    else:
        print("⚠ Table is empty - need to add test data")
        
except Exception as e:
    print(f"✗ Error: {e}")
    print("Possible issues:")
    print("  - AH_Projects table doesn't exist")
    print("  - BigQuery credentials not accessible")
    print("  - No data in table")
