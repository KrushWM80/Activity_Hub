#!/usr/bin/env python3
"""Validate Division vs Business_Area comparison"""

import sqlite3
import os

db_path = 'projects_cache.db'

if os.path.exists(db_path):
    print('=' * 60)
    print('DATABASE VALIDATION')
    print('=' * 60)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check record count
    cursor.execute('SELECT COUNT(*) FROM projects')
    count = cursor.fetchone()[0]
    print(f'\n✓ Total Records in cache: {count:,}')
    
    # Check sync metadata
    cursor.execute('SELECT key, value FROM sync_metadata')
    metadata = cursor.fetchall()
    print('\n✓ Sync Metadata:')
    for key, val in metadata:
        print(f'    {key}: {val}')
    
    print('\n' + '=' * 60)
    print('DIVISION FILTER ANALYSIS')
    print('=' * 60)
    
    # Check division column
    cursor.execute("SELECT COUNT(DISTINCT division) FROM projects WHERE division IS NOT NULL AND division != ''")
    div_count = cursor.fetchone()[0]
    print(f'\n✓ Distinct division values: {div_count}')
    
    cursor.execute("SELECT DISTINCT division FROM projects WHERE division IS NOT NULL AND division != '' ORDER BY division LIMIT 10")
    div_values = [row[0] for row in cursor.fetchall()]
    print(f'  Sample values: {div_values}')
    
    cursor.execute("SELECT COUNT(*) FROM projects WHERE division IS NOT NULL AND division != ''")
    div_populated = cursor.fetchone()[0]
    print(f'  Populated rows: {div_populated:,} ({(div_populated/count)*100:.1f}%)')
    
    print('\n' + '=' * 60)
    print('BUSINESS_AREA FILTER ANALYSIS')
    print('=' * 60)
    
    # Check business_area column
    cursor.execute("SELECT COUNT(DISTINCT business_area) FROM projects WHERE business_area IS NOT NULL AND business_area != ''")
    ba_count = cursor.fetchone()[0]
    print(f'\n✓ Distinct business_area values: {ba_count}')
    
    cursor.execute("SELECT DISTINCT business_area FROM projects WHERE business_area IS NOT NULL AND business_area != '' ORDER BY business_area LIMIT 10")
    ba_values = [row[0] for row in cursor.fetchall()]
    print(f'  Sample values: {ba_values}')
    
    cursor.execute("SELECT COUNT(*) FROM projects WHERE business_area IS NOT NULL AND business_area != ''")
    ba_populated = cursor.fetchone()[0]
    print(f'  Populated rows: {ba_populated:,} ({(ba_populated/count)*100:.1f}%)')
    
    print('\n' + '=' * 60)
    print('COMPARISON SUMMARY')
    print('=' * 60)
    
    print(f'\nDivision:')
    print(f'  - Distinct values: {div_count}')
    print(f'  - Data coverage: {(div_populated/count)*100:.1f}%')
    
    print(f'\nBusiness Area:')
    print(f'  - Distinct values: {ba_count}')
    print(f'  - Data coverage: {(ba_populated/count)*100:.1f}%')
    
    if ba_count == 0:
        print('\n❌ PROBLEM FOUND: business_area has NO distinct values!')
        print('   This explains why it is not returned in the filter endpoint.')
    elif ba_count < div_count:
        print(f'\n⚠️  WARNING: business_area has {div_count - ba_count} fewer values than division')
    else:
        print('\n✓ Both filters have comparable data')
    
    # Now test the actual filter query logic
    print('\n' + '=' * 60)
    print('TESTING ACTUAL FILTER QUERY LOGIC')
    print('=' * 60)
    
    print('\nTesting Division query:')
    cursor.execute("SELECT DISTINCT division FROM projects WHERE division IS NOT NULL AND division != '' ORDER BY division")
    div_result = [row[0] for row in cursor.fetchall()]
    print(f'  Result count: {len(div_result)}')
    print(f'  Sample: {div_result[:5]}')
    
    print('\nTesting Business_Area query:')
    cursor.execute("SELECT DISTINCT business_area FROM projects WHERE business_area IS NOT NULL AND business_area != '' ORDER BY business_area")
    ba_result = [row[0] for row in cursor.fetchall()]
    print(f'  Result count: {len(ba_result)}')
    print(f'  Sample: {ba_result[:5]}')
    
    conn.close()
    
    print('\n' + '=' * 60)
    print('CONCLUSION')
    print('=' * 60)
    
    if len(ba_result) > 0:
        print('\n✓ Business_Area data EXISTS in cache')
        print('✓ The sqlite_cache.get_filter_options() SHOULD return business_areas')
        print('❌ The problem is NOT data availability')
        print('❌ The problem IS that the endpoint is using the FALLBACK (database.py)')
    else:
        print('\n❌ Business_Area has NO data in cache')
        print('❌ Even if cache is valid, business_areas would be empty')
        print('⚠️  Need to check BigQuery source data')
    
else:
    print('❌ Cache database does not exist!')
