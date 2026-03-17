#!/usr/bin/env python3
"""
Query Workforce Data for Kathleen Reed from Store 30
"""
from google.cloud import bigquery
import pandas as pd

client = bigquery.Client(project='wmt-assetprotection-prod')

print('='*80)
print('CHECKING WORKFORCE DATA SCHEMA')
print('='*80)
print()

try:
    # List tables first to get exact names
    dataset = client.get_dataset('Store_Support_Dev')
    tables = list(client.list_tables(dataset))
    
    print('Available tables:')
    workforce_table = None
    for table in tables:
        print(f'  {table.table_id}')
        if 'workforce' in table.table_id.lower() or 'work' in table.table_id.lower():
            workforce_table = table.table_id
    
    print()
    print(f'Using table: {workforce_table}')
    print()
    
    if not workforce_table:
        print('ERROR: Could not find Workforce table')
        exit(1)
    
    # Get schema
    table = client.get_table(f'wmt-assetprotection-prod.Store_Support_Dev.{workforce_table}')
    print('Columns in this table:')
    for field in table.schema:
        print(f'  {field.name}')
    
    # Now search for Kathleen
    query2 = f"""
    SELECT *
    FROM `wmt-assetprotection-prod.Store_Support_Dev.{workforce_table}`
    WHERE (Store = 30 OR CAST(Store AS STRING) = '30')
    ORDER BY *  LIMIT 1000
    """
    
    results2 = client.query(query2).result()
    all_rows = list(results2)
    
    # Search for Kathleen in the results
    matches = []
    for row in all_rows:
        row_dict = dict(row)
        # Check all string values for Kathleen or Reed
        row_str = str(row_dict).lower()
        if 'kathleen' in row_str or 'reed' in row_str:
            matches.append(row_dict)
    
    if matches:
        print(f'✓ Found {len(matches)} potential match(es):')
        print()
        df = pd.DataFrame(matches)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)
        print(df.to_string())
    else:
        print('✗ No matches found for "Kathleen" or "Reed"')
        print()
        print(f'Showed {len(all_rows)} total rows from Store 30. Other associates:')
        if all_rows:
            df = pd.DataFrame([dict(r) for r in all_rows[:10]])
            print(df.to_string())
        
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
