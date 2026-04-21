"""
Generate Missing Job Codes Report with Sample Impacted Users
This script creates a CSV file showing:
- Job codes that are Missing in teaming
- Role/Title for each job code
- Sample impacted user name
- Store number for that employee
"""

import json
import pandas as pd
import os
import sys
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from main import load_job_code_data, cache
from sqlite_cache import get_cache

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
PARENT_DIR = os.path.join(os.path.dirname(__file__), '..')

def generate_missing_report():
    """Generate missing job codes report with sample employees and store numbers"""
    
    print("[REPORT] Starting missing job codes report generation...")
    
    try:
        # Get all job codes with their user counts
        job_codes = cache.get_job_codes()
        print(f"[REPORT] Loaded {len(job_codes) if job_codes else 0} total job codes")
        
        if not job_codes:
            print("[REPORT] ERROR: No job codes available")
            return None
        
        # Load teaming data to get assignment status
        merged_df, _ = load_job_code_data()
        print(f"[REPORT] Loaded teaming data: {len(merged_df) if merged_df is not None else 0} rows")
        
        # Load worker details with names and store numbers
        worker_file = os.path.join(PARENT_DIR, 'Worker_Names_Stores_JobCodes.csv')
        worker_df = None
        if os.path.exists(worker_file):
            worker_df = pd.read_csv(worker_file)
            print(f"[REPORT] Loaded worker data: {len(worker_df)} records")
        else:
            print(f"[REPORT] WARNING: Worker file not found: {worker_file}")
        
        # Build status map - 'Missing' if no composite_job_code (not assigned to a team)
        status_map = {}
        if merged_df is not None and len(merged_df) > 0:
            for _, row in merged_df.iterrows():
                job_code_str = str(row['job_code']).strip() if pd.notna(row['job_code']) else ""
                # A job code is "Assigned" if it has a composite_job_code, otherwise "Missing"
                is_assigned = pd.notna(row.get('composite_job_code'))
                status = 'Assigned' if is_assigned else 'Missing'
                status_map[job_code_str] = status
        
        print(f"[REPORT] Status map contains {len(status_map)} entries")
        
        # Filter for Missing status job codes
        missing_codes = []
        for jc in job_codes:
            job_code_str = str(jc.get("job_code", "")).strip()
            status = status_map.get(job_code_str, "Unknown")
            
            if status == "Missing":
                user_count = jc.get("user_count", 0)
                if user_count > 0:  # Only include if there are impacted users
                    
                    # Get sample employee info if available
                    sample_employee = "-"
                    sample_store = "-"
                    
                    if worker_df is not None and len(worker_df) > 0:
                        # Try to match by job code first
                        worker_records = worker_df[worker_df['job_code'] == job_code_str]
                        
                        if len(worker_records) > 0:
                            first_record = worker_records.iloc[0]
                            first_name = str(first_record.get('first_name', '')).strip()
                            last_name = str(first_record.get('last_name', '')).strip()
                            sample_employee = f"{first_name} {last_name}".strip()
                            sample_store = str(first_record.get('store_number', ''))
                    
                    missing_codes.append({
                        "job_code": job_code_str,
                        "role": jc.get("job_nm", ""),
                        "impacted_count": user_count,
                        "sample_user": sample_employee,
                        "store_number": sample_store,
                    })
        
        print(f"[REPORT] Found {len(missing_codes)} missing job codes with impacted users")
        
        # Create DataFrame
        df = pd.DataFrame(missing_codes)
        
        # Rename columns for output
        df.columns = ['Job Code', 'Role', 'Impacted Count', 'Sample User', 'Store Number']
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(DATA_DIR, f'missing_job_codes_{timestamp}.csv')
        
        # Save to CSV
        df.to_csv(output_file, index=False)
        
        print(f"[REPORT] Report saved to: {output_file}")
        print(f"[REPORT] Total rows: {len(df)}")
        print(f"[REPORT] Sample data:")
        print(df.head(10).to_string())
        
        return output_file
        
    except Exception as e:
        print(f"[REPORT] ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    output_file = generate_missing_report()
    if output_file:
        print(f"\n✅ Report generated successfully!")
        print(f"📁 File: {output_file}")
    else:
        print(f"\n❌ Failed to generate report")
        sys.exit(1)
