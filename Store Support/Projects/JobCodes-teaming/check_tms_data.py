import pandas as pd

# Check TMS Data file
tms_path = "Teaming/TMS Data (3).xlsx"

try:
    # Try to read all sheets
    xls = pd.ExcelFile(tms_path)
    print(f"TMS Data sheets: {xls.sheet_names}\n")
    
    # Read first sheet
    for sheet in xls.sheet_names:
        df = pd.read_excel(tms_path, sheet_name=sheet)
        print(f"\n=== SHEET: {sheet} ===")
        print(f"Shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        print(f"\nFirst 3 rows:")
        print(df.head(3).to_string())
        
        # Look for job code or role columns
        if 'Job Code' in df.columns or 'jobCode' in df.columns or 'full_job_code' in df.columns:
            print("\nFound job code related data in this sheet")
            
except Exception as e:
    print(f"Error: {e}")
