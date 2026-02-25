#!/usr/bin/env python3
"""
Extract User IDs for store-based associates by job code
Job Codes: 1-993-1076 (Food & Consumables Coach) and 1-16-101 (Lawn & Garden DM)
Source: JobCodes-teaming Teaming folder
"""

import csv
from pathlib import Path
from datetime import datetime

# Paths
jobcodes_path = Path(r'C:\Users\krush\Documents\VSCode\Activity-Hub\Store Support\Projects\JobCodes-teaming\Teaming')
worker_file = jobcodes_path / 'Worker_Names_Stores_JobCodes.csv'

# Job codes to extract
TARGET_JOB_CODES = ['1-993-1076', '1-16-101']

def extract_user_ids():
    """Extract User IDs for target job codes"""
    
    if not worker_file.exists():
        print(f"Error: File not found: {worker_file}")
        return False
    
    results = {jc: [] for jc in TARGET_JOB_CODES}
    
    print(f"Reading from: {worker_file}")
    print(f"Target Job Codes: {', '.join(TARGET_JOB_CODES)}\n")
    
    try:
        with open(worker_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                job_code = row.get('job_code', '').strip()
                
                if job_code in TARGET_JOB_CODES:
                    first_name = row.get('first_name', '').strip()
                    last_name = row.get('last_name', '').strip()
                    store_number = row.get('store_number', '').strip()
                    job_nm = row.get('job_nm', '').strip()
                    
                    results[job_code].append({
                        'first_name': first_name,
                        'last_name': last_name,
                        'store_number': store_number,
                        'job_code': job_code,
                        'job_nm': job_nm,
                        'full_name': f"{first_name} {last_name}".strip(),
                    })
        
        # Display results
        print("\n" + "="*80)
        print("EXTRACTION RESULTS")
        print("="*80 + "\n")
        
        total_records = 0
        
        for job_code in TARGET_JOB_CODES:
            data = results[job_code]
            total_records += len(data)
            
            print(f"\nJob Code: {job_code}")
            print(f"Records Found: {len(data)}")
            print("-" * 80)
            
            if data:
                # Show first 5 in detail
                for i, item in enumerate(data[:5], 1):
                    print(f"\n{i}. {item['full_name']}")
                    print(f"   Store: {item['store_number']}")
                    print(f"   Job Title: {item['job_nm']}")
                
                if len(data) > 5:
                    print(f"\n... and {len(data) - 5} more")
            else:
                print("No records found")
        
        # Save to CSV
        print(f"\n\n" + "="*80)
        print("SAVING RESULTS")
        print("="*80 + "\n")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = jobcodes_path / f'EXTRACTED_USER_IDS_{timestamp}.csv'
        
        all_data = []
        for job_code in TARGET_JOB_CODES:
            all_data.extend(results[job_code])
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['first_name', 'last_name', 'full_name', 'store_number', 'job_code', 'job_nm']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_data)
        
        print(f"File saved: {output_file}")
        print(f"Total records: {total_records}\n")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == '__main__':
    extract_user_ids()
