"""
Verify AMP Roles Updated.xlsx content
"""
import zipfile
import xml.etree.ElementTree as ET
import csv
from pathlib import Path

def verify_file():
    print("\n" + "="*70)
    print("VERIFYING AMP ROLES UPDATED.XLSX")
    print("="*70)
    
    # Load lookup
    lookup_path = Path(r"C:\Users\krush\Downloads\SMART_JobCode_Lookup.csv")
    lookup_dict = {}
    with open(lookup_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            smart_code = row['SMART Job Code'].strip()
            lookup_dict[smart_code] = {
                'role': row.get('Role Type', ''),
                'user_id': row.get('User ID', '')
            }
    
    print(f"✓ Lookup has {len(lookup_dict)} codes")
    
    # Read updated file
    excel_path = Path(r"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Job Codes\AMP Roles Updated.xlsx")
    
    with zipfile.ZipFile(excel_path, 'r') as zipf:
        # Read shared strings
        strings_xml = zipf.read('xl/sharedStrings.xml')
        strings_root = ET.fromstring(strings_xml)
        
        shared_strings = []
        for si in strings_root.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si'):
            t = si.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')
            if t is not None:
                shared_strings.append(t.text)
        
        print(f"✓ Shared strings: {len(shared_strings)} entries")
        
        # Read worksheet
        sheet_xml = zipf.read('xl/worksheets/sheet1.xml')
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
                            row_data.append(f"[Error: idx {idx}]")
                    except:
                        row_data.append(v.text)
                else:
                    row_data.append('')
            
            if row_data:
                rows.append(row_data)
        
        print(f"✓ Worksheet has {len(rows)} rows")
        
        if rows:
            print(f"\nFirst row (headers): {rows[0]}")
            
            # Count matches
            matched = 0
            with_user_id = 0
            
            sample_matches = []
            
            for idx, row in enumerate(rows[1:], 2):
                if len(row) > 0:
                    job_code = row[0].strip() if row[0] else ''
                    
                    if job_code in lookup_dict:
                        matched += 1
                        if len(row) > 2 and row[2]:
                            with_user_id += 1
                            if len(sample_matches) < 5:
                                sample_matches.append((job_code, row[1] if len(row) > 1 else '', row[2]))
            
            print(f"\n✓ Matched job codes: {matched}/{len(rows)-1}")
            print(f"✓ With User ID: {with_user_id}")
            
            if sample_matches:
                print(f"\nSample matches:")
                print(f"{'Job Code':<20} {'Role':<15} {'User ID':<20}")
                print("-" * 55)
                for jc, role, uid in sample_matches:
                    print(f"{jc:<20} {role:<15} {uid:<20}")
    
    print(f"\n✓ File: {excel_path}")
    print(f"✓ Size: {excel_path.stat().st_size:,} bytes")
    print("\n✅ VERIFICATION COMPLETE")

if __name__ == "__main__":
    verify_file()
