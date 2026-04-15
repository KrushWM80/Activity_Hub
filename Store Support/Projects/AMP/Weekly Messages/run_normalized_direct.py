#!/usr/bin/env python3
"""Run normalized loader with direct output."""
import sys
import os
import subprocess
import time

# Kill Excel
subprocess.run(['taskkill', '/F', '/IM', 'EXCEL.EXE'], stderr=subprocess.DEVNULL)
time.sleep(2)

os.chdir(r'C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\AMP\Weekly Messages')

# Run loader with NO timeout to see what happens
result = subprocess.Popen(
    [sys.executable, 'adobe_to_bigquery_loader.py'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

# Read output line by line and print immediately
try:
    for line in iter(result.stdout.readline, ''):
        if line:
            print(line, end='')
        sys.stdout.flush()
    
    result.wait(timeout=120)
    print(f"\n\nProcess exited with code: {result.returncode}")
except subprocess.TimeoutExpired:
    result.kill()
    print("\n\nProcess timed out after 120 seconds")
except KeyboardInterrupt:
    result.kill()
    print("\n\nInterrupted by user")
except Exception as e:
    print(f"\n\nError: {e}")
    result.kill()
