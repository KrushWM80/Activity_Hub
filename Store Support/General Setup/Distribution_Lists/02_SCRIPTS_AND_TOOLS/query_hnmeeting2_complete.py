"""
Query HNMeeting2 Members with Employee Details from BigQuery
Uses Polaris and Unified Profile with proper JOIN
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

# Convert to SQL-safe list for IN clause
emails_list = "', '".join(member_emails)

# Query using the structure you provided
query = f"""
WITH member_emails AS (
    SELECT email
    FROM UNNEST(['{emails_list}']) AS email
),
email_to_win AS (
    SELECT DISTINCT
        emp.employeeID AS win_nbr,
        LOWER(email.emailAddress) AS work_email
    FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW` AS emp,
    UNNEST(emp.contactInfo.emailInfo) AS email
    WHERE email.emailType = 'Work'
)

SELECT DISTINCT
    m.email,
    etw.win_nbr,
    t1.first_name,
    t1.last_name,
    t1.job_code,
    t1.job_nm AS job_title,
    t1.location_nm AS location,
    t1.hire_date
FROM member_emails m
LEFT JOIN email_to_win etw
    ON LOWER(m.email) = LOWER(etw.work_email)
LEFT JOIN `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule` AS t1
    ON CAST(etw.win_nbr AS INT64) = t1.win_nbr
ORDER BY m.email
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
            'First_Name': row.first_name or '',
            'Last_Name': row.last_name or '',
            'WIN': str(row.win_nbr) if row.win_nbr else '',
            'Job_Code': row.job_code or '',
            'Job_Title': row.job_title or '',
            'Location': row.location or '',
            'Hire_Date': str(row.hire_date) if row.hire_date else ''
        })
    
    # Export to CSV
    output_file = f'HNMeeting2_Members_Complete_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    if enriched_data:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=enriched_data[0].keys())
            writer.writeheader()
            writer.writerows(enriched_data)
        
        print(f"✓ SUCCESS!")
        print(f"✓ Exported {len(enriched_data)} members to: {output_file}\n")
        
        # Summary statistics
        print(f"Summary:")
        print(f"  Total emails queried: {len(member_emails)}")
        print(f"  Found with details: {len(enriched_data)}")
        print(f"  Not found: {len(member_emails) - len(enriched_data)}\n")
        
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
            for title, count in Counter(job_titles).most_common(5):
                print(f"  {title}: {count}")
    else:
        print("⚠ No results found. The query returned 0 rows.")
        print("\nPossible reasons:")
        print("  • Email addresses don't match Workday records")
        print("  • Members are not in current Polaris schedule (terminated/inactive)")
        print("  • Email format differences (walmart.com vs email.wal-mart.com)")
    
except Exception as e:
    print(f"❌ Error querying BigQuery: {e}\n")
    print(f"Troubleshooting:")
    print(f"  • Verify you have access to both tables")
    print(f"  • Check authentication: gcloud auth application-default login")
    print(f"  • Try running a simpler query first to test access")
