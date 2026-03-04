"""
Merge AMP Roles Updated.xlsx data into the original AMP Roles.xlsx
Fills in Role and User ID columns for matching job codes
"""
import zipfile
import xml.etree.ElementTree as ET
import csv
from pathlib import Path
from copy import deepcopy

def extract_excel_data(file_path):
    """Extract job code, role, user_id from Excel file"""
    data = {}
    
    with zipfile.ZipFile(file_path, 'r') as zf:
        # Read shared strings
        strings_xml = zf.read('xl/sharedStrings.xml')
        strings_root = ET.fromstring(strings_xml)
        
        shared_strings = []
        for si in strings_root.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si'):
            t = si.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')
            if t is not None:
                shared_strings.append(t.text or '')
        
        # Read worksheet
        sheet_xml = zf.read('xl/worksheets/sheet1.xml')
        sheet_root = ET.fromstring(sheet_xml)
        
        rows = []
        for row_elem in sheet_root.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row'):
            row_data = []
            for cell in row_elem.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c'):
                v = cell.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
                if v is not None and v.text is not None:
                    try:
                        idx = int(v.text)
                        if idx < len(shared_strings):
                            row_data.append(shared_strings[idx])
                        else:
                            row_data.append('')
                    except:
                        row_data.append(v.text)
                else:
                    row_data.append('')
            
            if row_data:
                rows.append(row_data)
    
    # Parse rows (skip header)
    for row in rows[1:]:
        if len(row) >= 3:
            job_code = row[0].strip() if row[0] else ''
            role = row[1].strip() if len(row) > 1 and row[1] else ''
            user_id = row[2].strip() if len(row) > 2 and row[2] else ''
            
            if job_code:
                data[job_code] = {
                    'role': role,
                    'user_id': user_id
                }
    
    return data

