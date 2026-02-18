"""
Find the correct table/field that has User IDs (AD usernames)
Example format: KEW005L.s00525
"""
from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Check Unified Profile for userID field
query = """
SELECT 
    employeeID,
    userID,
    employmentInfo.positionInfoHistory[SAFE_OFFSET(0)].storeNumber as storeNumber
FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`
WHERE employmentInfo.positionInfoHistory[SAFE_OFFSET(0)].storeNumber = 'US-00525'
  AND employmentInfo.isActive = true
LIMIT 5
"""

print("Checking Unified Profile for User IDs...")
print("="*80)

try:
    results = client.query(query).result()
    
    for row in results:
        print(f"Employee ID: {row.employeeID}")
        print(f"User ID: {row.userID}")
        print(f"Store: {row.storeNumber}")
        print("-"*40)
    
except Exception as e:
    print(f"Error: {e}")
    print("\nTrying alternate query...")
    
    # Try simpler query
    query2 = """
    SELECT 
        employeeID,
        userID,
        countryCode
    FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`
    WHERE userID IS NOT NULL
      AND userID LIKE '%.s00525'
    LIMIT 5
    """
    
    try:
        results = client.query(query2).result()
        print("\nFound User IDs with store pattern:")
        for row in results:
            print(f"Employee ID: {row.employeeID}, User ID: {row.userID}")
    except Exception as e2:
        print(f"Second error: {e2}")
