#!/usr/bin/env python3
"""
Check if 5 source projects are marked as duplicates or have data issues
"""

from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

missing_ids = [11466, 13767, 14798, 17919, 18056]

id_list = ','.join([str(pid) for pid in missing_ids])

query = f"""
SELECT 
    Intake_Card_Nbr,
    Project_Title,
    Project_Update_Date,
    Is_Duplicate_Row,
    ROW_NUMBER() OVER (PARTITION BY Intake_Card_Nbr ORDER BY Project_Update_Date DESC) as rn
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
WHERE Intake_Card_Nbr IN ({id_list})
ORDER BY Intake_Card_Nbr, Project_Update_Date DESC
"""

results = list(client.query(query).result())

print("\n" + "="*80)
print("SOURCE DATA FOR 5 'MISSING' PROJECTS")
print("="*80)

for row in results:
    dup = "✅ NO" if row.Is_Duplicate_Row != 'Yes' else "❌ YES (DUPLICATE)"
    rn = "✅ Selected" if row.rn == 1 else f"⚠️ Row #{row.rn}"
    date_val = row.Project_Update_Date if row.Project_Update_Date else "NULL"
    print(f"\n{row.Intake_Card_Nbr:6} | {row.Project_Title[:45]:45}")
    print(f"    Date: {date_val} | Duplicate: {dup} | {rn}")

print("\n" + "="*80)
