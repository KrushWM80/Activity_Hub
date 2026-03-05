"""
Create AMP Roles Updated.xlsx - Complete fresh build from CSV lookup only
"""
import zipfile
import xml.etree.ElementTree as ET
import csv
from pathlib import Path

def create_fresh_excel():
    """Build Excel entirely from lookup data"""
    print("\n" + "="*70)
    print("CREATING FRESH AMP ROLES UPDATED.XLSX")
    print("="*70)
    
    # 1. Load lookup data
    lookup_path = Path(r"C:\Users\krush\Downloads\SMART_JobCode_Lookup.csv")
    if not lookup_path.exists():
        print(f"❌ Lookup not found: {lookup_path}")
        return False
    
    lookup_data = []
    with open(lookup_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            lookup_data.append({
                'job_code': row['SMART Job Code'].strip(),
                'role_type': row.get('Role Type', '').strip(),
                'user_id': row.get('User ID', '').strip()
            })
    
    print(f"✓ Loaded {len(lookup_data)} job codes from lookup")
    
    # 2. Build shared strings
    print("\n1. Creating shared strings...")
    
    shared_strings = []
    string_to_idx = {}
    
    def get_string_idx(s):
        s = str(s) if s is not None else ''
        if s not in string_to_idx:
            string_to_idx[s] = len(shared_strings)
            shared_strings.append(s)
        return string_to_idx[s]
    
    # Pre-populate header
    header = ['Current Job Code', 'Role Type', 'User ID']
    for h in header:
        get_string_idx(h)
    
    # Add all lookup strings
    for item in lookup_data:
        get_string_idx(item['job_code'])
        get_string_idx(item['role_type'])
        get_string_idx(item['user_id'])
    
    print(f"✓ Created {len(shared_strings)} unique strings")
    
    # 3. Create sharedStrings.xml
    print("\n2. Building sharedStrings.xml...")
    
    sst_root = ET.Element('sst')
    sst_root.set('xmlns', 'http://schemas.openxmlformats.org/spreadsheetml/2006/main')
    sst_root.set('count', str(len(shared_strings)))
    sst_root.set('uniqueCount', str(len(shared_strings)))
    
    for s in shared_strings:
        si = ET.SubElement(sst_root, 'si')
        t = ET.SubElement(si, 't')
        t.text = s
    
    sst_str = ET.tostring(sst_root, encoding='utf-8')
    print(f"✓ sharedStrings.xml: {len(sst_str)} bytes")
    
    # 4. Create worksheet
    print("\n3. Building worksheet...")
    
    ws_root = ET.Element('worksheet')
    ws_root.set('xmlns', 'http://schemas.openxmlformats.org/spreadsheetml/2006/main')
    ws_root.set('xmlns:r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')
    
    sheet_data = ET.SubElement(ws_root, 'sheetData')
    
    # Header row
    header_row = ET.SubElement(sheet_data, 'row')
    header_row.set('r', '1')
    
    for col_idx, header_val in enumerate(header, 1):
        cell = ET.SubElement(header_row, 'c')
        cell.set('r', f'{chr(64+col_idx)}1')
        cell.set('t', 's')
        v = ET.SubElement(cell, 'v')
        v.text = str(get_string_idx(header_val))
    
    # Data rows
    for row_idx, item in enumerate(lookup_data, 2):
        row = ET.SubElement(sheet_data, 'row')
        row.set('r', str(row_idx))
        
        # Column A: Job Code
        cell = ET.SubElement(row, 'c')
        cell.set('r', f'A{row_idx}')
        cell.set('t', 's')
        v = ET.SubElement(cell, 'v')
        v.text = str(get_string_idx(item['job_code']))
        
        # Column B: Role Type
        cell = ET.SubElement(row, 'c')
        cell.set('r', f'B{row_idx}')
        cell.set('t', 's')
        v = ET.SubElement(cell, 'v')
        v.text = str(get_string_idx(item['role_type']))
        
        # Column C: User ID
        cell = ET.SubElement(row, 'c')
        cell.set('r', f'C{row_idx}')
        cell.set('t', 's')
        v = ET.SubElement(cell, 'v')
        v.text = str(get_string_idx(item['user_id']))
    
    ws_str = ET.tostring(ws_root, encoding='utf-8')
    print(f"✓ Worksheet: {len(ws_str)} bytes, {len(lookup_data)} data rows")
    
    # 5. Create workbook.xml
    print("\n4. Building workbook.xml...")
    
    wb_root = ET.Element('workbook')
    wb_root.set('xmlns', 'http://schemas.openxmlformats.org/spreadsheetml/2006/main')
    wb_root.set('xmlns:r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')
    
    sheets = ET.SubElement(wb_root, 'sheets')
    sheet = ET.SubElement(sheets, 'sheet')
    sheet.set('name', 'AMP Roles')
    sheet.set('sheetId', '1')
    sheet.set('r:id', 'rId1')
    
    wb_str = ET.tostring(wb_root, encoding='utf-8')
    print(f"✓ Workbook: {len(wb_str)} bytes")
    
    # 6. Build XLSX file
    print("\n5. Building XLSX package...")
    
    output_path = Path(r"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Job Codes\AMP Roles Updated.xlsx")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Remove old file if exists
    if output_path.exists():
        output_path.unlink()
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # [Content_Types].xml (no compression)
        ct_xml = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
</Types>'''
        zf.writestr('[Content_Types].xml', ct_xml, compress_type=zipfile.ZIP_STORED)
        
        # _rels/.rels
        rels_xml = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
</Relationships>'''
        zf.writestr('_rels/.rels', rels_xml, compress_type=zipfile.ZIP_STORED)
        
        # xl/_rels/workbook.xml.rels
        xl_rels = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>
</Relationships>'''
        zf.writestr('xl/_rels/workbook.xml.rels', xl_rels, compress_type=zipfile.ZIP_STORED)
        
        # Core properties
        core_xml = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<dc:creator>AMP System</dc:creator>
<dc:created xsi:type="dcterms:W3CDTF">2026-03-03T14:38:00Z</dc:created>
</cp:coreProperties>'''
        zf.writestr('docProps/core.xml', core_xml, compress_type=zipfile.ZIP_STORED)
        
        # Add actual data files
        zf.writestr('xl/workbook.xml', wb_str)
        zf.writestr('xl/worksheets/sheet1.xml', ws_str)
        zf.writestr('xl/sharedStrings.xml', sst_str)
    
    print(f"\n6. Verifying...")
    
    # Verify ZIP
    with zipfile.ZipFile(output_path, 'r') as zf:
        test = zf.testzip()
        if test is None:
            print(f"✓ ZIP integrity: VALID")
        else:
            print(f"⚠ ZIP issue: {test}")
        
        files = zf.namelist()
        print(f"✓ Files in ZIP: {len(files)}")
    
    print(f"\n✓ File: {output_path}")
    print(f"✓ Size: {output_path.stat().st_size:,} bytes")
    
    return True

if __name__ == "__main__":
    print("\n" + "="*70)
    print("AMP ROLES UPDATED - FRESH BUILD")
    print("="*70)
    
    try:
        if create_fresh_excel():
            print("\n" + "="*70)
            print("✅ SUCCESS - AMP Roles Updated.xlsx created")
            print("="*70)
            print("\nYou can now open this file in Excel!")
        else:
            print("\n❌ Creation failed")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
