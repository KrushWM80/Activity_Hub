"""
Identify the 308 people from BIITWI Audience who are NOT on current HNMeeting2
Then combine: Current HNMeeting2 + 308 Missing + 4 Other DLs
"""

import pandas as pd
from datetime import datetime

print("="*80)
print("COMBINING HNMEETING2 WITH BIITWI AUDIENCE AND FOUR OTHER DLS")
print("="*80)

# Step 1: Load BIITWI Audience (655 people)
print("\n1. Loading BIITWI Audience...")
biitwi_file = r"C:\Users\krush\Documents\BIITWI Audience.csv"
biitwi_df = pd.read_csv(biitwi_file)
# Normalize email column name
if 'Email' not in biitwi_df.columns and len(biitwi_df.columns) == 1:
    biitwi_df.columns = ['Email']

# Remove distribution list emails (like AllAPStoreMAPMs@email.wal-mart.com)
biitwi_df = biitwi_df[~biitwi_df['Email'].str.contains('@email.wal-mart.com', na=False)]
print(f"   ✓ Loaded {len(biitwi_df)} individual emails from BIITWI Audience")

# Step 2: Load current HNMeeting2 members
print("\n2. Loading current HNMeeting2 members...")
current_members_file = 'HNMeeting2_Members_Final_20251219_112826.csv'
current_df = pd.read_csv(current_members_file)
print(f"   ✓ Loaded {len(current_df)} current HNMeeting2 members")

# Step 3: Find who from BIITWI is NOT on HNMeeting2
print("\n3. Comparing BIITWI Audience to current HNMeeting2...")

# Normalize emails for comparison (lowercase)
biitwi_df['Email_Lower'] = biitwi_df['Email'].str.lower().str.strip()
current_df['Email_Lower'] = current_df['Email'].str.lower().str.strip()

# Find missing
missing_from_hnmeeting2 = biitwi_df[~biitwi_df['Email_Lower'].isin(current_df['Email_Lower'])].copy()
print(f"   ✓ Found {len(missing_from_hnmeeting2)} people from BIITWI NOT on HNMeeting2")

# Verify this is around 308
if abs(len(missing_from_hnmeeting2) - 308) > 50:
    print(f"   ⚠ WARNING: Expected ~308 missing, but found {len(missing_from_hnmeeting2)}")
else:
    print(f"   ✅ Count matches expectation (~308)")

# Clean up the missing list
missing_from_hnmeeting2 = missing_from_hnmeeting2.drop(columns=['Email_Lower'])
missing_from_hnmeeting2['Source'] = 'BIITWI Audience (Not on HNMeeting2)'

# Step 4: Prepare current members
current_prepared = current_df.drop(columns=['Email_Lower'])
current_prepared['Source'] = 'Current HNMeeting2'

# Step 5: Check if we have the four DL extracts
print("\n4. Checking for four DL extracts...")
import glob
import os

four_dl_files = glob.glob('Four_DL_Members_*.csv')

if four_dl_files:
    four_dl_file = max(four_dl_files, key=os.path.getctime)
    print(f"   ✓ Found: {four_dl_file}")
    four_dl_df = pd.read_csv(four_dl_file)
    four_dl_df = four_dl_df.rename(columns={'Source_DL': 'Source'})
    print(f"   ✓ Loaded {len(four_dl_df)} members from four DLs")
else:
    print("   ⚠ No Four_DL_Members file found - will skip for now")
    print("   Run Extract-Four-DL-Members.ps1 first, then re-run this script")
    four_dl_df = pd.DataFrame()

# Step 6: Combine all sources
print("\n5. Combining all sources...")

dfs_to_combine = [current_prepared, missing_from_hnmeeting2]
if not four_dl_df.empty:
    dfs_to_combine.append(four_dl_df)

combined_df = pd.concat(dfs_to_combine, ignore_index=True, sort=False)

print(f"   Total records before deduplication: {len(combined_df)}")

# Deduplicate by email
combined_df['Email_Lower'] = combined_df['Email'].str.lower().str.strip()
combined_df = combined_df.drop_duplicates(subset=['Email_Lower'], keep='first')
combined_df = combined_df.drop(columns=['Email_Lower'])

print(f"   Unique users after deduplication: {len(combined_df)}")

# Sort by email
combined_df = combined_df.sort_values('Email')

# Step 7: Export results
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Export the 308 missing separately for review
missing_output = f'BIITWI_Missing_From_HNMeeting2_{timestamp}.csv'
missing_from_hnmeeting2.to_csv(missing_output, index=False)

# Export final combined
combined_output = f'HNMeeting2_With_BIITWI_And_4DLs_{timestamp}.csv'
combined_df.to_csv(combined_output, index=False)

print(f"\n{'='*80}")
print("FINAL SUMMARY")
print(f"{'='*80}")
print(f"Current HNMeeting2 members:     {len(current_prepared)}")
print(f"BIITWI missing from HNMeeting2: {len(missing_from_hnmeeting2)}")
if not four_dl_df.empty:
    print(f"Members from four DLs:          {len(four_dl_df)}")
print(f"Final unique users:             {len(combined_df)}")
print(f"\n✅ Missing BIITWI members saved to: {missing_output}")
print(f"✅ Final combined file saved to: {combined_output}")
print(f"{'='*80}")

# Show source breakdown
print("\nBreakdown by source:")
source_counts = combined_df['Source'].value_counts()
for source, count in source_counts.items():
    print(f"  {source}: {count}")

# Show sample from missing BIITWI
print(f"\nSample of BIITWI members NOT on HNMeeting2 (first 15):")
print("-"*80)
print(missing_from_hnmeeting2[['Email', 'Source']].head(15).to_string(index=False))
