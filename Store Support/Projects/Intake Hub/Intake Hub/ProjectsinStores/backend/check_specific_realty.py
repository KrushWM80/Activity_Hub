"""Check specific Realty projects R-1915, R-1563, R-1784"""
from google.cloud import bigquery

client = bigquery.Client(project="wmt-assetprotection-prod")

# Check what Status values Realty uses
status_query = """
SELECT Status, COUNT(*) as cnt
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Project_Source = 'Realty'
GROUP BY Status
ORDER BY cnt DESC
"""
print("Realty Status values:\n")
for row in client.query(status_query).result():
    print(f"  '{row.Status}': {row.cnt}")

print("\n" + "="*60 + "\n")

# Check if "Inactive" is being treated as active in our logic
# Our WHERE excludes: 'Cancelled', 'Complete', 'Closed', 'On Hold'
# But "Inactive" is not in that list!
print("Checking: 'Inactive' status is NOT in our exclusion list!")
print("Our filter excludes: Cancelled, Complete, Closed, On Hold")
print("But 'Inactive' is a different value, so they slip through as 'Active'!\n")

# Count how many Realty projects have Project_Type = 'None' (string)
count_query = """
SELECT COUNT(*) as cnt
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Project_Source = 'Realty'
  AND Project_Type = 'None'
  AND Status NOT IN ('Cancelled', 'Complete', 'Closed', 'On Hold', 'Inactive')
"""
result = list(client.query(count_query).result())[0]
print(f"Realty with Project_Type='None' (truly active): {result.cnt}")

# Now show those
show_query = """
SELECT Project_Type, Initiative_Type, Status, FY
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
WHERE Project_Source = 'Realty'
  AND Project_Type = 'None'
  AND Status NOT IN ('Cancelled', 'Complete', 'Closed', 'On Hold', 'Inactive')
LIMIT 20
"""
print("\nRealty with Project_Type='None' (truly active):")
for i, row in enumerate(client.query(show_query).result(), 1):
    print(f"  {i}. Initiative_Type='{row.Initiative_Type}' | Status='{row.Status}' | FY='{row.FY}'")


print("Checking Realty projects R-1915, R-1563, R-1784...\n")
results = client.query(query).result()

for row in results:
    print(f"Realty_Project_ID: {row.Realty_Project_ID}")
    print(f"  Project_Type: '{row.Project_Type}'")
    print(f"  Initiative_Type: '{row.Initiative_Type}'")
    print(f"  PROJECT_TITLE: '{row.PROJECT_TITLE}'")
    print(f"  Title: '{row.Title}'")
    print(f"  Status: '{row.Status}'")
    print(f"  Is Active: {row.is_active}")
    print()
