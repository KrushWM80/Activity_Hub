from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Test with known good emails
test_emails = ['Allen.Guest@walmart.com', 'Ryan.Dunphy@walmart.com', 'Lauren.Pruitt@walmart.com']
emails_str = "', '".join([e.lower() for e in test_emails])

query = f"""
SELECT DISTINCT
  emp.employeeID AS WIN,
  emp.personalInfo.legalFirstName AS first_name,
  emp.personalInfo.legalLastName AS last_name,
  eI.emailAddress AS work_email,
  pI.businessTitle AS job_title,
  pI.jobCode AS job_code,
  emp.employmentInfo.isActive AS is_active
FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW` emp
LEFT JOIN UNNEST(emp.contactInfo.emailInfo) AS eI
LEFT JOIN UNNEST(emp.employmentInfo.positionInfo) AS pI
WHERE LOWER(eI.emailAddress) IN ('{emails_str}')
  AND eI.emailType = 'Work'
LIMIT 10
"""

print("Testing with 3 known emails...")
print("="*80)
results = client.query(query).result()

for row in results:
    print(f"WIN: {row.WIN}")
    print(f"  Name: {row.first_name} {row.last_name}")
    print(f"  Email: {row.work_email}")
    print(f"  Job: {row.job_title}")
    print(f"  Job Code: {row.job_code}")
    print(f"  Active: {row.is_active}")
    print()
