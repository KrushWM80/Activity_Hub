#!/usr/bin/env python3
"""
Update Windows Task Scheduler jobs to run DAILY at 7 AM.
(Reports arrive at 6 AM, VB processes, loaders run at 7 AM daily)
"""
import subprocess
import sys

VENV_PATH = r'C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\.venv\Scripts\python.exe'
LOADER_DIR = r'C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\AMP\Weekly Messages'

NORM_LOADER = rf'{LOADER_DIR}\adobe_to_bigquery_loader.py'
RAW_LOADER = rf'{LOADER_DIR}\adobe_raw_data_loader.py'

def delete_task(task_name):
    """Delete existing task."""
    cmd = ['schtasks', '/delete', '/tn', task_name, '/f']
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"  ✓ Deleted: {task_name}")
            return True
        else:
            # Task might not exist, which is fine
            if 'cannot find' in result.stderr.lower() or 'not found' in result.stderr.lower():
                print(f"  - {task_name} does not exist (OK)")
                return True
            print(f"  ✗ Error deleting {task_name}: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ✗ Exception: {e}")
        return False

def create_task(task_name, script_path, start_time):
    """Create a daily scheduled task."""
    # /sc DAILY - runs every day
    cmd = [
        'schtasks', '/create', '/tn', task_name, '/tr',
        f'"{VENV_PATH}" "{script_path}"',
        '/sc', 'DAILY', '/st', start_time,
        '/f'  # Force creation if exists
    ]
    
    print(f"\nCreating task: {task_name}")
    print(f"  Script: {script_path}")
    print(f"  Schedule: DAILY at {start_time}")
    
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

# Main execution
print("=" * 80)
print("UPDATING TASK SCHEDULER - DAILY AT 7 AM")
print("=" * 80)
print("Schedule: Reports arrive 6 AM → VB processes → Loaders run 7 AM DAILY\n")

# Delete existing weekly tasks
print("Step 1: Removing old weekly tasks...")
delete_task('AdobeAnalyticsNormalized')
delete_task('AdobeAnalyticsRaw')

# Create new daily tasks
print("\nStep 2: Creating new daily tasks...")
success_count = 0

# Task 1: Normalized data loader (Daily 7:00 AM)
if create_task(
    'AdobeAnalyticsNormalized',
    NORM_LOADER,
    '07:00:00'
):
    success_count += 1

# Task 2: Raw data loader (Daily 7:30 AM - staggered to avoid conflicts)
if create_task(
    'AdobeAnalyticsRaw',
    RAW_LOADER,
    '07:30:00'
):
    success_count += 1

print("\n" + "=" * 80)
print(f"RESULT: {success_count}/2 tasks created successfully")
print("=" * 80)

# Verify tasks were created
print("\nStep 3: Verifying tasks...")
try:
    result = subprocess.run(
        ['schtasks', '/query', '/tn', 'AdobeAnalyticsNormalized', '/fo', 'list'],
        capture_output=True,
        text=True,
        timeout=10
    )
    if 'AdobeAnalyticsNormalized' in result.stdout and 'DAILY' in result.stdout:
        print("✓ AdobeAnalyticsNormalized - DAILY schedule confirmed")
    else:
        print("✗ AdobeAnalyticsNormalized - Schedule verification failed")
except Exception as e:
    print(f"✗ Verification error: {e}")

try:
    result = subprocess.run(
        ['schtasks', '/query', '/tn', 'AdobeAnalyticsRaw', '/fo', 'list'],
        capture_output=True,
        text=True,
        timeout=10
    )
    if 'AdobeAnalyticsRaw' in result.stdout and 'DAILY' in result.stdout:
        print("✓ AdobeAnalyticsRaw - DAILY schedule confirmed")
    else:
        print("✗ AdobeAnalyticsRaw - Schedule verification failed")
except Exception as e:
    print(f"✗ Verification error: {e}")

print("\n" + "=" * 80)
print("SCHEDULE UPDATED")
print("=" * 80)
print("\nDaily Execution Timeline:")
print("  6:00 AM - Reports arrive")
print("  6:00-6:59 AM - VB processes and places files in folder")
print("  7:00 AM - AdobeAnalyticsNormalized loader runs")
print("  7:30 AM - AdobeAnalyticsRaw loader runs")
print("\nLogs: Store Support\\Projects\\AMP\\Weekly Messages\\logs\\")
print("=" * 80)

sys.exit(0 if success_count == 2 else 1)
