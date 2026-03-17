from google.cloud import bigquery
import pandas as pd

client = bigquery.Client()

def find_kathleen_reed():
    """
    Find Kathleen Reed from Store #30 using proven Polaris query pattern
    Returns: worker_id (User Name) and job_code
    """
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
    WHERE location_id = 30
       AND first_name = 'Kathleen'
       AND last_name = 'Reed'
    LIMIT 10
    '''
    try:
        print("="*80)
        print("FINDING KATHLEEN REED FROM STORE #30 (POLARIS)")
        print("="*80)
        print(f"\nQueryString:\n{query}\n")
        
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        df = pd.DataFrame(rows)
        
        if not df.empty:
            print(f"✓ Found {len(df)} record(s):\n")
            print(df.to_string())
            print("\n" + "="*80)
            print("SUMMARY:")
            for idx, row in df.iterrows():
                print(f"  Worker ID (User Name): {row['worker_id']}")
                print(f"  Job Code: {row['job_code']}")
                print(f"  Job Name: {row['job_nm']}")
                print(f"  Location: {row['location_nm']} (ID: {row['location_id']})")
            print("="*80)
        else:
            print("✗ No match found for Kathleen Reed in Store #30")
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    find_kathleen_reed()
