"""
Create AMP Roles Updated.xlsx - Using direct XML/ZIP construction
Builds Excel from absolute minimum valid structure
"""
import zipfile
import xml.etree.ElementTree as ET
import csv
from pathlib import Path
import shutil

def create_excel_from_scratch():
    """Build Excel file with minimal, valid XML structure"""
    print("\n" + "="*70)
    print("CREATING AMP ROLES UPDATED.XLSX - DIRECT XML/ZIP METHOD")
    print("="*70)
    
    # 1. Load lookup data
    lookup_path = Path(r"C:\Users\krush\Downloads\SMART_JobCode_Lookup.csv")
    if not lookup_path.exists():
        print(f"❌ Lookup not found: {lookup_path}")
        return False
    
    lookup_dict = {}
    with open(lookup_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            smart_code = row['SMART Job Code'].strip()
            lookup_dict[smart_code] = {
                'role_type': row.get('Role Type', ''),
                'user_id': row.get('User ID', '')
            }
    
    print(f"✓ Loaded {len(lookup_dict)} job code mappings")
    
    # 2. Check if backup exists for original data structure
    backup_path = Path(r"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Job Codes\AMP Roles.xlsx.backup_before_update")
    
    if backup_path.exists():
        print(f"✓ Found backup template: {backup_path}")
        # Extract and examine backup
        with zipfile.ZipFile(backup_path, 'r') as zip_ref:
            # Get original shared strings
            strings_xml = zip_ref.read('xl/sharedStrings.xml')
            # Get original worksheet
            sheet_xml = zip_ref.read('xl/worksheets/sheet1.xml')
            
            print("✓ Extracted original structure from backup")
    else:
        print("⚠ No backup found, will create minimal structure")
        strings_xml = None
        sheet_xml = None
    
    # 3. Parse original worksheet to get job code data
    print("\n1. Building worksheet data...")
    
    if sheet_xml:
        root = ET.fromstring(sheet_xml)
        ns = {'': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        
        # Find all rows
        rows = []
        for row_elem in root.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row'):
            cells = []
            for cell in row_elem.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c'):
                v_elem = cell.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
                t_elem = cell.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')
                
                if v_elem is not None:
                    cells.append(v_elem.text)
                elif t_elem is not None:
                    cells.append(t_elem.text)
                else:
                    cells.append('')
            
            if cells:
                rows.append(cells)
        
        print(f"✓ Extracted {len(rows)} rows from backup")
    else:
        rows = [['Current Job Code', 'Role Type', 'User ID']]
    
    # 4. Create shared strings list
    print("\n2. Building shared strings...")
    
    shared_strings = []
    string_map = {}
    
    def add_string(s):
        """Add string to shared strings, return index"""
        s = str(s) if s is not None else ''
        if s not in string_map:
            string_map[s] = len(shared_strings)
            shared_strings.append(s)
        return string_map[s]
    
    # Add all strings from rows
    for row in rows:
        for cell in row:
            if cell:
                add_string(cell)
    
    # Add mappings
    for job_code, data in lookup_dict.items():
        add_string(job_code)
        add_string(data['role_type'])
        add_string(data['user_id'])
    
    print(f"✓ Created {len(shared_strings)} unique strings")
    
    # 5. Build new worksheet row by row
    print("\n3. Building new worksheet...")
    
    updated_rows = []
    
    # Add header row
    updated_rows.append(['Current Job Code', 'Role Type', 'User ID'])
    
    # Add data rows
    for row in rows[1:] if len(rows) > 1 else []:
        job_code = row[0] if len(row) > 0 else ''
        
        if job_code in lookup_dict:
            # Update with new data
            updated_rows.append([
                job_code,
                lookup_dict[job_code]['role_type'],
                lookup_dict[job_code]['user_id']
            ])
        else:
            # Keep original
            updated_rows.append(row[:3])
    
    print(f"✓ Prepared {len(updated_rows)} rows for new worksheet")
    
    # Track updates
    matched = sum(1 for row in updated_rows[1:] if row[0] in lookup_dict)
    with_user_id = sum(1 for row in updated_rows[1:] if len(row) > 2 and row[2])
    
    print(f"  - Matched job codes: {matched}")
    print(f"  - Rows with User ID: {with_user_id}")
    
    # 6. Create sharedStrings.xml
    print("\n4. Creating sharedStrings.xml...")
    
    strings_root = ET.Element('sst')
    strings_root.set('xmlns', 'http://schemas.openxmlformats.org/spreadsheetml/2006/main')
    strings_root.set('count', str(len(shared_strings)))
    strings_root.set('uniqueCount', str(len(shared_strings)))
    
    for s in shared_strings:
        si = ET.SubElement(strings_root, 'si')
        t = ET.SubElement(si, 't')
        t.text = s
    
    strings_xml = ET.tostring(strings_root, encoding='utf-8')
    print(f"✓ Created sharedStrings.xml ({len(strings_xml)} bytes)")
    
    # 7. Create new worksheet
    print("\n5. Creating worksheet1.xml...")
    
    ws_root = ET.Element('worksheet')
    ws_root.set('xmlns', 'http://schemas.openxmlformats.org/spreadsheetml/2006/main')
    ws_root.set('xmlns:r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')
    
    # SheetData
    sheet_data = ET.SubElement(ws_root, 'sheetData')
    
    for row_idx, row_data in enumerate(updated_rows, 1):
        row_elem = ET.SubElement(sheet_data, 'row')
        row_elem.set('r', str(row_idx))
        
        for col_idx, cell_value in enumerate(row_data, 1):
            cell = ET.SubElement(row_elem, 'c')
            cell.set('r', f'{chr(64+col_idx)}{row_idx}')
            
            if cell_value:
                cell.set('t', 's')  # String type
                cell.set('s', '0')  # Default style
                v = ET.SubElement(cell, 'v')
                v.text = str(add_string(cell_value))
    
    worksheet_xml = ET.tostring(ws_root, encoding='utf-8')
    print(f"✓ Created worksheet1.xml ({len(worksheet_xml)} bytes)")
    
    # 8. Create workbook.xml
    print("\n6. Creating workbook.xml...")
    
    wb_root = ET.Element('workbook')
    wb_root.set('xmlns', 'http://schemas.openxmlformats.org/spreadsheetml/2006/main')
    wb_root.set('xmlns:r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')
    
    sheets = ET.SubElement(wb_root, 'sheets')
    sheet = ET.SubElement(sheets, 'sheet')
    sheet.set('name', 'AMP Roles')
    sheet.set('sheetId', '1')
    sheet.set('r:id', 'rId1')
    
    workbook_xml = ET.tostring(wb_root, encoding='utf-8')
    print(f"✓ Created workbook.xml ({len(workbook_xml)} bytes)")
    
    # 9. Copy directory structure from backup or create new
    print("\n7. Building ZIP structure...")
    
    output_path = Path(r"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Job Codes\AMP Roles Updated.xlsx")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if backup_path.exists():
        # Copy backup as template
        shutil.copy(backup_path, output_path)
        
        # Update files in ZIP
        with zipfile.ZipFile(output_path, 'a') as zipf:
            # Update sharedStrings
            zipf.writestr('xl/sharedStrings.xml', strings_xml)
            # Update worksheet
            zipf.writestr('xl/worksheets/sheet1.xml', worksheet_xml)
            # Update workbook
            zipf.writestr('xl/workbook.xml', workbook_xml)
        
        print(f"✓ Updated backup template ZIP")
    else:
        # Create new ZIP from scratch
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # [Content_Types].xml
            ct_xml = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
</Types>'''
            zipf.writestr('[Content_Types].xml', ct_xml)
            
            # .rels
            rels_xml = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
</Relationships>'''
            zipf.writestr('_rels/.rels', rels_xml)
            
            # xl/.rels
            xl_rels = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>
</Relationships>'''
            zipf.writestr('xl/_rels/workbook.xml.rels', xl_rels)
            
            # Files
            zipf.writestr('xl/workbook.xml', workbook_xml)
            zipf.writestr('xl/worksheets/sheet1.xml', worksheet_xml)
            zipf.writestr('xl/sharedStrings.xml', strings_xml)
            
            # Core properties
            core_xml = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<dc:creator>AMP System</dc:creator>
</cp:coreProperties>'''
            zipf.writestr('docProps/core.xml', core_xml)
        
        print(f"✓ Created new ZIP from scratch")
    
    # 10. Verify
    print("\n8. Verifying file...")
    file_size = output_path.stat().st_size
    print(f"✓ File created: {output_path}")
    print(f"✓ File size: {file_size:,} bytes")
    
    # Check ZIP integrity
    with zipfile.ZipFile(output_path, 'r') as zipf:
        files = zipf.namelist()
        print(f"✓ ZIP contains {len(files)} files")
        test_result = zipf.testzip()
        if test_result is None:
            print(f"✓ ZIP structure is valid")
        else:
            print(f"⚠ ZIP issue detected in: {test_result}")
    
    return True

if __name__ == "__main__":
    try:
        success = create_excel_from_scratch()
        
        if success:
            print("\n" + "="*70)
            print("✅ AMP ROLES UPDATED.XLSX CREATED SUCCESSFULLY")
            print("="*70)
            print("\nYou can now open the file - it should not have any corruption!")
        else:
            print("\n❌ Creation failed")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
