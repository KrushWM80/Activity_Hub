#!/usr/bin/env python3
"""Test different COM worksheet access methods."""

import win32com.client as win32
import time
import subprocess

# Kill existing Excel
subprocess.run(['taskkill', '/F', '/IM', 'EXCEL.EXE'], stderr=subprocess.DEVNULL)
time.sleep(1)

file_path = r'C:\Users\krush\OneDrive - Walmart Inc\AGE Team - Documents\Activity - Walmart US\Reporting\Data\Me@\MM\Input\Playbook Hub and Active Playbooks - Weekly Report.xlsx'

# Try the gencache approach
try:
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    print("Using gencache.EnsureDispatch")
except:
    excel = win32.Dispatch('Excel.Application')
    print("Using Dispatch (dynamic)")

print(f"Excel type: {type(excel)}")

workbook = excel.Workbooks.Open(file_path)
print(f"Workbook type: {type(workbook)}")
print(f"Workbook.Sheets type: {type(workbook.Sheets)}")
print(f"Workbook.Sheets.Count: {workbook.Sheets.Count}")

# Try different access method 1
try:
    print("\n--- Testing workbook.Sheets(1) ---")
    ws1 = workbook.Sheets(1)
    print(f"Success! Type: {type(ws1)}")
    print(f"Name: {ws1.Name}")
except Exception as e:
    print(f"Failed: {e}")

# Try different access method 2
try:
    print("\n--- Testing workbook.Sheets.Item(1) ---")
    ws2 = workbook.Sheets.Item(1)
    print(f"Success! Type: {type(ws2)}")
    print(f"Name: {ws2.Name}")
except Exception as e:
    print(f"Failed: {e}")

# Try different access method 3
try:
    print("\n--- Testing workbook.ActiveSheet ---")
    ws3 = workbook.ActiveSheet
    print(f"Success! Type: {type(ws3)}")
    print(f"Name: {ws3.Name}")
except Exception as e:
    print(f"Failed: {e}")

# Try different access method 4 - with __getitem__
try:
    print("\n--- Testing workbook.Sheets[0] ---")
    ws4 = workbook.Sheets[0]
    print(f"Success! Type: {type(ws4)}")
    print(f"Name: {ws4.Name}")
except Exception as e:
    print(f"Failed: {e}")

# Close
workbook.Close(SaveChanges=False)
excel.Quit()
print("\nDone!")
