"""
Compare two distribution lists: U.S. Comm - All MMs vs OPS_SUP_MARKET_TEAM
Shows members in both, only in first, only in second, and detailed comparison
"""

import pandas as pd
from datetime import datetime
import glob
import os

print("="*80)
print("DISTRIBUTION LIST COMPARISON")
print("U.S. Comm - All MMs  vs  OPS_SUP_MARKET_TEAM")
print("="*80)

# Look for the exported files
# Try to find recently exported CSVs
possible_files = {
    'US_Comm_All_MMs': [
        'US_Comm_All_MMs.csv',
        'U.S. Comm - All MMs*.csv',
        'Two_DL_Comparison_Raw_*.csv'
    ],
    'OPS_SUP_MARKET_TEAM': [
        'OPS_SUP_MARKET_TEAM.csv',
        'Two_DL_Comparison_Raw_*.csv'
    ]
}

def load_dl_members(dl_name, file_patterns):
    """Try to load distribution list members from various file patterns"""
    for pattern in file_patterns:
        files = glob.glob(pattern)
        if files:
            # Get most recent file
            latest_file = max(files, key=os.path.getctime)
            print(f"\n✓ Found file for {dl_name}: {latest_file}")
            
            df = pd.read_csv(latest_file)
            
            # Check if it's a combined export
            if 'DistributionList' in df.columns:
                df = df[df['DistributionList'].str.contains(dl_name, case=False, na=False)]
            
            # Standardize column names
            if 'mail' in df.columns:
                df['Email'] = df['mail']
            elif 'PrimarySmtpAddress' in df.columns:
                df['Email'] = df['PrimarySmtpAddress']
            elif 'Email' not in df.columns and len(df.columns) > 0:
                # Assume first column is email
                df.columns = ['Email'] + list(df.columns[1:])
            
            if 'displayName' in df.columns:
                df['Name'] = df['displayName']
            elif 'DisplayName' in df.columns:
                df['Name'] = df['DisplayName']
            
            return df
    
    return None

# Try to load both DLs
print("\nLooking for distribution list exports...")
dl1_df = load_dl_members('U.S. Comm - All MMs', possible_files['US_Comm_All_MMs'])
dl2_df = load_dl_members('OPS_SUP_MARKET_TEAM', possible_files['OPS_SUP_MARKET_TEAM'])

if dl1_df is None or dl2_df is None:
    print("\n" + "="*80)
    print("⚠ FILES NOT FOUND")
    print("="*80)
    print("\nPlease export the distribution lists first:")
    print("\n1. Run: .\\Extract-Two-DLs-For-Comparison.ps1")
    print("   OR")
    print("2. Manually export from Outlook/OWA and save as:")
    print("   - US_Comm_All_MMs.csv")
    print("   - OPS_SUP_MARKET_TEAM.csv")
    print("\nThen run this script again.")
    print("="*80)
    exit(1)

print(f"\n✓ Loaded U.S. Comm - All MMs: {len(dl1_df)} members")
print(f"✓ Loaded OPS_SUP_MARKET_TEAM: {len(dl2_df)} members")

# Normalize emails for comparison
dl1_df['Email_Lower'] = dl1_df['Email'].str.lower().str.strip()
dl2_df['Email_Lower'] = dl2_df['Email'].str.lower().str.strip()

dl1_emails = set(dl1_df['Email_Lower'])
dl2_emails = set(dl2_df['Email_Lower'])

# Perform comparison
in_both = dl1_emails & dl2_emails
only_in_dl1 = dl1_emails - dl2_emails
only_in_dl2 = dl2_emails - dl1_emails

print("\n" + "="*80)
print("COMPARISON RESULTS")
print("="*80)
print(f"\nU.S. Comm - All MMs:          {len(dl1_emails):>5} members")
print(f"OPS_SUP_MARKET_TEAM:          {len(dl2_emails):>5} members")
print(f"\n{'─'*40}")
print(f"In BOTH lists:                {len(in_both):>5} members")
print(f"ONLY in U.S. Comm - All MMs:  {len(only_in_dl1):>5} members")
print(f"ONLY in OPS_SUP_MARKET_TEAM:  {len(only_in_dl2):>5} members")

