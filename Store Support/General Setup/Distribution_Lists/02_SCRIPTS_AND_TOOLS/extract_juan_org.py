import pandas as pd

# Read the CSV
df = pd.read_csv('HNMeeting2_With_Hierarchy_20251219_115704.csv')

# Find Juan's WIN
juan_win = '231759243'

# Filter for people in Juan's org
juan_org = df[
    (df['Manager_WIN'].astype(str) == juan_win) |
    (df['Direct_Manager'].str.contains('Juan Galarraga', na=False)) |
    (df['Director'].str.contains('Juan Galarraga', na=False)) |
    (df['Senior_Director'].str.contains('Juan Galarraga', na=False)) |
    (df['Group_Director'].str.contains('Juan Galarraga', na=False)) |
    (df['VP'].str.contains('Juan Galarraga', na=False)) |
    (df['SVP'].str.contains('Juan Galarraga', na=False)) |
    (df['EVP'].str.contains('Juan Galarraga', na=False)) |
    (df['WIN'].astype(str) == juan_win)
].copy()

# Group by management level
print('='*80)
print('JUAN GALARRAGA ORGANIZATION STRUCTURE')
print('='*80)
print(f'Total people in organization: {len(juan_org)}')
print()

# Show Juan
juan = df[df['WIN'].astype(str) == juan_win].iloc[0]
print(f'SVP: {juan["First_Name"]} {juan["Last_Name"]}')
print(f'     Title: {juan["Job_Title"]}')
print(f'     WIN: {juan_win}')
print(f'     Email: {juan["Email"]}')
print()

# Show VPs reporting to Juan
vps = juan_org[juan_org['Manager_WIN'].astype(str) == juan_win]
print('='*80)
print(f'VPs REPORTING TO JUAN ({len(vps)})')
print('='*80)

for idx, vp in vps.iterrows():
    print(f'\n{vp["First_Name"]} {vp["Last_Name"]}')
    print(f'  Title: {vp["Job_Title"]}')
    print(f'  WIN: {vp["WIN"]}')
    print(f'  Email: {vp["Email"]}')
    
    # Find people under this VP
    vp_name = f'{vp["First_Name"]} {vp["Last_Name"]}'
    vp_directs = juan_org[juan_org['Manager_WIN'].astype(str) == str(vp['WIN'])]
    
    if len(vp_directs) > 0:
        print(f'  Direct Reports ({len(vp_directs)}):')
        for _, dr in vp_directs.iterrows():
            print(f'    - {dr["First_Name"]} {dr["Last_Name"]} ({dr["Job_Title"]})')

print()
print('='*80)
print('SUMMARY BY MANAGEMENT LEVEL')
print('='*80)
level_counts = juan_org['Management_Level'].value_counts()
for level, count in level_counts.items():
    print(f'{level}: {count}')

print()
print('='*80)
print('KEY ROLES')
print('='*80)
# Look for specific keywords in titles
keywords = ['Director', 'Senior Director', 'Vice President', 'Manager', 'Analyst', 'Engineer']
for keyword in keywords:
    matching = juan_org[juan_org['Job_Title'].str.contains(keyword, na=False, case=False)]
    if len(matching) > 0:
        print(f'\n{keyword} roles: {len(matching)}')
        for _, person in matching.head(10).iterrows():
            print(f'  - {person["First_Name"]} {person["Last_Name"]}: {person["Job_Title"]}')
