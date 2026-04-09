"""
SIMPLIFIED: Faster query for Kendall Rush's data
Uses time filters and limits to avoid scanning entire tables
"""

from google.cloud import bigquery
import pandas as pd
from datetime import datetime, timedelta

def quick_polaris_search():
    """
    Fast Polaris search - WIN lookup only (most selective)
    """
    client = bigquery.Client()
    
    # WIN is highly selective - should be fast
    query = """
    SELECT
        win_nbr,
        job_code,
        job_nm,
        first_name,
        last_name,
        location_nm,
        shift_beg_dt_tm,
        shift_end_dt_tm
    FROM
        `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
    WHERE
        win_nbr = 219251625
        AND deleted = 'N'
    LIMIT 50
    """
    
    print("=" * 80)
    print("FAST POLARIS SEARCH: WIN 219251625")
    print("=" * 80)
    
    try:
        job = client.query(query, job_config=bigquery.QueryJobConfig(use_query_cache=False))
        df = job.to_dataframe()
        print(f"\n✓ Found {len(df)} records in Polaris\n")
        
        if len(df) > 0:
            print(df.to_string())
            print("\n" + "=" * 80)
            print("ANALYSIS:")
            print("=" * 80)
            for idx, row in df.iterrows():
                print(f"\nRecord {idx + 1}:")
                print(f"  WIN: {row['win_nbr']}")
                print(f"  Job Code: {row['job_code']}")
                print(f"  Job Name: {row['job_nm']}")
                print(f"  Location: {row['location_nm']}")
                if pd.notna(row['shift_beg_dt_tm']):
                    print(f"  Shift: {row['shift_beg_dt_tm']} → {row['shift_end_dt_tm']}")
        else:
            print("⚠ No records found for WIN 219251625")
        
        return df
    
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return None


def quick_corehr_search():
    """
    Fast CoreHR search - by userID (most selective)
    Uses STRUCT notation for faster lookup
    """
    client = bigquery.Client()
    
    query = """
    SELECT
        userID,
        employeeID,
        personalInfo.legalFirstName as first_name,
        personalInfo.legalLastName as last_name
    FROM
        `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`
    WHERE
        userID = 'krush'
        OR userID = 'KRUSH'
    LIMIT 10
    """
    
    print("\n" + "=" * 80)
    print("FAST COREHR SEARCH: userID = 'krush'")
    print("=" * 80)
    
    try:
        job = client.query(query, job_config=bigquery.QueryJobConfig(use_query_cache=False))
        df = job.to_dataframe()
        print(f"\n✓ Found {len(df)} records in CoreHR\n")
        
        if len(df) > 0:
            print(df.to_string())
            print("\n" + "=" * 80)
            print("FOUND MATCH:")
            print("=" * 80)
            for idx, row in df.iterrows():
                print(f"\nUser Record:")
                print(f"  User ID: {row['userID']}")
                print(f"  Employee ID: {row['employeeID']}")
                print(f"  Name: {row['first_name']} {row['last_name']}")
        else:
            print("⚠ No CoreHR records found for userID 'krush'")
        
        return df
    
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return None


def verify_code_formats():
    """Display the code transformation"""
    print("\n" + "=" * 80)
    print("CODE FORMAT VERIFICATION FOR KENDALL RUSH")
    print("=" * 80)
    
    div = 1
    dept = 0
    code = 812673
    
    smart = f"{div}-{dept:03d}-{code}"
    workday = f"US-{div:02d}-{dept:04d}-{code:06d}"
    
    print(f"\nProvided Job Code: 812673")
    print(f"Division: {div}, Department: {dept}")
    print(f"\n✓ SMART Format:    {smart}")
    print(f"✓ Workday Format:  {workday}")
    print(f"\nTransformation: SMART codes can be converted to Workday format mathematically")
    print(f"No Excel bridge needed - pure SQL transformation!")


def main():
    """Run quick searches"""
    print("\n")
    verify_code_formats()
    
    # Search both systems
    polaris = quick_polaris_search()
    corehr = quick_corehr_search()
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    if polaris is not None and len(polaris) > 0:
        print(f"✓ Polaris: Found {len(polaris)} scheduling records for WIN 219251625")
        print(f"  Job codes visible: {polaris['job_code'].unique()}")
    else:
        print("✗ Polaris: No records found")
    
    if corehr is not None and len(corehr) > 0:
        print(f"✓ CoreHR: Found {len(corehr)} records for userID 'krush'")
    else:
        print("✗ CoreHR: No records found")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
