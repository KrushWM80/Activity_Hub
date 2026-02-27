#!/usr/bin/env python3
"""
Inspect BigQuery Table Schema
"""

from google.cloud import bigquery

client = bigquery.Client(project='athena-gateway-prod')

table_id = 'athena-gateway-prod.store_refresh.store_refresh_data'
table = client.get_table(table_id)

print("\n" + "=" * 80)
print(f"TABLE SCHEMA: {table_id}")
print("=" * 80)

for field in table.schema:
    print(f"{field.name:30} | {field.field_type:15} | {field.mode}")

print("\n" + "=" * 80)
print("SAMPLE DATA (First 5 rows)")
print("=" * 80)

query = """
SELECT *
FROM `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE exportDate BETWEEN '2026-02-15' AND '2026-02-21'
LIMIT 5
"""

results = client.query(query).result()
for row in results:
    print(row)
