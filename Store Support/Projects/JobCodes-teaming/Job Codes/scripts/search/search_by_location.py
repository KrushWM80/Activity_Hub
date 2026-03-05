from google.cloud import bigquery
import pandas as pd

client = bigquery.Client()

def search_associate_v2():
    # First, let's just get some sample data from location 1497 to understand the data structure
    query = '''
    SELECT 
        worker_id,
        location_id,
        location_nm,
        first_name,
        last_name,
        job_code,
        job_nm
    FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
    WHERE location_id = 1497
    LIMIT 20
    '''
    try:
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        df = pd.DataFrame(rows)
        print("\n" + "="*80)
        print("Sample records from location 1497 (Store 1497)")
        print("="*80)
        if not df.empty:
            print(f"Found {len(df)} record(s):\n")
            # Display with all columns visible
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', None)
            print(df.to_string())
            
            # Now search for matching worker_id
            print(f"\n\nLooking for worker_id containing 'a0a0dwp'...")
            matching = df[df['worker_id'].astype(str).str.contains('a0a0dwp', case=False, na=False)]
            if not matching.empty:
                print(f"Found {len(matching)} matching record(s):\n")
                print(matching.to_string())
            else:
                print("No records found with worker_id containing 'a0a0dwp'")
        else:
            print("No records found for location_id: 1497")
        return df
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    search_associate_v2()
