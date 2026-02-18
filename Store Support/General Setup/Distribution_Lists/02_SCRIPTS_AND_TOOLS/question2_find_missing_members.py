"""
Question 2: Identify Missing Members for HNMeeting2
Queries BigQuery to find people who SHOULD be on the list but aren't
"""

from google.cloud import bigquery
import csv
from datetime import datetime

client = bigquery.Client(project='wmt-assetprotection-prod')

print("="*80)
print("IDENTIFYING MISSING MEMBERS FOR HNMEETING2")
print("="*80)

# Load current member list
with open('archive/hnmeeting2_members.txt', 'r', encoding='utf-16') as f:
    current_members = set(line.strip().lower() for line in f if '@' in line and line.strip())

print(f"\nCurrent list size: {len(current_members)} emails")

# Define the job code-based criteria
tier1_codes = [
    'US-100015099',  # Market Manager
    'US-100017446',  # Senior Director, Merchandising
    'US-100019721',  # Senior Director, Merchandising Operations
    'US-100020695',  # Senior Director, Operations
    'US-100019946',  # Senior Director, Supply Chain Management
    'US-100022540',  # Senior Director, Product Management
    'US-100022319',  # Senior Director, Data Science
    'US-100022602',  # Senior Director, Advanced Analytics
    'US-100024103',  # Senior Director, Technology Operations
    'US-100019221',  # Senior Director, Real Estate
]

print("\n" + "="*80)
print("STEP 1: Query ALL people matching Tier 1 job codes")
print("="*80)

# Query for Tier 1 members
tier1_codes_str = "', '".join(tier1_codes)

query = f"""
SELECT DISTINCT
  eI.emailAddress AS email,
  emp.employeeID AS WIN,
  emp.personalInfo.legalFirstName AS first_name,
  emp.personalInfo.legalLastName AS last_name,
  pI.costCenter,
  pI.businessSegment AS department,
  pI.businessTitle AS job_title,
  pI.jobCode AS job_code,
  pI.managementLevelID AS management_level,
  pI.storeName AS location,
  emp.employmentInfo.hireDate AS hire_date,
  pI.managerWinNumber AS manager_win,
  emp.employmentInfo.terminationDate AS termination_date
FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW` emp
LEFT JOIN UNNEST(emp.contactInfo.emailInfo) AS eI
LEFT JOIN UNNEST(emp.employmentInfo.positionInfo) AS pI
WHERE pI.jobCode IN ('{tier1_codes_str}')
  AND eI.emailType = 'Work'
  AND emp.employmentInfo.terminationDate IS NULL
  AND pI.isPrimary = TRUE
"""

print("\nQuerying BigQuery for Tier 1 job codes...")
print(f"Job codes: {len(tier1_codes)}")

try:
    results = client.query(query).result()
    tier1_all = list(results)
    print(f"✓ Found {len(tier1_all)} people with Tier 1 job codes")
except Exception as e:
    print(f"✗ Error: {e}")
    tier1_all = []

# Identify missing Tier 1 members
tier1_emails = set(row.email.lower() for row in tier1_all if row.email)
tier1_missing = tier1_emails - current_members
tier1_on_list = tier1_emails & current_members

print(f"\n✓ On current list: {len(tier1_on_list)} ({(len(tier1_on_list)/len(tier1_emails)*100):.1f}%)")
print(f"✗ MISSING from list: {len(tier1_missing)} ({(len(tier1_missing)/len(tier1_emails)*100):.1f}%)")

print("\n" + "="*80)
print("STEP 2: Query Senior Directors (Title Pattern)")
print("="*80)

