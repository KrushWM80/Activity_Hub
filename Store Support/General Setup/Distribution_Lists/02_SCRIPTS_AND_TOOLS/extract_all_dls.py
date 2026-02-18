#!/usr/bin/env python3
"""
Extract ALL Distribution Lists from Active Directory
Creates a catalog of all DLs for the DL Selector tool
"""

import subprocess
import csv
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import sys


def get_all_distribution_lists():
    """
    Query AD for all groups with email addresses (distribution lists)
    """
    
    print("\n" + "="*80)
    print("EXTRACTING ALL DISTRIBUTION LISTS FROM ACTIVE DIRECTORY")
    print("="*80 + "\n")
    
    print("Querying Active Directory for all groups with email addresses...")
    
    # PowerShell script to get all DLs
    ps_script = '''
    $searcher = New-Object System.DirectoryServices.DirectorySearcher
    $searcher.Filter = "(&(objectClass=group)(mail=*))"
    $searcher.PropertiesToLoad.Add("mail") | Out-Null
    $searcher.PropertiesToLoad.Add("cn") | Out-Null
    $searcher.PropertiesToLoad.Add("displayName") | Out-Null
    $searcher.PropertiesToLoad.Add("description") | Out-Null
    $searcher.PropertiesToLoad.Add("managedBy") | Out-Null
    $searcher.PropertiesToLoad.Add("member") | Out-Null
    $searcher.PageSize = 1000
    
    $results = $searcher.FindAll()
    
    $dls = @()
    foreach ($result in $results) {
        $props = $result.Properties
        $dl = @{
            email = if ($props["mail"].Count -gt 0) { $props["mail"][0] } else { "" }
            name = if ($props["cn"].Count -gt 0) { $props["cn"][0] } else { "" }
            displayName = if ($props["displayName"].Count -gt 0) { $props["displayName"][0] } else { "" }
            description = if ($props["description"].Count -gt 0) { $props["description"][0] } else { "" }
            memberCount = if ($props["member"].Count -gt 0) { $props["member"].Count } else { 0 }
            managedBy = if ($props["managedBy"].Count -gt 0) { $props["managedBy"][0] } else { "" }
        }
        $dls += $dl
    }
    
    $dls | ConvertTo-Json
    '''
    
    try:
        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode != 0:
            print(f"X Error querying AD: {result.stderr}")
            return None
        
        dls = json.loads(result.stdout)
        
        # Handle single result (not in array)
        if isinstance(dls, dict):
            dls = [dls]
        
        print(f"+ Found {len(dls)} distribution lists")
        return dls
        
    except Exception as e:
        print(f"X Error: {e}")
        return None


def get_owner_email(managed_by_dn):
    """
    Convert managedBy DN to email address
    """
    if not managed_by_dn:
        return ""
    
    ps_script = f'''
    $searcher = New-Object System.DirectoryServices.DirectorySearcher
    $searcher.Filter = "(distinguishedName={managed_by_dn})"
    $searcher.PropertiesToLoad.Add("mail") | Out-Null
    $result = $searcher.FindOne()
    if ($result -and $result.Properties["mail"].Count -gt 0) {{
        $result.Properties["mail"][0]
    }}
    '''
    
    try:
        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout.strip()
    except:
        return ""


def export_to_csv(dls, filename="all_distribution_lists.csv"):
    """
    Export DL catalog to CSV
    """
    
    print(f"\nExporting to CSV: {filename}")
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'email', 'name', 'displayName', 'description', 
                'memberCount', 'ownerEmail', 'category'
            ])
            writer.writeheader()
            
            for dl in dls:
                # Categorize DLs by name patterns
                name = dl.get('name', '').lower()
                category = 'General'
                if 'ops' in name or 'operations' in name:
                    category = 'Operations'
                elif 'market' in name:
                    category = 'Market'
                elif 'region' in name:
                    category = 'Region'
                elif 'support' in name:
                    category = 'Support'
                elif 'management' in name or 'mgmt' in name:
                    category = 'Management'
                elif 'team' in name:
                    category = 'Team'
                
                writer.writerow({
                    'email': dl.get('email', ''),
                    'name': dl.get('name', ''),
                    'displayName': dl.get('displayName', ''),
                    'description': dl.get('description', ''),
                    'memberCount': dl.get('memberCount', 0),
                    'ownerEmail': '',  # Will populate in next version
                    'category': category
                })
        
        print(f"+ Exported {len(dls)} distribution lists to {filename}")
        return True
        
    except Exception as e:
        print(f"X Error exporting: {e}")
        return False


def export_to_json(dls, filename="all_distribution_lists.json"):
    """
    Export DL catalog to JSON
    """
    
    print(f"Exporting to JSON: {filename}")
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'extracted_date': datetime.now().isoformat(),
                'total_lists': len(dls),
                'distribution_lists': dls
            }, f, indent=2)
        
        print(f"+ Exported to {filename}")
        return True
        
    except Exception as e:
        print(f"X Error exporting: {e}")
        return False


def generate_stats(dls):
    """
    Generate statistics about DLs
    """
    
    print("\n" + "="*80)
    print("DISTRIBUTION LIST STATISTICS")
    print("="*80 + "\n")
    
    total = len(dls)
    total_members = sum(dl.get('memberCount', 0) for dl in dls)
    
    print(f"Total Distribution Lists: {total}")
    print(f"Total Memberships (sum): {total_members:,}")
    print(f"Average Members per DL: {total_members // total if total > 0 else 0}")
    
    # Size categories
    small = sum(1 for dl in dls if dl.get('memberCount', 0) < 50)
    medium = sum(1 for dl in dls if 50 <= dl.get('memberCount', 0) < 500)
    large = sum(1 for dl in dls if dl.get('memberCount', 0) >= 500)
    
    print(f"\nBy Size:")
    print(f"  Small (<50 members):    {small}")
    print(f"  Medium (50-499):        {medium}")
    print(f"  Large (500+):           {large}")
    
    # Top 10 largest DLs
    sorted_dls = sorted(dls, key=lambda x: x.get('memberCount', 0), reverse=True)
    
    print(f"\nTop 10 Largest Distribution Lists:")
    for i, dl in enumerate(sorted_dls[:10], 1):
        print(f"  {i}. {dl.get('name', 'Unknown')} - {dl.get('memberCount', 0)} members")
    
    print(f"\n" + "="*80)


def main():
    """
    Main execution
    """
    
    # Extract all DLs
    dls = get_all_distribution_lists()
    
    if not dls:
        print("\nX Failed to extract distribution lists")
        print("  Check your AD connection and permissions")
        sys.exit(1)
    
    # Generate statistics
    generate_stats(dls)
    
    # Export to files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = f"all_distribution_lists_{timestamp}.csv"
    json_file = f"all_distribution_lists_{timestamp}.json"
    
    export_to_csv(dls, csv_file)
    export_to_json(dls, json_file)
    
    print("\n" + "="*80)
    print("COMPLETE")
    print("="*80)
    print(f"\nFiles created:")
    print(f"  {csv_file}")
    print(f"  {json_file}")
    print(f"\nNext step: Use these files to build the DL Selector tool")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
