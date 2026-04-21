"""Convert CSV worker data to JSON for frontend"""
import pandas as pd
import json
import os

csv_file = r'c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\Worker_Names_Stores_Missing_JobCodes.csv'
json_file = r'c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\Worker_Names_Stores_Missing_JobCodes.json'

# Convert CSV to JSON  
df = pd.read_csv(csv_file)
data = df.to_dict('records')

with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f'✓ JSON file created successfully')
print(f'  Location: {json_file}')
print(f'  Total records: {len(data):,}')
print(f'  File size: {os.path.getsize(json_file) / 1024 / 1024:.1f} MB')
print()
print('Sample worker records:')
for i, r in enumerate(data[:3]):
    print(f'  {i+1}. {r["first_name"]} {r["last_name"]} - Store #{r["store_number"]} - {r["job_code"]}')
