"""
Query the Workforce Data table that we have access to
"""

from google.cloud import bigquery
import pandas as pd

def query_workforce_kendall():
    """Query Workforce Data for Kendall Rush"""
    client = bigquery.Client()
    
    # Query 1: Search by name and store
    query = """
    SELECT
        *
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Workforce Data`
    WHERE 
        (first_name LIKE '%Kendall%' OR first_name LIKE '%kendall%')
        AND (last_name LIKE '%Rush%' OR last_name LIKE '%rush%')
    LIMIT 50
    """
    
    print("=" * 80)
    print("SEARCHING WORKFORCE DATA FOR KENDALL RUSH")
    print("=" * 80)
    
    try:
        job = client.query(query)
        df = job.result().to_dataframe()
        
        print(f"\n✓ Found {len(df)} records\n")
        if len(df) > 0:
            print(df.to_string())
            print("\n" + "=" * 80)
            print("COLUMN NAMES:")
            print("=" * 80)
            print(df.columns.tolist())
        else:
            print("No records found for Kendall Rush")
        
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None

def query_Store_Roster():
    """Query Store Roster Contacts"""
    client = bigquery.Client()
    
    query = """
    SELECT
        COUNT(*) as total_records,
        COUNT(DISTINCT Store) as unique_stores
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Store Roster Contacts`
    """
    
    print("\n" + "=" * 80)
    print("CHECKING STORE ROSTER CONTACTS")
    print("=" * 80)
    
    try:
        job = client.query(query)
        df = job.result().to_dataframe()
        
        print(f"\n{df.to_string()}\n")
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    query_workforce_kendall()
    query_Store_Roster()
