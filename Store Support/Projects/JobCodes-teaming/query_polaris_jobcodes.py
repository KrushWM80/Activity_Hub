"""
BigQuery Query: Extract Polaris Job Codes and Related Data
Purpose: Pull job code authority data from Polaris analytics view
Connection: Requires BigQuery authentication (service account or user credentials)
"""

from google.cloud import bigquery
import pandas as pd

def query_polaris_job_codes():
    """
    Extract distinct job codes from Polaris analytics with key scheduling context
    
    Query Strategy:
    - Use vw_polaris_current_schedule view as authoritative source
    - Get DISTINCT job_code records (271 codes in dataset)
    - Include job_nm (which embeds the code) for validation
    - Get scheduling and staffing context
    """
    
    client = bigquery.Client()
    
    # Big Query SQL for Polaris
    query = """
    SELECT DISTINCT
        job_code,
        job_nm,
        job_id,
        COUNT(DISTINCT worker_id) as unique_workers,
        COUNT(DISTINCT location_id) as locations_assigned,
        MIN(insert_ts) as first_record_date,
        MAX(insert_ts) as last_record_date,
        worker_payment_type,  -- H (Hourly), P (Part-time)
        tenant_id
    FROM
        `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
    WHERE
        deleted = 'N'
        AND job_code IS NOT NULL
    GROUP BY
        job_code,
        job_nm,
        job_id,
        worker_payment_type,
        tenant_id
    ORDER BY
        job_code
    """
    
    print("Executing Polaris query...")
    print("-" * 80)
    print(f"Query:\n{query}")
    print("-" * 80)
    
    try:
        df = client.query(query).to_dataframe()
        print(f"\n✓ Retrieved {len(df)} distinct job codes from Polaris")
        print(f"Columns: {list(df.columns)}")
        print(f"\nFirst 5 records:")
        print(df.head())
        
        return df
    
    except Exception as e:
        print(f"\n✗ Error executing Polaris query: {e}")
        return None


def query_polaris_schedule_detail():
    """
    Alternative: Get full schedule detail (no DISTINCT) for join operations
    Use this when you need worker-level scheduling information
    """
    
    client = bigquery.Client()
    
    query = """
    SELECT
        job_code,
        job_nm,
        worker_id,
        location_id,
        location_nm,
        shift_id,
        shift_beg_dt_tm,
        shift_end_dt_tm,
        worker_payment_type,
        first_name,
        last_name,
        hire_date,
        insert_ts
    FROM
        `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
    WHERE
        deleted = 'N'
        AND job_code IS NOT NULL
    LIMIT 100  -- Start with sample for testing
    """
    
    print("Executing Polaris schedule detail query...")
    
    try:
        df = client.query(query).to_dataframe()
        print(f"✓ Retrieved {len(df)} schedule records")
        return df
    
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


if __name__ == "__main__":
    print("=" * 80)
    print("POLARIS JOB CODE EXTRACTION")
    print("=" * 80)
    
    # Execute main query
    polaris_codes = query_polaris_job_codes()
    
    # Save results
    if polaris_codes is not None:
        output_file = "polaris_job_codes_extracted.csv"
        polaris_codes.to_csv(output_file, index=False)
        print(f"\n✓ Saved {len(polaris_codes)} records to {output_file}")
    
    print("\n" + "=" * 80)
