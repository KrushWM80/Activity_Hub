#!/usr/bin/env python3
"""Test both loaders."""
import subprocess
import sys
import time

# Kill Excel first
subprocess.run(['taskkill', '/F', '/IM', 'EXCEL.EXE'], stderr=subprocess.DEVNULL)
time.sleep(2)

print("=" * 80)
print("TESTING NORMALIZED LOADER")
print("=" * 80)

result1 = subprocess.run([
    sys.executable,
    r'C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\AMP\Weekly Messages\adobe_to_bigquery_loader.py'
], capture_output=True, text=True, timeout=120)

output1 = (result1.stdout + result1.stderr).split('\n')
print('\n'.join(output1[-40:]))
print(f'\nReturn code: {result1.returncode}')

time.sleep(3)
subprocess.run(['taskkill', '/F', '/IM', 'EXCEL.EXE'], stderr=subprocess.DEVNULL)
time.sleep(2)

print("\n" + "=" * 80)
print("TESTING RAW DATA LOADER")
print("=" * 80)

result2 = subprocess.run([
    sys.executable,
    r'C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\AMP\Weekly Messages\adobe_raw_data_loader.py'
], capture_output=True, text=True, timeout=120)

output2 = (result2.stdout + result2.stderr).split('\n')
print('\n'.join(output2[-40:]))
print(f'\nReturn code: {result2.returncode}')
