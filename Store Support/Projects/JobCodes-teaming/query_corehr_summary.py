"""
Query CoreHR and extract key employment fields
"""

from google.cloud import bigquery

def query_corehr_summary():
    """Query CoreHR with selected fields"""
    client = bigquery.Client()
    
    # Query that extracts the key fields we need
    query = """
    SELECT
        userID,
        employeeID,
        personalInfo.legalFirstName as first_name,
        personalInfo.legalLastName as last_name,
        ARRAY_LENGTH(employmentInfo.positionInfoHistory) as num_positions
    FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`
    WHERE employeeID = '216386453'
    LIMIT 1
    """
    
    print("=" * 80)
    print("COREHR SUMMARY FOR WIN 216386453")
    print("=" * 80)
    
    try:
        job = client.query(query)
        results = job.result()
        rows = list(results)
        
        if len(rows) > 0:
            row = rows[0]
            print(f"\n✓ Found record:\n")
            print(f"  UserID (Workday format):   {row['userID']}")
            print(f"  EmployeeID (WIN):          {row['employeeID']}")
            print(f"  First Name:                {row['first_name']}")
            print(f"  Last Name:                 {row['last_name']}")
            print(f"  Position History Length:   {row['num_positions']}")
            
            print(f"\n✓ This confirms CoreHR and Polaris can be queried directly!")
            print(f"✓ WIN {row['employeeID']} data accessible in CoreHR")
        else:
            print("\n✗ No records found")
            
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    query_corehr_summary()
