#!/usr/bin/env python3
"""Test simple data reading without sheet name."""

import win32com.client as win32
import time
import subprocess

# Kill existing Excel
subprocess.run(['taskkill', '/F', '/IM', 'EXCEL.EXE'], stderr=subprocess.DEVNULL)
time.sleep(1)

file_path = r'C:\Users\krush\OneDrive - Walmart Inc\AGE Team - Documents\Activity - Walmart US\Reporting\Data\Me@\MM\Input\Playbook Hub and Active Playbooks - Weekly Report.xlsx'

excel = win32.gencache.EnsureDispatch('Excel.Application')
workbook = excel.Workbooks.Open(file_path)

# Just loop through sheets and read data
for sheet_index in range(1, workbook.Sheets.Count + 1):
    worksheet = workbook.Sheets(sheet_index)
    print(f"\nSheet {sheet_index}:")
    
    # Try to get the name using different methods
    try:
        # Method 1: Direct property
        name = worksheet.Name
        print(f"  Name (direct): {name}")
    except Exception as e1:
        print(f"  Name (direct) failed: {e1}")
        try:
            # Method 2: getattr
            name = getattr(worksheet, 'Name', 'UNKNOWN')
            print(f"  Name (getattr): {name}")
        except Exception as e2:
            print(f"  Name (getattr) failed: {e2}")
    
    # Try to get UsedRange
    try:
        ur = worksheet.UsedRange
        print(f"  UsedRange type: {type(ur)}")
        data = ur.Value
        if data:
            print(f"  Data: {len(data)} rows")
        else:
            print(f"  Data: None or empty")
    except Exception as e:
        print(f"  UsedRange failed: {e}")

# Close
workbook.Close(SaveChanges=False)
excel.Quit()
print("\nDone!")
