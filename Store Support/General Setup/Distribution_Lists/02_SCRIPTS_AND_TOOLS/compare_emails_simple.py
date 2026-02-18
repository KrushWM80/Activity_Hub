#!/usr/bin/env python3
"""
Simple offline comparison - Compare CSV against exported DL member list
Works without Exchange Online connection if you have a DL export
"""

import csv
from datetime import datetime


def load_emails_from_csv(csv_file, col_name=None):
    """Load emails from CSV file"""
    
    print(f"\nLoading: {csv_file}")
    emails = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            fieldnames = list(reader.fieldnames)
            
            # Find email column
            if col_name:
                email_col = col_name
            else:
                email_col = None
                for col in fieldnames:
                    if 'email' in col.lower() or 'mail' in col.lower():
                        email_col = col
                        break
                if not email_col:
                    email_col = fieldnames[0]
            
            print(f"  Columns: {', '.join(fieldnames)}")
            print(f"  Using: {email_col}")
            
            for row in reader:
                email = row.get(email_col, '').strip().lower()
                if email and '@' in email:
                    emails.append(email)
        
        print(f"  ✓ Loaded {len(emails)} emails\n")
        return set(emails)
        
    except Exception as e:
        print(f"  X Error: {e}\n")
        return set()


def main():
    print("\n" + "="*80)
    print("EMAIL LIST COMPARISON")
    print("="*80 + "\n")
    
    # Load BIITWI Audience
    biitwi_file = r"C:\Users\krush\Documents\BIITWI Audience.csv"
    biitwi_emails = load_emails_from_csv(biitwi_file)
    
    print(f"BIITWI Audience has: {len(biitwi_emails)} unique emails")
    
    # Option 1: Compare against your OPS Support extraction
    print("\n" + "-"*80)
    print("OPTION 1: Compare against OPS Support team members")
    print("-"*80 + "\n")
    
    ops_file = r"c:\Users\krush\Documents\VSCode\Spark-Playground\General Setup\Distribution_Lists\ad_groups_20251215_154559.csv"
    ops_emails = load_emails_from_csv(ops_file)
    
    if ops_emails:
        overlap = biitwi_emails.intersection(ops_emails)
        in_biitwi_only = biitwi_emails.difference(ops_emails)
        in_ops_only = ops_emails.difference(biitwi_emails)
        
        print(f"OPS Support members:          {len(ops_emails)}")
        print(f"BIITWI Audience:              {len(biitwi_emails)}")
        print(f"In both lists:                {len(overlap)}")
        print(f"Only in BIITWI:               {len(in_biitwi_only)}")
        print(f"Only in OPS Support:          {len(in_ops_only)}")
        
        # Export results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if in_biitwi_only:
            file_only = f"only_in_biitwi_{timestamp}.txt"
            with open(file_only, 'w') as f:
                f.write(f"Emails only in BIITWI Audience ({len(in_biitwi_only)} total)\n")
                f.write("="*80 + "\n\n")
                for email in sorted(in_biitwi_only):
                    f.write(f"{email}\n")
            print(f"\n✓ Exported BIITWI-only emails to: {file_only}")
        
        if overlap:
            file_both = f"in_both_lists_{timestamp}.txt"
            with open(file_both, 'w') as f:
                f.write(f"Emails in both BIITWI and OPS Support ({len(overlap)} total)\n")
                f.write("="*80 + "\n\n")
                for email in sorted(overlap):
                    f.write(f"{email}\n")
            print(f"✓ Exported common emails to: {file_both}")
    
    # Instructions for DL comparison
    print("\n" + "="*80)
    print("TO COMPARE AGAINST HNMeeting2 DISTRIBUTION LIST:")
    print("="*80 + "\n")
    
    print("Method 1: Export DL members manually")
    print("-" * 40)
    print("1. Open Outlook")
    print("2. Search for: HNMeeting2@email.wal-mart.com")
    print("3. Right-click the group → Properties")
    print("4. Members tab → Export → Save as CSV")
    print("5. Save as: hnmeeting2_members.csv")
    print("6. Place it in this folder")
    print("7. Run this script again\n")
    
    print("Method 2: Use PowerShell (if you have Exchange admin rights)")
    print("-" * 40)
    print("Run in PowerShell:")
    print('''
Get-DistributionGroupMember -Identity "HNMeeting2@email.wal-mart.com" |
    Select-Object PrimarySmtpAddress |
    Export-Csv -Path "hnmeeting2_members.csv" -NoTypeInformation
    ''')
    
    # Check if DL export exists
    dl_exports = [
        "hnmeeting2_members.csv",
        "HNMeeting2_members.csv",
        "dl_members_HNMeeting2.csv"
    ]
    
    print("\n" + "-"*80)
    print("OPTION 2: Compare against exported DL list (if available)")
    print("-"*80 + "\n")
    
    found_dl = False
    for dl_file in dl_exports:
        try:
            with open(dl_file, 'r'):
                dl_emails = load_emails_from_csv(dl_file)
                if dl_emails:
                    found_dl = True
                    
                    already_on = biitwi_emails.intersection(dl_emails)
                    need_add = biitwi_emails.difference(dl_emails)
                    
                    print(f"HNMeeting2 DL has:            {len(dl_emails)} members")
                    print(f"BIITWI Audience has:          {len(biitwi_emails)} emails")
                    print(f"Already on DL:                {len(already_on)} ✓")
                    print(f"Need to add to DL:            {len(need_add)} ←")
                    
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    
                    if need_add:
                        need_file = f"need_to_add_to_hnmeeting2_{timestamp}.txt"
                        with open(need_file, 'w') as f:
                            f.write(f"Emails to add to HNMeeting2 ({len(need_add)} total)\n")
                            f.write("="*80 + "\n\n")
                            for email in sorted(need_add):
                                f.write(f"{email}\n")
                        print(f"\n✓ Emails to add: {need_file}")
                    
                    if already_on:
                        already_file = f"already_on_hnmeeting2_{timestamp}.txt"
                        with open(already_file, 'w') as f:
                            f.write(f"Already on HNMeeting2 ({len(already_on)} total)\n")
                            f.write("="*80 + "\n\n")
                            for email in sorted(already_on):
                                f.write(f"{email}\n")
                        print(f"✓ Already on DL: {already_file}")
                    
                    break
        except FileNotFoundError:
            continue
    
    if not found_dl:
        print("No DL member export found yet.")
        print("Follow instructions above to export HNMeeting2 members first.")
    
    print("\n" + "="*80)
    print("COMPLETE")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
