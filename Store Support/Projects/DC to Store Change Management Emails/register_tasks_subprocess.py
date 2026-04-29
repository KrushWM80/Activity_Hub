#!/usr/bin/env python3
"""
Register PayCycle Tasks using subprocess + schtasks.exe
Proper shell quoting avoids COM API path issues
"""

import subprocess
import sys

# Task configuration
BATCH_WRAPPER = r"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails\paycycle_wrapper.bat"

# PayCycle dates (MM/DD/YYYY format for schtasks)
PAYCYCLE_DATES = {
    7: ("05/01/2026", "06:00:00"),
    8: ("05/15/2026", "06:00:00"),
    9: ("05/29/2026", "06:00:00"),
    10: ("06/12/2026", "06:00:00"),
    11: ("06/26/2026", "06:00:00"),
    12: ("07/10/2026", "06:00:00"),
    13: ("07/24/2026", "06:00:00"),
    14: ("08/07/2026", "06:00:00"),
    15: ("08/21/2026", "06:00:00"),
    16: ("09/04/2026", "06:00:00"),
    17: ("09/18/2026", "06:00:00"),
    18: ("10/02/2026", "06:00:00"),
    19: ("10/16/2026", "06:00:00"),
    20: ("10/30/2026", "06:00:00"),
    21: ("11/13/2026", "06:00:00"),
    22: ("11/27/2026", "06:00:00"),
    23: ("12/11/2026", "06:00:00"),
    24: ("12/25/2026", "06:00:00"),
    25: ("01/08/2027", "06:00:00"),
    26: ("01/22/2027", "06:00:00"),
}

def register_paycycle_tasks():
    """Register all PayCycle tasks"""
    
    print("=" * 70)
    print("REGISTERING PAYCYCLE TASKS (PC-07 - PC-26) via schtasks.exe")
    print("=" * 70)
    print()
    
    success_count = 0
    failure_count = 0
    
    for pc_num, (date, time) in sorted(PAYCYCLE_DATES.items()):
        task_name = f"DC-EMAIL-PC-{pc_num:02d}-FY27"
        
        try:
            # Build schtasks command
            # Format: schtasks /create /tn NAME /tr "COMMAND ARGS" /sc once /st TIME /sd DATE /f
            command = [
                "schtasks",
                "/create",
                "/tn", task_name,
                "/tr", f'"{BATCH_WRAPPER}" {pc_num}',
                "/sc", "once",
                "/st", time,
                "/sd", date,
                "/f"
            ]
            
            # Run schtasks
            result = subprocess.run(command, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"[OK] PC-{pc_num}: {task_name}")
                print(f"     Date: {date} @ {time}")
                success_count += 1
            else:
                print(f"[FAIL] PC-{pc_num}: {task_name}")
                print(f"       Exit: {result.returncode}")
                if result.stderr:
                    print(f"       Error: {result.stderr.strip()}")
                if result.stdout:
                    print(f"       Output: {result.stdout.strip()}")
                failure_count += 1
                
        except Exception as e:
            print(f"[FAIL] PC-{pc_num}: {task_name}")
            print(f"       Exception: {e}")
            failure_count += 1
    
    print()
    print("=" * 70)
    print(f"Results: {success_count} successful, {failure_count} failed")
    print("=" * 70)
    print()
    
    # Verify registration
    print("Verifying task registration...")
    print()
    
    verified_count = 0
    for pc_num in sorted(PAYCYCLE_DATES.keys()):
        task_name = f"DC-EMAIL-PC-{pc_num:02d}-FY27"
        try:
            result = subprocess.run(
                ["schtasks", "/query", "/tn", task_name, "/fo", "list"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"  ✓ PC-{pc_num}: Registered")
                verified_count += 1
        except:
            pass
    
    print()
    print(f"Verified: {verified_count} / 20 tasks")
    print()
    
    return success_count == 20

if __name__ == "__main__":
    try:
        success = register_paycycle_tasks()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"[FATAL] {e}")
        sys.exit(1)
