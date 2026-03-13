#!/usr/bin/env python3
"""
Search for Kathleen Reed in all available datasets
"""
from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Check Store Roster Contacts schema
print('Checking Store Roster Contacts table...')
print()

try:
    table = client.get_table('wmt-assetprotection-prod.Store_Support_Dev.`Store Roster Contacts`')
    print('Columns in Store Roster Contacts:')
    for field in table.schema:
        print(f'  {field.name}: {field.field_type}')
    print()
    
    # Try to query it
    query = """
    SELECT *
    FROM `wmt-assetprotection-prod.Store_Support_Dev.`Store Roster Contacts``
    WHERE Store = 30
      AND (Name LIKE '%Kathleen%' OR Name LIKE '%Reed%')
    LIMIT 20
    """
    
    results = client.query(query).result()
    rows = list(results) 
    if rows:
        print(f'Found {len(rows)} matching contacts:')
        for row in rows:
            print(row)
    else:
        print('No matches found.')
        
except Exception as e:
    print(f'Error: {e}')
