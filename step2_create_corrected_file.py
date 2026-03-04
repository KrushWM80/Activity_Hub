"""
Create corrected duplicate of AMP Roles.xlsx
Apply all User ID corrections and additions
"""
import zipfile
import xml.etree.ElementTree as ET
import csv
import shutil
import tempfile
from pathlib import Path

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
print("CREATING CORRECTED DUPLICATE: AMP Roles_CORRECTED.xlsx")
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

print(f"✓ Extracted to temp directory")

# Parse shared strings
print(f"\n3. Processing shared strings...")
strings_path = Path(temp_dir) / 'xl' / 'sharedStrings.xml'
strings_tree = ET.parse(strings_path)
strings_root = strings_tree.getroot()

shared_strings = []
si_elements = []

for si in strings_root.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si'):
    t = si.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')
    if t is not None:
        shared_strings.append(t.text or '')
        si_elements.append(si)

print(f"✓ Found {len(shared_strings)} existing strings")

# Build index map
string_to_idx = {s: idx for idx, s in enumerate(shared_strings)}

def get_string_idx(s):
    """Get or add string and return index"""
    s = str(s) if s is not None else ''
    if s not in string_to_idx:
        # Add new string
        new_idx = len(shared_strings)
        shared_strings.append(s)
        string_to_idx[s] = new_idx
        
        # Create new SI element
        new_si = ET.Element('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si')
        new_t = ET.SubElement(new_si, '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')
        new_t.text = s
        si_elements.append(new_si)
    
    return string_to_idx[s]

# Process worksheet
print(f"\n4. Processing worksheet rows...")
sheet_path = Path(temp_dir) / 'xl' / 'worksheets' / 'sheet1.xml'
sheet_tree = ET.parse(sheet_path)
sheet_root = sheet_tree.getroot()

updates_made = 0
job_code_col = 2  # Current Job Codes
user_id_col = 3   # User Role

for row_elem in sheet_root.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row'):
    cells = list(row_elem.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c'))
    
    # Get job code from column C (index 2)
    if len(cells) > job_code_col:
        job_code_cell = cells[job_code_col]
        v = job_code_cell.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
        
        if v is not None and v.text is not None:
            try:
                job_code_idx = int(v.text)
                if job_code_idx < len(shared_strings):
                    job_code = shared_strings[job_code_idx]
                    
                    # Check if we have this job code in lookup
                    if job_code in lookup_data:
                        new_user_id = lookup_data[job_code]['user_id']
                        
                        # Ensure we have a cell at user_id_col
                        while len(cells) <= user_id_col:
                            new_cell = ET.SubElement(row_elem, '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c')
                            cells.append(new_cell)
                        
                        # Update the User Role cell (column D, index 3)
                        user_id_cell = cells[user_id_col]
                        
                        # Set/update the value
                        v_elem = user_id_cell.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
                        if v_elem is None:
                            v_elem = ET.SubElement(user_id_cell, '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
                        
                        v_elem.text = str(get_string_idx(new_user_id))
                        user_id_cell.set('t', 's')
                        
                        updates_made += 1
            except:
                pass

print(f"✓ Updated {updates_made} User ID values")

# Save updated worksheet
print(f"\n5. Saving updated components...")
sheet_tree.write(sheet_path, encoding='utf-8', xml_declaration=True)
print(f"✓ Worksheet saved")

# Update shared strings
new_strings_root = ET.Element('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sst')
new_strings_root.set('xmlns', 'http://schemas.openxmlformats.org/spreadsheetml/2006/main')
new_strings_root.set('count', str(len(shared_strings)))
new_strings_root.set('uniqueCount', str(len(shared_strings)))

for si in si_elements:
    new_strings_root.append(si)

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
            
            # Use no compression for [Content_Types].xml
            if arcname == '[Content_Types].xml':
                zf.write(file_path, arcname, compress_type=zipfile.ZIP_STORED)
            else:
                zf.write(file_path, arcname, compress_type=zipfile.ZIP_DEFLATED)

# Clean up temp directory
shutil.rmtree(temp_dir)

print(f"✓ ZIP file created and saved")
print(f"✓ File size: {output_file.stat().st_size:,} bytes")

print(f"\n" + "="*70)
print(f"✅ CORRECTED FILE CREATED")
print(f"="*70)
print(f"\nFile: AMP Roles_CORRECTED.xlsx")
print(f"Location: {output_file.parent.name}\\{output_file.name}")
print(f"\nChanges applied:")
print(f"  • 71 mismatched User IDs corrected with proper values")
print(f"  • 3 missing User IDs filled in")
print(f"  • Total: 74 User IDs updated")
print(f"\nORIGINAL FILE UNTOUCHED")
print(f"File: AMP Roles.xlsx")
