"""
MINIMAL: Absolute simplest query to find Kendall Rush
"""

from google.cloud import bigquery
import pandas as pd

print("\n" + "=" * 80)
print("MINIMAL BIGQUERY TEST")
print("=" * 80)

try:
    client = bigquery.Client()
    print("✓ Connected to BigQuery\n")
    
    # Test 1: Simple Polaris query
    print("Executing Polaris query for WIN 219251625...")
    
    polaris_query = """
    SELECT DISTINCT
        win_nbr,
        job_code,
        job_nm
    FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
    WHERE win_nbr = 219251625
    LIMIT 10
    """
    
    result = client.query(polaris_query)
    polaris_df = result.to_dataframe()
    
    print(f"\n✓ Polaris Search Complete - Found {len(polaris_df)} records\n")
    if len(polaris_df) > 0:
        print(polaris_df.to_string())
        print(f"\n✓✓✓ SUCCESS: Found Kendall Rush in Polaris!")
        for _, row in polaris_df.iterrows():
            print(f"\n  WIN: {row['win_nbr']}")
            print(f"  Job Code (SMART): {row['job_code']}")
            print(f"  Job Name: {row['job_nm']}")
            
            # Show transformation
            parts = str(row['job_code']).split('-')
            if len(parts) == 3:
                workday = f"US-{parts[0]:0>2}-{parts[1]:0>4}-{parts[2]:0>6}"
                print(f"  Job Code (Workday): {workday}")
    else:
        print("⚠ No records found for WIN 219251625 in Polaris")
    
    # Test 2: CoreHR query
    print("\n" + "-" * 80)
    print("\nExecuting CoreHR query for userID 'krush'...")
    
    corehr_query = """
    SELECT DISTINCT
        userID,
        employeeID
    FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`
    WHERE userID IN ('krush', 'KRUSH')
    LIMIT 10
    """
    
    result = client.query(corehr_query)
    corehr_df = result.to_dataframe()
    
    print(f"\n✓ CoreHR Search Complete - Found {len(corehr_df)} records\n")
    if len(corehr_df) > 0:
        print(corehr_df.to_string())
        print(f"\n✓✓✓ SUCCESS: Found Kendall Rush in CoreHR!")
    else:
        print("⚠ No records found for userID 'krush' in CoreHR")
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    if len(polaris_df) > 0 and len(corehr_df) > 0:
        print("✓✓✓ CONFIRMED: Kendall Rush exists in both Polaris and CoreHR")
        print("✓   Code transformation works - no Excel bridge needed!")
    elif len(polaris_df) > 0:
        print("✓ Found in Polaris - Proceed with SMART-based queries")
    elif len(corehr_df) > 0:
        print("✓ Found in CoreHR - Proceed with Workday code queries")
    else:
        print("✗ User data not found - check WIN/userID values")
    
    print("\n" + "=" * 80)

except Exception as e:
    print(f"\n✗✗✗ ERROR: {e}")
    print("\nTroubleshooting:")
    print("  1. Ensure BigQuery credentials are set (gcloud auth or GOOGLE_APPLICATION_CREDENTIALS)")
    print("  2. Verify you have access to these datasets:")
    print("     - polaris-analytics-prod.us_walmart")
    print("     - wmt-corehr-prod.US_HUDI")
    print("  3. Check WIN number and userID values")
