import os
import glob
from datetime import datetime
import sys

def convert_csv_to_xlsx():
    """Convert the latest CSV file to XLSX format"""
    source_folder = r"C:\Users\krush\Documents\VSCode\AMP\Weekly Messages\Docs"
    destination_path = r"C:\Users\krush\Walmart Inc\ATC Team - Documents\Activity - Walmart US\Reporting\Data\Me@\MM\Input\Weekly Messages Area Reports - Tables FY27.xlsx"
    
    try:
        # Find the most recent CSV file
        csv_files = glob.glob(os.path.join(source_folder, "*Weekly Messages Area Reports*.csv"))
        
        if not csv_files:
            print(f"✗ No Weekly Messages CSV file found in: {source_folder}")
            return False
        
        # Get the most recent file
        latest_csv = max(csv_files, key=os.path.getctime)
        print(f"Found source file: {latest_csv}")
        print(f"Converting to: {destination_path}")
        
        # Ensure destination folder exists
        dest_folder = os.path.dirname(destination_path)
        os.makedirs(dest_folder, exist_ok=True)
        
        # Use pandas to read CSV and write XLSX
        try:
            import pandas as pd
            df = pd.read_csv(latest_csv)
            df.to_excel(destination_path, index=False, engine='openpyxl')
            print(f"✓ Successfully converted and saved to: {destination_path}")
            print(f"✓ Weekly Messages report processed successfully at {datetime.now()}")
            return True
        except ImportError:
            # Fall back to using Excel COM object if pandas not available
            import win32com.client as win32
            excel = win32.Dispatch("Excel.Application")
            excel.Visible = False
            excel.DisplayAlerts = False
            
            # Open CSV and resave as XLSX
            workbook = excel.Workbooks.Open(latest_csv)
            workbook.SaveAs(destination_path, FileFormat=51)  # 51 = XLSX
            workbook.Close()
            excel.Quit()
            
            print(f"✓ Successfully converted and saved to: {destination_path}")
            print(f"✓ Weekly Messages report processed successfully at {datetime.now()}")
            return True
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = convert_csv_to_xlsx()
    sys.exit(0 if success else 1)
