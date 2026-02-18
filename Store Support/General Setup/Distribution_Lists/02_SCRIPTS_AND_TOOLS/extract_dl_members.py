#!/usr/bin/env python3
"""
Extract members from specific distribution list
Usage: python extract_dl_members.py HNMeeting2@email.wal-mart.com
"""

import subprocess
import csv
import json
import sys
from datetime import datetime

def extract_dl_members(dl_email):
    """Extract members from a distribution list"""
    
    print(f"\nExtracting members from: {dl_email}")
    print("="*80)
    
    # PowerShell script to get DL members
    ps_script = f'''
    $dl = Get-DistributionGroup -Identity "{dl_email}" -ErrorAction SilentlyContinue
    
    if ($dl) {{
        $members = Get-DistributionGroupMember -Identity "{dl_email}" | Select-Object Name, PrimarySmtpAddress, Title, Department
        $members | ConvertTo-Json
    }} else {{
        Write-Output "DL_NOT_FOUND"
    }}
    '''
    
    try:
        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if "DL_NOT_FOUND" in result.stdout:
            print(f"X Distribution list not found: {dl_email}")
            print("\nPossible reasons:")
            print("  - DL doesn't exist")
            print("  - You don't have permission to view it")
            print("  - Wrong email format")
            return None
        
        members = json.loads(result.stdout)
        
        if not isinstance(members, list):
            members = [members]
        
        print(f"+ Found {len(members)} members")
        
        # Export to CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_file = f"dl_members_{dl_email.split('@')[0]}_{timestamp}.csv"
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Name', 'Email', 'Title', 'Department'])
            writer.writeheader()
            
            for member in members:
                writer.writerow({
                    'Name': member.get('Name', ''),
                    'Email': member.get('PrimarySmtpAddress', ''),
                    'Title': member.get('Title', ''),
                    'Department': member.get('Department', '')
                })
        
        print(f"+ Exported to: {csv_file}")
        return members
        
    except Exception as e:
        print(f"X Error: {e}")
        return None

def add_members_to_dl(dl_email, email_list_file):
    """Add members from email list to distribution list"""
    
    print(f"\nAdding members to: {dl_email}")
    print(f"From file: {email_list_file}")
    print("="*80)
    
    # Read email list
    try:
        with open(email_list_file, 'r') as f:
            emails = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"X File not found: {email_list_file}")
        return False
    
    print(f"Found {len(emails)} emails to add")
    
    # PowerShell script to add members
    ps_script = f'''
    $dlEmail = "{dl_email}"
    $emails = @(
        {', '.join([f'"{email}"' for email in emails])}
    )
    
    $added = 0
    $failed = 0
    
    foreach ($email in $emails) {{
        try {{
            Add-DistributionGroupMember -Identity $dlEmail -Member $email -ErrorAction Stop
            $added++
            Write-Output "Added: $email"
        }} catch {{
            $failed++
            Write-Output "Failed: $email - $($_.Exception.Message)"
        }}
    }}
    
    Write-Output ""
    Write-Output "Summary: $added added, $failed failed"
    '''
    
    try:
        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes for large lists
        )
        
        print(result.stdout)
        return True
        
    except Exception as e:
        print(f"X Error: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Extract members: python extract_dl_members.py HNMeeting2@email.wal-mart.com")
        print("  Add members:     python extract_dl_members.py HNMeeting2@email.wal-mart.com --add email_list.txt")
        return
    
    dl_email = sys.argv[1]
    
    if len(sys.argv) > 2 and sys.argv[2] == '--add':
        if len(sys.argv) < 4:
            print("X Please provide email list file")
            print("  Usage: python extract_dl_members.py DL_EMAIL --add email_list.txt")
            return
        
        email_list_file = sys.argv[3]
        add_members_to_dl(dl_email, email_list_file)
    else:
        extract_dl_members(dl_email)

if __name__ == "__main__":
    main()
