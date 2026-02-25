from google.cloud import bigquery
import pandas as pd

client = bigquery.Client()

def search_corehr_simple():
    """Search CoreHR using simple WHERE clause on userID"""
    query = '''
    SELECT 
        userID,
        employeeID,
        personalInfo.legalFirstName as first_name,
        personalInfo.legalLastName as last_name,
        createdTs,
        modifiedTs
    FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`
    WHERE userID LIKE '%a0a0dwp%'
    LIMIT 100
    '''
    try:
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        df = pd.DataFrame(rows)
        print("\n" + "="*80)
        print("Results: CoreHR Search by User ID")
        print("="*80)
        if not df.empty:
            print(f"Found {len(df)} record(s):\n")
            print(df.to_string())
            return df
        else:
            print("✗ No matches found for User ID containing 'a0a0dwp'")
            return None
    except Exception as e:
        print(f"Error in User ID search: {e}")
        return None

def search_corehr_by_store():
    """Search CoreHR by store number"""
    query = '''
    SELECT 
        userID,
        employeeID,
        personalInfo.legalFirstName as first_name,
        personalInfo.legalLastName as last_name,
        createdTs
    FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`,
    UNNEST(employmentInfo.positionInfoHistory) as pos
    WHERE CAST(REGEXP_EXTRACT(pos.storeNumber, r'(\d+)') AS STRING) LIKE '%1497%'
       OR pos.storeName LIKE '%1497%'
    LIMIT 100
    '''
    try:
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        df = pd.DataFrame(rows)
        print("\n" + "="*80)
        print("Results: CoreHR Search by Store Number 1497")
        print("="*80)
        if not df.empty:
            print(f"Found {len(df)} record(s):\n")
            print(df.to_string())
            return df
        else:
            print("✗ No matches found for Store Number 1497")
            return None
    except Exception as e:
        print(f"Error in Store search: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("\n--- SEARCH 1: By User ID ---")
    results1 = search_corehr_simple()
    
    print("\n\n--- SEARCH 2: By Store Number ---")
    results2 = search_corehr_by_store()
