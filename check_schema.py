#!/usr/bin/env python3
from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')
results = client.query("""
SELECT column_name, data_type
FROM `wmt-assetprotection-prod.Store_Support_Dev.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'Output - AMP ALL 2'
ORDER BY ordinal_position
""").result()

print("\n" + "="*60)
print("BigQuery Schema for 'Output - AMP ALL 2'")
print("="*60 + "\n")

for row in results:
    col_name = row[0]
    col_type = row[1]
    print(f"{col_name:40} {col_type}")

print("\n" + "="*60)
