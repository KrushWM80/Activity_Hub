import pandas as pd
import win32com.client as win32
from datetime import datetime
from pathlib import Path

file_path = r"C:\Users\krush\OneDrive - Walmart Inc\AGE Team - Documents\Activity - Walmart US\Reporting\Data\Me@\MM\Input\Playbook Hub and Active Playbooks - Weekly Report.xlsx"

excel = win32.gencache.EnsureDispatch('Excel.Application')
excel.Visible = False
workbook = excel.Workbooks.Open(file_path)

playbook_categories = ['Playbook Hub', 'Valentines', 'Baby Days', 'Easter']
playbook_rows = []
report_date = datetime.now().date()
extracted_date = datetime.now()

# Read all sheets
for sheet_index in range(1, workbook.Sheets.Count + 1):
    worksheet = workbook.Sheets(sheet_index)
    sheet_name = worksheet.Name
    
    # Try to match to category
    matched_category = None
    for cat in playbook_categories:
        if cat.lower() in sheet_name.lower():
            matched_category = cat
            break
    
    if not matched_category:
        print(f"Skipping sheet (no category match): {sheet_name}")
        continue
    
    print(f"\nProcessing sheet: {sheet_name} -> Category: {matched_category}")
    
    # Read used range
    usedRange = worksheet.UsedRange
    data = usedRange.Value
    
    if not data:
        continue
    
    # Convert to DataFrame
    try:
        df = pd.DataFrame(list(data[1:]), columns=data[0])
        print(f"  DataFrame shape: {df.shape}")
        print(f"  Columns: {df.columns.tolist()}")
        
        # Show first few rows
        print(f"  First 5 rows:")
        for idx, row in df.head(5).iterrows():
            page_name = row.iloc[0] if len(row) > 0 else None
            print(f"    {idx}: {page_name}")
        
        # Check for duplicates
        page_names = df.iloc[:, 0].dropna()
        dups = page_names[page_names.duplicated(keep=False)]
        if not dups.empty:
            print(f"  WARNING: Found {len(dups)} duplicate page names!")
            for name in dups.unique():
                print(f"    - {name}")
    except Exception as e:
        print(f"  Error: {e}")

workbook.Close(False)
excel.Quit()
