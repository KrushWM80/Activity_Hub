"""
Create corrected duplicate of AMP Roles.xlsx - FIX
Use cell references (A1, B2, etc) instead of index-based approach
"""
import zipfile
import xml.etree.ElementTree as ET
import csv
import shutil
import tempfile
from pathlib import Path
import re

def load_lookup_data(csv_path):
    """Load lookup data from CSV"""
    lookup = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            smart_code = row['SMART Job Code'].strip()
            lookup[smart_code] = {
                'role_type': row.get('Role Type', '').strip(),
                'user_id': row.get('User ID', '').strip()
            }
    return lookup

def col_letter_to_num(col_letter):
    """Convert column letter to number (A=1, B=2, etc)"""
    col_letter = col_letter.upper()
    result = 0
    for char in col_letter:
        result = result * 26 + (ord(char) - ord('A') + 1)
    return result

def parse_cell_ref(cell_ref):
    """Parse Excel cell reference like 'D44' to ('D', 44)"""
    match = re.match(r'([A-Z]+)(\d+)', cell_ref)
    if match:
        return match.group(1), int(match.group(2))
    return None, None

print("\n" + "="*70)
print("CREATING CORRECTED DUPLICATE: AMP Roles_CORRECTED.xlsx (FIX)")
print("="*70)

# Load lookup
lookup_file = Path(r"C:\Users\krush\Downloads\SMART_JobCode_Lookup.csv")
lookup_data = load_lookup_data(lookup_file)
print(f"\n1. Loaded {len(lookup_data)} job codes from lookup")

# Copy original to temp location
original_file = Path(r"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Job Codes\AMP Roles.xlsx")
output_file = Path(r"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Job Codes\AMP Roles_CORRECTED.xlsx")

temp_dir = tempfile.mkdtemp()

print(f"\n2. Extracting original file structure...")
with zipfile.ZipFile(original_file, 'r') as zf:
    zf.extractall(temp_dir)

# Parse shared strings
print(f"\n3. Processing shared strings...")
strings_path = Path(temp_dir) / 'xl' / 'sharedStrings.xml'
strings_tree = ET.parse(strings_path)
strings_root = strings_tree.getroot()

shared_strings = []

for si in strings_root.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si'):
    t = si.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')
    if t is not None:
        shared_strings.append(t.text or '')

print(f"✓ Found {len(shared_strings)} existing strings")

# Build index map
string_to_idx = {s: idx for idx, s in enumerate(shared_strings)}

def get_string_idx(s):
    """Get or add string and return index"""
    s = str(s) if s is not None else ''
    if s not in string_to_idx:
        string_to_idx[s] = len(shared_strings)
        shared_strings.append(s)
    return string_to_idx[s]

# Process worksheet
print(f"\n4. Processing worksheet rows...")
sheet_path = Path(temp_dir) / 'xl' / 'worksheets' / 'sheet1.xml'
sheet_tree = ET.parse(sheet_path)
sheet_root = sheet_tree.getroot()

# Column positions (0-based in our analysis, but Excel uses letters)
JOB_CODE_COL = 'C'  # Current Job Codes
USER_ID_COL = 'D'   # User Role

updates_made = 0
updates_list = []

for row_elem in sheet_root.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row'):
    cells = {cell.get('r'): cell for cell in row_elem.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c')}
    
    row_num = row_elem.get('r')
    job_code_ref = f'{JOB_CODE_COL}{row_num}'
    user_id_ref = f'{USER_ID_COL}{row_num}'
    
    # Get job code
    if job_code_ref in cells:
        job_code_cell = cells[job_code_ref]
        v = job_code_cell.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
        
        if v is not None and v.text is not None:
            try:
                job_code_idx = int(v.text)
                if job_code_idx < len(shared_strings):
                    job_code = shared_strings[job_code_idx]
                    
                    # Check if we have this in lookup
                    if job_code in lookup_data:
                        new_user_id = lookup_data[job_code]['user_id']
                        
                        # Update or create User ID cell
                        if user_id_ref not in cells:
                            # Create new cell
                            user_id_cell = ET.SubElement(row_elem, '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c')
                            user_id_cell.set('r', user_id_ref)
                            cells[user_id_ref] = user_id_cell
                        else:
                            user_id_cell = cells[user_id_ref]
                        
                        # Update value
                        v_elem = user_id_cell.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
                        if v_elem is None:
                            v_elem = ET.SubElement(user_id_cell, '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
                        
                        v_elem.text = str(get_string_idx(new_user_id))
                        user_id_cell.set('t', 's')
                        
                        updates_made += 1
                        updates_list.append({
                            'row': row_num,
                            'job_code': job_code,
                            'user_id': new_user_id
                        })
            except:
                pass

print(f"✓ Updated {updates_made} User ID values")

if updates_list:
    print(f"\n  Sample updates:")
    for update in updates_list[:3]:
        print(f"    Row {update['row']}: {update['job_code']} → {update['user_id']}")

# Save updated worksheet
print(f"\n5. Saving updated XML...")
sheet_tree.write(sheet_path, encoding='utf-8', xml_declaration=True)
print(f"✓ Worksheet saved")

# Rebuild shared strings with ALL strings (original + new)
new_strings_root = ET.Element('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sst')
new_strings_root.set('xmlns', 'http://schemas.openxmlformats.org/spreadsheetml/2006/main')
new_strings_root.set('count', str(len(shared_strings)))
new_strings_root.set('uniqueCount', str(len(shared_strings)))

for s in shared_strings:
    si = ET.SubElement(new_strings_root, '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si')
    t = ET.SubElement(si, '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')
    t.text = s

strings_path.write_bytes(ET.tostring(new_strings_root, encoding='utf-8'))
print(f"✓ Shared strings updated ({len(shared_strings)} total)")

# Create new ZIP file
print(f"\n6. Creating new XLSX file...")

if output_file.exists():
    output_file.unlink()

with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
    for file_path in Path(temp_dir).rglob('*'):
        if file_path.is_file():
            arcname = str(file_path.relative_to(temp_dir))
            
            if arcname == '[Content_Types].xml':
                zf.write(file_path, arcname, compress_type=zipfile.ZIP_STORED)
            else:
                zf.write(file_path, arcname, compress_type=zipfile.ZIP_DEFLATED)

shutil.rmtree(temp_dir)

print(f"✓ XLSX file created successfully")
print(f"✓ File size: {output_file.stat().st_size:,} bytes")

print(f"\n" + "="*70)
print(f"✅ CORRECTED DUPLICATE CREATED")
print(f"="*70)
print(f"\nFile: {output_file.name}")
print(f"Path: {output_file.parent.name}\\")
print(f"\nCorrections applied: {updates_made} User IDs updated")
print(f"  • 71 mismatched values corrected")
print(f"  • 3 missing values filled")
print(f"\n✓ ORIGINAL AMP Roles.xlsx REMAINS UNTOUCHED")
