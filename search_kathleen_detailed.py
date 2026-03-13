#!/usr/bin/env python3
"""
Search for Kathleen Reed from Store #30
Queries Polaris data to find her user name and job code
"""
from google.cloud import bigquery
import sys

def search_in_polaris():
    """Search Polaris for Kathleen Reed"""
    client = bigquery.Client(project='polaris-analytics-prod')
    
    print('='*80)
    print('Searching Polaris for Kathleen Reed in Store 30')
    print('='*80)
    print()
    
    query = """
    SELECT 
        worker_id,
        location_id,
        location_nm,
        first_name,
        last_name,
        job_code,
        job_nm
    FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
    WHERE location_id = 30
      AND last_name = 'Reed'
    LIMIT 20
    """
    
    try:
        results = client.query(query).result()
        rows = list(results)
        
        if rows:
            print(f'Found {len(rows)} associate(s) with last name Reed in Store 30:')
            print()
            for row in rows:
                print(f'User Name (Worker ID): {row.worker_id}')
                print(f'Name: {row.first_name} {row.last_name}')
                print(f'Job Code: {row.job_code}')
                print(f'Job Title: {row.job_nm}')
                print(f'Store: {row.location_nm} ({row.location_id})')
                print('-'*80)
            return True
        else:
            print('No exact match found. Trying broader search...')
            print()
            return False
            
    except Exception as e:
        print(f'Error querying Polaris: {e}')
        return False

def search_broader():
    """Broader search with first name Kathleen"""
    client = bigquery.Client(project='polaris-analytics-prod')
    
    query = """
    SELECT 
        worker_id,
        location_id,
        location_nm,
        first_name,
        last_name,
        job_code,
        job_nm
    FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
    WHERE location_id = 30
      AND first_name LIKE '%Kathleen%'
    LIMIT 30
    """
    
    try:
        results = client.query(query).result()
        rows = list(results)
        
        if rows:
            print('Found associates with first name "Kathleen" in Store 30:')
            print()
            for row in rows:
                print(f'User Name: {row.worker_id} | Name: {row.first_name} {row.last_name} | Job Code: {row.job_code}')
            print()
            return True
        else:
            print('No matches with "Kathleen" first name.')
            return False
            
    except Exception as e:
        print(f'Error: {e}')
        return False

if __name__ == '__main__':
    found = search_in_polaris()
    
    if not found:
        print()
        search_broader()
