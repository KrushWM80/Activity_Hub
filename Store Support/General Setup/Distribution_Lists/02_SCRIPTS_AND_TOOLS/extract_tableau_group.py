#!/usr/bin/env python3
"""
Extract tableau_home_office_all_type_a AD Group Members
Uses the same extraction logic as ad_group_extractor.py
"""

import subprocess
import csv
from datetime import datetime
from pathlib import Path
import sys

# Add parent directory to path to import from ad_group_extractor
sys.path.insert(0, str(Path(__file__).parent))

# Import the ADGroupExtractor
try:
    from ad_group_extractor import ADGroupExtractor
except ImportError:
    print("ERROR: Could not import ADGroupExtractor")
    print("Make sure ad_group_extractor.py is in the same directory")
    sys.exit(1)

def main():
    print("\n" + "="*80)
    print("Tableau AD Group Extractor")
    print("="*80)
    
    extractor = ADGroupExtractor()
    
    # Define the Tableau group
    groups = ["tableau_home_office_all_type_a"]
    
    print(f"\nExtracting: {groups[0]}")
    print("-" * 80)
    
    # Extract members and details
    group_users = extractor.extract_groups(groups)
    
    if not group_users or not group_users.get(groups[0]):
        print("\n❌ ERROR: Could not extract group members")
        print("\nPossible reasons:")
        print("  1. Group name is incorrect")
        print("  2. You don't have permission to query this group")
        print("  3. You're not connected to the domain")
        sys.exit(1)
    
    # Print summary
    extractor.print_summary(group_users)
    
    # Export results with specific naming
    print("\n" + "="*80)
    print("EXPORTING RESULTS")
    print("="*80 + "\n")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Export CSV
    csv_filename = f"tableau_home_office_all_type_a_{timestamp}.csv"
    try:
        with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'group', 'username', 'email', 'display_name', 'title', 
                'department', 'employee_number', 'job_code', 'position_code',
                'business_unit', 'business_unit_type', 'employment_status',
                'workday_job_number', 'workday_job_description'
            ])
            writer.writeheader()
            
            for group_name, users in group_users.items():
                for user in users:
                    row = {
                        'group': group_name,
                        'username': user.username,
                        'email': user.email,
                        'display_name': user.display_name,
                        'title': user.title,
                        'department': user.department,
                        'employee_number': user.employee_number,
                        'job_code': user.job_code,
                        'position_code': user.position_code,
                        'business_unit': user.business_unit,
                        'business_unit_type': user.business_unit_type,
                        'employment_status': user.employment_status,
                        'workday_job_number': user.workday_job_number,
                        'workday_job_description': user.workday_job_description
                    }
                    writer.writerow(row)
        
        print(f"✓ Exported CSV: {csv_filename}")
    except Exception as e:
        print(f"✗ CSV export failed: {e}")
    
    print("\n" + "="*80)
    print("EXTRACTION COMPLETE")
    print("="*80)
    print(f"\nOutput file: {csv_filename}")
    print("\nYou can now run: python compare_ops_vs_tableau.py")

if __name__ == "__main__":
    main()
