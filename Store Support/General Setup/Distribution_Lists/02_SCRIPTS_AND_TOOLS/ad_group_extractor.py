#!/usr/bin/env python3
"""
Walmart AD Group Email Extractor
Extracts members from AD groups and retrieves their email addresses
"""

import subprocess
import json
import csv
from pathlib import Path
from typing import List, Dict, Set
from dataclasses import dataclass, asdict
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


@dataclass
class ADUser:
    """Represents an AD user"""
    username: str
    email: str = ""
    display_name: str = ""
    title: str = ""
    department: str = ""
    # Walmart custom attributes
    employee_number: str = ""
    job_code: str = ""
    position_code: str = ""
    business_unit: str = ""
    business_unit_type: str = ""
    employment_status: str = ""
    # Workday fields (to be populated)
    workday_job_number: str = ""
    workday_job_description: str = ""
    
    def __hash__(self):
        return hash(self.username)
    
    def __eq__(self, other):
        if not isinstance(other, ADUser):
            return False
        return self.username == other.username


class ADGroupExtractor:
    """Extract members from AD groups and get their details"""

    def __init__(self):
        self.users: Set[ADUser] = set()

    def get_group_members(self, group_name: str) -> List[str]:
        """
        Get all members of an AD group using 'net group' command
        Returns list of usernames
        """
        try:
            result = subprocess.run(
                ["net", "group", group_name, "/domain"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                print(f"X Error querying group '{group_name}': {result.stderr}")
                return []
            
            # Parse the output
            lines = result.stdout.split('\n')
            members = []
            in_members_section = False
            
            for line in lines:
                line = line.strip()
                
                # Skip headers and empty lines
                if not line or 'Members' in line or '---' in line:
                    if 'Members' in line:
                        in_members_section = True
                    continue
                
                if 'command completed successfully' in line.lower():
                    break
                
                # Parse member lines (usernames are typically alphanumeric)
                if in_members_section and line:
                    # Split by whitespace and add valid-looking usernames
                    usernames = line.split()
                    for username in usernames:
                        if username and len(username) > 2:
                            members.append(username.lower())
            
            print(f"+ Found {len(members)} members in {group_name}")
            return members
            
        except subprocess.TimeoutExpired:
            print(f"X Timeout querying group '{group_name}'")
            return []
        except Exception as e:
            print(f"X Error: {e}")
            return []

    def get_user_details(self, username: str) -> ADUser:
        """
        Get user details from AD using PowerShell including Walmart custom attributes
        """
        try:
            # Use PowerShell to query AD via DirectorySearcher
            ps_command = (
                f"$filter = '(sAMAccountName={username})';"
                "$searcher = New-Object System.DirectoryServices.DirectorySearcher($filter);"
                "@('displayName', 'mail', 'title', 'department', 'wm-employeenumber', 'wm-jobcode', "
                "'wm-positioncode', 'wm-businessunitnumber', 'wm-businessunittype', 'wm-employmentstatus') "
                "| foreach { $searcher.PropertiesToLoad.Add($_) | Out-Null };"
                "$result = $searcher.FindOne();"
                "if ($result) { "
                "$user = $result.Properties; "
                "Write-Host 'displayName:' ($user['displayname'][0]); "
                "Write-Host 'mail:' ($user['mail'][0]); "
                "Write-Host 'title:' ($user['title'][0]); "
                "Write-Host 'department:' ($user['department'][0]); "
                "Write-Host 'employeenumber:' ($user['wm-employeenumber'][0]); "
                "Write-Host 'jobcode:' ($user['wm-jobcode'][0]); "
                "Write-Host 'positioncode:' ($user['wm-positioncode'][0]); "
                "Write-Host 'businessunitnumber:' ($user['wm-businessunitnumber'][0]); "
                "Write-Host 'businessunittype:' ($user['wm-businessunittype'][0]); "
                "Write-Host 'employmentstatus:' ($user['wm-employmentstatus'][0]); "
                "} else { Write-Host 'notfound'; }"
            )
            
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps_command],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            user = ADUser(username=username)
            
            if result.returncode == 0 and "notfound" not in result.stdout.lower():
                lines = result.stdout.split('\n')
                for line in lines:
                    if ':' in line:
                        parts = line.split(':', 1)
                        if len(parts) == 2:
                            key, value = parts
                            value = value.strip()
                            key = key.strip().lower()
                            
                            if key == 'displayname':
                                user.display_name = value
                            elif key == 'mail':
                                user.email = value
                            elif key == 'title':
                                user.title = value
                            elif key == 'department':
                                user.department = value
                            elif key == 'employeenumber':
                                user.employee_number = value
                            elif key == 'jobcode':
                                user.job_code = value
                            elif key == 'positioncode':
                                user.position_code = value
                            elif key == 'businessunitnumber':
                                user.business_unit = value
                            elif key == 'businessunittype':
                                user.business_unit_type = value
                            elif key == 'employmentstatus':
                                user.employment_status = value
            
            return user
            
        except subprocess.TimeoutExpired:
            return ADUser(username=username)
        except Exception:
            return ADUser(username=username)  # Silently return basic user

    def extract_groups(self, group_names: List[str], max_workers: int = 10) -> Dict[str, List[ADUser]]:
        """
        Extract all members from multiple groups with parallel lookup
        """
        results = {}
        all_usernames = set()
        
        print("\n" + "="*80)
        print("EXTRACTING GROUP MEMBERS")
        print("="*80)
        
        # Get members from each group
        for group_name in group_names:
            print(f"\nQuerying group: {group_name}")
            members = self.get_group_members(group_name)
            results[group_name] = members
            all_usernames.update(members)
        
        # Get detailed info for each unique user using thread pool
        print("\n" + "="*80)
        print(f"RETRIEVING USER DETAILS ({len(all_usernames)} unique users with {max_workers} workers)")
        print("="*80)
        
        completed = 0
        lock = threading.Lock()
        
        def update_progress(future):
            nonlocal completed
            with lock:
                completed += 1
                if completed % 25 == 0:
                    print(f"  Progress: {completed}/{len(all_usernames)}...")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.get_user_details, username): username 
                      for username in all_usernames}
            
            for future in as_completed(futures):
                try:
                    user = future.result()
                    self.users.add(user)
                except Exception:
                    pass
                update_progress(future)
        
        # Organize users by group
        group_users = {}
        for group_name, members in results.items():
            group_users[group_name] = [u for u in self.users if u.username in members]
        
        return group_users

    def export_csv(self, group_users: Dict[str, List[ADUser]], filename: str = None):
        """
        Export results to CSV
        """
        if filename is None:
            filename = f"ad_groups_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                fieldnames = [
                    'group', 'username', 'email', 'display_name', 'title', 'department',
                    'employee_number', 'job_code', 'position_code', 'business_unit',
                    'business_unit_type', 'employment_status', 'workday_job_number',
                    'workday_job_description'
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for group_name, users in group_users.items():
                    for user in sorted(users, key=lambda u: u.username):
                        row = asdict(user)
                        row['group'] = group_name
                        writer.writerow(row)
            
            print(f"+ Exported to CSV: {filename}")
            return filename
        except Exception as e:
            print(f"X CSV export failed: {e}")
            return None

    def export_json(self, group_users: Dict[str, List[ADUser]], filename: str = None):
        """
        Export results to JSON
        """
        if filename is None:
            filename = f"ad_groups_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            data = {}
            for group_name, users in group_users.items():
                data[group_name] = [
                    asdict(user) for user in sorted(users, key=lambda u: u.username)
                ]
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            print(f"+ Exported to JSON: {filename}")
            return filename
        except Exception as e:
            print(f"X JSON export failed: {e}")
            return None

    def export_emails_only(self, group_users: Dict[str, List[ADUser]], filename: str = None):
        """
        Export just the email addresses (for distribution list creation)
        """
        if filename is None:
            filename = f"email_list_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            emails = set()
            for users in group_users.values():
                for user in users:
                    if user.email:
                        emails.add(user.email)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(sorted(emails)))
            
            print(f"+ Exported {len(emails)} emails to: {filename}")
            return filename
        except Exception as e:
            print(f"X Email export failed: {e}")
            return None

    def print_summary(self, group_users: Dict[str, List[ADUser]]):
        """
        Print a summary of the extraction
        """
        print("\n" + "="*80)
        print("EXTRACTION SUMMARY")
        print("="*80)
        
        total_users = len(self.users)
        total_with_email = len([u for u in self.users if u.email])
        
        for group_name, users in group_users.items():
            users_with_email = len([u for u in users if u.email])
            print(f"\n{group_name}:")
            print(f"  Total members: {len(users)}")
            print(f"  With email: {users_with_email}")
        
        print(f"\nTotal unique users: {total_users}")
        print(f"Total with email: {total_with_email}")
        print(f"Overall coverage: {total_with_email/total_users*100:.1f}%" if total_users > 0 else "N/A")


def main():
    print("\n" + "="*80)
    print("Walmart AD Group Email Extractor (Enhanced with Workday Attributes)")
    print("="*80)
    
    extractor = ADGroupExtractor()
    
    # Define groups to extract
    groups = [
        "OPS_SUP_MARKET_TEAM",
        "OPS_SUP_REGION_TEAM",
        "OPS_SUP_BU_TEAM"
    ]
    
    # Extract members and details
    group_users = extractor.extract_groups(groups)
    
    # Print summary
    extractor.print_summary(group_users)
    
    # Export results
    print("\n" + "="*80)
    print("EXPORTING RESULTS")
    print("="*80 + "\n")
    
    csv_file = extractor.export_csv(group_users)
    json_file = extractor.export_json(group_users)
    email_file = extractor.export_emails_only(group_users)
    
    print("\n+ Complete! Check the exported files for results.")
    print(f"  CSV: {csv_file}")
    print(f"  JSON: {json_file}")
    print(f"  Email List: {email_file}")


if __name__ == "__main__":
    main()