query = """
SELECT DISTINCT
  eI.emailAddress AS email,
  emp.employeeID AS WIN,
  emp.personalInfo.legalFirstName AS first_name,
  emp.personalInfo.legalLastName AS last_name,
  pI.costCenter,
  pI.businessSegment AS department,
  pI.businessTitle AS job_title,
  pI.jobCode AS job_code,
  pI.managementLevelID AS management_level,
  pI.storeName AS location,
  emp.employmentInfo.hireDate AS hire_date,
  pI.managerWinNumber AS manager_win
FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW` emp
LEFT JOIN UNNEST(emp.contactInfo.emailInfo) AS eI
LEFT JOIN UNNEST(emp.employmentInfo.positionInfo) AS pI
WHERE LOWER(pI.businessTitle) LIKE '%senior director%'
  AND eI.emailType = 'Work'
  AND pI.businessSegment = 'HO'
  AND emp.employmentInfo.terminationDate IS NULL
  AND pI.isPrimary = TRUE
"""

print("\nQuerying for all Senior Directors in Home Office...")

try:
    results = client.query(query).result()
    sr_dir_all = list(results)
    print(f"✓ Found {len(sr_dir_all)} Senior Directors in HO")
except Exception as e:
    print(f"✗ Error: {e}")
    sr_dir_all = []

# Identify missing Senior Directors
sr_dir_emails = set(row.email.lower() for row in sr_dir_all if row.email)
sr_dir_missing = sr_dir_emails - current_members
sr_dir_on_list = sr_dir_emails & current_members

print(f"\n✓ On current list: {len(sr_dir_on_list)} ({(len(sr_dir_on_list)/len(sr_dir_emails)*100):.1f}%)")
print(f"✗ MISSING from list: {len(sr_dir_missing)} ({(len(sr_dir_missing)/len(sr_dir_emails)*100):.1f}%)")

print("\n" + "="*80)
print("STEP 3: Query Group Directors (Relevant Functions)")
print("="*80)

query = """
SELECT DISTINCT
  eI.emailAddress AS email,
  emp.employeeID AS WIN,
  emp.personalInfo.legalFirstName AS first_name,
  emp.personalInfo.legalLastName AS last_name,
  pI.costCenter,
  pI.businessSegment AS department,
  pI.businessTitle AS job_title,
  pI.jobCode AS job_code,
  pI.managementLevelID AS management_level,
  pI.storeName AS location,
  emp.employmentInfo.hireDate AS hire_date,
  pI.managerWinNumber AS manager_win
FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW` emp
LEFT JOIN UNNEST(emp.contactInfo.emailInfo) AS eI
LEFT JOIN UNNEST(emp.employmentInfo.positionInfo) AS pI
WHERE LOWER(pI.businessTitle) LIKE '%group director%'
  AND eI.emailType = 'Work'
  AND pI.businessSegment = 'HO'
  AND (
    LOWER(pI.businessTitle) LIKE '%operations%'
    OR LOWER(pI.businessTitle) LIKE '%supply chain%'
    OR LOWER(pI.businessTitle) LIKE '%merchandising%'
    OR LOWER(pI.businessTitle) LIKE '%product%'
    OR LOWER(pI.businessTitle) LIKE '%technology%'
    OR LOWER(pI.businessTitle) LIKE '%data science%'
  )
  AND emp.employmentInfo.terminationDate IS NULL
  AND pI.isPrimary = TRUE
"""

print("\nQuerying for Group Directors in relevant functions...")

try:
    results = client.query(query).result()
    group_dir_all = list(results)
    print(f"✓ Found {len(group_dir_all)} Group Directors")
except Exception as e:
    print(f"✗ Error: {e}")
    group_dir_all = []

# Identify missing Group Directors
group_dir_emails = set(row.email.lower() for row in group_dir_all if row.email)
group_dir_missing = group_dir_emails - current_members
group_dir_on_list = group_dir_emails & current_members

print(f"\n✓ On current list: {len(group_dir_on_list)} ({(len(group_dir_on_list)/len(group_dir_emails)*100 if len(group_dir_emails) > 0 else 0):.1f}%)")
print(f"✗ MISSING from list: {len(group_dir_missing)} ({(len(group_dir_missing)/len(group_dir_emails)*100 if len(group_dir_emails) > 0 else 0):.1f}%)")

