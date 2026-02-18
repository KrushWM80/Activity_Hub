"""
Merge the four extracted DL lists with the combined HNMeeting2 data
Run this AFTER Extract-Four-DL-Members.ps1 has been executed
"""

import pandas as pd
from datetime import datetime
import glob
import os

print("="*80)
print("MERGING FOUR DL MEMBERS WITH HNMEETING2 COMBINED DATA")
print("="*80)

# Step 1: Find the most recent Four_DL_Members CSV
print("\n1. Looking for extracted Four DL Members file...")
four_dl_files = glob.glob('Four_DL_Members_*.csv')

if not four_dl_files:
    print("   ⚠ No Four_DL_Members_*.csv file found!")
    print("   Please run Extract-Four-DL-Members.ps1 first")
    exit(1)

# Get most recent file
four_dl_file = max(four_dl_files, key=os.path.getctime)
print(f"   ✓ Found: {four_dl_file}")

four_dl_df = pd.read_csv(four_dl_file)
print(f"   ✓ Loaded {len(four_dl_df)} members from four DLs")

# Step 2: Find the most recent combined file
print("\n2. Looking for combined HNMeeting2 file...")
combined_files = glob.glob('HNMeeting2_Combined_All_Sources_*.csv')

if not combined_files:
    print("   ⚠ No HNMeeting2_Combined_All_Sources_*.csv file found!")
    exit(1)

combined_file = max(combined_files, key=os.path.getctime)
print(f"   ✓ Found: {combined_file}")

combined_df = pd.read_csv(combined_file)
print(f"   ✓ Loaded {len(combined_df)} existing combined members")

# Step 3: Normalize and merge
print("\n3. Merging data...")

# Normalize four DL data
four_dl_normalized = four_dl_df[['Email', 'Name', 'Source_DL']].copy()
four_dl_normalized.rename(columns={'Source_DL': 'Source'}, inplace=True)

# Combine
all_data = pd.concat([combined_df, four_dl_normalized], ignore_index=True, sort=False)

print(f"   Total records before deduplication: {len(all_data)}")

# Remove duplicates based on email (case-insensitive)
all_data['Email_Lower'] = all_data['Email'].str.lower()
all_data = all_data.drop_duplicates(subset=['Email_Lower'], keep='first')
all_data = all_data.drop(columns=['Email_Lower'])

print(f"   Unique users after deduplication: {len(all_data)}")

# Sort by email
all_data = all_data.sort_values('Email')

# Step 4: Export final combined file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f'HNMeeting2_Final_Combined_{timestamp}.csv'

all_data.to_csv(output_file, index=False)

print(f"\n{'='*80}")
print("FINAL SUMMARY")
print(f"{'='*80}")
print(f"Members from four DLs:        {len(four_dl_df)}")
print(f"Previous combined total:      {len(combined_df)}")
print(f"Final unique users:           {len(all_data)}")
print(f"New members added:            {len(all_data) - len(combined_df)}")
print(f"\n✅ Final combined file saved to: {output_file}")
print(f"{'='*80}")

# Show source breakdown
print("\nBreakdown by source:")
source_counts = all_data['Source'].value_counts()
for source, count in source_counts.items():
    print(f"  {source}: {count}")

# Show sample
print(f"\nSample records (first 10):")
print("-"*80)
sample_cols = ['Email', 'WIN', 'First_Name', 'Last_Name', 'Source']
available_cols = [col for col in sample_cols if col in all_data.columns]
print(all_data[available_cols].head(10).to_string(index=False))
