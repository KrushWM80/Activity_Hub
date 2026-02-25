#!/usr/bin/env python3
"""
Inspect BigQuery schema and extract Week 7 engagement metrics
"""

from google.cloud import bigquery

client = bigquery.Client(project='athena-gateway-prod')

print("\n" + "="*80)
print("BIGQUERY SCHEMA INSPECTION")
print("="*80 + "\n")

# Get schema
table_id = 'athena-gateway-prod.store_refresh.store_refresh_data'
table = client.get_table(table_id)

print(f"Table: {table_id}")
print(f"\nFields available:")
print("-" * 80)

for field in table.schema:
    print(f"  {field.name:30} {field.field_type:15} ({field.mode})")

print("\n" + "="*80)
print("\nNow extracting Week 7 (2026-02-23) engagement data...\n")

# Try simpler query to get data structure
query = """
SELECT *
FROM `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE exportDate = '2026-02-23'
LIMIT 3
"""

print("Sample rows from Week 7:")
print("-" * 80)

try:
    df = client.query(query).to_dataframe()
    print(df.head(3).to_string())
    print(f"\nTotal rows in Week 7: {len(df)}")
    print(f"\nColumns: {list(df.columns)}")
except Exception as e:
    print(f"ERROR: {e}")
