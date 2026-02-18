"""
Combine HNMeeting2 with four other DL lists and 308 missing users
Creates a consolidated CSV with all unique users
"""

import pandas as pd
from datetime import datetime
import subprocess
import json

print("="*80)
print("COMBINING DISTRIBUTION LISTS FOR HNMEETING2")
print("="*80)

# Distribution lists to extract
other_dls = [
    'HN-MerchTeam@email.wal-mart.com',
    'HN-SupplyChainteam@email.wal-mart.com',
    'HN-SupportTeam@email.wal-mart.com',
    'HN-TomWardTeam@email.wal-mart.com'
]

# Step 1: Load the 308 missing members
print("\n1. Loading missing members from HNMeeting2...")
missing_members_file = 'HNMeeting2_Missing_Members_20251219_122841.csv'
missing_df = pd.read_csv(missing_members_file)
print(f"   ✓ Loaded {len(missing_df)} missing members")

# Step 2: Load current HNMeeting2 members
print("\n2. Loading current HNMeeting2 members...")
current_members_file = 'HNMeeting2_Members_Final_20251219_112826.csv'
try:
    current_df = pd.read_csv(current_members_file)
    print(f"   ✓ Loaded {len(current_df)} current HNMeeting2 members")
except FileNotFoundError:
    print(f"   ⚠ {current_members_file} not found, will extract from PowerShell")
    current_df = None

# Step 3: Extract members from the four other distribution lists
print("\n3. Extracting members from other distribution lists...")
other_members = []

for dl_email in other_dls:
    print(f"\n   Extracting: {dl_email}")
    
    # PowerShell command to get distribution list members
    ps_command = f"""
    $members = Get-DistributionGroupMember -Identity "{dl_email}" -ResultSize Unlimited
    $members | Select-Object Name, PrimarySmtpAddress, @{{n='WIN';e={{$_.CustomAttribute1}}}} | ConvertTo-Json
    """
    
    try:
        # Run PowerShell command
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0 and result.stdout:
            members_json = json.loads(result.stdout)
            
            # Handle single member (dict) vs multiple members (list)
            if isinstance(members_json, dict):
                members_json = [members_json]
            
            for member in members_json:
                other_members.append({
                    'Email': member.get('PrimarySmtpAddress', ''),
                    'Name': member.get('Name', ''),
                    'WIN': member.get('WIN', ''),
                    'Source_DL': dl_email
                })
            
            print(f"   ✓ Found {len(members_json)} members")
        else:
            print(f"   ⚠ Failed to extract: {result.stderr}")
    
    except Exception as e:
        print(f"   ⚠ Error extracting {dl_email}: {str(e)}")

other_df = pd.DataFrame(other_members)
print(f"\n   ✓ Total members from other DLs: {len(other_df)}")

# Step 4: Combine all data
print("\n4. Combining all data sources...")

# Normalize email columns for comparison
all_dfs = []

# Add missing members
if not missing_df.empty:
    missing_normalized = missing_df.copy()
    missing_normalized['Source'] = 'Missing from HNMeeting2'
    all_dfs.append(missing_normalized)

# Add current members if available
if current_df is not None and not current_df.empty:
    current_normalized = current_df.copy()
    current_normalized['Source'] = 'Current HNMeeting2'
    all_dfs.append(current_normalized)

# Add other DL members
if not other_df.empty:
    # Normalize to match the structure of missing_df
    other_normalized = pd.DataFrame()
    other_normalized['Email'] = other_df['Email']
    other_normalized['WIN'] = other_df['WIN']
    other_normalized['Source'] = other_df['Source_DL']
    all_dfs.append(other_normalized)

# Combine all DataFrames
combined_df = pd.concat(all_dfs, ignore_index=True, sort=False)

# Remove duplicates based on email (keep first occurrence)
print(f"\n   Total records before deduplication: {len(combined_df)}")
combined_df = combined_df.drop_duplicates(subset=['Email'], keep='first')
print(f"   Unique users after deduplication: {len(combined_df)}")

# Sort by email
combined_df = combined_df.sort_values('Email')

# Step 5: Export to CSV
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f'HNMeeting2_Combined_All_Sources_{timestamp}.csv'

combined_df.to_csv(output_file, index=False)

print(f"\n{'='*80}")
print("SUMMARY")
print(f"{'='*80}")
print(f"Missing members:              {len(missing_df)}")
if current_df is not None:
    print(f"Current HNMeeting2 members:   {len(current_df)}")
print(f"Members from other 4 DLs:     {len(other_df)}")
print(f"Total unique users:           {len(combined_df)}")
print(f"\n✅ Combined file saved to: {output_file}")
print(f"{'='*80}")

# Show source breakdown
print("\nBreakdown by source:")
source_counts = combined_df['Source'].value_counts()
for source, count in source_counts.items():
    print(f"  {source}: {count}")

# Show sample records
print(f"\nSample records (first 10):")
print("-"*80)
sample_cols = ['Email', 'WIN', 'First_Name', 'Last_Name', 'Source']
available_cols = [col for col in sample_cols if col in combined_df.columns]
print(combined_df[available_cols].head(10).to_string(index=False))
