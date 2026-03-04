"""
1. Read original AMP Roles.xlsx
2. Verify existing User IDs against lookup
3. Identify missing User IDs
4. Create detailed report of changes needed
5. Duplicate file with all corrections applied
"""
import zipfile
import xml.etree.ElementTree as ET
import csv
from pathlib import Path
from copy import deepcopy

def read_excel_file(file_path):
    """Read Excel file and extract all data"""
    data = []
    
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
    
    return rows

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
print("ANALYSIS: AMP Roles.xlsx - User ID Verification & Completion")
print("="*70)

# Step 1: Read original file
original_file = Path(r"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Job Codes\AMP Roles.xlsx")
print(f"\n1. Reading original file...")
print(f"   {original_file.name}")

original_rows = read_excel_file(original_file)
print(f"   ✓ Found {len(original_rows)} total rows (including header)")
print(f"   ✓ Header: {original_rows[0]}")

# Step 2: Load lookup data
lookup_file = Path(r"C:\Users\krush\Downloads\SMART_JobCode_Lookup.csv")
print(f"\n2. Loading lookup data...")
lookup_data = load_lookup_data(lookup_file)
print(f"   ✓ Loaded {len(lookup_data)} job codes from lookup")

# Step 3: Analyze current state
print(f"\n3. Analyzing current Job Codes and User IDs...")

# Determine column positions
header = original_rows[0]
print(f"   Header columns: {header}")

job_code_col = None
user_id_col = None

for idx, col_name in enumerate(header):
    col_lower = col_name.lower() if col_name else ''
    if 'job code' in col_lower:
        job_code_col = idx
    if 'user' in col_lower or 'role' in col_lower:
        if 'user' in col_lower:
            user_id_col = idx

print(f"\n   Job Code Column: {job_code_col} ({header[job_code_col] if job_code_col is not None else 'NOT FOUND'})")
print(f"   User ID Column: {user_id_col} ({header[user_id_col] if user_id_col is not None else 'NOT FOUND'})")

# Analyze each row
existing_ids = []      # Rows that already have User IDs
missing_ids = []       # Rows that are missing User IDs
invalid_ids = []       # Rows with User IDs that don't match lookup
replacements = []      # Rows where we'll replace with lookup data

for row_idx, row in enumerate(original_rows[1:], 2):  # Skip header
    if len(row) > job_code_col:
        job_code = row[job_code_col].strip() if job_code_col < len(row) else ''
        current_user_id = row[user_id_col].strip() if user_id_col is not None and user_id_col < len(row) else ''
        
        if job_code:
            if job_code in lookup_data:
                lookup_user_id = lookup_data[job_code]['user_id']
                
                if current_user_id:
                    # Has User ID - verify if it matches lookup
                    if current_user_id == lookup_user_id:
                        existing_ids.append({
                            'row': row_idx,
                            'job_code': job_code,
                            'current_user_id': current_user_id,
                            'status': 'VALID'
                        })
                    else:
                        # User ID exists but doesn't match lookup
                        invalid_ids.append({
                            'row': row_idx,
                            'job_code': job_code,
                            'current_user_id': current_user_id,
                            'correct_user_id': lookup_user_id,
                            'status': 'MISMATCH'
                        })
                        replacements.append({
                            'row': row_idx,
                            'job_code': job_code,
                            'old_user_id': current_user_id,
                            'new_user_id': lookup_user_id
                        })
                else:
                    # Missing User ID - provide from lookup
                    missing_ids.append({
                        'row': row_idx,
                        'job_code': job_code,
                        'lookup_user_id': lookup_user_id,
                        'status': 'MISSING'
                    })
                    replacements.append({
                        'row': row_idx,
                        'job_code': job_code,
                        'old_user_id': '',
                        'new_user_id': lookup_user_id
                    })

# Print summary
print(f"\n4. SUMMARY OF FINDINGS:")
print(f"   " + "-" * 66)
print(f"   ✓ Valid existing User IDs: {len(existing_ids)}")
print(f"   ⚠ Mismatched User IDs (need correction): {len(invalid_ids)}")
print(f"   ✗ Missing User IDs (can be filled): {len(missing_ids)}")
print(f"   " + "-" * 66)
print(f"   Total changes needed: {len(replacements)}")

# Show samples
if existing_ids:
    print(f"\n5. SAMPLE - Valid Existing User IDs:")
    for item in existing_ids[:3]:
        print(f"   Row {item['row']}: {item['job_code']} → {item['current_user_id']} ✓")

if invalid_ids:
    print(f"\n6. SAMPLE - Mismatched User IDs (NEED CORRECTION):")
    for item in invalid_ids[:3]:
        print(f"   Row {item['row']}: {item['job_code']}")
        print(f"      Current: {item['current_user_id']}")
        print(f"      Correct: {item['correct_user_id']} ⚠")

if missing_ids:
    print(f"\n7. SAMPLE - Missing User IDs (CAN BE FILLED):")
    for item in missing_ids[:3]:
        print(f"   Row {item['row']}: {item['job_code']} → {item['lookup_user_id']}")

# Save detailed report
report_path = Path(r"C:\Users\krush\Downloads\USER_ID_VERIFICATION_REPORT.txt")
with open(report_path, 'w', encoding='utf-8') as f:
    f.write("="*70 + "\n")
    f.write("USER ID VERIFICATION REPORT\n")
    f.write("="*70 + "\n\n")
    
    f.write(f"SUMMARY:\n")
    f.write(f"  Valid existing User IDs: {len(existing_ids)}\n")
    f.write(f"  Mismatched User IDs: {len(invalid_ids)}\n")
    f.write(f"  Missing User IDs: {len(missing_ids)}\n")
    f.write(f"  Total changes needed: {len(replacements)}\n\n")
    
    if existing_ids:
        f.write(f"VALID EXISTING USER IDS ({len(existing_ids)}):\n")
        f.write("-"*70 + "\n")
        for item in existing_ids:
            f.write(f"  Row {item['row']}: {item['job_code']} → {item['current_user_id']}\n")
        f.write("\n")
    
    if invalid_ids:
        f.write(f"MISMATCHED USER IDS ({len(invalid_ids)}) - NEED CORRECTION:\n")
        f.write("-"*70 + "\n")
        for item in invalid_ids:
            f.write(f"  Row {item['row']}: {item['job_code']}\n")
            f.write(f"    Current: {item['current_user_id']}\n")
            f.write(f"    Correct: {item['correct_user_id']}\n")
        f.write("\n")
    
    if missing_ids:
        f.write(f"MISSING USER IDS ({len(missing_ids)}) - CAN BE FILLED:\n")
        f.write("-"*70 + "\n")
        for item in missing_ids:
            f.write(f"  Row {item['row']}: {item['job_code']} → {item['lookup_user_id']}\n")
        f.write("\n")
    
    f.write(f"\nALL REPLACEMENTS NEEDED ({len(replacements)}):\n")
    f.write("-"*70 + "\n")
    for item in replacements:
        f.write(f"  Row {item['row']}: {item['job_code']}\n")
        if item['old_user_id']:
            f.write(f"    Change from: {item['old_user_id']}\n")
        else:
            f.write(f"    Add new: (currently empty)\n")
        f.write(f"    Change to:   {item['new_user_id']}\n")

print(f"\n✓ Detailed report saved to: {report_path}")
print(f"\n" + "="*70)
print("ANALYSIS COMPLETE")
print("="*70)
print(f"\nReady to create corrected duplicate file with all User IDs updated.")
print(f"Next step: Run duplication script to create corrected file.")
