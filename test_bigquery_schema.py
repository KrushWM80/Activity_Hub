#!/usr/bin/env python3
"""Test script to check BigQuery table schema"""

from google.cloud import bigquery
import json

PROJECT_ID = 'wmt-assetprotection-prod'
DATASET_ID = 'Store_Support_Dev'
TABLE_ID = 'Output - AMP ALL 2'

try:
    client = bigquery.Client(project=PROJECT_ID)
    table = client.get_table(f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}")
    
    print(f"\n✅ Table found: {table.full_table_id}")
    print(f"Rows: {table.num_rows}")
    print(f"Columns: {len(table.schema)}\n")
    
    print("=" * 80)
    print("ACTUAL COLUMN NAMES IN TABLE:")
    print("=" * 80)
    
    for i, field in enumerate(table.schema, 1):
        print(f"{i:3d}. {field.name:40s} {field.field_type:15s}")
    
    # Now run a test query
    print("\n" + "=" * 80)
    print("TEST QUERY - First 3 rows:")
    print("=" * 80 + "\n")
    
    query = f"""
    SELECT * 
    FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
    LIMIT 3
    """
    
    results = client.query(query).result()
    
    for i, row in enumerate(results, 1):
        print(f"\n--- Row {i} ---")
        for key, value in dict(row).items():
            print(f"  {key}: {value}")
            
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
