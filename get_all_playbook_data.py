import win32com.client
import time

# Close any existing Excel instances
try:
    excel = win32com.client.GetObject(class_string="Excel.Application")
    if excel:
        excel.Quit()
except:
    pass

time.sleep(1)

excel = win32com.client.gencache.EnsureDispatch('Excel.Application')
excel.Visible = False

playbook_path = r"C:\Users\krush\OneDrive - Walmart Inc\AGE Team - Documents\Activity - Walmart US\Reporting\Data\Me@\MM\Input\Playbook Hub and Active Playbooks - Weekly Report.xlsx"

print("PLAYBOOK - ALL ROWS:")
print("=" * 100)

try:
    wb = excel.Workbooks.Open(playbook_path, ReadOnly=True)
    ws = wb.Sheets.Item(1)
    
    last_row = ws.Cells.SpecialCells(11).Row
    last_col = ws.Cells.SpecialCells(11).Column
    
    for row in range(1, last_row + 1):
        row_data = []
        for col in range(1, last_col + 1):
            val = ws.Cells(row, col).Value
            row_data.append(str(val) if val is not None else "")
        print(f"{row:3d}: {row_data}")
    
    wb.Close(SaveChanges=False)
except Exception as e:
    print(f"Error: {e}")

excel.Quit()
