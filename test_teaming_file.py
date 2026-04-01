import pandas as pd
import os

file_path = r'c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\TMS Data (3).xlsx'

if os.path.exists(file_path):
    try:
        df = pd.read_excel(file_path, nrows=3)
        print("TMS Data (3).xlsx - LOADED SUCCESSFULLY!")
        print(f"\nColumns found ({len(df.columns)}):")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i:2}. {col}")
        
        print(f"\nFirst row data:")
        for col in df.columns:
            val = df.iloc[0][col] if len(df) > 0 else None
            print(f"  {col:30} = {val}")
        
        print("\n--- Required columns check ---")
        required = {'jobCode', 'teamName', 'workgroupName', 'deptNumber', 'divNumber'}
        found = required & set(df.columns)
        missing = required - found
        
        if missing:
            print(f"MISSING columns: {missing}")
            print("\nAttempting fuzzy match:")
            for req in missing:
                candidates = [c for c in df.columns if req.lower() in c.lower()]
                if candidates:
                    print(f"  {req:20} -> try: {candidates}")
        else:
            print("All required columns present!")
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
else:
    print(f"File not found: {file_path}")
