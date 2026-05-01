#!/usr/bin/env python3
"""
Add Role Title column to teaming export CSV by querying TMS Data (3).xlsx
"""
import pandas as pd
from pathlib import Path

def main():
    # Define paths
    script_dir = Path(__file__).parent
    tms_path = script_dir.parent / "Teaming" / "TMS Data (3).xlsx"
    csv_path = script_dir.parent / "teaming_all_actions_2026-04-27.csv"
    output_path = script_dir.parent / "teaming_all_actions_2026-04-27_with_roles.csv"
    
    print("=" * 80)
    print("ADDING ROLE TITLE TO TEAMING EXPORT")
    print("=" * 80)
    
    # Read TMS data
    print(f"\n1. Reading TMS data from: {tms_path}")
    try:
        tms_df = pd.read_excel(tms_path, sheet_name='data')
        print(f"   ✓ Loaded {len(tms_df)} records")
        print(f"   Columns: {tms_df.columns.tolist()[:5]}... (showing first 5)")
    except Exception as e:
        print(f"   ✗ Error reading TMS data: {e}")
        return
    
    # Read export CSV
    print(f"\n2. Reading teaming export from: {csv_path}")
    try:
        export_df = pd.read_csv(csv_path)
        print(f"   ✓ Loaded {len(export_df)} records")
        print(f"   Columns: {export_df.columns.tolist()}")
    except Exception as e:
        print(f"   ✗ Error reading CSV: {e}")
        return
    
    # Create lookup dictionary from TMS data
    print(f"\n3. Creating lookup dictionary for job codes...")
    
    # Remove duplicates and keep first occurrence (in case of duplicates)
    tms_unique = tms_df.drop_duplicates(subset=['jobCode'], keep='first')
    role_lookup = dict(zip(tms_unique['jobCode'].astype(str), tms_unique['jobCodeTitle']))
    
    print(f"   ✓ Created lookup with {len(role_lookup)} job codes")
    print(f"   Sample mappings:")
    for i, (code, title) in enumerate(list(role_lookup.items())[:5]):
        print(f"      {code} -> {title}")
    
    # Add Role Title column to export
    print(f"\n4. Mapping role titles to export records...")
    
    def get_role_title(job_code):
        """Lookup role title from TMS data"""
        if pd.isna(job_code):
            return "Unknown"
        
        code_str = str(int(job_code) if isinstance(job_code, (int, float)) else job_code)
        return role_lookup.get(code_str, "Unknown")
    
    # Add the Role Title column using jobCode from export
    export_df['roleTitle'] = export_df['jobCode'].apply(get_role_title)
    
    # Count matched roles
    matched = (export_df['roleTitle'] != 'Unknown').sum()
    unmatched = (export_df['roleTitle'] == 'Unknown').sum()
    print(f"   ✓ Matched {matched} records")
    if unmatched > 0:
        print(f"   ⚠ {unmatched} records with unknown role title")
    
    # Reorder columns to put Role Title after jobCode
    cols = export_df.columns.tolist()
    if 'roleTitle' in cols:
        cols.remove('roleTitle')
        # Insert after jobCode
        idx = cols.index('jobCode') + 1
        cols.insert(idx, 'roleTitle')
        export_df = export_df[cols]
    
    # Save the updated CSV
    print(f"\n5. Saving updated export to: {output_path}")
    try:
        export_df.to_csv(output_path, index=False)
        print(f"   ✓ Successfully saved {len(export_df)} records")
        print(f"\n   New column order:")
        for i, col in enumerate(export_df.columns, 1):
            print(f"      {i:2d}. {col}")
    except Exception as e:
        print(f"   ✗ Error saving CSV: {e}")
        return
    
    # Show sample data
    print(f"\n6. Sample of updated export:")
    sample_cols = ['jobCode', 'roleTitle', 'teamName', 'workgroupName', 'status']
    print(export_df[sample_cols].head(10).to_string())
    
    print(f"\n✓ COMPLETE: Export with role titles saved to:")
    print(f"  {output_path}")
    
if __name__ == "__main__":
    main()
