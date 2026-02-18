#!/usr/bin/env python3
"""
Compare email list against Distribution List members
Checks which emails are already on the DL and which need to be added
"""

import subprocess
import csv
import json
from datetime import datetime


def get_dl_members(dl_email):
    """Get current members from distribution list"""
    
    print(f"\nFetching members from: {dl_email}")
    print("="*80)
    
    ps_script = f'''
    try {{
        $members = Get-DistributionGroupMember -Identity "{dl_email}" -ErrorAction Stop | 
                   Select-Object -ExpandProperty PrimarySmtpAddress
        $members | ConvertTo-Json
    }} catch {{
        Write-Output "ERROR: $($_.Exception.Message)"
    }}
    '''
    
    try:
        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if "ERROR:" in result.stdout:
            print(f"X Error: {result.stdout}")
            print("\nPossible issues:")
            print("  - DL doesn't exist or wrong email")
            print("  - You don't have permission to view members")
            print("  - Not connected to Exchange Online")
            return None
        
        members_json = result.stdout.strip()
        if not members_json:
            print("X No members found or access denied")
            return None
        
        members = json.loads(members_json)
        
        # Handle single member (not in array)
        if isinstance(members, str):
            members = [members]
        
        # Normalize to lowercase for comparison
        members_set = set(email.lower() for email in members if email)
        
        print(f"+ Found {len(members_set)} current members in DL")
        return members_set
        
    except json.JSONDecodeError as e:
        print(f"X Error parsing DL members: {e}")
        print(f"Output was: {result.stdout[:200]}")
        return None
    except Exception as e:
        print(f"X Error: {e}")
        return None


def load_csv_emails(csv_file):
    """Load emails from CSV file"""
    
    print(f"\nLoading emails from: {csv_file}")
    print("="*80)
    
    emails = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8-sig') as f:
            # Try to detect email column
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            
            print(f"Columns found: {', '.join(fieldnames)}")
            
            # Find email column (case-insensitive)
            email_col = None
            for col in fieldnames:
                if 'email' in col.lower() or 'mail' in col.lower() or '@' in col.lower():
                    email_col = col
                    break
            
            if not email_col:
                # If no email column found, try first column
                email_col = fieldnames[0]
            
            print(f"Using column: {email_col}")
            
            for row in reader:
                email = row.get(email_col, '').strip().lower()
                if email and '@' in email:
                    emails.append(email)
        
        print(f"+ Loaded {len(emails)} emails from CSV")
        return emails
        
    except Exception as e:
        print(f"X Error reading CSV: {e}")
        return None


def compare_lists(dl_members, csv_emails):
    """Compare CSV emails against DL members"""
    
    print("\n" + "="*80)
    print("COMPARISON RESULTS")
    print("="*80 + "\n")
    
    if dl_members is None or csv_emails is None:
        print("X Cannot compare - missing data")
        return None
    
    csv_set = set(csv_emails)
    
    # Find matches and differences
    already_on_dl = csv_set.intersection(dl_members)
    need_to_add = csv_set.difference(dl_members)
    
    # Results
    results = {
        'total_csv_emails': len(csv_set),
        'total_dl_members': len(dl_members),
        'already_on_dl': len(already_on_dl),
        'need_to_add': len(need_to_add),
        'already_list': sorted(already_on_dl),
        'need_add_list': sorted(need_to_add)
    }
    
    # Display summary
    print(f"Total emails in your CSV:        {results['total_csv_emails']}")
    print(f"Current members in DL:           {results['total_dl_members']}")
    print(f"Already on DL (no action):       {results['already_on_dl']} ✓")
    print(f"Need to add to DL:               {results['need_to_add']} ←")
    
    # Export results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Export already on DL
    if already_on_dl:
        already_file = f"already_on_dl_{timestamp}.txt"
        with open(already_file, 'w') as f:
            f.write(f"Emails already on HNMeeting2 DL ({len(already_on_dl)} total)\n")
            f.write("="*80 + "\n\n")
            for email in sorted(already_on_dl):
                f.write(f"{email}\n")
        print(f"\n+ Exported existing members to: {already_file}")
    
    # Export need to add
    if need_to_add:
        need_add_file = f"need_to_add_{timestamp}.txt"
        with open(need_add_file, 'w') as f:
            f.write(f"Emails to add to HNMeeting2 DL ({len(need_to_add)} total)\n")
            f.write("="*80 + "\n\n")
            for email in sorted(need_to_add):
                f.write(f"{email}\n")
        print(f"+ Exported emails to add to: {need_add_file}")
        
        # Also create CSV for easy import
        need_add_csv = f"need_to_add_{timestamp}.csv"
        with open(need_add_csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Email'])
            for email in sorted(need_to_add):
                writer.writerow([email])
        print(f"+ Exported as CSV: {need_add_csv}")
    
    # Detailed report
    report_file = f"dl_comparison_report_{timestamp}.txt"
    with open(report_file, 'w') as f:
        f.write("DISTRIBUTION LIST COMPARISON REPORT\n")
        f.write("="*80 + "\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Distribution List: HNMeeting2@email.wal-mart.com\n\n")
        
        f.write(f"Total emails in CSV:        {results['total_csv_emails']}\n")
        f.write(f"Current DL members:         {results['total_dl_members']}\n")
        f.write(f"Already on DL:              {results['already_on_dl']}\n")
        f.write(f"Need to add:                {results['need_to_add']}\n\n")
        
        f.write("="*80 + "\n")
        f.write("ALREADY ON DL (No action needed)\n")
        f.write("="*80 + "\n")
        for email in sorted(already_on_dl):
            f.write(f"  ✓ {email}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("NEED TO ADD TO DL\n")
        f.write("="*80 + "\n")
        for email in sorted(need_to_add):
            f.write(f"  + {email}\n")
    
    print(f"+ Full report saved to: {report_file}")
    
    return results


def main():
    """Main comparison workflow"""
    
    print("\n" + "="*80)
    print("DISTRIBUTION LIST EMAIL COMPARISON")
    print("="*80)
    
    # Configuration
    dl_email = "HNMeeting2@email.wal-mart.com"
    csv_file = r"C:\Users\krush\Documents\BIITWI Audience.csv"
    
    # Step 1: Get current DL members
    dl_members = get_dl_members(dl_email)
    
    # Step 2: Load CSV emails
    csv_emails = load_csv_emails(csv_file)
    
    # Step 3: Compare
    results = compare_lists(dl_members, csv_emails)
    
    if results and results['need_to_add'] > 0:
        print("\n" + "="*80)
        print("NEXT STEPS")
        print("="*80)
        print("\nTo add the missing emails, run:")
        print(f"  python extract_dl_members.py {dl_email} --add need_to_add_*.txt")
        print("\nOr use PowerShell:")
        print(f"  Get-Content need_to_add_*.txt | ForEach-Object {{")
        print(f"      Add-DistributionGroupMember -Identity '{dl_email}' -Member $_")
        print(f"  }}")
    
    print("\n" + "="*80)
    print("COMPLETE")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
