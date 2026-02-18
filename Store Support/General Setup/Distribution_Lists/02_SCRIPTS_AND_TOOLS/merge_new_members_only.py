"""
Merge ONLY: 298 BIITWI Missing + Four DL exports
This creates a list of NEW people to ADD to HNMeeting2
(Does NOT include current HNMeeting2 members)
"""

import pandas as pd
from datetime import datetime

print("="*80)
print("MERGING NEW MEMBERS ONLY: BIITWI MISSING + FOUR DLS")
print("="*80)

# Map the exported files to their DL names
four_dl_files = {
    'exportGroupMembers_2025-12-23.csv': 'HN-MerchTeam',
    'HN-SupplyChaintea - exportGroupMembers_2025-12-23.csv': 'HN-SupplyChainteam',
    'HN-SupportTeam@email.wal-mart.com List.csv': 'HN-SupportTeam',
    'HN-TomWardTeam list.csv': 'HN-TomWardTeam'
}

# Step 1: Load the 298 BIITWI missing members
print("\n1. Loading BIITWI members NOT on HNMeeting2...")
biitwi_missing_file = 'BIITWI_Missing_From_HNMeeting2_20251223_110038.csv'
biitwi_df = pd.read_csv(biitwi_missing_file)
print(f"   ✓ Loaded {len(biitwi_df)} BIITWI members to add")

# Step 2: Load and combine the four DL exports
print("\n2. Loading four distribution list exports...")
all_dl_members = []

for filename, dl_name in four_dl_files.items():
    try:
        df = pd.read_csv(filename)
        # Extract email and displayName
        if 'mail' in df.columns:
            df_subset = df[['mail', 'displayName']].copy()
            df_subset.columns = ['Email', 'Name']
            df_subset['Source'] = dl_name
            all_dl_members.append(df_subset)
            print(f"   ✓ {dl_name}: {len(df_subset)} members")
        else:
            print(f"   ⚠ {dl_name}: No 'mail' column found")
    except Exception as e:
        print(f"   ❌ {dl_name}: Error loading - {str(e)}")

# Combine all four DL dataframes
if all_dl_members:
    four_dls_df = pd.concat(all_dl_members, ignore_index=True)
    print(f"\n   Total from four DLs: {len(four_dls_df)}")
else:
    print(f"\n   ⚠ No DL members loaded")
    four_dls_df = pd.DataFrame()

# Step 3: Merge BIITWI missing + Four DLs
print("\n3. Merging BIITWI missing + Four DLs...")

all_data = pd.concat([biitwi_df, four_dls_df], ignore_index=True, sort=False)

print(f"   Total records before deduplication: {len(all_data)}")

# Deduplicate by email (case-insensitive)
all_data['Email_Lower'] = all_data['Email'].str.lower().str.strip()
all_data = all_data.drop_duplicates(subset=['Email_Lower'], keep='first')
all_data = all_data.drop(columns=['Email_Lower'])

print(f"   Unique users after deduplication: {len(all_data)}")

# Sort by email
all_data = all_data.sort_values('Email')

# Step 4: Export final list of NEW members to add
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f'HNMeeting2_NEW_Members_To_Add_{timestamp}.csv'

all_data.to_csv(output_file, index=False)

print(f"\n{'='*80}")
print("FINAL SUMMARY - NEW MEMBERS TO ADD TO HNMEETING2")
print(f"{'='*80}")
print(f"BIITWI Missing:                  {len(biitwi_df)}")
print(f"Four DL members:                 {len(four_dls_df)}")
print(f"Total before deduplication:      {len(biitwi_df) + len(four_dls_df)}")
print(f"Unique NEW members to add:       {len(all_data)}")
print(f"Duplicates removed:              {len(biitwi_df) + len(four_dls_df) - len(all_data)}")

print(f"\n✅ NEW members list saved to: {output_file}")
print(f"{'='*80}")

# Show source breakdown
print("\nBreakdown by source:")
source_counts = all_data['Source'].value_counts()
for source, count in source_counts.items():
    print(f"  {source:40} {count:>5} members")

# Show sample
print(f"\nSample of NEW members to add (first 15):")
print("-"*80)
sample_cols = ['Email', 'Source']
if 'Name' in all_data.columns:
    sample_cols.insert(1, 'Name')

available_cols = [col for col in sample_cols if col in all_data.columns]
print(all_data[available_cols].head(15).to_string(index=False))

print(f"\n{'='*80}")
print("✅ READY TO ADD THESE MEMBERS TO HNMEETING2")
print(f"{'='*80}")
