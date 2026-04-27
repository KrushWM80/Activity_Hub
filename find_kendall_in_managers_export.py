#!/usr/bin/env python3
"""
Find Kendall Rush's Leadership Chain from managers_export.xlsx
"""

import os
import pandas as pd
from pathlib import Path

# Path to managers export file
MANAGERS_FILE = r"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails\data_input\managers_export.xlsx"

def find_kendall_in_managers_export():
    """Search managers_export.xlsx for Kendall Rush"""
    print("=" * 80)
    print("SEARCHING: managers_export.xlsx for Kendall Rush")
    print("=" * 80)
    
    if not os.path.exists(MANAGERS_FILE):
        print(f"\n✗ File not found: {MANAGERS_FILE}")
        return None
    
    try:
        # Read Excel file
        print(f"\nReading: {MANAGERS_FILE}")
        xls = pd.ExcelFile(MANAGERS_FILE)
        
        print(f"\nAvailable sheets: {xls.sheet_names}")
        
        # Try each sheet
        for sheet_name in xls.sheet_names:
            print(f"\n--- Checking sheet: '{sheet_name}' ---")
            df = pd.read_excel(MANAGERS_FILE, sheet_name=sheet_name)
            
            print(f"Columns: {list(df.columns)}")
            print(f"Rows: {len(df)}")
            
            # Search for Kendall
            kendall_rows = df[
                (df.apply(lambda row: row.astype(str).str.contains('Kendall', case=False, na=False).any(), axis=1)) |
                (df.apply(lambda row: row.astype(str).str.contains('Rush', case=False, na=False).any(), axis=1))
            ]
            
            if not kendall_rows.empty:
                print(f"\n✓ Found {len(kendall_rows)} matching row(s):\n")
                print(kendall_rows.to_string())
                return kendall_rows
        
        print("\n✗ Kendall Rush not found in any sheet")
        return None
        
    except Exception as e:
        print(f"\n✗ Error reading Excel file: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    print("=" * 80)
    print("KENDALL RUSH ORGANIZATIONAL DATA - MANAGERS EXPORT")
    print("=" * 80)
    
    result = find_kendall_in_managers_export()
    
    print("\n" + "=" * 80)
    print("SEARCH COMPLETE")
    print("=" * 80)


if __name__ == '__main__':
    main()
