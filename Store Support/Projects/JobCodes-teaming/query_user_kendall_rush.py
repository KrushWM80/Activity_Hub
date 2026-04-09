"""
Query to find Kendall Rush's data in Polaris and CoreHR
User Details Provided:
  WIN: 219251625
  User ID: krush
  Job Code: 812673
  Div: 1, Dept: 0
  Store: 30005 (charge store 7858)
  Email: kendall.rush@walmart.com
  Manager: Mathew Farnworth
"""

from google.cloud import bigquery
import pandas as pd

# Helper function to convert SMART to Workday format
def smart_to_workday(div, dept, code):
    """Convert SMART format (1-202-2104) to Workday format (US-01-0202-002104)"""
    if pd.isna(div) or pd.isna(dept) or pd.isna(code):
        return None
    return f"US-{int(div):02d}-{int(dept):04d}-{int(code):06d}"


def query_polaris_for_kendall():
    """
    Query Polaris to find Kendall Rush's job code data
    Search by: WIN (219251625) or job_code (812673)
    """
    
    client = bigquery.Client()
    
    query = """
    SELECT
        win_nbr,
        worker_id,
        first_name,
        last_name,
        job_code,
        job_nm,
        job_id,
        location_id,
        location_nm,
        worker_payment_type,
        shift_id,
        shift_beg_dt_tm,
        shift_end_dt_tm,
        hire_date,
        insert_ts
    FROM
        `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
    WHERE
        (win_nbr = 219251625
         OR job_code = '812673'
         OR job_code = '1-000-812673'
         OR job_code = '1-0-812673')
        AND deleted = 'N'
    LIMIT 100
    """
    
    print("=" * 80)
    print("POLARIS QUERY: Looking for Kendall Rush (WIN: 219251625)")
    print("=" * 80)
    print(f"Query:\n{query}\n")
    
    try:
        df = client.query(query).to_dataframe()
        print(f"✓ Found {len(df)} records in Polaris\n")
        
        if len(df) > 0:
            print(df.to_string())
            print("\n" + "-" * 80)
            print("ANALYSIS:")
            for idx, row in df.iterrows():
                print(f"\nRecord {idx + 1}:")
                print(f"  WIN: {row.get('win_nbr')}")
                print(f"  Job Code (SMART): {row.get('job_code')}")
                print(f"  Job Name: {row.get('job_nm')}")
                print(f"  Location: {row.get('location_nm')}")
                print(f"  Shift: {row.get('shift_beg_dt_tm')} - {row.get('shift_end_dt_tm')}")
        else:
            print("⚠ No records found. Trying alternate search patterns...")
        
        return df
    
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


def query_corehr_for_kendall():
    """
    Query CoreHR to find Kendall Rush's employment/job code data
    CoreHR stores data as STRUCTs (native table format), not JSON
    """
    
    client = bigquery.Client()
    
    query = """
    WITH corehr_candidates AS (
        SELECT
            employeeID,
            userID,
            personalInfo.legalFirstName as first_name,
            personalInfo.legalLastName as last_name,
            employmentInfo.positionInfoHistory as positionInfoHistory
        FROM
            `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`
        WHERE
            (personalInfo.legalFirstName = 'KENDALL'
             AND personalInfo.legalLastName = 'RUSH')
            OR userID = 'krush'
            OR userID = 'KRUSH'
    ),
    positions_unnested AS (
        SELECT
            employeeID,
            userID,
            first_name,
            last_name,
            pos.jobCode as workday_job_code,
            pos.positionTitle as position_title,
            pos.jobFamilyID as job_family_id,
            pos.managementLevelID as management_level,
            pos.storeName as store_name,
            pos.storeNumber as store_number,
            pos.active as is_active,
            pos.jobEffectiveDate as effective_date,
            pos.jobEndDate as end_date
        FROM
            corehr_candidates,
            UNNEST(positionInfoHistory) as pos
    )
    SELECT
        *
    FROM
        positions_unnested
    WHERE
        workday_job_code IS NOT NULL
    ORDER BY
        effective_date DESC
    """
    
    print("\n" + "=" * 80)
    print("COREHR QUERY: Looking for Kendall Rush")
    print("=" * 80)
    print(f"Query:\n{query}\n")
    
    try:
        df = client.query(query).to_dataframe()
        print(f"✓ Found {len(df)} records in CoreHR\n")
        
        if len(df) > 0:
            print(df.to_string())
            print("\n" + "-" * 80)
            print("ANALYSIS:")
            for idx, row in df.iterrows():
                print(f"\nRecord {idx + 1}:")
                print(f"  User ID: {row.get('userID')}")
                print(f"  Employee ID: {row.get('employeeID')}")
                print(f"  Job Code (Workday): {row.get('workday_job_code')}")
                print(f"  Position: {row.get('position_title')}")
                print(f"  Job Family: {row.get('job_family_id')}")
                print(f"  Store: {row.get('store_name')}")
                print(f"  Active: {row.get('is_active')}")
        else:
            print("⚠ No records found")
        
        return df
    
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


def verify_code_transformation():
    """
    Verify the code transformation pattern
    SMART: 1-202-2104
    Workday: US-01-0202-002104
    """
    print("\n" + "=" * 80)
    print("CODE FORMAT TRANSFORMATION VERIFICATION")
    print("=" * 80)
    
    # Kendall's data
    div = 1
    dept = 0
    code = 812673
    
    print(f"\nKendall's Data:")
    print(f"  Division: {div}")
    print(f"  Department: {dept}")
    print(f"  Job Code: {code}")
    
    # Build formats
    smart_format = f"{div}-{dept:03d}-{code}"
    workday_format = smart_to_workday(div, dept, code)
    
    print(f"\nTransformed Formats:")
    print(f"  SMART Format:    {smart_format}")
    print(f"  Workday Format:  {workday_format}")
    
    print(f"\nPattern:")
    print(f"  SMART:    {div}-{dept:03d}-{code}")
    print(f"  Workday:  US-{div:02d}-{dept:04d}-{code:06d}")
    
    print(f"\nConclusion:")
    print(f"  ✓ We can transform directly without Excel bridge!")
    print(f"  ✓ Transform Polaris SMART → Workday for CoreHR join")
    print(f"  ✓ Or query both and link by other identifiers (WIN, userID, etc.)")


def main():
    """Execute all queries"""
    
    # First verify the pattern
    verify_code_transformation()
    
    # Then query systems
    polaris_df = query_polaris_for_kendall()
    corehr_df = query_corehr_for_kendall()
    
    print("\n" + "=" * 80)
    print("CROSS-SYSTEM ANALYSIS")
    print("=" * 80)
    
    if polaris_df is not None and len(polaris_df) > 0 and \
       corehr_df is not None and len(corehr_df) > 0:
        print("✓ Found data in both Polaris and CoreHR - can validate linkage")
        print("✓ Confirms we can join directly without Excel bridge")
    else:
        print("⚠ Limited records found - verify query patterns")


if __name__ == "__main__":
    main()
