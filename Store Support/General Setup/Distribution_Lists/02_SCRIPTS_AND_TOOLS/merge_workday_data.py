#!/usr/bin/env python3
"""
Merge Workday Job Data with Extracted AD Users

This script takes the extracted AD user CSV and enriches it with Workday
job descriptions and job numbers.

Usage:
    python merge_workday_data.py --ad-csv ad_groups_*.csv --workday-csv workday_jobs.csv --output final_users_with_jobs.csv
"""

import csv
import json
import argparse
from pathlib import Path
from typing import Dict, List
from datetime import datetime
import sys

# Import the Workday lookup module
sys.path.insert(0, str(Path(__file__).parent))
from workday_job_lookup import WorkdayJobLookup


def load_ad_users(csv_file: str) -> List[Dict]:
    """
    Load users from AD extraction CSV
    """
    users = []
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            users = list(reader)
        print(f"+ Loaded {len(users)} users from {csv_file}")
        return users
    except Exception as e:
        print(f"X Error loading AD users: {e}")
        return []


def merge_user_with_job(user: Dict, job_lookup: WorkdayJobLookup) -> Dict:
    """
    Merge a single user with their job data
    """
    job_code = user.get('job_code', '').strip()
    
    if job_code:
        job = job_lookup.get_job(job_code)
        if job:
            user['workday_job_number'] = job.job_number
            user['workday_job_description'] = job.job_description
            user['job_family'] = job.job_family
            user['job_level'] = job.job_level
            user['grade'] = job.grade
        else:
            # No match found
            user['workday_job_number'] = 'NOT_FOUND'
            user['workday_job_description'] = 'NOT_FOUND'
    
    return user


def merge_users_with_jobs(users: List[Dict], job_lookup: WorkdayJobLookup) -> List[Dict]:
    """
    Merge all users with job data
    """
    print(f"\nMerging {len(users)} users with Workday job data...")
    
    merged_users = []
    found_count = 0
    not_found_count = 0
    missing_jobcode = 0
    
    for i, user in enumerate(users):
        if i % 200 == 0:
            print(f"  Progress: {i}/{len(users)}")
        
        job_code = user.get('job_code', '').strip()
        
        if not job_code:
            missing_jobcode += 1
        else:
            job = job_lookup.get_job(job_code)
            if job:
                user['workday_job_number'] = job.job_number
                user['workday_job_description'] = job.job_description
                user['job_family'] = job.job_family
                user['job_level'] = job.job_level
                user['grade'] = job.grade
                found_count += 1
            else:
                not_found_count += 1
                user['workday_job_number'] = 'NOT_FOUND'
                user['workday_job_description'] = 'NOT_FOUND'
        
        merged_users.append(user)
    
    print(f"\n+ Job matches found: {found_count}")
    print(f"+ Job codes not found in lookup: {not_found_count}")
    print(f"+ Users without job code: {missing_jobcode}")
    
    return merged_users


def export_merged_users(users: List[Dict], output_file: str) -> bool:
    """
    Export merged users to CSV
    """
    try:
        if not users:
            print("X No users to export")
            return False
        
        # Get all fieldnames from first user, plus new fields
        fieldnames = list(users[0].keys())
        new_fields = ['job_family', 'job_level', 'grade']
        for field in new_fields:
            if field not in fieldnames:
                fieldnames.append(field)
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(users)
        
        print(f"+ Exported {len(users)} merged users to {output_file}")
        return True
    except Exception as e:
        print(f"X Error exporting: {e}")
        return False


def print_sample(users: List[Dict], count: int = 5) -> None:
    """
    Print sample of merged data
    """
    print(f"\nSample of first {min(count, len(users))} users with Workday data:\n")
    
    for user in users[:count]:
        print(f"  Username: {user.get('username')}")
        print(f"  Name: {user.get('display_name')}")
        print(f"  Email: {user.get('email')}")
        print(f"  Job Code: {user.get('job_code')}")
        print(f"  Job Number: {user.get('workday_job_number')}")
        print(f"  Job Description: {user.get('workday_job_description')}")
        print(f"  Job Family: {user.get('job_family')}")
        print(f"  Job Level: {user.get('job_level')}")
        print(f"  Grade: {user.get('grade')}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description='Merge AD user data with Workday job information'
    )
    parser.add_argument(
        '--ad-csv',
        required=True,
        help='Path to AD extraction CSV file (e.g., ad_groups_*.csv)'
    )
    parser.add_argument(
        '--workday-csv',
        required=True,
        help='Path to Workday job mapping CSV file'
    )
    parser.add_argument(
        '--output',
        default=None,
        help='Output file (default: ad_users_with_workday_*.csv)'
    )
    parser.add_argument(
        '--format',
        choices=['csv', 'json'],
        default='csv',
        help='Output format (default: csv)'
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*80)
    print("AD Users + Workday Job Data Merger")
    print("="*80 + "\n")
    
    # Load AD users
    if not Path(args.ad_csv).exists():
        print(f"X AD CSV file not found: {args.ad_csv}")
        return
    
    users = load_ad_users(args.ad_csv)
    if not users:
        print("X No users loaded")
        return
    
    # Load Workday job data
    if not Path(args.workday_csv).exists():
        print(f"X Workday CSV file not found: {args.workday_csv}")
        print("\nTo get Workday job data:")
        print("1. Export job master from Workday with columns:")
        print("   job_code, job_number, job_description, job_family, job_level, grade")
        print("2. Save as CSV file")
        print("3. Run this script with --workday-csv <your_file.csv>")
        return
    
    lookup = WorkdayJobLookup()
    if not lookup.load_from_csv(args.workday_csv):
        print("X Failed to load Workday data")
        return
    
    # Merge data
    merged_users = merge_users_with_jobs(users, lookup)
    
    # Determine output file
    output_file = args.output
    if not output_file:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"ad_users_with_workday_{timestamp}.csv"
    
    # Export
    if export_merged_users(merged_users, output_file):
        print_sample(merged_users)
        print("\n+ Merge complete!")
    else:
        print("X Merge failed")


if __name__ == "__main__":
    main()