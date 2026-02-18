from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Check total records
query = """
SELECT COUNT(*) as total
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
"""

print("=== TOTAL RECORDS ===")
for row in client.query(query).result():
    print(f"Total records: {row.total}")

# Check Status values
query2 = """
SELECT Status, COUNT(*) as count
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
GROUP BY Status
ORDER BY count DESC
"""

print("\n=== STATUS BREAKDOWN ===")
for row in client.query(query2).result():
    status_val = repr(row.Status) if row.Status is not None else 'NULL'
    print(f"{status_val}: {row.count}")

# Check Project_Source values
query3 = """
SELECT Project_Source, COUNT(*) as count
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
GROUP BY Project_Source
ORDER BY count DESC
"""

print("\n=== PROJECT SOURCE BREAKDOWN ===")
for row in client.query(query3).result():
    source_val = repr(row.Project_Source) if row.Project_Source is not None else 'NULL'
    print(f"{source_val}: {row.count}")

# Check distinct projects count
query4 = """
SELECT 
    COUNT(DISTINCT Intake_Card) as distinct_projects,
    COUNT(DISTINCT Facility) as distinct_stores,
    COUNT(DISTINCT CASE WHEN Project_Source = 'Operations' THEN Intake_Card END) as operations_projects,
    COUNT(DISTINCT CASE WHEN Project_Source = 'Intake Hub' THEN Intake_Card END) as intake_hub_projects,
    COUNT(DISTINCT CASE WHEN Project_Source = 'Realty' THEN Intake_Card END) as realty_projects
FROM `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data`
"""

print("\n=== DISTINCT COUNTS ===")
for row in client.query(query4).result():
    print(f"Distinct Projects: {row.distinct_projects}")
    print(f"Distinct Stores: {row.distinct_stores}")
    print(f"Operations Projects: {row.operations_projects}")
    print(f"Intake Hub Projects: {row.intake_hub_projects}")
    print(f"Realty Projects: {row.realty_projects}")
