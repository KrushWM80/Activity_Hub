#!/usr/bin/env python3
"""
Search for Kathleen Reed from Store #30
Uses Store_Support_Dev.Workforce Data table
"""
from google.cloud import bigquery

def search_workforce_data():
    """Search Workforce Data for Kathleen Reed"""
    client = bigquery.Client(project='wmt-assetprotection-prod')
    
    print('='*80)
    print('Searching Workforce Data for Kathleen Reed in Store 30')
    print('='*80)
    print()
    
    # List what tables are available
    try:
        # Try different table name possibilities
        tables_to_try = [
            'Workforce Data',
            'Workforce_Data',
            'wf_data',
            'associate_data'
        ]
        
        dataset = client.get_dataset('Store_Support_Dev')
        available_tables = [t.table_id for t in client.list_tables(dataset)]
        
        print('Searching available tables...')
        print()
        
        for table_name in available_tables:
            if 'workforce' in table_name.lower() or 'associate' in table_name.lower():
                print(f'Found potential table: {table_name}')
        
        print()
        print('Attempting search in "Workforce Data" table...')
        
        query = """
        SELECT *
        FROM `wmt-assetprotection-prod.Store_Support_Dev.`Workforce Data``
        WHERE location_id = 30 OR Store = 30
        LIMIT 5
        """
        
        results = client.query(query).result()
        # Get column names
        print('Columns available:', [col for col in results.schema])
        
    except Exception as e:
        print(f'Error: {e}')
        
        # Try a simpler approach - just list the schema
        try:
            table = client.get_table('wmt-assetprotection-prod.Store_Support_Dev.`Workforce Data`')
            print()
            print('Columns in Workforce Data table:')
            for field in table.schema:
                print(f'  - {field.name}')
                
        except Exception as e2:
            print(f'Could not access Workforce Data: {e2}')

if __name__ == '__main__':
    search_workforce_data()
