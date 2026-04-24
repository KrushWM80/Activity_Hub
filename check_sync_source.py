from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

print("=" * 80)
print("SOURCE: Output - Intake Accel Council Data (Project 18049)")
print("=" * 80)

# Check what's in the Intake source for card 18049
sql_source = """
SELECT *
FROM `wmt-assetprotection-prod.Store_Support_Dev.`Output - Intake Accel Council Data``
WHERE Intake_Card_Nbr = 18049
"""

try:
    results = list(client.query(sql_source).result())
    
    if results:
        row = results[0]
        print("\n✓ Found in Source!\n")
        
        # Get all field names and values
        fields = row.keys()
        for field in sorted(fields):
            value = getattr(row, field, 'N/A')
            value_display = str(value)[:100] if value is not None else 'NULL'
            print(f"  {field}: {value_display}")
    else:
        print("\n✗ Project 18049 NOT found in source Intake data")
        
        # Show a sample of what's in the table
        print("\n\nSample projects in source (first 5):\n")
        sql_sample = """
        SELECT 
            Intake_Card_Nbr,
            Project_Name,
            Project_Lead,
            Store_Area
        FROM `wmt-assetprotection-prod.Store_Support_Dev.`Output - Intake Accel Council Data``
        LIMIT 5
        """
        
        sample_results = list(client.query(sql_sample).result())
        for r in sample_results:
            print(f"  Card {r.Intake_Card_Nbr}: {r.Project_Name} (Lead: {r.Project_Lead})")

except Exception as e:
    print(f"\n✗ Error querying source: {str(e)}")

# Now show the current AH_Projects state
print("\n\n" + "=" * 80)
print("CURRENT: AH_Projects Table (Project 18049)")
print("=" * 80 + "\n")

sql_ah = """
SELECT *
FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
WHERE project_id = '18049'
"""

results_ah = list(client.query(sql_ah).result())
if results_ah:
    row = results_ah[0]
    fields = row.keys()
    
    print("Current AH_Projects state:\n")
    for field in sorted(fields):
        value = getattr(row, field, 'N/A')
        value_display = str(value)[:100] if value is not None else 'NULL'
        is_null = "← MISSING" if value is None or value == '' else ""
        print(f"  {field}: {value_display} {is_null}")

print("\n\n" + "=" * 80)
print("DIAGNOSIS")
print("=" * 80)
print("""
The sync process works as follows:
1. Reads from 'Output - Intake Accel Council Data' table
2. Maps columns: Intake_Card_Nbr → project_id
3. Creates or updates rows in AH_Projects

Issues causing invisibility:
- If business_organization is empty → filtered out by API (WHERE business_organization != '')
- If title is NULL → cannot display properly
- If owner is NULL → not shown under owner filter

Solution: Either:
A) Fix the source data in 'Output - Intake Accel Council Data'
B) Manually populate the missing fields in AH_Projects (18049)
C) Run sync again if source was recently updated
""")
