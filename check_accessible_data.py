#!/usr/bin/env python3
"""
Check what we can access and find alternatives for getting user_id
"""
from google.cloud import bigquery

client = bigquery.Client()

print('='*80)
print('CHECKING ACCESSIBLE DATA SOURCES')
print('='*80)
print(f'Default Project: {client.project}')
print()

# Try to list datasets in default project
print('Datasets in default project:')
try:
    datasets = list(client.list_datasets())
    for ds in datasets:
        print(f'  - {ds.dataset_id}')
except Exception as e:
    print(f'  Error listing datasets: {e}')

print()
print('='*80)
print('LOOKING FOR ASSOCIATE/USER DATA TABLES')
print('='*80)
print()

# Check Store_Support_Dev for other tables that might have user info
try:
    dataset = client.get_dataset('Store_Support_Dev')
    tables = list(client.list_tables(dataset))
    
    # Look for tables that might have associate/user/roster info
    potential_tables = []
    for table in tables:
        name_lower = table.table_id.lower()
        if any(keyword in name_lower for keyword in 
               ['contact', 'roster', 'associate', 'user', 'employee', 'staff', 'personnel']):
            potential_tables.append(table.table_id)
    
    if potential_tables:
        print(f'Found {len(potential_tables)} potentially useful tables:')
        for table_name in potential_tables:
            print(f'\n  ➤ {table_name}')
            try:
                table = client.get_table(f'{client.project}.Store_Support_Dev.{table_name}')
                print(f'    Columns: {", ".join([f.name for f in table.schema[:10]])}')
                if len(table.schema) > 10:
                    print(f'    ... and {len(table.schema) - 10} more')
            except Exception as e:
                print(f'    Error reading schema: {e}')
    else:
        print('No contact/roster/user tables found')
        
except Exception as e:
    print(f'Error: {e}')
