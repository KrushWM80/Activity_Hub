"""
Debug: Check if HNMeeting2 emails map to WIN numbers
"""

from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Load HNMeeting2 member emails
with open('archive/hnmeeting2_members.txt', 'r') as f:
    member_emails = [line.strip() for line in f if '@' in line]

# Take first 20 for testing
test_emails = member_emails[:20]
emails_list = "', '".join([e.lower() for e in test_emails])

print(f"Testing first 20 emails from HNMeeting2...\n")

# Step 1: Check email to WIN mapping
query1 = f"""
SELECT DISTINCT
    email.emailAddress,
    emp.employeeID AS win_nbr
FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW` AS emp,
UNNEST(emp.contactInfo.emailInfo) AS email
WHERE LOWER(email.emailAddress) IN ('{emails_list}')
LIMIT 20
"""

print("Step 1: Checking email-to-WIN mapping...")
print("="*80)
results1 = client.query(query1).result()
wins_found = []
for row in results1:
    print(f"  {row.emailAddress:40} -> WIN: {row.win_nbr}")
    wins_found.append(str(row.win_nbr))

if not wins_found:
    print("  ❌ No WIN numbers found for these emails!")
else:
    print(f"\n✓ Found {len(wins_found)} WIN numbers\n")
    
    # Step 2: Check if those WINs exist in Polaris
    wins_list = "', '".join(wins_found)
    query2 = f"""
    SELECT 
        win_nbr,
        first_name,
        last_name,
        job_code,
        job_nm
    FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
    WHERE CAST(win_nbr AS STRING) IN ('{wins_list}')
    LIMIT 20
    """
    
    print("\nStep 2: Checking if WINs exist in Polaris schedule...")
    print("="*80)
    results2 = client.query(query2).result()
    polaris_count = 0
    for row in results2:
        print(f"  WIN {row.win_nbr}: {row.first_name} {row.last_name} - {row.job_nm}")
        polaris_count += 1
    
    if polaris_count == 0:
        print("  ❌ None of these WIN numbers found in Polaris!")
        print("  (Employees may be terminated or not in current schedule)")
    else:
        print(f"\n✓ Found {polaris_count} employees in Polaris")
