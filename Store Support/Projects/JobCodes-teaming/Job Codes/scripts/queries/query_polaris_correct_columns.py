from google.cloud import bigquery
import pandas as pd

client = bigquery.Client()

def query_polaris_with_correct_columns():
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
        shift_end_dt_tm,
        hire_date
    FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
    WHERE worker_id = 'a0a0dwp'
       OR location_id = 1497
    LIMIT 100
    '''
    results = client.query(query).result()
    rows = [dict(row) for row in results]
    df = pd.DataFrame(rows)
    print("\n" + "="*80)
    print("Results from JobCodes-teaming (Polaris vw_polaris_current_schedule)")
    print("="*80)
    if not df.empty:
        print(f"Found {len(df)} record(s):")
        print()
        print(df.to_string())
    else:
        print("No match found for worker_id: a0a0dwp or location_id: 1497")
    return df

if __name__ == "__main__":
    query_polaris_with_correct_columns()
