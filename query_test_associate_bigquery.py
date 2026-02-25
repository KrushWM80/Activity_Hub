from google.cloud import bigquery
import pandas as pd

# Set up BigQuery client (assumes GOOGLE_APPLICATION_CREDENTIALS is set)
client = bigquery.Client()

# --- 1. Distribution_Lists Table ---
def query_distribution_lists():
    query = '''
    SELECT * FROM `wmt-assetprotection-prod.Store_Support_Dev.dl_catalog`
    WHERE email = 'a0a0dwp.s01497.us@wal-mart.com'
       OR name LIKE '%a0a0dwp%'
       OR description LIKE '%1497%'
    '''
    results = client.query(query).result()
    rows = [dict(row) for row in results]
    df = pd.DataFrame(rows)
    print("\nResults from dl_catalog:")
    print(df if not df.empty else "No match found.")
    return df

# --- 2. JobCodes-teaming (Polaris) Table ---
def query_jobcodes_teaming():
    query = '''
    SELECT * FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
    WHERE user_id = 'a0a0dwp'
       OR store = '1497'
       OR email = 'a0a0dwp.s01497.us@wal-mart.com'
    '''
    results = client.query(query).result()
    rows = [dict(row) for row in results]
    df = pd.DataFrame(rows)
    print("\nResults from vw_polaris_current_schedule:")
    print(df if not df.empty else "No match found.")
    return df

if __name__ == "__main__":
    query_distribution_lists()
    query_jobcodes_teaming()
