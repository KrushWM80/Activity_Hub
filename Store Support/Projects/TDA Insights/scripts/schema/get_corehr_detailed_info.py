from google.cloud import bigquery
import pandas as pd

client = bigquery.Client()

def get_detailed_info():
    """Get detailed information about the test associate"""
    query = '''
    SELECT 
        userID,
        employeeID,
        personalInfo.legalFirstName,
        personalInfo.legalLastName,
        personalInfo.preferredFirstName,
        personalInfo.preferredLastName,
        personalInfo.birthDate,
        personalInfo.gender,
        contactInfo.emailInfo,
        employmentInfo.activeStatusDate,
        employmentInfo.hireDate,
        employmentInfo.isActive,
        employmentInfo.employeeStatusCode,
        employmentInfo.employeeTypeCode,
        employmentInfo.positionInfoHistory
    FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`
    WHERE userID = 'a0a0dwp.s01497'
    '''
    try:
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        
        if rows:
            row = rows[0]
            print("\n" + "="*80)
            print("DETAILED INFORMATION: Test Associate a0a0dwp.s01497")
            print("="*80)
            print(f"\nUser ID:        {row.get('userID')}")
            print(f"Employee ID:    {row.get('employeeID')}")
            print(f"First Name:     {row.get('legalFirstName')}")
            print(f"Last Name:      {row.get('legalLastName')}")
            print(f"Preferred Name: {row.get('preferredFirstName')} {row.get('preferredLastName')}")
            print(f"Birth Date:     {row.get('birthDate')}")
            print(f"Gender:         {row.get('gender')}")
            print(f"Hire Date:      {row.get('hireDate')}")
            print(f"Active Status:  {row.get('isActive')}")
            print(f"Employee Type:  {row.get('employeeTypeCode')}")
            
            print(f"\n--- Email Information ---")
            emails = row.get('emailInfo', [])
            if emails:
                for idx, email in enumerate(emails, 1):
                    print(f"Email {idx}: {email.get('emailAddress')} ({email.get('emailType')})")
            
            print(f"\n--- Store Information ---")
            positions = row.get('positionInfoHistory', [])
            if positions:
                for idx, pos in enumerate(positions, 1):
                    print(f"\nPosition {idx}:")
                    print(f"  Store Number: {pos.get('storeNumber')}")
                    print(f"  Store Name:   {pos.get('storeName')}")
                    print(f"  Job Code:     {pos.get('jobCode')}")
                    print(f"  Job Title:    {pos.get('positionTitle')}")
                    print(f"  Position ID:  {pos.get('positionID')}")
                    print(f"  Effective Date: {pos.get('positionEffectiveDate')}")
                    print(f"  End Date:     {pos.get('positionEndDate')}")
            
            return row
        else:
            print("No detailed information found")
            return None
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    get_detailed_info()
