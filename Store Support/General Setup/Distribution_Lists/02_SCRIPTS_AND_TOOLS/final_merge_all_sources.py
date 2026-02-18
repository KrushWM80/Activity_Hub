"""
Final merge: HNMeeting2 + BIITWI Missing + Four DL exports
Creates the ultimate combined distribution list
"""

import pandas as pd
from datetime import datetime

print("="*80)
print("FINAL MERGE: HNMEETING2 + BIITWI + FOUR DLS")
print("="*80)

# Map the exported files to their DL names
four_dl_files = {
    'exportGroupMembers_2025-12-23.csv': 'HN-MerchTeam',
    'HN-SupplyChaintea - exportGroupMembers_2025-12-23.csv': 'HN-SupplyChainteam',
    'HN-SupportTeam@email.wal-mart.com List.csv': 'HN-SupportTeam',
    'HN-TomWardTeam list.csv': 'HN-TomWardTeam'
}

# Step 1: Load current HNMeeting2 + BIITWI combined file
print("\n1. Loading HNMeeting2 + BIITWI combined data...")
combined_file = 'HNMeeting2_With_BIITWI_And_4DLs_20251223_110038.csv'
base_df = pd.read_csv(combined_file)
print(f"   ✓ Loaded {len(base_df)} members (HNMeeting2 + BIITWI)")

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

# Step 3: Merge everything
print("\n3. Merging all data sources...")

if not four_dls_df.empty:
    all_data = pd.concat([base_df, four_dls_df], ignore_index=True, sort=False)
else:
    all_data = base_df.copy()

print(f"   Total records before deduplication: {len(all_data)}")

# Deduplicate by email (case-insensitive)
all_data['Email_Lower'] = all_data['Email'].str.lower().str.strip()
all_data = all_data.drop_duplicates(subset=['Email_Lower'], keep='first')
all_data = all_data.drop(columns=['Email_Lower'])

print(f"   Unique users after deduplication: {len(all_data)}")

# Sort by email
all_data = all_data.sort_values('Email')

# Step 4: Export final combined file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f'HNMeeting2_FINAL_Combined_{timestamp}.csv'

all_data.to_csv(output_file, index=False)

print(f"\n{'='*80}")
print("FINAL SUMMARY")
print(f"{'='*80}")
print(f"Current HNMeeting2:              1,246")
print(f"BIITWI Missing (to add):           298")
if not four_dls_df.empty:
    print(f"Four DL members:                 {len(four_dls_df)}")
    print(f"After deduplication:             {len(all_data)}")
    print(f"New members from 4 DLs:          {len(all_data) - len(base_df)}")
else:
    print(f"Total unique users:              {len(all_data)}")

print(f"\n✅ FINAL combined file saved to: {output_file}")
print(f"{'='*80}")

# Show source breakdown
print("\nBreakdown by source:")
source_counts = all_data['Source'].value_counts()
for source, count in source_counts.items():
    print(f"  {source:40} {count:>5} members")

# Calculate statistics
print(f"\nStatistics:")
print(f"  Total unique email addresses:    {len(all_data)}")
print(f"  Emails with WIN data:            {all_data['WIN'].notna().sum()}")
print(f"  Emails with Name data:           {all_data['Name'].notna().sum() if 'Name' in all_data.columns else all_data['First_Name'].notna().sum()}")

# Show sample
print(f"\nSample records (first 10):")
print("-"*80)
sample_cols = ['Email', 'Source']
if 'Name' in all_data.columns:
    sample_cols.insert(1, 'Name')
elif 'First_Name' in all_data.columns:
    sample_cols.insert(1, 'First_Name')
    sample_cols.insert(2, 'Last_Name')

available_cols = [col for col in sample_cols if col in all_data.columns]
print(all_data[available_cols].head(10).to_string(index=False))

print(f"\n{'='*80}")
print("✅ PROCESS COMPLETE - READY TO UPDATE DISTRIBUTION LIST")
print(f"{'='*80}")
