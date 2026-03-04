"""
Debug: Find the actual worksheet structure
"""
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

original_file = Path(r"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Job Codes\AMP Roles.xlsx")

print("Checking files in ZIP...")
with zipfile.ZipFile(original_file, 'r') as zf:
    print("ZIP contains:")
    for name in zf.namelist():
        if 'sheet' in name.lower():
            print(f"  {name}")

# Try reading sheet differently
with zipfile.ZipFile(original_file, 'r') as zf:
    sheet_xml = zf.read('xl/worksheets/sheet1.xml')
    
    # Parse with namespace handling
    ET.register_namespace('', 'http://schemas.openxmlformats.org/spreadsheetml/2006/main')
    root = ET.fromstring(sheet_xml)
    
    # Print first 500 chars of XML to see structure
    print("\nFirst 1000 chars of sheet XML:")
    sheet_str = sheet_xml.decode('utf-8')
    print(sheet_str[:1000])
    
    # Try to find elements without namespace
    print("\n\nElements directly in root:")
    for child in root:
        print(f"  {child.tag}")
        if 'sheetData' in child.tag:
            print(f"    SheetData found, children count: {len(list(child))}")
            for subchild in list(child)[:3]:
                print(f"      {subchild.tag}")
