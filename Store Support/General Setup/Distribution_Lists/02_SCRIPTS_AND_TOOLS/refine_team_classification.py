"""
Refine team classification using manager hierarchy for mixed roles
"""

import pandas as pd
import numpy as np

print("="*80)
print("REFINING TEAM CLASSIFICATION USING MANAGER HIERARCHY")
print("="*80)

# Load the classified data
df = pd.read_csv('HNMeeting2_With_Team_Classification.csv')

print(f"\nTotal records: {len(df)}")
print(f"Mixed 'Merch Operations' roles to resolve: {(df['Team_Classification'] == 'Merch Operations').sum()}")

# Create a mapping of WIN to Team Classification
win_to_team = df.set_index('WIN')['Team_Classification'].to_dict()

# Function to determine team from manager hierarchy
def determine_team_from_manager(row):
    """Look up manager's team to help classify mixed roles"""
    if pd.notna(row['Manager_WIN']) and row['Manager_WIN'] in win_to_team:
        return win_to_team[row['Manager_WIN']]
    return None

# Analyze mixed roles
print("\n" + "="*80)
print("ANALYZING MIXED 'MERCH OPERATIONS' ROLES")
print("="*80)

mixed_roles = df[df['Team_Classification'] == 'Merch Operations'].copy()
print(f"\nFound {len(mixed_roles)} mixed roles:")

if len(mixed_roles) > 0:
    print(f"\n{'Email':<40} {'Job Title':<50} Manager Team")
    print("-"*120)
    
    for _, row in mixed_roles.iterrows():
        manager_team = determine_team_from_manager(row)
        email = row['Email'][:39]
        title = row['Job_Title'][:49] if pd.notna(row['Job_Title']) else 'N/A'
        mgr_team = manager_team if manager_team else 'Unknown'
        print(f"{email:<40} {title:<50} {mgr_team}")

# Refine classification
print("\n" + "="*80)
print("REFINING CLASSIFICATIONS")
print("="*80)

df['Refined_Team'] = df['Team_Classification'].copy()

# For mixed roles, try to determine from context
for idx, row in df[df['Team_Classification'] == 'Merch Operations'].iterrows():
    title = str(row['Job_Title']).lower() if pd.notna(row['Job_Title']) else ''
    manager_team = determine_team_from_manager(row)
    
    # Logic to determine team:
    # 1. If manager is clearly Merch or Ops, follow manager
    if manager_team in ['Merchandising', 'Operations']:
        df.at[idx, 'Refined_Team'] = manager_team
        df.at[idx, 'Refinement_Reason'] = f'Manager is {manager_team}'
    
    # 2. Look at title weighting - "Merchandising Operations" is Merch-focused
    elif 'merchandising' in title and 'operations' in title:
        # If Merchandising comes first, it's likely Merch
        if title.index('merchandising') < title.index('operations'):
            df.at[idx, 'Refined_Team'] = 'Merchandising'
            df.at[idx, 'Refinement_Reason'] = 'Title: Merchandising (primary)'
        else:
            df.at[idx, 'Refined_Team'] = 'Operations'
            df.at[idx, 'Refinement_Reason'] = 'Title: Operations (primary)'
    
    # 3. If only one keyword is stronger
    elif 'supply chain' in title or 'logistics' in title or 'distribution' in title:
        df.at[idx, 'Refined_Team'] = 'Operations'
        df.at[idx, 'Refinement_Reason'] = 'Supply Chain/Logistics focus'
    
    elif 'buyer' in title or 'category' in title or 'merchant' in title:
        df.at[idx, 'Refined_Team'] = 'Merchandising'
        df.at[idx, 'Refinement_Reason'] = 'Buyer/Category focus'
    
    else:
        # Keep as mixed if can't determine
        df.at[idx, 'Refinement_Reason'] = 'Unable to determine - kept as Merch Operations'

# Fill in refinement reason for non-mixed
df['Refinement_Reason'] = df['Refinement_Reason'].fillna('Original classification')

# Show refinements made
print("\nRefinements made:")
refinements = df[df['Team_Classification'] != df['Refined_Team']]
if len(refinements) > 0:
    print(f"\n{'Email':<40} {'Original':<20} {'Refined':<20} Reason")
    print("-"*120)
    for _, row in refinements.iterrows():
        email = row['Email'][:39]
        print(f"{email:<40} {row['Team_Classification']:<20} {row['Refined_Team']:<20} {row['Refinement_Reason']}")
else:
    print("  No changes made to mixed roles")

# Summary statistics
print("\n" + "="*80)
print("BEFORE vs AFTER REFINEMENT")
print("="*80)

print("\nBEFORE Refinement:")
before_counts = df['Team_Classification'].value_counts()
for team, count in before_counts.items():
    print(f"  {team:<25} {count:>5} members")

print("\nAFTER Refinement:")
after_counts = df['Refined_Team'].value_counts()
for team, count in after_counts.items():
    print(f"  {team:<25} {count:>5} members")

# Export refined classification
output_file = 'HNMeeting2_Refined_Team_Classification.csv'
df.to_csv(output_file, index=False)

print(f"\n✅ Refined classification saved to: {output_file}")

# Create summary for merch-only list
merch_only = df[df['Refined_Team'] == 'Merchandising'].copy()
merch_output = 'HNMeeting2_Merchandising_Team_Only.csv'
merch_only.to_csv(merch_output, index=False)

ops_only = df[df['Refined_Team'] == 'Operations'].copy()
ops_output = 'HNMeeting2_Operations_Team_Only.csv'
ops_only.to_csv(ops_output, index=False)

print(f"✅ Merchandising team only ({len(merch_only)} members): {merch_output}")
print(f"✅ Operations team only ({len(ops_only)} members): {ops_output}")

print("\n" + "="*80)
print("CLASSIFICATION COMPLETE")
print("="*80)
print(f"\n📊 Merchandising Team:    {len(merch_only):>5} members")
print(f"📊 Operations Team:       {len(ops_only):>5} members")
print(f"📊 Other/Tech/Support:    {len(df[df['Refined_Team'] == 'Other']):>5} members")
if len(df[df['Refined_Team'] == 'Merch Operations']) > 0:
    print(f"📊 Still Mixed:           {len(df[df['Refined_Team'] == 'Merch Operations']):>5} members")

print("="*80)
