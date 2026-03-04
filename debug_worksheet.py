"""
Debug: Inspect actual worksheet structure
"""
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

original_file = Path(r"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Job Codes\AMP Roles.xlsx")

with zipfile.ZipFile(original_file, 'r') as zf:
    # Get shared strings
    strings_xml = zf.read('xl/sharedStrings.xml')
    strings_root = ET.fromstring(strings_xml)
    
    shared_strings = []
    for si in strings_root.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si'):
        t = si.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')
        if t is not None:
            shared_strings.append(t.text or '')
    
    # Get worksheet
    sheet_xml = zf.read('xl/worksheets/sheet1.xml')
    sheet_root = ET.fromstring(sheet_xml)
    
    print("="*70)
    print("WORKSHEET STRUCTURE - DEBUG")
    print("="*70)
    
    row_count = 0
    for row_elem in sheet_root.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row')[:5]:
        row_count += 1
        row_num = row_elem.get('r')
        print(f"\nRow {row_num}:")
        
        cells = row_elem.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c')
        print(f"  Cell count: {len(cells)}")
        
        for idx, cell in enumerate(cells):
            cell_ref = cell.get('r')
            v = cell.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
            
            if v is not None and v.text is not None:
                try:
                    str_idx = int(v.text)
                    if str_idx < len(shared_strings):
                        value = shared_strings[str_idx]
                        print(f"    {cell_ref}: [{str_idx}] = '{value}'")
                except:
                    print(f"    {cell_ref}: {v.text} (raw)")
    
    print(f"\nTotal rows in worksheet: {len(list(sheet_root.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row')))}")
    print(f"Total shared strings: {len(shared_strings)}")
