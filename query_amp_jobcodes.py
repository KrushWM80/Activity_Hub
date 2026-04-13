from google.cloud import bigquery
import os
import pandas as pd
from datetime import datetime

# Set Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

def query_amp_job_codes():
    """Query Polaris BigQuery for AMP job code definitions and paytypes"""
    
    try:
        print("=" * 120)
        print("POLARIS JOB CODE QUERY - AMP GROUPS")
        print("=" * 120)
        print(f"\nStarting query at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        print("Initializing BigQuery client...")
        client = bigquery.Client(project='wmt-assetprotection-prod', location='US')
        
        # Test connection
        print("Testing BigQuery connection...")
        test_query = "SELECT 1 as test"
        test_result = client.query(test_query, job_config=bigquery.QueryJobConfig(maximum_bytes_billed=1000000)).result(timeout=10)
        print("✓ BigQuery connection successful\n")

        # Job codes by AMP category
        team_lead_codes = [
            '1-600-7200', '1-600-7220', '1-610-7210', '1-615-7200', '1-615-7210',
            '1-620-7200', '1-625-7200', '1-630-7200', '1-635-7240', '1-640-7200',
            '1-640-7210', '1-990-7210', '1-695-7500', '59-65-2104', '6-10-101',
            '6-37-814', '71-76-121', '71-76-122', '71-76-123', '1-695-7530'
        ]
        hr_codes = ['1-910-7250']
        sm_codes = ['1-993-1001', '1-993-1071', '1-993-3001', '1-993-1026']
        coach_codes = [
            '71-76-622', '71-76-623', '1-993-1099', '1-993-1072', '1-993-1077',
            '1-993-1097', '1-993-1076', '1-993-1075', '1-993-1078', '1-993-1062',
            '1-993-1074', '1-993-1079', '1-996-758', '6-10-812', '6-10-811', '1-993-1085'
        ]

        all_codes = sorted(set(team_lead_codes + hr_codes + sm_codes + coach_codes))

        print(f"Total codes to query: {len(all_codes)}\n")

        # Query 1: Get all requested codes with timeout
        print("Querying Polaris for all codes...")
        codes_list = "', '".join(all_codes)
        query = f"""
        SELECT DISTINCT
            job_code,
            job_nm AS job_title,
            worker_payment_type AS paytype
        FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
        WHERE job_code IN ('{codes_list}')
        ORDER BY job_code
        """

        # Use job master table instead of schedule view for faster queries
        print("Attempting to query job master table...")
        
        # Try job master first, fall back to schedule if not available
        try:
            table_source = "`polaris-analytics-prod.us_walmart.vw_job`"
            test_query = f"SELECT COUNT(*) as cnt FROM {table_source} LIMIT 1"
            client.query(test_query, location='US').result(timeout=10)
        except:
            try:
                table_source = "`polaris-analytics-prod.us_walmart.job_master`"
                test_query = f"SELECT COUNT(*) as cnt FROM {table_source} LIMIT 1"
                client.query(test_query, location='US').result(timeout=10)
            except:
                # Fall back to schedule view with smaller dataset
                table_source = "`polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`"
        
        print(f"✓ Using table source: {table_source}\n")
        
        job_config = bigquery.QueryJobConfig()  # No byte limit
        
        # Query 1: Get all requested codes - no byte limit
        print("Querying Polaris for all codes...")
        codes_list = "', '".join(all_codes)
        query = f"""
        SELECT DISTINCT
            job_code,
            job_nm AS job_title,
            worker_payment_type AS paytype
        FROM {table_source}
        WHERE job_code IN ('{codes_list}')
        ORDER BY job_code
        LIMIT 100
        """
        
        result = client.query(query, location='US').result(timeout=60)
        df = result.to_dataframe()

        print(f"✓ Query returned: {len(df)} results\n")
        print("ALL RESULTS:")
        print("-" * 120)
        for idx, row in df.iterrows():
            paytype_display = row['paytype'] if pd.notna(row['paytype']) else 'UNKNOWN'
            print(f"  {row['job_code']:15} | {str(row['job_nm'])[:45]:45} | {paytype_display}")

        found_codes = set(df['job_code'].tolist())
        missing_codes = set(all_codes) - found_codes

        if missing_codes:
            print(f"\n⚠ MISSING ({len(missing_codes)} codes not found in Polaris):")
            for code in sorted(missing_codes):
                print(f"  - {code}")
        else:
            print(f"\n✓ All {len(all_codes)} codes found in Polaris")

        # Query 2: Summary by category
        print("\n" + "=" * 120)
        print("SUMMARY BY CATEGORY")
        print("=" * 120)

        categories = {
            'TEAM LEAD': team_lead_codes,
            'HR PERSONNEL': hr_codes,
            'STORE MANAGER': sm_codes,
            'COACH': coach_codes
        }
        
        for cat_name, cat_codes in categories.items():
            cat_codes_sorted = sorted(cat_codes)
            cat_codes_list = "', '".join(cat_codes_sorted)
            cat_query = f"""
            SELECT DISTINCT 
                job_code, 
                job_nm, 
                worker_payment_type
            FROM {table_source}
            WHERE job_code IN ('{cat_codes_list}')
            ORDER BY job_code
            LIMIT 100
            """
            
            print(f"{cat_name}...")
            cat_result = client.query(cat_query, location='US').result(timeout=60)
            cat_df = cat_result.to_dataframe()
            found_cat = len(cat_df)
            
            print(f"\n{cat_name}: {found_cat}/{len(cat_codes)}")
            print("-" * 120)
            
            if not cat_df.empty:
                for idx, row in cat_df.iterrows():
                    paytype_display = row['worker_payment_type'] if pd.notna(row['worker_payment_type']) else 'UNKNOWN'
                    print(f"  {row['job_code']:15} | {str(row['job_nm'])[:45]:45} | {paytype_display}")
            
            missing_cat = set(cat_codes_sorted) - set(cat_df['job_code'].tolist())
            if missing_cat:
                print(f"\n  ⚠ Missing from Polaris: {', '.join(sorted(missing_cat))}")

        print("\n" + "=" * 120)
        print(f"QUERY COMPLETE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 120)

    except TimeoutError as e:
        print(f'\n⏱ TIMEOUT ERROR: Query took too long to complete')
        print(f'   Details: {e}')
        print('\n   Try: Running queries with smaller batch sizes or during off-peak hours')
    except Exception as e:
        print(f'\n❌ ERROR: {e}')
        import traceback
        traceback.print_exc()
        print('\n   Check: BigQuery credentials, network connectivity, and table access')



if __name__ == '__main__':
    query_amp_job_codes()
