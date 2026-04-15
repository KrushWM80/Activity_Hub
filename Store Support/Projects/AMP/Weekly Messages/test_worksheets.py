#!/usr/bin/env python3
"""Test accessing worksheets through collection."""

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

# Try accessing through Worksheets or Sheets
try:
    # Method 1: worksheets collection
    worksheets = workbook.Worksheets
    print(f"Worksheets type: {type(worksheets)}")
    print(f"Worksheets count:  {worksheets.Count}")
    
    # Try Item access
    ws = worksheets.Item(1)
    print(f"Item(1) success! Type: {type(ws)}")
    print(f"Item(1).Name: {ws.Name}")
except Exception as e:
    print(f"Worksheets.Item(1) failed: {e}")

# Try raw_data = worksheets(1)
try:
    ws2 = worksheets(1)
    print(f"Worksheets(1) success! Type: {type(ws2)}")
    print(f"Worksheets(1).Name: {ws2.Name}")  
except Exception as e:
    print(f"Worksheets(1) failed: {e}")
    
# Try accessing  _Worksheet directly
try:
    ws3 = workbook._default_method()
    print(f"Default method: {ws3}")
except:
    pass

# Try iterate
try:
    for idx, ws in enumerate(workbook.Worksheets):
        print(f"Iteration {idx}: {type(ws)} - {ws.Name if hasattr(ws, 'Name') else 'NO NAME'}")
except Exception as e:
    print(f"Iteration failed: {e}")

# Close
workbook.Close(SaveChanges=False)
excel.Quit()
