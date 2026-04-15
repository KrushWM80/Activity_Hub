#!/usr/bin/env python3
"""Simple test: iterate and read data without accessing names."""

import win32com.client as win32
import time
import subprocess

# Kill existing Excel
subprocess.run(['taskkill', '/F', '/IM', 'EXCEL.EXE'], stderr=subprocess.DEVNULL)
time.sleep(1)

file_path = r'C:\Users\krush\OneDrive - Walmart Inc\AGE Team - Documents\Activity - Walmart US\Reporting\Data\Me@\MM\Input\Playbook Hub and Active Playbooks - Weekly Report.xlsx'

excel = win32.Dispatch('Excel.Application')
excel.Visible = False
workbook = excel.Workbooks.Open(file_path)

print(f"Sheets count: {workbook.Sheets.Count}")

# Iterate and read each sheet
for sheet_idx in range(1, workbook.Sheets.Count + 1):
    print(f"\n--- Sheet {sheet_idx} ---")
    
    # Get worksheet through iteration
    worksheets = workbook.Worksheets
    ws_collection = worksheets
    
    # Try getting the worksheet object
    ws = None
    for idx_check, ws_iter in enumerate(ws_collection):
        if idx_check + 1 == sheet_idx:
            ws = ws_iter
            break
    
    if ws:
        print(f"Got worksheet object via iteration: {type(ws)}")
        
        # Try to read UsedRange
        try:
            ur = ws.UsedRange
            print(f"UsedRange: {type(ur)}")
            data = ur.Value
            if data:
                print(f"Data rows: {len(data)}")
                print(f"First row: {data[0] if data else None}")
            else:
                print("Data is None")
        except Exception as e:
            print(f"UsedRange failed: {e}")
            
        # Try accessing via _oleobj_
        try:
            print(f"_oleobj_: {ws._oleobj_}")
        except:
            pass
    else:
        # Fall back to numeric indexing
        print(f"Iteration failed, trying numeric indexing...")
        try:
            ws = workbook.Sheets(sheet_idx)
            print(f"Got worksheet via Sheets({sheet_idx}): {type(ws)}")
            ur = ws.UsedRange
            data = ur.Value
            print(f"Data rows: {len(data) if data else 0}")
        except Exception as e:
            print(f"Numeric indexing failed: {e}")

# Close
try:
    workbook.Close(SaveChanges=False)
except:
    pass
    
try:
    excel.Quit()
except:
    pass

print("\nDone!")
