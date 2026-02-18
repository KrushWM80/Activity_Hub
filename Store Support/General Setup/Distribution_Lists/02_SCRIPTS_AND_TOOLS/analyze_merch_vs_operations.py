"""
Analyze job codes and titles to identify Merchandising vs Operations teams
"""

import pandas as pd

print("="*80)
print("ANALYZING JOB CODES: MERCHANDISING VS OPERATIONS")
print("="*80)

# Load the enriched data with job codes and titles
file_path = 'HNMeeting2_Missing_Members_20251219_122841.csv'
df = pd.read_csv(file_path)

print(f"\nTotal records with job data: {len(df)}")

# Analyze Job Titles
print("\n" + "="*80)
print("ANALYSIS BY JOB TITLE")
print("="*80)

# Find Merchandising roles
merch_keywords = ['Merchandising', 'Merch', 'Buyer', 'Category', 'Merchant']
df['Is_Merchandising'] = df['Job_Title'].str.contains('|'.join(merch_keywords), case=False, na=False)

# Find Operations roles
ops_keywords = ['Operations', 'Supply Chain', 'Logistics', 'Distribution', 'Fulfillment', 'Store']
df['Is_Operations'] = df['Job_Title'].str.contains('|'.join(ops_keywords), case=False, na=False)

merch_count = df['Is_Merchandising'].sum()
ops_count = df['Is_Operations'].sum()
both_count = (df['Is_Merchandising'] & df['Is_Operations']).sum()
neither_count = len(df) - df['Is_Merchandising'].sum() - ops_count + both_count

print(f"\nBy Job Title:")
print(f"  Merchandising roles:        {merch_count}")
print(f"  Operations roles:           {ops_count}")
print(f"  Both keywords:              {both_count}")
print(f"  Neither (Other):            {neither_count}")

# Analyze Job Codes
print("\n" + "="*80)
print("ANALYSIS BY JOB CODE")
print("="*80)

# Common Merchandising job codes
merchandising_codes = [
    'US-100017446',  # Senior Director, Merchandising
    'US-100019721',  # Senior Director, Merchandising Operations
]

# Common Operations job codes  
operations_codes = [
    'US-100020695',  # Senior Director, Operations
    'US-100024103',  # Senior Director, Technology Operations
    'US-100015099',  # Market Manager (Operations)
]

df['Merch_By_Code'] = df['Job_Code'].isin(merchandising_codes)
df['Ops_By_Code'] = df['Job_Code'].isin(operations_codes)

print(f"\nBy Known Job Codes:")
print(f"  Merchandising codes:        {df['Merch_By_Code'].sum()}")
print(f"  Operations codes:           {df['Ops_By_Code'].sum()}")

# Show top job codes
print("\n" + "="*80)
print("TOP JOB CODES IN DATA")
print("="*80)
top_codes = df.groupby(['Job_Code', 'Job_Title']).size().reset_index(name='Count')
top_codes = top_codes.sort_values('Count', ascending=False).head(15)

print(f"\n{'Job Code':<20} {'Count':>6}  Job Title")
print("-"*80)
for _, row in top_codes.iterrows():
    title = row['Job_Title'][:50] if pd.notna(row['Job_Title']) else 'N/A'
    print(f"{row['Job_Code']:<20} {row['Count']:>6}  {title}")

# Show Merchandising examples
print("\n" + "="*80)
print("MERCHANDISING EXAMPLES")
print("="*80)
merch_examples = df[df['Is_Merchandising']].head(10)[['Email', 'Job_Code', 'Job_Title']]
print(merch_examples.to_string(index=False))

# Show Operations examples
print("\n" + "="*80)
print("OPERATIONS EXAMPLES")
print("="*80)
ops_examples = df[df['Is_Operations']].head(10)[['Email', 'Job_Code', 'Job_Title']]
print(ops_examples.to_string(index=False))

# Export classifications
df['Team_Classification'] = 'Other'
df.loc[df['Is_Merchandising'], 'Team_Classification'] = 'Merchandising'
df.loc[df['Is_Operations'], 'Team_Classification'] = 'Operations'
df.loc[df['Is_Merchandising'] & df['Is_Operations'], 'Team_Classification'] = 'Merch Operations'

output_file = 'HNMeeting2_With_Team_Classification.csv'
df.to_csv(output_file, index=False)

print(f"\n✅ Classification saved to: {output_file}")

# Summary
print("\n" + "="*80)
print("TEAM CLASSIFICATION SUMMARY")
print("="*80)
team_counts = df['Team_Classification'].value_counts()
for team, count in team_counts.items():
    print(f"  {team:<20} {count:>5} members")

print("\n" + "="*80)
print("KEY IDENTIFIERS")
print("="*80)
print("\n📊 MERCHANDISING Indicators:")
print("  - Job Codes: US-100017446, US-100019721")
print("  - Keywords in Title: 'Merchandising', 'Merch', 'Buyer', 'Category'")
print("  - Common titles: Senior Director Merchandising, Buyer, Category Manager")

print("\n📊 OPERATIONS Indicators:")
print("  - Job Codes: US-100020695, US-100024103, US-100015099")
print("  - Keywords in Title: 'Operations', 'Supply Chain', 'Logistics', 'Distribution'")
print("  - Common titles: Senior Director Operations, Market Manager, Supply Chain")

print("="*80)
