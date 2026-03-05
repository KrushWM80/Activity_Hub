from google.cloud import bigquery
import pandas as pd

client = bigquery.Client()

def explore_corehr_schema():
    """First, explore the schema and sample data"""
    query = '''
    SELECT *
    FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`
    LIMIT 1
    '''
    try:
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        if rows:
            first_row = rows[0]
            print("\nAvailable columns in UNIFIED_PROFILE_SENSITIVE_VW:")
            for col in sorted(first_row.keys()):
                print(f"  - {col}")
            print("\nSample data (first row):")
            for key, value in sorted(first_row.items()):
                if value is not None:
                    print(f"  {key}: {value}")
    except Exception as e:
        print(f"Error exploring schema: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    explore_corehr_schema()
