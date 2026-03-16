#!/usr/bin/env python3
"""
Search for Kathleen Reed from Store #30 using proven Polaris method
Uses: polaris-analytics-prod.us_walmart.vw_polaris_current_schedule
"""
from google.cloud import bigquery
import pandas as pd

client = bigquery.Client()

def search_kathleen_reed_polaris():
    """Search Polaris current schedule for Kathleen Reed in Store 30"""
    
    query = """
    SELECT 
        worker_id,
        location_id,
        location_nm,
        first_name,
        last_name,
        job_code,
        job_nm,
        hire_date,
        empl_type_code
    FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
    WHERE location_id = 30
      AND first_name LIKE '%Kathleen%'
      AND last_name LIKE '%Reed%'
    LIMIT 20
    """
    
    try:
        print("\n" + "="*80)
        print("SEARCHING: Kathleen Reed in Store #30")
        print("="*80)
        print()
        
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        df = pd.DataFrame(rows)
        
        if not df.empty:
            print(f"✓ FOUND {len(df)} matching record(s):\n")
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', None)
            pd.set_option('display.max_colwidth', None)
            print(df.to_string())
            
            print("\n" + "="*80)
            print("SUMMARY")
            print("="*80)
            for idx, row in df.iterrows():
                print(f"\nAssociate: {row['first_name']} {row['last_name']}")
                print(f"  User Name (Worker ID): {row['worker_id']}")
                print(f"  Job Code: {row['job_code']}")
                print(f"  Job Title: {row['job_nm']}")
                print(f"  Store: {row['location_nm']} ({row['location_id']})")
                print(f"  Hire Date: {row['hire_date']}")
                print(f"  Employment Type: {row['empl_type_code']}")
            
            return df
        else:
            print("✗ No exact matches found. Trying broader search...\n")
            
            # Broader search with just first name
            query2 = '''
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
              AND (first_name LIKE '%Kathleen%' OR last_name LIKE '%Reed%')
            LIMIT 30
            '''
            
            results2 = client.query(query2).result()
            rows2 = [dict(row) for row in results2]
            df2 = pd.DataFrame(rows2)
            
            if not df2.empty:
                print(f"Found {len(df2)} associates in Store 30 with Kathleen OR Reed:\n")
                print(df2[['worker_id', 'first_name', 'last_name', 'job_code', 'job_nm']].to_string())
            else:
                print("✗ No matches found even with broader search")
            
            return df2
            
    except Exception as e:
        print(f"Error querying Polaris: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    search_kathleen_reed_polaris()
