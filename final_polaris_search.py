from google.cloud import bigquery
import pandas as pd

client = bigquery.Client()

def final_search():
    query = '''
    SELECT 
        worker_id,
        location_id,
        location_nm,
        first_name,
        last_name,
        job_code,
        job_nm,
        hire_date
    FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
    WHERE location_nm = '1497'
       OR location_nm LIKE '%1497%'
    LIMIT 50
    '''
    try:
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        df = pd.DataFrame(rows)
        print("\n" + "="*80)
        print("Results: Searching for Store 1497 by location_nm")
        print("="*80)
        if not df.empty:
            print(f"✓ Found {len(df)} record(s) for Store 1497:\n")
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', None)
            print(df.to_string())
            
            # Check for specific worker_id
            print(f"\n\n" + "="*80)
            print("Searching for User ID: a0a0dwp in these records...")
            print("="*80)
            matching = df[df['worker_id'].astype(str).str.lower().str.contains('a0a0dwp', na=False)]
            if not matching.empty:
                print(f"✓ Found {len(matching)} record(s) for the specific user:\n")
                print(matching.to_string())
            else:
                print(f"✗ User ID 'a0a0dwp' NOT FOUND in Store 1497 records")
                print(f"\nAvailable worker_ids in Store 1497:")
                print(df[['worker_id', 'first_name', 'last_name']].drop_duplicates().to_string())
        else:
            print("✗ Store 1497 NOT FOUND in the Polaris table")
        return df
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    final_search()
