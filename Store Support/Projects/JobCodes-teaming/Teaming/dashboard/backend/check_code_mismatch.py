import sqlite3
import json

db_path = r"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend\cache\jobcodes_cache.db"
json_path = r"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\job_codes_master.json"

# Get sample Polaris codes
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT job_code FROM polaris_job_codes LIMIT 10")
polaris_samples = [row[0] for row in cursor.fetchall()]
print("Sample Polaris job codes:")
for code in polaris_samples:
    print(f"  {code}")

conn.close()

# Get sample Excel codes
with open(json_path, 'r', encoding='utf-8') as f:
    json_data = json.load(f)
    print(f"\nSample Excel 'SMART Job Code' values:")
    for record in json_data['job_codes'][:10]:
        smart_code = record.get('SMART Job Code', 'N/A')
        print(f"  {smart_code}")

print(f"\nTotal Polaris codes: 271")
print(f"Total Excel codes in JSON: {len(json_data['job_codes'])}")
print(f"Successfully synced: 10")
print(f"Match percentage: {(10/271)*100:.1f}%")

# Check if the Workday codes match
print(f"\nChecking Workday Job Code format...")
for record in json_data['job_codes'][:5]:
    print(f"  SMART: {record.get('SMART Job Code')} -> Workday: {record.get('Workday Job Code')}")
