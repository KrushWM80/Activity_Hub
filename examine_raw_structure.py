import win32com.client
import time
from pathlib import Path

# Close any existing Excel instances
try:
    excel = win32com.client.GetObject(class_string="Excel.Application")
    if excel:
        excel.Quit()
except:
    pass

time.sleep(1)

# Start fresh Excel
excel = win32com.client.gencache.EnsureDispatch('Excel.Application')
excel.Visible = False

print("=" * 120)
print("PLAYBOOK HUB TABLE STRUCTURE")
print("=" * 120)

playbook_path = r"C:\Users\krush\OneDrive - Walmart Inc\AGE Team - Documents\Activity - Walmart US\Reporting\Data\Me@\MM\Input\Playbook Hub and Active Playbooks - Weekly Report.xlsx"

try:
    wb = excel.Workbooks.Open(playbook_path, ReadOnly=True)
    ws = wb.Sheets.Item(1)
    
    # Get dimensions
    last_row = ws.Cells.SpecialCells(11).Row
    last_col = ws.Cells.SpecialCells(11).Column
    
    print(f"Sheet: {ws.Name}")
    print(f"Dimensions: {last_row} rows × {last_col} columns")
    print(f"\nColumn headers (Row 1):")
    
    for col in range(1, last_col + 1):
        cell_val = ws.Cells(1, col).Value
        print(f"  Col {col}: {cell_val}")
    
    print(f"\nFirst 15 rows (all columns):")
    for row in range(1, min(16, last_row + 1)):
        row_data = []
        for col in range(1, last_col + 1):
            val = ws.Cells(row, col).Value
            row_data.append(str(val)[:25] if val else "")
        print(f"Row {row:2d}: {row_data}")
    
    wb.Close(SaveChanges=False)
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 120)
print("WEEKLY MESSAGES TABLE STRUCTURE")
print("=" * 120)

weekly_path = r"C:\Users\krush\OneDrive - Walmart Inc\AGE Team - Documents\Activity - Walmart US\Reporting\Data\Me@\MM\Input\Weekly Messages Area Reports - Tables FY27.xlsx"

try:
    wb = excel.Workbooks.Open(weekly_path, ReadOnly=True)
    ws = wb.Sheets.Item(1)
    
    # Get dimensions
    last_row = ws.Cells.SpecialCells(11).Row
    last_col = ws.Cells.SpecialCells(11).Column
    
    print(f"Sheet: {ws.Name}")
    print(f"Dimensions: {last_row} rows × {last_col} columns")
    print(f"\nColumn headers (Row 1):")
    
    for col in range(1, last_col + 1):
        cell_val = ws.Cells(1, col).Value
        print(f"  Col {col}: {cell_val}")
    
    print(f"\nFirst 15 rows (all columns):")
    for row in range(1, min(16, last_row + 1)):
        row_data = []
        for col in range(1, last_col + 1):
            val = ws.Cells(row, col).Value
            row_data.append(str(val)[:25] if val else "")
        print(f"Row {row:2d}: {row_data}")
    
    wb.Close(SaveChanges=False)
except Exception as e:
    print(f"Error: {e}")

excel.Quit()
