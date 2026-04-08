#!/usr/bin/env python3
"""
Convert Excel Job Code Master file to JSON for fallback loading when openpyxl is unavailable.
Uses alternative methods to read Excel data.
"""

import os
import json
import sys
from pathlib import Path

# Try different Excel reading methods
def try_openpyxl():
    """Try using openpyxl if available"""
    try:
        import openpyxl
        excel_file = r"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Job Codes\Job_Code_Master_Table.xlsx"
        wb = openpyxl.load_workbook(excel_file)
        ws = wb.active
        
        data = []
        headers = []
        for i, row in enumerate(ws.iter_rows(values_only=True)):
            if i == 0:
                headers = row
            else:
                if any(row):  # Skip empty rows
                    data.append(dict(zip(headers, row)))
        
        return data
    except ImportError:
        return None
    except Exception as e:
        print(f"openpyxl error: {e}", file=sys.stderr)
        return None

def try_pandas():
    """Try using pandas if available"""
    try:
        import pandas as pd
        excel_file = r"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Job Codes\Job_Code_Master_Table.xlsx"
        df = pd.read_excel(excel_file)
        data = df.replace({pd.NA: None, pd.NaT: None, float('nan'): None}).to_dict('records')
        return data
    except ImportError:
        return None
    except Exception as e:
        print(f"pandas error: {e}", file=sys.stderr)
        return None

def try_pyxlsx():
    """Try using pyxlsx library if available"""
    try:
        from pyxlsx import Workbook
        excel_file = r"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Job Codes\Job_Code_Master_Table.xlsx"
        # This library isn't common, skip
        return None
    except ImportError:
        return None

def try_zipfile_method():
    """
    Excel files are ZIP archives containing XML.
    Try to extract and parse the XML directly.
    """
    try:
        import zipfile
        from xml.etree import ElementTree as ET
        
        excel_file = r"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Job Codes\Job_Code_Master_Table.xlsx"
        
        with zipfile.ZipFile(excel_file, 'r') as zip_ref:
            # Read the sheet1.xml
            with zip_ref.open('xl/worksheets/sheet1.xml') as f:
                tree = ET.parse(f)
                root = tree.getroot()
                
                ns = {'': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                rows = root.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row')
                
                # Read shared strings for cell values
                shared_strings = []
                try:
                    with zip_ref.open('xl/sharedStrings.xml') as ss_f:
                        ss_tree = ET.parse(ss_f)
                        ss_root = ss_tree.getroot()
                        shared_strings = [t.text for t in ss_root.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')]
                except:
                    pass
                
                data = []
                headers = []
                
                for row_idx, row in enumerate(rows):
                    row_data = []
                    cells = row.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c')
                    
                    for cell in cells:
                        v_elem = cell.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
                        cell_type = cell.get('t', 'n')
                        
                        if v_elem is not None:
                            value = v_elem.text
                            # If it's a shared string ref, look it up
                            if cell_type == 's':
                                try:
                                    value = shared_strings[int(value)]
                                except:
                                    pass
                        else:
                            value = None
                        
                        row_data.append(value)
                    
                    if row_idx == 0:
                        headers = row_data
                    else:
                        if any(row_data):
                            data.append(dict(zip(headers, row_data)))
                
                return data
        
    except Exception as e:
        print(f"zipfile XML parsing error: {e}", file=sys.stderr)
        return None

def load_excel_data():
    """Try multiple methods to load Excel data"""
    print("Attempting to load Excel Job Code Master data...")
    
    # Try methods in order of preference
    methods = [
        ("pandas", try_pandas),
        ("openpyxl", try_openpyxl),
        ("zipfile XML", try_zipfile_method),
    ]
    
    for name, method in methods:
        print(f"  Trying {name}...", end=" ")
        data = method()
        if data is not None:
            print(f"✓ Success! Loaded {len(data)} records")
            return data
        print("✗ Not available")
    
    print("❌ Could not load Excel with any method")
    return None

def convert_to_json():
    """Main conversion function"""
    data = load_excel_data()
    
    if data is None:
        print("Failed to load Excel data")
        return False
    
    # Save to JSON
    output_file = r"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend\job_codes_master.json"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "job_codes": data,
                "count": len(data),
                "source": "Excel Job_Code_Master_Table.xlsx"
            }, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved to {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error saving JSON: {e}")
        return False

if __name__ == "__main__":
    success = convert_to_json()
    sys.exit(0 if success else 1)
