#!/usr/bin/env python3
"""
Alternative Excel reader using Windows COM (win32com)
Reads Excel files without requiring openpyxl
"""

import sys
import json
import pandas as pd

def read_excel_via_com(file_path, sheet_name=0):
    """
    Read Excel file using Windows COM if available,
    otherwise fall back to pandas with xlrd/default engine.
    """
    try:
        import win32com.client as win32
        
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        excel.Visible = False
        workbook = excel.Workbooks.Open(file_path)
        
        # Get sheet
        if isinstance(sheet_name, int):
            worksheet = workbook.Sheets(sheet_name + 1)  # COM uses 1-based indexing
        else:
            worksheet = workbook.Sheets(sheet_name)
        
        # Read data
        usedRange = worksheet.UsedRange
        data = usedRange.Value
        
        workbook.Close(False)
        excel.Quit()
        
        # Convert to DataFrame
        if data:
            df = pd.DataFrame(list(data[1:]), columns=data[0])
            return df
        else:
            return pd.DataFrame()
    
    except ImportError:
        print("win32com not available, using pandas fallback", file=sys.stderr)
        # Fall back to pandas
        try:
            return pd.read_excel(file_path, sheet_name=sheet_name, engine='python')
        except:
            return pd.read_excel(file_path, sheet_name=sheet_name)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: read_excel_com.py <file_path> [sheet_number]", file=sys.stderr)
        sys.exit(1)
    
    file_path = sys.argv[1]
    sheet_num = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    
    df = read_excel_via_com(file_path, sheet_num)
    print(json.dumps(df.to_dict(orient='records')))
