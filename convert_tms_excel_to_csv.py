"""
Convert TMS Data Excel file to CSV for processing without openpyxl dependency
This uses Windows COM/Excel API directly if Excel is available
"""
import os
import subprocess
import sys

file_path = r'C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\TMS Data (3).xlsx'
output_csv = r'C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\TMS_Data_3_converted.csv'

print(f"Converting: {file_path}")
print(f"To: {output_csv}")

# Try Method 1: Using Excel COM (Windows only, if Excel is installed)
try:
    print("\n[Attempt 1] Using Excel COM API...")
    import win32com.client
    excel = win32com.client.Dispatch("Excel.Application")
    workbook = excel.Workbooks.Open(os.path.abspath(file_path))
    worksheet = workbook.Sheets(1)
    
    # Get data range
    used_range = worksheet.UsedRange
    
    # Convert to CSV
    converted_path = output_csv.replace('.csv', '_temp.xlsx')
    workbook.SaveAs(converted_path, FileFormat=6)  # 6 = xlCSV
    workbook.Close()
    excel.Quit()
    
    # Rename to final
    if os.path.exists(converted_path):
        os.rename(converted_path, output_csv)
        print(f"SUCCESS: File converted to {output_csv}")
    
except ImportError:
    print("Win32COM not available, trying PowerShell method...")
    
    # Method 2: Using PowerShell
    ps_script = f'''
    $excel = New-Object -ComObject Excel.Application
    $workbook = $excel.Workbooks.Open('{os.path.abspath(file_path)}')
    $worksheet = $workbook.Sheets(1)
    $workbook.SaveAs('{output_csv}', 6)  # 6 = xlCSV
    $workbook.Close()
    $excel.Quit()
    Write-Host "File converted successfully"
    '''
    
    try:
        result = subprocess.run(['powershell', '-NoProfile', '-Command', ps_script], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"SUCCESS: File converted: {output_csv}")
            print(result.stdout)
        else:
            print(f"PowerShell conversion failed: {result.stderr}")
    except Exception as e:
        print(f"PowerShell method failed: {e}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Check if conversion worked
if os.path.exists(output_csv):
    print(f"\nConverted file exists: {output_csv}")
    # Try to read it
    try:
        import csv
        with open(output_csv, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            print(f"CSV has {len(rows)} rows")
            if rows:
                print(f"Columns: {rows[0]}")
    except Exception as e:
        print(f"Error reading CSV: {e}")
else:
    print(f"Conversion failed - file not created")
