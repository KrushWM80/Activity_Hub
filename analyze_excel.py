import pandas as pd

file_path = r'Store Support\Projects\JobCodes-teaming\Teaming\TMS Data (3).xlsx'

# Get sheet names - try different engines
try:
    xl_file = pd.ExcelFile(file_path, engine='openpyxl')
except:
    try:
        xl_file = pd.ExcelFile(file_path, engine='xlrd')
    except:
        try:
            xl_file = pd.ExcelFile(file_path)
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            exit(1)

print('=== SHEET NAMES ===')
print(xl_file.sheet_names)
print()

# Read all sheets and analyze
for sheet_name in xl_file.sheet_names:
    print(f'=== SHEET: {sheet_name} ===')
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    print(f'Columns ({len(df.columns)}):')
    for i, col in enumerate(df.columns, 1):
        print(f'  {i}. {col}')
    
    print(f'\nFirst 5 rows:')
    print(df.head(5).to_string())
    print('\nData types:')
    print(df.dtypes)
    print('\n' + '='*60 + '\n')
