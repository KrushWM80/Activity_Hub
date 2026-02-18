"""
Query HNMeeting2 Members - Batched approach to handle large email list
"""

from google.cloud import bigquery
import csv
from datetime import datetime

client = bigquery.Client(project='wmt-assetprotection-prod')

# Load emails
print("Loading HNMeeting2 member emails...")
with open('archive/hnmeeting2_members.txt', 'r', encoding='utf-16') as f:  # UTF-16 for Windows PowerShell output
    member_emails = [line.strip().lower() for line in f if '@' in line and line.strip()]

print(f"Found {len(member_emails)} member emails\n")

# Process in batches of 100
batch_size = 100
all_results = []

total_batches = (len(member_emails) + batch_size - 1) // batch_size

for i in range(0, len(member_emails), batch_size):
    batch = member_emails[i:i+batch_size]
    batch_num = (i // batch_size) + 1
    
    print(f"Processing batch {batch_num}/{total_batches} ({len(batch)} emails)...", end=' ')
    
    emails_list = "', '".join(batch)
    
    query = f"""
    SELECT DISTINCT
      eI.emailAddress AS email,
      emp.employeeID AS WIN,
      emp.personalInfo.legalFirstName AS first_name,
      emp.personalInfo.legalLastName AS last_name,
      pI.costCenter,
      pI.businessTitle AS job_title,
      pI.jobCode AS job_code,
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
        print(f"Found {len(batch_results)} active employees")
    except Exception as e:
        print(f"Error: {e}")

print(f"\n✓ Total active employees found: {len(all_results)}\n")

# Convert to CSV format
enriched_data = []
for row in all_results:
    enriched_data.append({
        'Email': row.email or '',
        'WIN': str(row.WIN) if row.WIN else '',
        'First_Name': row.first_name or '',
        'Last_Name': row.last_name or '',
        'Cost_Center': row.costCenter or '',
        'Job_Title': row.job_title or '',
        'Job_Code': row.job_code or '',
        'Location': row.location or '',
        'Hire_Date': str(row.hire_date) if row.hire_date else '',
        'Manager_WIN': str(row.manager_win) if row.manager_win else ''
    })

# Export
output_file = f'HNMeeting2_Members_Final_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

if enriched_data:
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=enriched_data[0].keys())
        writer.writeheader()
        writer.writerows(enriched_data)
    
    print(f"✓ Exported to: {output_file}\n")
    
    # Summary
    from collections import Counter
    print("Summary:")
    print(f"  Total emails queried: {len(member_emails)}")
    print(f"  Active employees: {len(enriched_data)}")
    print(f"  Not found/inactive: {len(member_emails) - len(enriched_data)}\n")
    
    # Top job titles
    job_titles = [row['Job_Title'] for row in enriched_data if row['Job_Title']]
    if job_titles:
        print("Top Job Titles:")
        for title, count in Counter(job_titles).most_common(10):
            print(f"  {title}: {count}")
else:
    print("No active employees found.")
