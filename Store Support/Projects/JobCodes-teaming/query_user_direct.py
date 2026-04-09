"""
Query CoreHR and Polaris directly for WIN 219251625
"""

from google.cloud import bigquery
import pandas as pd

def query_corehr():
    """Query CoreHR for employeeID 216386453 (Jennifer Spaulding)"""
    client = bigquery.Client()
    
    query = """
    Select *
    FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`
    Where employeeID = '216386453'
    """
    
    print("=" * 80)
    print("COREHR QUERY: WIN 216386453 (Jennifer Spaulding)")
    print("=" * 80)
    
    try:
        job = client.query(query)
        results = job.result()
        rows = list(results)
        
        print(f"✓ Found {len(rows)} records\n")
        if len(rows) > 0:
            print("Columns:")
            print([schema.name for schema in results.schema])
            print("\nData:")
            for i, row in enumerate(rows, 1):
                print(f"\nRow {i}:")
                for field, value in zip([schema.name for schema in results.schema], row):
                    print(f"  {field}: {value}")
        else:
            print("No records found")
        
        return rows
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def query_polaris():
    """Query Polaris for WIN 216386453 (may be empty if no active schedules)"""
    client = bigquery.Client()
    
    query = """
    Select *
    FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
    where win_nbr = 216386453
    limit 5
    """
    
    print("\n" + "=" * 80)
    print("POLARIS QUERY: WIN 216386453 (Active Schedules - Optional)")
    print("=" * 80)
    print("Note: May be empty if associate has no active store schedule\n")
    
    try:
        job = client.query(query)
        results = job.result()
        rows = list(results)
        
        print(f"✓ Found {len(rows)} records\n")
        if len(rows) > 0:
            print("Columns:")
            print([schema.name for schema in results.schema])
            print("\nData:")
            for i, row in enumerate(rows, 1):
                print(f"\nRow {i}:")
                for field, value in zip([schema.name for schema in results.schema], row):
                    print(f"  {field}: {value}")
        else:
            print("No records found")
        
        return rows
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    corehr_df = query_corehr()
    polaris_df = query_polaris()
