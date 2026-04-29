#!/usr/bin/env python3
"""
Register Daily Snapshot Generation Task
Runs daily_check_smart.py at 5:00 AM to generate today's snapshot
This ensures snapshot is ready before PayCycle emails run at 6:00 AM
"""

import subprocess
import sys

# Task configuration
BATCH_WRAPPER = r"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails\snapshot_generator_wrapper.bat"

def register_daily_snapshot_task():
    """Register the daily snapshot generation task"""
    
    print("=" * 70)
    print("REGISTERING DAILY SNAPSHOT GENERATION TASK")
    print("=" * 70)
    print()
    
    task_name = "DC-EMAIL-Daily-Snapshot-Generator-FY27"
    
    try:
        # Build schtasks command for daily recurrence at 5:00 AM
        # /sc daily /st HH:MM:SS (runs every day at specified time)
        command = [
            "schtasks",
            "/create",
            "/tn", task_name,
            "/tr", f'"{BATCH_WRAPPER}"',
            "/sc", "daily",
            "/st", "05:00:00",
            "/f"
        ]
        
        print(f"Creating task: {task_name}")
        print(f"Schedule: Daily at 5:00 AM")
        print(f"Purpose: Generate manager snapshots before PayCycle emails")
        print(f"Wrapper: {BATCH_WRAPPER}")
        print()
        
        # Run schtasks
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"[OK] Task registered successfully")
            print(f"     Name: {task_name}")
            print(f"     Trigger: Daily @ 05:00:00")
            success = True
        else:
            print(f"[FAIL] Task registration failed")
            print(f"       Exit code: {result.returncode}")
            if result.stderr:
                print(f"       Error: {result.stderr.strip()}")
            if result.stdout:
                print(f"       Output: {result.stdout.strip()}")
            success = False
        
        print()
        
        # Verify registration
        print("Verifying registration...")
        print()
        
        result = subprocess.run(
            ["schtasks", "/query", "/tn", task_name, "/fo", "list"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"  ✓ Task verified in Task Scheduler")
            print(f"    Status: Ready")
        else:
            print(f"  ✗ Task verification failed")
        
        print()
        print("=" * 70)
        print(f"Result: {'SUCCESS' if success else 'FAILED'}")
        print("=" * 70)
        print()
        
        if success:
            print("Daily Snapshot Generation Task is now active!")
            print()
            print("TIMELINE:")
            print("  05:00 AM - daily_check_smart.py runs")
            print("  (creates snapshots_local/manager_snapshot_YYYY-MM-DD.json)")
            print("  06:00 AM - PayCycle emails send (PC-07-26 use fresh snapshots)")
            print()
        
        return success
        
    except Exception as e:
        print(f"[FATAL] {e}")
        return False

if __name__ == "__main__":
    try:
        success = register_daily_snapshot_task()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"[FATAL] {e}")
        sys.exit(1)