print("\n" + "="*80)
print("SUMMARY: MISSING MEMBERS ANALYSIS")
print("="*80)

# Combine all missing (remove duplicates)
all_missing_emails = tier1_missing | sr_dir_missing | group_dir_missing
all_should_be = tier1_emails | sr_dir_emails | group_dir_emails

print(f"\nTotal people who SHOULD be on list: {len(all_should_be)}")
print(f"Currently on list: {len(current_members)}")
print(f"\n✗ TOTAL MISSING: {len(all_missing_emails)} people")
print(f"\nMissing Rate: {(len(all_missing_emails)/len(all_should_be)*100):.1f}%")

# Break down by category
print(f"\nBreakdown of Missing Members:")
print(f"  Tier 1 (Core Job Codes): {len(tier1_missing)} missing")
print(f"  Senior Directors: {len(sr_dir_missing)} missing")
print(f"  Group Directors: {len(group_dir_missing)} missing")

# Create combined list of ALL people who should be on list
all_results = tier1_all + sr_dir_all + group_dir_all

# Build lookup for missing details
missing_details = []
for row in all_results:
    if row.email and row.email.lower() in all_missing_emails:
        missing_details.append({
            'Email': row.email,
            'WIN': str(row.WIN) if row.WIN else '',
            'First_Name': row.first_name or '',
            'Last_Name': row.last_name or '',
            'Cost_Center': row.costCenter or '',
            'Department': row.department or '',
            'Job_Title': row.job_title or '',
            'Job_Code': row.job_code or '',
            'Management_Level': row.management_level or '',
            'Location': row.location or '',
            'Hire_Date': str(row.hire_date) if row.hire_date else '',
            'Manager_WIN': str(row.manager_win) if row.manager_win else ''
        })

# Export missing members
output_file = f'HNMeeting2_Missing_Members_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

if missing_details:
    # Remove duplicates by email
    seen = set()
    unique_missing = []
    for member in missing_details:
        email_lower = member['Email'].lower()
        if email_lower not in seen:
            seen.add(email_lower)
            unique_missing.append(member)
    
    fieldnames = ['Email', 'WIN', 'First_Name', 'Last_Name', 'Cost_Center', 'Department',
                  'Job_Title', 'Job_Code', 'Management_Level', 'Location', 'Hire_Date', 'Manager_WIN']
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(unique_missing)
    
    print(f"\n✓ Missing members exported to: {output_file}")
    print(f"✓ Total unique missing: {len(unique_missing)}")
    
    # Analysis of missing by job code
    from collections import Counter
    missing_job_codes = Counter([m['Job_Code'] for m in unique_missing if m['Job_Code']])
    
    print(f"\nTop Missing Job Codes:")
    for code, count in missing_job_codes.most_common(10):
        title = next((m['Job_Title'] for m in unique_missing if m['Job_Code'] == code), 'N/A')
        print(f"  {code}: {count} - {title}")

print("\n" + "="*80)
print("RECOMMENDATIONS")
print("="*80)

print(f"""
ACTION ITEMS:

1. REVIEW & ADD {len(all_missing_emails)} missing members
   - Export file: {output_file}
   - Prioritize Tier 1 job codes ({len(tier1_missing)} missing)
   - Review Senior Directors ({len(sr_dir_missing)} missing)
   
2. VALIDATE current {len(current_members)} members
   - Check for people who should be REMOVED
   - Verify employment status (terminated, transferred, etc.)
   
3. IMPLEMENT automated sync
   - Use job code-based parameters from Question 1
   - Schedule quarterly reviews
   - Set up alerts for new hires in key job codes
   
4. ESTABLISH governance
   - Define list owner
   - Document inclusion criteria
   - Track addition/removal justifications
""")

print("\n✓ Analysis complete!")
