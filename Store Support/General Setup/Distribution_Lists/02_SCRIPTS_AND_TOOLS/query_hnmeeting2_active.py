"""
Query HNMeeting2 Members with Employee Details - Using Unified Profile directly
"""

from google.cloud import bigquery
import csv
from datetime import datetime

# Initialize BigQuery client
client = bigquery.Client(project='wmt-assetprotection-prod')

# Load HNMeeting2 member emails
print("Loading HNMeeting2 member emails...")
with open('archive/hnmeeting2_members.txt', 'r') as f:
    member_emails = [line.strip() for line in f if '@' in line]

print(f"Found {len(member_emails)} member emails\n")

# Convert to SQL-safe list
emails_list = "', '".join([e.lower() for e in member_emails])

# Query using the structure you provided
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
  AND emp.employmentInfo.isActive = TRUE
  AND eI.emailType = 'Work'
  AND pI.isPrimary = TRUE
ORDER BY emp.personalInfo.legalLastName, emp.personalInfo.legalFirstName
"""

print("Querying BigQuery for employee details...")
print("This may take 30-60 seconds...\n")

try:
    query_job = client.query(query)
    results = query_job.result()
    
    # Convert to list
    enriched_data = []
    for row in results:
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
    
    # Export to CSV
    output_file = f'HNMeeting2_Members_Active_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    if enriched_data:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=enriched_data[0].keys())
            writer.writeheader()
            writer.writerows(enriched_data)
        
        print(f"✓ SUCCESS!")
        print(f"✓ Exported {len(enriched_data)} ACTIVE members to: {output_file}\n")
        
        # Summary statistics
        print(f"Summary:")
        print(f"  Total emails queried: {len(member_emails)}")
        print(f"  Active employees found: {len(enriched_data)}")
        print(f"  Not active/not found: {len(member_emails) - len(enriched_data)}\n")
        
        # Top locations
        from collections import Counter
        locations = [row['Location'] for row in enriched_data if row['Location']]
        if locations:
            print("Top Locations:")
            for loc, count in Counter(locations).most_common(10):
                print(f"  {loc}: {count}")
        
        # Top job titles
        job_titles = [row['Job_Title'] for row in enriched_data if row['Job_Title']]
        if job_titles:
            print("\nTop Job Titles:")
            for title, count in Counter(job_titles).most_common(10):
                print(f"  {title}: {count}")
                
        # Top cost centers
        cost_centers = [row['Cost_Center'] for row in enriched_data if row['Cost_Center']]
        if cost_centers:
            print("\nTop Cost Centers:")
            for cc, count in Counter(cost_centers).most_common(5):
                print(f"  {cc}: {count}")
    else:
        print("⚠ No active employees found matching the email list.")
        print("\nNote: This query only returns ACTIVE employees (isActive = TRUE)")
        print("Distribution list members who are terminated/inactive won't appear.")
    
except Exception as e:
    print(f"❌ Error querying BigQuery: {e}\n")
    print(f"Troubleshooting:")
    print(f"  • Verify you have access to the table")
    print(f"  • Check authentication: gcloud auth application-default login")
