import pandas as pd

# Read TMS and export
tms = pd.read_excel("Teaming/TMS Data (3).xlsx", sheet_name='data')
export = pd.read_csv("teaming_all_actions_2026-04-27_with_roles.csv")

# Find unknowns
unknowns = export[export['roleTitle'] == 'Unknown']

print(f"UNKNOWN JOB CODES ({len(unknowns)} records):\n")
print("jobCode  | Full Job Code  | Workgroup         | Team")
print("-" * 60)
for _, row in unknowns[['jobCode', 'full_job_code', 'workgroupName', 'teamName']].drop_duplicates().iterrows():
    print(f"{row['jobCode']:>7} | {row['full_job_code']:>13} | {str(row['workgroupName'])[:16]:>16} | {row['teamName']}")

print(f"\n\nTMS DATA AVAILABLE JOB CODES BY TEAM:\n")
teams = tms.groupby('teamName')['jobCode'].nunique()
print(teams.to_string())

print(f"\n\nALL TMS JOB CODES ({len(tms['jobCode'].unique())} unique):")
print(sorted(tms['jobCode'].unique()))
