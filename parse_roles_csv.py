import pandas as pd
from google.cloud import bigquery
import csv

# First, parse the CSV file
csv_path = r"C:\Users\krush\Downloads\Roles.csv"

# Read the CSV to extract job codes
print("Reading Roles.csv...")
df = pd.read_csv(csv_path, header=0)

# Display the structure
print("\nFile structure:")
print(df.head(10))
print(f"\nColumns: {df.columns.tolist()}")
print(f"Total rows: {len(df)}")

# Extract unique job codes from all columns (except the first column which is Role Type)
job_codes_set = set()
role_type_mapping = {}  # Map job code to role type

for idx, row in df.iterrows():
    role_type = row.iloc[0]  # First column is Role Type (Salary/Hourly)
    
    # Iterate through remaining columns to get job codes
    for col_idx in range(1, len(row)):
        job_code = row.iloc[col_idx]
        if pd.notna(job_code) and job_code.strip() != "":
            job_code = str(job_code).strip()
            job_codes_set.add(job_code)
            if job_code not in role_type_mapping:
                role_type_mapping[job_code] = role_type

# Convert to sorted list
job_codes_list = sorted(list(job_codes_set))

print(f"\n\nTotal unique job codes extracted: {len(job_codes_list)}")
print(f"\nFirst 20 job codes:")
for i, jc in enumerate(job_codes_list[:20], 1):
    print(f"{i}. {jc} ({role_type_mapping.get(jc, 'Unknown')})")
