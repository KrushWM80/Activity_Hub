from google.cloud import bigquery
import pandas as pd

client = bigquery.Client()

def find_by_store_roster():
    """
    Query Store Roster Contacts table directly for Kathleen Reed at Store 30
    This is the data source we should have used instead of Polaris
    """
    query = '''
    SELECT 
        *
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Store Roster Contacts`
    WHERE location_number = 30
       AND (first_name LIKE '%Kathleen%' 
            OR last_name LIKE '%Reed%'
            OR LOWER(first_name) = 'kathleen'
            OR LOWER(last_name) = 'reed')
    LIMIT 20
    '''
    
    try:
        print("="*80)
        print("SEARCHING STORE ROSTER CONTACTS - STORE 30")
        print("="*80)
        
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        df = pd.DataFrame(rows)
        
        if not df.empty:
            print(f"\n✓ Found {len(df)} record(s):\n")
            print(df.to_string())
            return df
        else:
            print("\n✗ No matches in Store Roster Contacts")
            print("\nTrying broader search on Workforce Data table...\n")
            return search_workforce_table()
            
    except Exception as e:
        print(f"Error querying Store Roster Contacts: {e}")
        print("\nTrying Workforce Data table instead...\n")
        return search_workforce_table()

def search_workforce_table():
    """Fallback to Workforce Data table"""
    query = '''
    SELECT 
        *
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Workforce Data`
    WHERE location_nm LIKE '%30%' OR win_nbr = 30
    LIMIT 5
    '''
    
    try:
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        df = pd.DataFrame(rows)
        
        if not df.empty:
            print(f"Found {len(df)} rows in Workforce Data")
            print(df.columns.tolist())
            return df
        
    except Exception as e:
        print(f"Error with Workforce Data: {e}")
    
    return None

if __name__ == "__main__":
    find_by_store_roster()
