import pandas as pd

# Read master and export
master = pd.read_excel("Job Codes/Job_Code_Master_Table.xlsx")
export = pd.read_csv("teaming_all_actions_2026-04-27.csv")

print("MASTER SAMPLE (first 3):")
print(master[['SMART Job Code', 'Job Title']].head(3).to_string())

print("\n\nEXPORT SAMPLE (first 3):")
print(export[['jobCode', 'full_job_code', 'teamName']].head(3).to_string())

print("\n\nTRYING TO MATCH:")
print("Export full_job_code '1-10-101' matches master SMART Job Code?")
matches = master[master['SMART Job Code'] == '1-10-101']
print(matches[['SMART Job Code', 'Job Title']].to_string() if len(matches) > 0 else "No match found")

print("\n\nAll unique master SMART Job Codes (first 20):")
print(master['SMART Job Code'].unique()[:20])

print("\n\nAll unique export full_job_codes (first 20):")
print(export['full_job_code'].unique()[:20])
