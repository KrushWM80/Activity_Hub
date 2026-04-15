#!/usr/bin/env python3
"""Run both loaders with timeout protection."""
import subprocess
import sys
import time
import os

os.chdir(r'C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\AMP\Weekly Messages')

print("=" * 80)
print("TESTING ADOBE ANALYTICS LOADERS")
print("=" * 80)

# Kill Excel first
try:
    subprocess.run(['taskkill', '/F', '/IM', 'EXCEL.EXE'], stderr=subprocess.DEVNULL, timeout=5)
except:
    pass
time.sleep(2)

# Test 1: Normalized Loader
print("\n[1/2] Testing Normalized Loader (adobe_to_bigquery_loader.py)...")
try:
    result = subprocess.run(
        [sys.executable, 'adobe_to_bigquery_loader.py'],
        capture_output=True,
        text=True,
        timeout=60
    )
    
    lines = (result.stdout + result.stderr).split('\n')
    print('\n'.join(lines[-35:]))
    
    if result.returncode == 0:
        print("\n✓ NORMALIZED LOADER SUCCESS")
    else:
        print(f"\n✗ NORMALIZED LOADER FAILED (exit code: {result.returncode})")
except subprocess.TimeoutExpired:
    print("✗ NORMALIZED LOADER TIMEOUT (exceeded 60s)")
except Exception as e:
    print(f"✗ NORMALIZED LOADER ERROR: {e}")

time.sleep(3)

# Kill Excel again
try:
    subprocess.run(['taskkill', '/F', '/IM', 'EXCEL.EXE'], stderr=subprocess.DEVNULL, timeout=5)
except:
    pass
time.sleep(2)

# Test 2: Raw Data Loader
print("\n[2/2] Testing Raw Data Loader (adobe_raw_data_loader.py)...")
try:
    result = subprocess.run(
        [sys.executable, 'adobe_raw_data_loader.py'],
        capture_output=True,
        text=True,
        timeout=60
    )
    
    lines = (result.stdout + result.stderr).split('\n')
    print('\n'.join(lines[-35:]))
    
    if result.returncode == 0:
        print("\n✓ RAW DATA LOADER SUCCESS")
    else:
        print(f"\n✗ RAW DATA LOADER FAILED (exit code: {result.returncode})")
except subprocess.TimeoutExpired:
    print("✗ RAW DATA LOADER TIMEOUT (exceeded 60s)")
except Exception as e:
    print(f"✗ RAW DATA LOADER ERROR: {e}")

print("\n" + "=" * 80)
