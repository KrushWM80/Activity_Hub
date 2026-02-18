"""
Query User IDs, WIN Numbers, and Emails for Specific Walmart Store Numbers
Queries BigQuery Unified Profile table for employees at specified stores
"""

from google.cloud import bigquery
import csv
from datetime import datetime

# Initialize BigQuery client
client = bigquery.Client(project='wmt-assetprotection-prod')

# Store numbers to query
store_numbers = [
    525, 1166, 1268, 1348, 1352, 1392, 2580, 2772, 2944, 3606, 
    3629, 3862, 4065, 4273, 4561, 5005, 5816, 5817, 5818, 5819, 
    5820, 6398, 7243
]

print(f"Querying employees for {len(store_numbers)} stores...")
print(f"Store numbers: {', '.join(map(str, store_numbers))}\n")

# Convert store numbers to SQL-safe list
stores_list = ', '.join(map(str, store_numbers))

# Query to get employee details by joining Polaris with Unified Profile
# Polaris has current schedule/store info, Unified Profile has User IDs and emails
query = f"""
WITH store_employees AS (
    SELECT DISTINCT
        location_nm as store_number,
        win_nbr,
        first_name,
        last_name,
        job_nm as job_title,
        job_code
    FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
    WHERE CAST(location_nm AS INT64) IN ({stores_list})
      AND win_nbr IS NOT NULL
)
SELECT DISTINCT
    se.store_number,
    se.win_nbr,
    up.userID as user_id,
    COALESCE(
        up.contactInfo.emailInfo[SAFE_OFFSET(0)].emailAddress,
        CONCAT(CAST(se.win_nbr AS STRING), '@walmart.com')
    ) as email,
    se.first_name,
    se.last_name,
    se.job_title,
    se.job_code
FROM store_employees se
LEFT JOIN `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW` up
    ON CAST(se.win_nbr AS STRING) = CAST(up.employeeID AS STRING)
WHERE up.employmentInfo.isActive = true
ORDER BY se.store_number, se.last_name, se.first_name
"""

print("Querying BigQuery for store employees...")
print("This may take 30-60 seconds...\n")

try:
    query_job = client.query(query)
    results = query_job.result()
    
    # Convert to list
    employee_data = []
    store_counts = {}
    
    for row in results:
        store_nbr = row.store_number
        employee_data.append({
            'Store_Number': store_nbr,
            'WIN_Number': row.win_nbr or '',
            'User_ID': row.user_id or '',
            'Email_Address': row.email or '',
            'First_Name': row.first_name or '',
            'Last_Name': row.last_name or '',
            'Job_Title': row.job_title or '',
            'Job_Code': row.job_code or ''
        })
        
        # Count by store
        store_counts[store_nbr] = store_counts.get(store_nbr, 0) + 1
    
    # Display summary
    print(f"\n{'='*80}")
    print(f"QUERY RESULTS SUMMARY")
    print(f"{'='*80}")
    print(f"Total employees found: {len(employee_data)}")
    print(f"\nEmployees by Store:")
    print(f"{'-'*40}")
    
    for store in sorted(store_counts.keys()):
        print(f"Store {store:>5}: {store_counts[store]:>4} employees")
    
    # Check for stores with no employees
    missing_stores = [s for s in store_numbers if s not in store_counts]
    if missing_stores:
        print(f"\n⚠ Stores with no employees found: {', '.join(map(str, missing_stores))}")
    
    # Export to CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f'Store_Employees_{timestamp}.csv'
    
    if employee_data:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=employee_data[0].keys())
            writer.writeheader()
            writer.writerows(employee_data)
        
        print(f"\n✅ Data exported to: {output_file}")
        print(f"{'='*80}\n")
    else:
        print("\n⚠ No employee data found for the specified stores.")
    
    # Display sample records (first 5)
    if employee_data:
        print(f"\nSample Records (first 5):")
        print(f"{'-'*80}")
        for i, emp in enumerate(employee_data[:5], 1):
            print(f"\n{i}. Store {emp['Store_Number']} - {emp['First_Name']} {emp['Last_Name']}")
            print(f"   WIN: {emp['WIN_Number']}")
            print(f"   User ID: {emp['User_ID']}")
            print(f"   Email: {emp['Email_Address']}")
            print(f"   Title: {emp['Job_Title']}")

except Exception as e:
    print(f"\n❌ Error querying BigQuery: {str(e)}")
    print("\nTroubleshooting:")
    print("1. Verify you have BigQuery access to polaris-analytics-prod")
    print("2. Check that the vw_polaris_current_schedule view exists")
    print("3. Ensure your service account has proper permissions")
    print("4. Try running a simple query to test connection")
