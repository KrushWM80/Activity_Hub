"""Investigate Phase vs Facility_Phase in BQ table"""
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'
from google.cloud import bigquery
client = bigquery.Client(project='wmt-assetprotection-prod')
P = 'wmt-assetprotection-prod'
D = 'Store_Support_Dev'
T = 'Output- TDA Report'

print("=== 1. ALL COLUMNS IN TABLE ===")
q1 = f"SELECT column_name, data_type FROM `{P}.{D}.INFORMATION_SCHEMA.COLUMNS` WHERE table_name = 'Output- TDA Report' ORDER BY ordinal_position"
for r in client.query(q1).result():
    print(f"  {r.column_name}: {r.data_type}")

print("\n=== 2. DISTINCT Facility_Phase VALUES ===")
q2 = f"SELECT DISTINCT Facility_Phase FROM `{P}.{D}.{T}` ORDER BY Facility_Phase"
for r in client.query(q2).result():
    print(f"  '{r.Facility_Phase}'")

print("\n=== 3. Phase vs Facility_Phase cross-tab ===")
q3 = f"SELECT Phase, Facility_Phase, COUNT(*) as cnt, SUM(Facility) as sum_fac FROM `{P}.{D}.{T}` WHERE Topic IS NOT NULL GROUP BY Phase, Facility_Phase ORDER BY Phase, Facility_Phase"
for r in client.query(q3).result():
    print(f"  Phase={str(r.Phase):<15} Facility_Phase={str(r.Facility_Phase):<15} Rows={r.cnt:<5} SUM(Facility)={r.sum_fac}")

print("\n=== 4. 3rd Party Cut Fruit Test - ALL ROWS ===")
q4 = f"SELECT Topic, Phase, Facility_Phase, Facility, Health_Update FROM `{P}.{D}.{T}` WHERE Topic = '3rd Party Cut Fruit Test'"
for r in client.query(q4).result():
    print(f"  Phase={r.Phase}, Facility_Phase={r.Facility_Phase}, Facility={r.Facility}, Health={r.Health_Update}")

print("\n=== 5. Topics where Phase != Facility_Phase (mismatches) ===")
q5 = f"SELECT DISTINCT Topic, Phase, Facility_Phase FROM `{P}.{D}.{T}` WHERE Topic IS NOT NULL AND Phase != Facility_Phase AND Facility_Phase != 'No List' ORDER BY Topic"
for r in client.query(q5).result():
    print(f"  {str(r.Topic):<50} Phase={str(r.Phase):<15} Facility_Phase={r.Facility_Phase}")

print("\n=== 6. Store count comparison: current (SUM all) vs correct (SUM where Facility_Phase=Phase) ===")
q6 = f"""SELECT Topic, Phase,
    SUM(Facility) as current_sum_all,
    SUM(CASE WHEN Facility_Phase = Phase THEN Facility ELSE 0 END) as correct_sum_matching
FROM `{P}.{D}.{T}` WHERE Topic IS NOT NULL
GROUP BY Topic, Phase
HAVING SUM(Facility) != SUM(CASE WHEN Facility_Phase = Phase THEN Facility ELSE 0 END)
ORDER BY Topic"""
for r in client.query(q6).result():
    print(f"  {str(r.Topic):<50} Phase={str(r.Phase):<15} Current={r.current_sum_all:<8} Correct={r.correct_sum_matching}")

print("\nDone!")