# Calculate overlap percentage
overlap_pct_dl1 = (len(in_both) / len(dl1_emails) * 100) if len(dl1_emails) > 0 else 0
overlap_pct_dl2 = (len(in_both) / len(dl2_emails) * 100) if len(dl2_emails) > 0 else 0

print(f"\nOverlap: {overlap_pct_dl1:.1f}% of U.S. Comm - All MMs")
print(f"         {overlap_pct_dl2:.1f}% of OPS_SUP_MARKET_TEAM")

# Create detailed comparison datasets
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Members in both
in_both_df = dl1_df[dl1_df['Email_Lower'].isin(in_both)].copy()
in_both_df['Status'] = 'In Both Lists'
in_both_file = f'DL_Comparison_In_Both_{timestamp}.csv'
in_both_df.drop(columns=['Email_Lower']).to_csv(in_both_file, index=False)

# Only in DL1
only_dl1_df = dl1_df[dl1_df['Email_Lower'].isin(only_in_dl1)].copy()
only_dl1_df['Status'] = 'Only in U.S. Comm - All MMs'
only_dl1_file = f'DL_Comparison_Only_US_Comm_All_MMs_{timestamp}.csv'
only_dl1_df.drop(columns=['Email_Lower']).to_csv(only_dl1_file, index=False)

# Only in DL2
only_dl2_df = dl2_df[dl2_df['Email_Lower'].isin(only_in_dl2)].copy()
only_dl2_df['Status'] = 'Only in OPS_SUP_MARKET_TEAM'
only_dl2_file = f'DL_Comparison_Only_OPS_SUP_MARKET_TEAM_{timestamp}.csv'
only_dl2_df.drop(columns=['Email_Lower']).to_csv(only_dl2_file, index=False)

# Combined comparison
all_comparison = pd.concat([in_both_df, only_dl1_df, only_dl2_df], ignore_index=True)
all_comparison = all_comparison.sort_values('Email')
comparison_file = f'DL_Comparison_Complete_{timestamp}.csv'
all_comparison.drop(columns=['Email_Lower']).to_csv(comparison_file, index=False)

print("\n" + "="*80)
print("FILES CREATED")
print("="*80)
print(f"\n✅ Members in both:             {in_both_file}")
print(f"✅ Only in U.S. Comm - All MMs: {only_dl1_file}")
print(f"✅ Only in OPS_SUP_MARKET_TEAM: {only_dl2_file}")
print(f"✅ Complete comparison:         {comparison_file}")

# Show samples
print("\n" + "="*80)
print("SAMPLE: MEMBERS IN BOTH LISTS (first 10)")
print("="*80)
if len(in_both_df) > 0:
    display_cols = ['Email', 'Name'] if 'Name' in in_both_df.columns else ['Email']
    print(in_both_df[display_cols].head(10).to_string(index=False))
else:
    print("No common members")

print("\n" + "="*80)
print("SAMPLE: ONLY IN U.S. COMM - ALL MMs (first 10)")
print("="*80)
if len(only_dl1_df) > 0:
    display_cols = ['Email', 'Name'] if 'Name' in only_dl1_df.columns else ['Email']
    print(only_dl1_df[display_cols].head(10).to_string(index=False))
else:
    print("All members are in OPS_SUP_MARKET_TEAM")

print("\n" + "="*80)
print("SAMPLE: ONLY IN OPS_SUP_MARKET_TEAM (first 10)")
print("="*80)
if len(only_dl2_df) > 0:
    display_cols = ['Email', 'Name'] if 'Name' in only_dl2_df.columns else ['Email']
    print(only_dl2_df[display_cols].head(10).to_string(index=False))
else:
    print("All members are in U.S. Comm - All MMs")

print("\n" + "="*80)
print("COMPARISON COMPLETE")
print("="*80)
