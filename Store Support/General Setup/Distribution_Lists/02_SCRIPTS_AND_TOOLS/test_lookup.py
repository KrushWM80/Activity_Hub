import pandas as pd

# Load the exportGroupMembers file
df = pd.read_csv('exportGroupMembers_2025-12-23.csv')
print(f'Total members in group: {len(df)}')
print(f'Columns: {df.columns.tolist()}\n')

# Test emails
emails = [
    'crystal.mcdonagh@wal-mart.com', 
    'scott.lukomske@wal-mart.com', 
    'yasmin.tooley@wal-mart.com', 
    'nicolas.cordero@wal-mart.com', 
    'nathan.schmidt0@wal-mart.com'
]

print("=" * 80)
print("SEARCH RESULTS")
print("=" * 80)

for email in emails:
    username = email.split('@')[0]
    result = df[df['mail'].str.contains(username, case=False, na=False)]
    
    print(f'\nSearching for: {email}')
    print(f'Found: {len(result)} match(es)')
    
    if len(result) > 0:
        for idx, row in result.iterrows():
            print(f'  Name: {row["displayName"]}')
            print(f'  Email: {row["mail"]}')
            print(f'  User ID: {row["id"]}')
