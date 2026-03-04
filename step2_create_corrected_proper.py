"""
Create corrected duplicate - PROPER VERSION
Find sheetData first, then process rows
"""
import zipfile
import xml.etree.ElementTree as ET
import csv
import shutil
import tempfile
from pathlib import Path

NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

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

print("\n" + "="*70)
print("CREATING CORRECTED DUPLICATE - AMP Roles_CORRECTED.xlsx")
print("="*70)

# Load lookup
lookup_file = Path(r"C:\Users\krush\Downloads\SMART_JobCode_Lookup.csv")
lookup_data = load_lookup_data(lookup_file)
print(f"\n1. Loaded {len(lookup_data)} job codes")

# Setup
original_file = Path(r"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Job Codes\AMP Roles.xlsx")
output_file = Path(r"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Job Codes\AMP Roles_CORRECTED.xlsx")

temp_dir = tempfile.mkdtemp()

print(f"\n2. Extracting original file...")
with zipfile.ZipFile(original_file, 'r') as zf:
    zf.extractall(temp_dir)

# Parse shared strings
print(f"\n3. Loading shared strings...")
strings_path = Path(temp_dir) / 'xl' / 'sharedStrings.xml'
strings_tree = ET.parse(strings_path)
strings_root = strings_tree.getroot()

shared_strings = []
for si in strings_root.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si'):
    t = si.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')
    if t is not None:
        shared_strings.append(t.text or '')

print(f"✓ {len(shared_strings)} strings loaded")

string_to_idx = {s: idx for idx, s in enumerate(shared_strings)}

def get_string_idx(s):
    """Get or add string"""
    s = str(s) if s is not None else ''
    if s not in string_to_idx:
        string_to_idx[s] = len(shared_strings)
        shared_strings.append(s)
    return string_to_idx[s]

# Process worksheet
print(f"\n4. Processing worksheet...")
sheet_path = Path(temp_dir) / 'xl' / 'worksheets' / 'sheet1.xml'
sheet_tree = ET.parse(sheet_path)
sheet_root = sheet_tree.getroot()

JOB_CODE_COL = 'C'  # Current Job Codes (column C)
USER_ID_COL = 'D'   # User Role (column D)

updates_made = 0

# Find sheetData element
ns_uri = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
sheet_data = sheet_root.find(f'{ns_uri}sheetData')

if sheet_data is None:
    print(f"❌ SheetData not found!")
else:
    print(f"✓ Found sheetData with {len(list(sheet_data))} rows")
    
    # Process each row
    for row_elem in sheet_data.findall(f'{ns_uri}row'):
        row_num = row_elem.get('r')
        
        # Build dict of cells by reference
        cells_dict = {}
        for cell in row_elem.findall(f'{ns_uri}c'):
            cell_ref = cell.get('r')
            cells_dict[cell_ref] = cell
        
        # Get job code
        job_code_ref = f'{JOB_CODE_COL}{row_num}'
        user_id_ref = f'{USER_ID_COL}{row_num}'
        
        if job_code_ref in cells_dict:
            job_code_cell = cells_dict[job_code_ref]
            v = job_code_cell.find(f'{ns_uri}v')
            
            if v is not None and v.text is not None:
                try:
                    idx = int(v.text)
                    if idx < len(shared_strings):
                        job_code = shared_strings[idx]
                        
                        if job_code in lookup_data:
                            new_user_id = lookup_data[job_code]['user_id']
                            
                            # Update or create User ID cell
                            if user_id_ref not in cells_dict:
                                # Create new cell
                                user_id_cell = ET.SubElement(row_elem, f'{ns_uri}c')
                                user_id_cell.set('r', user_id_ref)
                                cells_dict[user_id_ref] = user_id_cell
                            else:
                                user_id_cell = cells_dict[user_id_ref]
                            
                            # Set value
                            v_elem = user_id_cell.find(f'{ns_uri}v')
                            if v_elem is None:
                                v_elem = ET.SubElement(user_id_cell, f'{ns_uri}v')
                            
                            v_elem.text = str(get_string_idx(new_user_id))
                            user_id_cell.set('t', 's')
                            
                            updates_made += 1
                except:
                    pass

print(f"✓ Updated {updates_made} User ID values")

# Save worksheet
print(f"\n5. Saving updated worksheet...")
sheet_tree.write(sheet_path, encoding='utf-8', xml_declaration=True)

# Rebuild shared strings
new_strings_root = ET.Element(f'{ns_uri}sst')
new_strings_root.set('xmlns', 'http://schemas.openxmlformats.org/spreadsheetml/2006/main')
new_strings_root.set('count', str(len(shared_strings)))
new_strings_root.set('uniqueCount', str(len(shared_strings)))

for s in shared_strings:
    si = ET.SubElement(new_strings_root, f'{ns_uri}si')
    t = ET.SubElement(si, f'{ns_uri}t')
    t.text = s

strings_path.write_bytes(ET.tostring(new_strings_root, encoding='utf-8'))
print(f"✓ Saved {len(shared_strings)} strings")

# Create new ZIP
print(f"\n6. Creating XLSX file...")
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

print(f"✓ File size: {output_file.stat().st_size:,} bytes")

print(f"\n" + "="*70)
print(f"✅ SUCCESS - CORRECTED DUPLICATE CREATED")
print(f"="*70)
print(f"\nNew file: {output_file.name}")
print(f"Updates: {updates_made} User IDs")
print(f"\n✓ Original AMP Roles.xlsx UNCHANGED")
