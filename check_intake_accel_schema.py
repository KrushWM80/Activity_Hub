#!/usr/bin/env python3
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

from google.cloud import bigquery

client = bigquery.Client()

# Check schema of Output - Intake Accel Council Data
print("Schema of 'Output - Intake Accel Council Data' table:")
print("=" * 80)

dataset_id = "Store_Support_Dev"
table_id = "Output - Intake Accel Council Data"

try:
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    table = client.get_table(table_ref)

    for field in table.schema:
        print(f"  {field.name:40} {field.field_type}")
        
    print(f"\nTable found successfully!")
    
    # Check sample data
    sql = r"""
    SELECT COUNT(*) as cnt, COUNT(DISTINCT PROJECT_ID) as distinct_proj
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
    """
    results = client.query(sql).result()
    for row in results:
        print(f"\nTotal records: {row.cnt}")
        print(f"Distinct projects: {row.distinct_proj}")
        
except Exception as e:
    print(f"Error: {e}")
