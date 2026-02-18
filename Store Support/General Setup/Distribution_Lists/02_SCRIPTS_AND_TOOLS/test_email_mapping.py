from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Test 1: Sample work emails from Unified Profile
print("Sample work emails from Unified Profile:")
print("="*80)
q1 = """
SELECT email.emailAddress, email.emailType
FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`,
UNNEST(contactInfo.emailInfo) AS email
WHERE email.emailType = 'Work'
LIMIT 10
"""
results = client.query(q1).result()
for row in results:
    print(f"  {row.emailAddress} ({row.emailType})")

# Test 2: Check if any HNMeeting2 emails match
print("\n\nChecking for HNMeeting2 member matches:")
print("="*80)
test_emails = ['Allen.Guest@walmart.com', 'Ryan.Dunphy@walmart.com', 'Lauren.Pruitt@walmart.com']
emails_str = "', '".join([e.lower() for e in test_emails])

q2 = f"""
SELECT 
    email.emailAddress,
    emp.employeeID
FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW` AS emp,
UNNEST(emp.contactInfo.emailInfo) AS email
WHERE LOWER(email.emailAddress) IN ('{emails_str}')
LIMIT 10
"""
results = client.query(q2).result()
count = 0
for row in results:
    print(f"  {row.emailAddress} -> WIN: {row.employeeID}")
    count += 1

if count == 0:
    print("  No matches found!")
    print("\n  Trying with @email.wal-mart.com domain...")
    test_emails_alt = [e.replace('@walmart.com', '@email.wal-mart.com') for e in test_emails]
    emails_str_alt = "', '".join([e.lower() for e in test_emails_alt])
    q3 = f"""
    SELECT 
        email.emailAddress,
        emp.employeeID
    FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW` AS emp,
    UNNEST(emp.contactInfo.emailInfo) AS email
    WHERE LOWER(email.emailAddress) IN ('{emails_str_alt}')
    LIMIT 10
    """
    results = client.query(q3).result()
    for row in results:
        print(f"    {row.emailAddress} -> WIN: {row.employeeID}")