def update_excel_with_data(target_file, lookup_data):
    """Update target Excel file with lookup data"""
    print(f"\n1. Extracting target file structure...")
    
    # Extract all files from target
    import tempfile
    temp_dir = tempfile.mkdtemp()
    
    with zipfile.ZipFile(target_file, 'r') as zf:
        zf.extractall(temp_dir)
    
    print(f"✓ Extracted to {temp_dir}")
    
    # Read current shared strings
    strings_path = Path(temp_dir) / 'xl' / 'sharedStrings.xml'
    strings_root = ET.parse(strings_path).getroot()
    
    shared_strings = []
    for si in strings_root.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si'):
        t = si.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')
        if t is not None:
            shared_strings.append(t.text or '')
    
    print(f"✓ Found {len(shared_strings)} existing strings")
    
    # Build string index map
    string_to_idx = {s: idx for idx, s in enumerate(shared_strings)}
    
    def get_string_idx(s):
        """Get or create string index"""
        s = str(s) if s is not None else ''
        if s not in string_to_idx:
            string_to_idx[s] = len(shared_strings)
            shared_strings.append(s)
        return string_to_idx[s]
    
    # Read worksheet
    print(f"\n2. Processing worksheet...")
    
    sheet_path = Path(temp_dir) / 'xl' / 'worksheets' / 'sheet1.xml'
    sheet_root = ET.parse(sheet_path).getroot()
    
    ns = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    
    updated_count = 0
    
    # Find all rows and update
    for row_elem in sheet_root.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row'):
        cells = row_elem.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c')
        
        if len(cells) >= 1:
            # Get job code from first cell
            first_cell = cells[0]
            v = first_cell.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
            
            if v is not None and v.text is not None:
                try:
                    job_code_idx = int(v.text)
                    if job_code_idx < len(shared_strings):
                        job_code = shared_strings[job_code_idx]
                        
                        if job_code in lookup_data:
                            # Update role and user_id
                            data = lookup_data[job_code]
                            
                            # Ensure we have at least 3 cells
                            while len(cells) < 3:
                                cells.append(None)
                            
                            # Update cell B (role) - index 1
                            if len(cells) > 1 and cells[1] is not None:
                                role_cell = cells[1]
                                role_v = role_cell.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
                                if role_v is None:
                                    role_v = ET.SubElement(role_cell, '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
                                role_v.text = str(get_string_idx(data['role']))
                                role_cell.set('t', 's')
                            
                            # Update cell C (user_id) - index 2
                            if len(cells) > 2 and cells[2] is not None:
                                uid_cell = cells[2]
                                uid_v = uid_cell.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
                                if uid_v is None:
                                    uid_v = ET.SubElement(uid_cell, '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
                                uid_v.text = str(get_string_idx(data['user_id']))
                                uid_cell.set('t', 's')
                            
                            updated_count += 1
                except Exception as e:
                    print(f"  Warning: {e}")
    
    print(f"✓ Updated {updated_count} rows with lookup data")
    
    # Update shared strings
    print(f"\n3. Updating shared strings...")
    
    new_strings_root = ET.Element('sst')
    new_strings_root.set('xmlns', 'http://schemas.openxmlformats.org/spreadsheetml/2006/main')
    new_strings_root.set('count', str(len(shared_strings)))
    new_strings_root.set('uniqueCount', str(len(shared_strings)))
    
    for s in shared_strings:
        si = ET.SubElement(new_strings_root, 'si')
        t = ET.SubElement(si, 't')
        t.text = s
    
    strings_path.write_bytes(ET.tostring(new_strings_root, encoding='utf-8'))
    print(f"✓ Updated strings to {len(shared_strings)} entries")
    
    # Update worksheet
    print(f"\n4. Saving worksheet...")
    sheet_path.write_bytes(ET.tostring(sheet_root, encoding='utf-8'))
    print(f"✓ Worksheet saved")
    
    # Repackage as ZIP
    print(f"\n5. Creating new XLSX file...")
    
    import shutil
    
    # Remove old file
    if target_file.exists():
        target_file.unlink()
    
    # Create new ZIP
    with zipfile.ZipFile(target_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in Path(temp_dir).rglob('*'):
            if file_path.is_file():
                arcname = str(file_path.relative_to(temp_dir))
                
                # Use no compression for [Content_Types].xml
                if arcname == '[Content_Types].xml':
                    zf.write(file_path, arcname, compress_type=zipfile.ZIP_STORED)
                else:
                    zf.write(file_path, arcname, compress_type=zipfile.ZIP_DEFLATED)
    
    # Clean up
    shutil.rmtree(temp_dir)
    
    print(f"✓ XLSX file created")
    print(f"✓ File size: {target_file.stat().st_size:,} bytes")
    
    return updated_count

print("\n" + "="*70)
print("MERGING AMP ROLES UPDATED DATA INTO ORIGINAL AMP ROLES.XLSX")
print("="*70)

try:
    # Load lookup from updated file
    updated_file = Path(r"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Job Codes\AMP Roles Updated.xlsx")
    
    print(f"\n📂 Loading lookup from: {updated_file.name}")
    lookup_data = extract_excel_data(updated_file)
    print(f"✓ Loaded {len(lookup_data)} job codes with roles and user IDs")
    
    # Show sample
    sample = list(lookup_data.items())[:3]
    print(f"\n  Sample lookup data:")
    for code, data in sample:
        print(f"    {code}: {data['role']} → {data['user_id']}")
    
    # Update original file
    target_file = Path(r"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Job Codes\AMP Roles.xlsx")
    
    print(f"\n📂 Updating: {target_file.name}")
    updated_count = update_excel_with_data(target_file, lookup_data)
    
    print(f"\n" + "="*70)
    print(f"✅ MERGE COMPLETE")
    print(f"="*70)
    print(f"Updated {updated_count} rows in AMP Roles.xlsx")
    print(f"\nFile: {target_file}")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
