from google.cloud import bigquery
import pandas as pd

client = bigquery.Client()

def query_polaris_current_schedule():
    query = '''
    SELECT * FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
    WHERE user_id = 'a0a0dwp'
       OR store = '1497'
       OR email LIKE '%a0a0dwp.s01497.us@wal-mart.com%'
       OR email LIKE '%a0a0dwp%'
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
        print("No match found for User ID: a0a0dwp, Store Number: 1497, or Email: a0a0dwp.s01497.us@wal-mart.com")
    return df

if __name__ == "__main__":
    query_polaris_current_schedule()
