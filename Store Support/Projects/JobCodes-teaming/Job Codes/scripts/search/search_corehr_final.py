from google.cloud import bigquery
import pandas as pd

client = bigquery.Client()

def search_corehr_final():
    """Simple search for User ID in CoreHR"""
    query = '''
    SELECT 
        userID,
        employeeID,
        personalInfo.legalFirstName,
        personalInfo.legalLastName
    FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`
    WHERE userID LIKE '%a0a0dwp%'
    '''
    try:
        print("\n" + "="*80)
        print("Searching CoreHR for User ID: a0a0dwp")
        print("="*80)
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        df = pd.DataFrame(rows)
        
        if not df.empty:
            print(f"✓ Found {len(df)} record(s):\n")
            print(df.to_string())
        else:
            print("✗ No matches found for User ID containing 'a0a0dwp'")
        
        return df
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

if __name__ == "__main__":
    search_corehr_final()
