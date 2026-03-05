from google.cloud import bigquery
import pandas as pd
import json

client = bigquery.Client()

def search_corehr_for_associate():
    """Search CoreHR for the test associate"""
    query = '''
    SELECT 
        userID,
        employeeID,
        JSON_EXTRACT_SCALAR(personalInfo, '$.legalFirstName') as first_name,
        JSON_EXTRACT_SCALAR(personalInfo, '$.legalLastName') as last_name,
        JSON_EXTRACT_SCALAR(personalInfo, '$.preferredFirstName') as preferred_first_name,
        JSON_EXTRACT_SCALAR(personalInfo, '$.preferredLastName') as preferred_last_name,
        JSON_EXTRACT_SCALAR(contactInfo, '$.emailInfo[0].emailAddress') as email_address,
        JSON_EXTRACT_SCALAR(employmentInfo, '$.positionInfoHistory[0].storeNumber') as store_number,
        JSON_EXTRACT_SCALAR(employmentInfo, '$.positionInfoHistory[0].storeName') as store_name,
        createdTs,
        modifiedTs
    FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`
    WHERE userID LIKE '%a0a0dwp%'
       OR JSON_EXTRACT_SCALAR(employmentInfo, '$.positionInfoHistory[0].storeNumber') LIKE '%1497%'
       OR JSON_EXTRACT_SCALAR(contactInfo, '$.emailInfo[0].emailAddress') LIKE '%a0a0dwp%'
    LIMIT 100
    '''
    try:
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        df = pd.DataFrame(rows)
        print("\n" + "="*80)
        print("Results: CoreHR UNIFIED_PROFILE_SENSITIVE_VW")
        print("="*80)
        if not df.empty:
            print(f"Found {len(df)} record(s):\n")
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', None)
            pd.set_option('display.max_colwidth', None)
            print(df.to_string())
            
            # Check specifically for our test associate
            print(f"\n\n" + "="*80)
            print("Detailed search for User ID: a0a0dwp and Store Number: 1497")
            print("="*80)
            
            exact_match = df[df['userID'].astype(str).str.lower().str.contains('a0a0dwp.s01497', na=False)]
            if not exact_match.empty:
                print(f"✓ FOUND exact match for a0a0dwp.s01497:\n")
                print(exact_match.to_string())
            else:
                print(f"✗ Exact match for a0a0dwp.s01497 NOT found")
                print(f"\nMatching records found:")
                print(df[['userID', 'first_name', 'last_name', 'store_number']].to_string())
        else:
            print("✗ No matches found for User ID: a0a0dwp, Store: 1497, or Email containing 'a0a0dwp'")
        return df
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    search_corehr_for_associate()
