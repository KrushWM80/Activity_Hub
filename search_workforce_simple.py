#!/usr/bin/env python3
"""
Search Workforce Data for Kathleen Reed from Store 30
"""
from google.cloud import bigquery
import pandas as pd

client = bigquery.Client(project='wmt-assetprotection-prod')

print('='*80)
print('SEARCHING WORKFORCE DATA FOR KATHLEEN REED - STORE 30')
print('='*80)
print()

try:
    # Query Workforce Data table - use proper identifier quoting
    query = """
    SELECT *
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Workforce Data`
    WHERE location_nm LIKE '%30%' OR location_nm = '30'
    LIMIT 100
    """
    
    print("Querying Workforce Data (note: user_id may not be present)...")
    results = client.query(query, timeout=60).result()
    rows = list(results)
    
    print(f"Retrieved {len(rows)} rows from Store 30")
    print()
    
    # Look for Kathleen or Reed
    matches = []
    for row in rows:
        row_dict = dict(row)
        row_str = str(row_dict).lower()
        if 'kathleen' in row_str or 'reed' in row_str:
            matches.append(row_dict)
    
    if matches:
        print(f"✓ Found {len(matches)} match(es) for Kathleen or Reed:")
        print()
        df = pd.DataFrame(matches)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)
        print(df.to_string())
        print()
        print("="*80)
        print("Summary:")
        print("="*80)
        for match in matches:
            print(f"Row: {match}")
    else:
        print(f"✗ No 'Kathleen' or 'Reed' found in Store 30 data")
        print()
        print("Sample of Store 30 data (first 3 rows):")
        if rows:
            df = pd.DataFrame([dict(r) for r in rows[:3]])
            print(df.to_string())
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
