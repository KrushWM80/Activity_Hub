"""Investigate store count (SUM vs COUNT) and Test phase discrepancy"""
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

from google.cloud import bigquery
client = bigquery.Client(project='wmt-assetprotection-prod')

PROJECT = 'wmt-assetprotection-prod'
DATASET = 'Store_Support_Dev'
TABLE = 'Output- TDA Report'

print("=" * 80)
print("1. RAW FACILITY VALUES FOR 'Body Worn Cameras'")
print("=" * 80)
q1 = f"""
SELECT Topic, Facility, Phase, Health_Update
FROM `{PROJECT}.{DATASET}.{TABLE}`
WHERE Topic = 'Body Worn Cameras'
ORDER BY Facility
"""
for row in client.query(q1).result():
    print(f"  Facility={row.Facility}, Phase={row.Phase}, Health={row.Health_Update}")

print("\n" + "=" * 80)
print("2. COMPARE COUNT(DISTINCT) vs SUM vs COUNT(*) for ALL topics")
print("=" * 80)
q2 = f"""
SELECT 
    Topic,
    Phase,
    Health_Update,
    COUNT(*) as row_count,
    COUNT(DISTINCT Facility) as distinct_facilities,
    SUM(CAST(Facility AS INT64)) as sum_facility,
    MIN(Facility) as min_fac,
    MAX(Facility) as max_fac
FROM `{PROJECT}.{DATASET}.{TABLE}`
WHERE Topic IS NOT NULL
GROUP BY Topic, Phase, Health_Update
ORDER BY Topic
"""
print(f"{'Topic':<45} {'Phase':<12} {'Rows':>5} {'DISTINCT':>8} {'SUM':>8} {'Min':>6} {'Max':>6}")
print("-" * 100)
for row in client.query(q2).result():
    print(f"{str(row.Topic)[:44]:<45} {str(row.Phase):<12} {row.row_count:>5} {row.distinct_facilities:>8} {row.sum_facility or 'NULL':>8} {row.min_fac or 'N/A':>6} {row.max_fac or 'N/A':>6}")

print("\n" + "=" * 80)
print("3. FACILITY COLUMN DATA TYPE")
print("=" * 80)
q3 = f"""
SELECT column_name, data_type 
FROM `{PROJECT}.{DATASET}.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'Output- TDA Report' AND column_name = 'Facility'
"""
for row in client.query(q3).result():
    print(f"  Column: {row.column_name}, Type: {row.data_type}")

print("\n" + "=" * 80)
print("4. SAMPLE FACILITY VALUES (first 20 raw rows)")
print("=" * 80)
q4 = f"""
SELECT Topic, Facility
FROM `{PROJECT}.{DATASET}.{TABLE}`
WHERE Facility IS NOT NULL
ORDER BY Topic
LIMIT 20
"""
for row in client.query(q4).result():
    print(f"  Topic={row.Topic}, Facility={row.Facility}")

print("\n" + "=" * 80)
print("5. TEST PHASE - ALL TOPICS")
print("=" * 80)
q5 = f"""
SELECT 
    Topic,
    Health_Update,
    COUNT(*) as rows,
    COUNT(DISTINCT Facility) as distinct_fac,
    SUM(SAFE_CAST(Facility AS INT64)) as sum_fac
FROM `{PROJECT}.{DATASET}.{TABLE}`
WHERE Phase = 'Test' AND Topic IS NOT NULL
GROUP BY Topic, Health_Update
ORDER BY Topic
"""
for row in client.query(q5).result():
    print(f"  {row.Topic:<45} Health={row.Health_Update:<12} Rows={row.rows} Distinct={row.distinct_fac} Sum={row.sum_fac}")

print("\n" + "=" * 80)
print("6. CHECKOUT ANYWHERE - FULL DETAIL")
print("=" * 80)
q6 = f"""
SELECT *
FROM `{PROJECT}.{DATASET}.{TABLE}`
WHERE Topic = 'Checkout Anywhere'
"""
for row in client.query(q6).result():
    print(f"  Phase={row.Phase}, Health={row.Health_Update}, Facility={row.Facility}")
    print(f"  Dallas_POC={str(row.Dallas_POC)[:60]}")
    print(f"  Intake_n_Testing={str(row.Intake_n_Testing)[:60]}")
    print(f"  Deployment={str(row.Deployment)[:60]}")

print("\n" + "=" * 80)
print("7. ALL COLUMNS IN TABLE")
print("=" * 80)
q7 = f"""
SELECT column_name, data_type
FROM `{PROJECT}.{DATASET}.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'Output- TDA Report'
ORDER BY ordinal_position
"""
for row in client.query(q7).result():
    print(f"  {row.column_name}: {row.data_type}")

print("\nDone!")
