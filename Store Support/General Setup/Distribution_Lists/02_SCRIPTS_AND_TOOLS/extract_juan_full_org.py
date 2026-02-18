import pandas as pd

df = pd.read_csv('HNMeeting2_With_Hierarchy_20251219_115704.csv')

# Search for Juan in any hierarchy column
juan_matches = df[
    df['SVP'].str.contains('Juan Galarraga', na=False) |
    df['EVP'].str.contains('Juan Galarraga', na=False) |
    df['VP'].str.contains('Juan Galarraga', na=False)
]

print('='*80)
print('FULL JUAN GALARRAGA ORGANIZATION')
print('='*80)
print(f'Total people with Juan Galarraga in their reporting chain: {len(juan_matches)}')
print()

# Show management levels
print('Management Level Distribution:')
level_counts = juan_matches['Management_Level'].value_counts().sort_index()
for level, count in level_counts.items():
    print(f'  {level}: {count} people')
print()

# Show VPs
print('='*80)
print('VPs IN ORGANIZATION')
print('='*80)
vps = juan_matches[juan_matches['Management_Level'] == 'C'].copy()
print(f'Total VPs: {len(vps)}\n')
for _, vp in vps.iterrows():
    name = f"{vp['First_Name']} {vp['Last_Name']}"
    print(f'{name}')
    print(f'  Title: {vp["Job_Title"]}')
    print(f'  Email: {vp["Email"]}')
    print()

# Show Senior Directors
print('='*80)
print('SENIOR DIRECTORS IN ORGANIZATION')
print('='*80)
sds = juan_matches[juan_matches['Management_Level'] == 'D'].copy()
print(f'Total Senior Directors: {len(sds)}\n')
for _, sd in sds.head(50).iterrows():
    name = f"{sd['First_Name']} {sd['Last_Name']}"
    print(f'{name}')
    print(f'  Title: {sd["Job_Title"]}')
    print(f'  Reports to VP: {sd["VP"]}')
    print()

# Show Directors
print('='*80)
print('DIRECTORS IN ORGANIZATION (Sample)')
print('='*80)
directors = juan_matches[juan_matches['Management_Level'] == 'E'].copy()
print(f'Total Directors: {len(directors)}\n')
for _, d in directors.head(30).iterrows():
    name = f"{d['First_Name']} {d['Last_Name']}"
    print(f'{name}')
    print(f'  Title: {d["Job_Title"]}')
    print(f'  Reports to: {d["Senior_Director"]}')
    print()

# Show summary statistics
print('='*80)
print('ORGANIZATION SUMMARY')
print('='*80)
print(f'Total Headcount: {len(juan_matches)}')
print(f'VPs: {len(vps)}')
print(f'Senior Directors: {len(sds)}')
print(f'Directors: {len(directors)}')
print(f'Managers & ICs: {len(juan_matches) - len(vps) - len(sds) - len(directors)}')
