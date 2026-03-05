from google.cloud import bigquery
import pandas as pd

client = bigquery.Client()

def explore_polaris_locations():
    # Check what location_ids exist and get a sample
    query = '''
    SELECT 
        DISTINCT location_id,
        location_nm,
        COUNT(*) as record_count
    FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
    GROUP BY location_id, location_nm
    ORDER BY record_count DESC
    LIMIT 30
    '''
    try:
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        df = pd.DataFrame(rows)
        print("\n" + "="*80)
        print("Sample locations in Polaris table (sorted by record count)")
        print("="*80)
        print(df.to_string())
        print("\n")
        
        # Check if any location_id matches 1497
        if not df.empty:
            match_1497 = df[df['location_id'] == 1497]
            if not match_1497.empty:
                print(f"✓ Found location_id: 1497")
                print(match_1497.to_string())
            else:
                print(f"✗ Location_id 1497 NOT FOUND in this table")
                print(f"\nAvailable location_ids range from {df['location_id'].min()} to {df['location_id'].max()}")
        
        return df
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    explore_polaris_locations()
