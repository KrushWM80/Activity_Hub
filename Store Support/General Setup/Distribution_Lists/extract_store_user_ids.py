#!/usr/bin/env python3
"""
Extract User IDs for store-based associates by job code
Filters: 1-993-1076 (Food and Consumables Coach) and 1-16-101 (Lawn & Garden DM)
"""

import csv
import sys
from pathlib import Path

# Input file
input_file = Path(__file__).parent / 'archive' / 'OLD_ANALYSIS' / 'Store_Employees_20251222_170730.csv'

# Job codes to filter
target_job_codes = ['1-993-1076', '1-16-101']

def extract_user_ids():
    """Extract User IDs for target job codes"""
    
    if not input_file.exists():
        print(f"❌ File not found: {input_file}")
        sys.exit(1)
    
    data = []
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                job_code = row.get('Job_Code', '').strip()
                
                # Filter by job code
                if job_code in target_job_codes:
                    store_number = row.get('Store_Number', '').strip()
                    user_id = row.get('User_ID', '').strip()
                    first_name = row.get('First_Name', '').strip()
                    last_name = row.get('Last_Name', '').strip()
                    job_title = row.get('Job_Title', '').strip()
                    
                    data.append({
                        'store_number': store_number,
                        'user_id': user_id,
                        'job_code': job_code,
                        'first_name': first_name,
                        'last_name': last_name,
                        'job_title': job_title,
                        'formatted_id': f"{user_id}.s{store_number.zfill(5)}"
                    })
        
        # Display results
        if data:
            print(f"\n✅ Found {len(data)} matches for job codes {target_job_codes}\n")
            print("User IDs (extracted format):")
            print("=" * 70)
            
            for item in data:
                print(f"{item['user_id']:15} | Store: {item['store_number']:5} | {item['job_code']}")
            
            print("\n\nUser IDs (formatted with store number - .s format):")
            print("=" * 70)
            
            for item in data:
                print(item['formatted_id'])
            
            # Save to output file
            output_file = input_file.parent / 'EXTRACTED_USER_IDS_BY_JOB_CODE.csv'
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['first_name', 'last_name', 'store_number', 'job_code', 'job_title', 'user_id', 'formatted_id'])
                writer.writeheader()
                writer.writerows(data)
            
            print(f"\n\n✅ Results saved to: {output_file}")
            print(f"Total records extracted: {len(data)}")
        else:
            print(f"❌ No records found for job codes: {target_job_codes}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    extract_user_ids()
