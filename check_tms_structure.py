"""
Analyze TMS Data (3).xlsx to see actual column structure
"""
import pandas as pd
import sys

tms_file = r"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\TMS Data (3).xlsx"

print("="*80)
print("TMS DATA (3).XLSX STRUCTURE ANALYSIS")
print("="*80)

try:
    # Load the file
    df = pd.read_excel(tms_file)
    
    print(f"\n✓ File loaded successfully")
    print(f"\nShape: {df.shape[0]} rows × {df.shape[1]} columns")
    
    print(f"\n📋 COLUMN NAMES:")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i}. {col}")
    
    print(f"\n📊 FIRST 3 ROWS:")
    print(df.head(3).to_string())
    
    print(f"\n✓ Column data types:")
    print(df.dtypes)
    
    print(f"\n✓ Null count per column:")
    print(df.isnull().sum())
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
