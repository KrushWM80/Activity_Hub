"""Check Realty Status values"""
from google.cloud import bigquery

client = bigquery.Client(project="wmt-assetprotection-prod")

# Check all Status values
query = """
SELECT Status, COUNT(*) as cnt
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Project_Source = 'Realty'
GROUP BY Status
ORDER BY cnt DESC
"""

print("Realty Status values:\n")
for row in client.query(query).result():
    print(f"  '{row.Status}': {row.cnt}")

# Now check Active Realty projects with Project_Type = 'None'
query2 = """
SELECT Project_Type, Initiative_Type, Status, Facility, FY
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Project_Source = 'Realty'
  AND Status = 'Active'
  AND (Project_Type = 'None' OR Project_Type IS NULL)
LIMIT 30
"""

print("\n" + "="*60)
print("\nACTIVE Realty projects with Project_Type = 'None' or NULL:\n")
count = 0
for row in client.query(query2).result():
    count += 1
    facility = int(row.Facility) if row.Facility else 'None'
    print(f"  R-{facility}: Project_Type='{row.Project_Type}' | Initiative_Type='{row.Initiative_Type}' | FY={row.FY}")

print(f"\nTotal ACTIVE with missing Project_Type: {count}")
