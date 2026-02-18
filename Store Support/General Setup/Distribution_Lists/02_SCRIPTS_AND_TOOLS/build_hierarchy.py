"""
Enhanced HNMeeting2 Query with Department and Management Hierarchy
"""

from google.cloud import bigquery
import csv
from datetime import datetime
from collections import defaultdict

client = bigquery.Client(project='wmt-assetprotection-prod')

print("="*80)
print("STEP 1: Loading HNMeeting2 Members with Full Details")
print("="*80)

# Load emails
with open('archive/hnmeeting2_members.txt', 'r', encoding='utf-16') as f:
    member_emails = [line.strip().lower() for line in f if '@' in line and line.strip()]

print(f"\nFound {len(member_emails)} member emails")

# Get all member data with department
batch_size = 100
all_results = []
total_batches = (len(member_emails) + batch_size - 1) // batch_size

print(f"\nQuerying BigQuery in {total_batches} batches...\n")

for i in range(0, len(member_emails), batch_size):
    batch = member_emails[i:i+batch_size]
    batch_num = (i // batch_size) + 1
    
    print(f"Batch {batch_num}/{total_batches}...", end=' ')
    
    emails_list = "', '".join(batch)
    
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
      pI.managerWinNumber AS manager_win
    FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW` emp
    LEFT JOIN UNNEST(emp.contactInfo.emailInfo) AS eI
    LEFT JOIN UNNEST(emp.employmentInfo.positionInfo) AS pI
    WHERE LOWER(eI.emailAddress) IN ('{emails_list}')
      AND eI.emailType = 'Work'
    """
    
    try:
        results = client.query(query).result()
        batch_results = list(results)
        all_results.extend(batch_results)
        print(f"✓ {len(batch_results)} found")
    except Exception as e:
        print(f"✗ Error: {e}")

print(f"\n✓ Total: {len(all_results)} members retrieved\n")

# Convert to dictionaries
members = []
manager_wins = set()

for row in all_results:
    member = {
        'Email': row.email or '',
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
    }
    members.append(member)
    if member['Manager_WIN']:
        manager_wins.add(member['Manager_WIN'])

print("="*80)
print("STEP 2: Building Management Hierarchy")
print("="*80)

# Get manager details for hierarchy
print(f"\nQuerying {len(manager_wins)} unique managers...")

manager_cache = {}

# Query managers in batches
manager_list = list(manager_wins)
for i in range(0, len(manager_list), 100):
    batch = manager_list[i:i+100]
    wins_str = "', '".join(batch)
    
    query = f"""
    SELECT DISTINCT
      emp.employeeID AS WIN,
      emp.personalInfo.legalFirstName AS first_name,
      emp.personalInfo.legalLastName AS last_name,
      pI.businessTitle AS job_title,
      pI.managementLevelID AS management_level,
      pI.managerWinNumber AS manager_win
    FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW` emp
    LEFT JOIN UNNEST(emp.employmentInfo.positionInfo) AS pI
    WHERE emp.employeeID IN ('{wins_str}')
      AND pI.isPrimary = TRUE
    """
    
    try:
        results = client.query(query).result()
        for row in results:
            manager_cache[str(row.WIN)] = {
                'name': f"{row.first_name} {row.last_name}",
                'title': row.job_title or '',
                'level': row.management_level or '',
                'manager_win': str(row.manager_win) if row.manager_win else ''
            }
    except Exception as e:
        print(f"Error querying managers: {e}")

print(f"✓ Cached {len(manager_cache)} manager details\n")

# Build hierarchy for each member
print("Building management chains...")

for member in members:
    current_win = member['Manager_WIN']
    chain = []
    visited = set()
    
    # Traverse up the management chain
    while current_win and current_win in manager_cache and current_win not in visited:
        visited.add(current_win)
        mgr = manager_cache[current_win]
        chain.append({
            'name': mgr['name'],
            'title': mgr['title'],
            'level': mgr['level']
        })
        current_win = mgr['manager_win']
        
        if len(chain) >= 10:  # Safety limit
            break
    
    # Extract hierarchy levels
    member['Direct_Manager'] = chain[0]['name'] if len(chain) > 0 else ''
    member['Direct_Manager_Title'] = chain[0]['title'] if len(chain) > 0 else ''
    
    # Find specific levels in the chain
    member['Director'] = ''
    member['Senior_Director'] = ''
    member['Group_Director'] = ''
    member['VP'] = ''
    member['SVP'] = ''
    member['EVP'] = ''
    
    for mgr in chain:
        title_lower = mgr['title'].lower()
        level_lower = mgr['level'].lower()
        
        if 'evp' in title_lower or 'executive vice president' in title_lower:
            if not member['EVP']:
                member['EVP'] = mgr['name']
        elif 'senior vice president' in title_lower or 'svp' in title_lower:
            if not member['SVP']:
                member['SVP'] = mgr['name']
        elif 'vice president' in title_lower or ('vp' in level_lower and 'svp' not in title_lower):
            if not member['VP']:
                member['VP'] = mgr['name']
        elif 'group director' in title_lower:
            if not member['Group_Director']:
                member['Group_Director'] = mgr['name']
        elif 'senior director' in title_lower:
            if not member['Senior_Director']:
                member['Senior_Director'] = mgr['name']
        elif 'director' in title_lower and 'senior' not in title_lower and 'group' not in title_lower:
            if not member['Director']:
                member['Director'] = mgr['name']

print(f"✓ Management chains built for {len(members)} members\n")

# Export enhanced CSV
output_file = f'HNMeeting2_With_Hierarchy_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

if members:
    fieldnames = ['Email', 'WIN', 'First_Name', 'Last_Name', 'Cost_Center', 'Department', 
                  'Job_Title', 'Job_Code', 'Management_Level', 'Location', 'Hire_Date',
                  'Manager_WIN', 'Direct_Manager', 'Direct_Manager_Title', 'Director', 'Senior_Director', 
                  'Group_Director', 'VP', 'SVP', 'EVP']
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(members)
    
    print("="*80)
    print("EXPORT COMPLETE")
    print("="*80)
    print(f"\n✓ File: {output_file}")
    print(f"✓ Records: {len(members)}")
    print(f"✓ Columns: {len(fieldnames)}\n")

    # Quick summary
    from collections import Counter
    
    print("Quick Summary:")
    print("-"*80)
    
    departments = Counter([m['Department'] for m in members if m['Department']])
    print(f"\nTop Departments:")
    for dept, count in departments.most_common(5):
        print(f"  {dept}: {count}")
    
    job_titles = Counter([m['Job_Title'] for m in members if m['Job_Title']])
    print(f"\nTop Job Titles:")
    for title, count in job_titles.most_common(5):
        print(f"  {title}: {count}")
    
    print(f"\nHierarchy Coverage:")
    print(f"  Has Director: {sum(1 for m in members if m['Director'])}")
    print(f"  Has Senior Director: {sum(1 for m in members if m['Senior_Director'])}")
    print(f"  Has Group Director: {sum(1 for m in members if m['Group_Director'])}")
    print(f"  Has VP: {sum(1 for m in members if m['VP'])}")
    print(f"  Has SVP: {sum(1 for m in members if m['SVP'])}")
    print(f"  Has EVP: {sum(1 for m in members if m['EVP'])}")

print("\n✓ Ready for analysis!")
