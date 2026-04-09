"""
Query Store Roster Contacts for Kendall Rush
"""

from google.cloud import bigquery
import pandas as pd

def query_kendall():
    """Query Store Roster Contacts for Kendall Rush"""
    client = bigquery.Client()
    
    query = """
    SELECT
        win_nbr,
        first_name,
        last_name,
        job_nm,
        location_nm
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Store Roster Contacts`
    WHERE 
        (first_name LIKE '%Kendall%' OR first_name LIKE '%kendall%')
        AND (last_name LIKE '%Rush%' OR last_name LIKE '%rush%')
    LIMIT 50
    """
    
    print("=" * 80)
    print("SEARCHING STORE ROSTER CONTACTS FOR KENDALL RUSH")
    print("=" * 80)
    
    try:
        job = client.query(query)
        df = job.result().to_dataframe()
        
        print(f"\n✓ Found {len(df)} records\n")
        if len(df) > 0:
            print(df.to_string())
            
            # Extract the WIN for verification
            win = df['win_nbr'].iloc[0]
            print(f"\n" + "=" * 80)
            print("EXTRACTED WIN:")
            print("=" * 80)
            print(f"WIN: {win}")
            print(f"Expected WIN: 219251625")
            print(f"Match: {win == 219251625}")
        else:
            print("No records found for Kendall Rush")
        
        return df
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    query_kendall()
