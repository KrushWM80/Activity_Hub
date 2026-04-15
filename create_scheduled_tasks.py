#!/usr/bin/env python3
"""
Create Windows Task Scheduler jobs for Adobe Analytics loaders.
Runs both loaders weekly on Sundays 6-7 AM.
"""
import subprocess
import sys

VENV_PATH = r'C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe'
LOADER_DIR = r'C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\AMP\Weekly Messages'

NORM_LOADER = rf'{LOADER_DIR}\adobe_to_bigquery_loader.py'
RAW_LOADER = rf'{LOADER_DIR}\adobe_raw_data_loader.py'

def create_task(task_name, script_path, start_time):
    """Create a scheduled task."""
    cmd = [
        'schtasks', '/create', '/tn', task_name, '/tr',
        f'"{VENV_PATH}" "{script_path}"',
        '/sc', 'weekly', '/d', 'SUN', '/st', start_time,
        '/f'  # Force creation if exists
    ]
    
    print(f"\nCreating task: {task_name}")
    print(f"  Script: {script_path}")
    print(f"  Time: Sunday {start_time}")
    print(f"  Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"  ✓ SUCCESS")
            return True
        else:
            print(f"  ✗ FAILED: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ✗ ERROR: {e}")
        return False

# Create tasks
print("=" * 80)
print("CREATING TASK SCHEDULER JOBS FOR ADOBE ANALYTICS LOADERS")
print("=" * 80)

success_count = 0

# Task 1: Normalized data loader (Sunday 6:00 AM)
if create_task(
    'AdobeAnalyticsNormalized',
    NORM_LOADER,
    '06:00:00'
):
    success_count += 1

# Task 2: Raw data loader (Sunday 6:30 AM - staggered to avoid conflicts)
if create_task(
    'AdobeAnalyticsRaw',
    RAW_LOADER,
    '06:30:00'
):
    success_count += 1

print("\n" + "=" * 80)
print(f"RESULT: {success_count}/2 tasks created successfully")
print("=" * 80)

# Verify tasks were created
print("\nVerifying created tasks...")
try:
    result = subprocess.run(
        ['schtasks', '/query', '/tn', 'AdobeAnalyticsNormalized', '/fo', 'list'],
        capture_output=True,
        text=True,
        timeout=10
    )
    if 'AdobeAnalyticsNormalized' in result.stdout:
        print("✓ AdobeAnalyticsNormalized task found")
    else:
        print("✗ AdobeAnalyticsNormalized task NOT found")
except Exception as e:
    print(f"✗ Verification error: {e}")

try:
    result = subprocess.run(
        ['schtasks', '/query', '/tn', 'AdobeAnalyticsRaw', '/fo', 'list'],
        capture_output=True,
        text=True,
        timeout=10
    )
    if 'AdobeAnalyticsRaw' in result.stdout:
        print("✓ AdobeAnalyticsRaw task found")
    else:
        print("✗ AdobeAnalyticsRaw task NOT found")
except Exception as e:
    print(f"✗ Verification error: {e}")

print("\nDone!")
sys.exit(0 if success_count == 2 else 1)
