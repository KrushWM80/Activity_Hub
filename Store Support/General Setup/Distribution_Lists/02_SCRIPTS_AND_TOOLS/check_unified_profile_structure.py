"""
Check Unified Profile structure to find where store number is located
"""
from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Get a sample row
q = """
SELECT * 
FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW` 
WHERE employmentInfo.isActive = true
LIMIT 1
"""

try:
    row = list(client.query(q).result())[0]
    
    print("Top level fields:")
    print("="*80)
    for k in row.keys():
        print(f"  - {k}")
    
    print("\n\nemploymentInfo structure:")
    print("="*80)
    if 'employmentInfo' in row and row.employmentInfo:
        emp_info = row.employmentInfo
        for k in emp_info.keys():
            print(f"  - {k}: {type(emp_info[k])}")
        
        # Check positionInfo which likely has store
        if 'positionInfo' in emp_info and emp_info['positionInfo']:
            print("\n\npositionInfo[0] fields:")
            print("="*80)
            pos = emp_info['positionInfo'][0] if len(emp_info['positionInfo']) > 0 else None
            if pos:
                for k, v in pos.items():
                    if v and 'store' in k.lower():
                        print(f"  ✓ {k}: {v}")
                    elif v and k in ['storeNumber', 'costCenter', 'locationID']:
                        print(f"  ✓ {k}: {v}")
        
        # Check positionInfoHistory
        if 'positionInfoHistory' in emp_info and emp_info['positionInfoHistory']:
            print("\n\npositionInfoHistory[0] fields (recent):")
            print("="*80)
            pos = emp_info['positionInfoHistory'][0]
            for k, v in pos.items():
                if v and 'store' in k.lower():
                    print(f"  ✓ {k}: {v}")
    
    print("\n\ncontactInfo structure:")
    print("="*80)
    if 'contactInfo' in row and row.contactInfo:
        contact = row.contactInfo
        for k in contact.keys():
            print(f"  - {k}: {type(contact[k])}")
        
        # Check emailInfo
        if 'emailInfo' in contact and contact['emailInfo']:
            print("\n\nemailInfo[0]:")
            print("="*80)
            email = contact['emailInfo'][0]
            for k, v in email.items():
                if k in ['emailAddress', 'emailType', 'isPrimary']:
                    print(f"  ✓ {k}: {v}")

except Exception as e:
    print(f"Error: {e}")
