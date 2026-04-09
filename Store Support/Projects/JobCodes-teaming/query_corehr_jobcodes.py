"""
BigQuery Query: Extract CoreHR Job Codes and Employment Data
Purpose: Pull job code and employment information from CoreHR unified profile view
Challenge: Data is deeply nested JSON - requires JSON unpacking

CoreHR Structure:
- Raw: employmentInfo.positionInfoHistory[] (array of position changes)
- Each position has: jobCode (Workday format), jobFamilyID, managementLevelID, etc.
- Multiple historical positions per employee (employment history)
- Need to extract CURRENT/ACTIVE position or most recent
"""

from google.cloud import bigquery
import pandas as pd
import json

def query_corehr_job_codes():
    """
    Extract job codes from CoreHR with employment context
    
    Complexity: Must handle nested JSON arrays
    - employmentInfo = main employment record
    - positionInfoHistory = array of position history records
    - jobCode appears in format like: US-01-0990-007410 (Workday format, not SMART)
    
    Strategy:
    1. Unnest positionInfoHistory array
    2. Filter to active/current positions
    3. Extract jobCode, job family, management level
    4. Get user identification for linking to Polaris
    """
    
    client = bigquery.Client()
    
    # Query: Extract from nested positionInfoHistory
    query = """
    WITH corehr_raw AS (
        SELECT
            employeeID,
            userID,
            countryCode,
            JSON_EXTRACT_SCALAR(employmentInfo, '$.hireDate') as hire_date,
            JSON_EXTRACT_SCALAR(employmentInfo, '$.terminationDate') as termination_date,
            JSON_EXTRACT_SCALAR(employmentInfo, '$.isTerminated') as is_terminated,
            JSON_EXTRACT_ARRAY(employmentInfo, '$.positionInfoHistory') as position_history
        FROM
            `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`
        WHERE
            countryCode = 'US'
    ),
    positions_unnested AS (
        SELECT
            employeeID,
            userID,
            countryCode,
            hire_date,
            termination_date,
            is_terminated,
            -- Unnest each position from the array
            JSON_EXTRACT_SCALAR(position, '$.jobCode') as workday_job_code,
            JSON_EXTRACT_SCALAR(position, '$.positionTitle') as position_title,
            JSON_EXTRACT_SCALAR(position, '$.jobFamilyID') as job_family_id,
            JSON_EXTRACT_SCALAR(position, '$.managementLevelID') as management_level_id,
            JSON_EXTRACT_SCALAR(position, '$.storeName') as store_name,
            JSON_EXTRACT_SCALAR(position, '$.storeNumber') as store_number,
            JSON_EXTRACT_SCALAR(position, '$.active') as is_position_active,
            JSON_EXTRACT_SCALAR(position, '$.isPrimary') as is_primary_position,
            JSON_EXTRACT_SCALAR(position, '$.payRateType') as pay_rate_type,
            JSON_EXTRACT_SCALAR(position, '$.jobEffectiveDate') as job_effective_date,
            JSON_EXTRACT_SCALAR(position, '$.jobEndDate') as job_end_date
        FROM
            corehr_raw,
            UNNEST(position_history) as position
        WHERE
            employment_history IS NOT NULL
    )
    SELECT
        employeeID,
        userID,
        workday_job_code,
        position_title,
        job_family_id,
        management_level_id,
        store_name,
        store_number,
        is_position_active,
        is_primary_position,
        pay_rate_type,
        job_effective_date,
        job_end_date,
        hire_date,
        termination_date,
        is_terminated
    FROM
        positions_unnested
    WHERE
        workday_job_code IS NOT NULL
    ORDER BY
        employeeID,
        job_effective_date DESC
    """
    
    print("Executing CoreHR query...")
    print("-" * 80)
    print(f"Query:\n{query}")
    print("-" * 80)
    
    try:
        df = client.query(query).to_dataframe()
        print(f"\n✓ Retrieved {len(df)} job code records from CoreHR")
        print(f"Columns: {list(df.columns)}")
        print(f"\nFirst 5 records:")
        print(df.head())
        
        return df
    
    except Exception as e:
        print(f"\n✗ Error executing CoreHR query: {e}")
        print(f"Note: This query requires BigQuery access and proper JSON path handling")
        return None


def query_corehr_distinct_codes():
    """
    Alternative: Get DISTINCT job codes from CoreHR (simpler version)
    Shows how many employees per Workday job code
    """
    
    client = bigquery.Client()
    
    query = """
    WITH positions_unnested AS (
        SELECT
            JSON_EXTRACT_SCALAR(position, '$.jobCode') as workday_job_code,
            JSON_EXTRACT_SCALAR(position, '$.jobFamilyID') as job_family_id,
            JSON_EXTRACT_SCALAR(position, '$.positionTitle') as position_title
        FROM
            `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`,
            UNNEST(JSON_EXTRACT_ARRAY(employmentInfo, '$.positionInfoHistory')) as position
        WHERE
            countryCode = 'US'
            AND JSON_EXTRACT_SCALAR(position, '$.jobCode') IS NOT NULL
    )
    SELECT
        workday_job_code,
        job_family_id,
        position_title,
        COUNT(DISTINCT workday_job_code) as count
    FROM
        positions_unnested
    GROUP BY
        workday_job_code,
        job_family_id,
        position_title
    ORDER BY
        workday_job_code
    """
    
    print("Executing CoreHR distinct codes query...")
    
    try:
        df = client.query(query).to_dataframe()
        print(f"✓ Retrieved {len(df)} distinct Workday job codes")
        return df
    
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


if __name__ == "__main__":
    print("=" * 80)
    print("COREHR JOB CODE EXTRACTION")
    print("=" * 80)
    
    # Execute query
    corehr_codes = query_corehr_job_codes()
    
    # Save results
    if corehr_codes is not None:
        output_file = "corehr_job_codes_extracted.csv"
        corehr_codes.to_csv(output_file, index=False)
        print(f"\n✓ Saved {len(corehr_codes)} records to {output_file}")
    
    print("\n" + "=" * 80)
    print("\nNOTE: CoreHR uses Workday format job codes (US-01-XXXX-XXXXXX)")
    print("      Polaris uses SMART format job codes (1-XXX-XXX)")
    print("      Excel master file has both formats for mapping")
    print("=" * 80)
