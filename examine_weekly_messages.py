import win32com.client
import os

path = r"C:\Users\krush\OneDrive - Walmart Inc\AGE Team - Documents\Activity - Walmart US\Reporting\Data\Me@\MM\Input\Weekly Messages Area Reports - Tables FY27.xlsx"

excel = win32com.client.gencache.EnsureDispatch('Excel.Application')
excel.Visible = False
wb = excel.Workbooks.Open(path)

try:
    sheet = wb.Sheets(1)
    print("Looking for data tables...")
    print("=" * 100)
    
    # Scan first 30 rows to find structure
    for row in range(1, 31):
        values = []
        for col in range(1, 7):
            cell = sheet.Cells(row, col)
            val = str(cell.Value)[:30] if cell.Value else ""
            values.append(val)
        line = " | ".join(values)
        print(f"Row {row:2d}: {line}")
        
        if row == 20:
            print("..." if row < 30 else "")
finally:
    wb.Close()
    excel.Quit()
