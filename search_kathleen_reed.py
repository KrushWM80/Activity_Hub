"""
Search for Kathleen Reed from Store #30
"""
from google.cloud import bigquery
import pandas as pd

client = bigquery.Client()

def search_kathleen_reed():
    # Search for Kathleen Reed in Store 30
    query = '''
    SELECT 
        worker_id,
        location_id,
        location_nm,
        first_name,
        last_name,
        job_code,
        job_nm,
        shift_beg_dt_tm,
        shift_end_dt_tm
    FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
    WHERE location_id = 30
      AND first_name LIKE '%Kathleen%'
      AND last_name LIKE '%Reed%'
    LIMIT 10
    '''

    try:
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        df = pd.DataFrame(rows)
        
        print('\n' + '='*80)
        print('KATHLEEN REED - STORE #30')
        print('='*80)
        
        if not df.empty:
            for idx, row in df.iterrows():
                print(f'\n✓ Found Associate:')
                print(f'  Worker ID (User Name): {row["worker_id"]}')
                print(f'  First Name: {row["first_name"]}')
                print(f'  Last Name: {row["last_name"]}')
                print(f'  Job Code: {row["job_code"]}')
                print(f'  Job Title: {row["job_nm"]}')
                print(f'  Store: {row["location_nm"]} ({row["location_id"]})')
                if row.get('shift_beg_dt_tm'):
                    print(f'  Next Shift: {row["shift_beg_dt_tm"]} - {row["shift_end_dt_tm"]}')
        else:
            print('\n⚠ No exact match found. Trying broader search...')
            # Try broader search
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
            LIMIT 20
            '''
            results2 = client.query(query2).result()
            rows2 = [dict(row) for row in results2]
            df2 = pd.DataFrame(rows2)
            if not df2.empty:
                print('\nMatching associates in Store #30:')
                print(df2[['worker_id', 'first_name', 'last_name', 'job_code', 'job_nm']].to_string(index=False))
            else:
                print('\n✗ No associates found matching those criteria in Store #30')
            
    except Exception as e:
        print(f'✗ Error querying Polaris: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    search_kathleen_reed()
