REM Quick fix - replace the bigquery client line before running
REM This runs a simple Python patcher first
python -c "
import sys
file_path = r'%JOBCODES_PATH%\main.py'
try:
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Fix the bigquery Client line
    old_line = 'client = bigquery.Client(project=\"polaris-analytics-prod\")'
    new_line = 'client = bigquery.Client()'
    
    if old_line in content:
        content = content.replace(old_line, new_line)
        with open(file_path, 'w') as f:
            f.write(content)
        print('[PATCH] Fixed bigquery.Client() in main.py')
    else:
        if 'client = bigquery.Client()' in content:
            print('[PATCH] Already using Client() without project')
        else:
            print('[PATCH] Could not find Client line to fix')
except Exception as e:
    print(f'[PATCH ERROR] {e}')
    pass
" 2>&1 | findstr /i "PATCH"
