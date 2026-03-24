#!/usr/bin/env python3
"""Check columns in TDA Report table"""

from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')
dataset_id = 'Store_Support_Dev'

try:
    # List all tables
    ds = client.get_dataset(dataset_id)
    print(f"\n📊 Tables in {dataset_id}:")
    tables = list(client.list_tables(ds))
    for i, table in enumerate(tables, 1):
        print(f"  {i:2d}. {table.table_id}")
    
    # Get schema for first table that looks like TDA
    tda_table = None
    for table in tables:
        if 'TDA' in table.table_id or 'Output' in table.table_id:
            tda_table = table.table_id
            break
    
    if tda_table:
        print(f"\n🗂️  Analyzing: {tda_table}")
        table = client.get_table(f'{dataset_id}.{tda_table}')
        print(f"📋 Columns ({len(table.schema)}):")
        for i, field in enumerate(table.schema, 1):
            print(f"  {i:2d}. {field.name}")
except Exception as e:
    print(f"❌ Error: {e}", exc_info=True)
