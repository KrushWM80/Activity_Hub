"""
Query HNMeeting2 Members with Employee Details from BigQuery
Uses Polaris and Unified Profile tables to get WIN, Job Code, Title
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

print(f"Found {len(member_emails)} member emails")

# Convert to SQL-safe list
emails_list = "', '".join(member_emails)

# Query to get employee details
# Note: This assumes there's a way to map email to WIN in your environment
# You may need to adjust based on available tables

query = f"""
WITH member_emails AS (
    SELECT email
    FROM UNNEST(['{emails_list}']) AS email
)

SELECT 
    m.email,
    ps.first_name,
    ps.last_name,
    CONCAT(ps.first_name, ' ', ps.last_name) AS name,
    ps.win_nbr AS win,
    ps.job_code,
    ps.job_nm AS job_title,
    ps.location_nm AS location,
    ps.hire_date
FROM member_emails m
LEFT JOIN `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule` ps
    ON CAST(ps.win_nbr AS STRING) = REGEXP_EXTRACT(m.email, r'(\\d+)')  -- Try extracting WIN from email
ORDER BY ps.last_name, ps.first_name
LIMIT 1000
"""

print("\nQuerying BigQuery for employee details...")
print("This may take 30-60 seconds...\n")

try:
    query_job = client.query(query)
    results = query_job.result()
    
    # Convert to list
    enriched_data = []
    for row in results:
        enriched_data.append({
            'Email': row.email,
            'Name': row.name or '',
            'WIN': row.win or '',
            'Job_Code': row.job_code or '',
            'Job_Title': row.job_title or '',
            'Department': row.department or '',
            'Location': row.location_name or '',
            'Hire_Date': str(row.hire_date) if row.hire_date else '',
            'Manager': row.manager_name or ''
        })
    
    # Export to CSV
    output_file = f'HNMeeting2_Members_with_Details_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        if enriched_data:
            writer = csv.DictWriter(f, fieldnames=enriched_data[0].keys())
            writer.writeheader()
            writer.writerows(enriched_data)
    
    print(f"✓ SUCCESS!")
    print(f"✓ Exported {len(enriched_data)} members to: {output_file}\n")
    
    # Summary statistics
    found_count = sum(1 for row in enriched_data if row['WIN'])
    not_found_count = len(enriched_data) - found_count
    
    print(f"Summary:")
    print(f"  Total emails: {len(enriched_data)}")
    print(f"  Found in Unified Profile: {found_count}")
    print(f"  Not found: {not_found_count}\n")
    
    # Top departments
    from collections import Counter
    departments = [row['Department'] for row in enriched_data if row['Department']]
    if departments:
        print("Top Departments:")
        for dept, count in Counter(departments).most_common(5):
            print(f"  {dept}: {count}")
    
except Exception as e:
    print(f"Error querying BigQuery: {e}")
    print(f"\nTroubleshooting:")
    print(f"  • Verify you have access to these tables:")
    print(f"    - wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW")
    print(f"    - polaris-analytics-prod.us_walmart.vw_polaris_current_schedule")
    print(f"  • Check you're authenticated: gcloud auth application-default login")
