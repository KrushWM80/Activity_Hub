#!/usr/bin/env python3
"""
Register PayCycle Tasks in Windows Task Scheduler using COM API
No shell escaping issues, works in regular Python
"""

import win32com.client
import sys
from datetime import datetime, timedelta

# Task configuration - use batch wrapper to avoid path escaping issues
BATCH_WRAPPER = r"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\DC to Store Change Management Emails\paycycle_wrapper.bat"

# PayCycle dates
PAYCYCLE_DATES = {
    7: (2026, 5, 1),
    8: (2026, 5, 15),
    9: (2026, 5, 29),
    10: (2026, 6, 12),
    11: (2026, 6, 26),
    12: (2026, 7, 10),
    13: (2026, 7, 24),
    14: (2026, 8, 7),
    15: (2026, 8, 21),
    16: (2026, 9, 4),
    17: (2026, 9, 18),
    18: (2026, 10, 2),
    19: (2026, 10, 16),
    20: (2026, 10, 30),
    21: (2026, 11, 13),
    22: (2026, 11, 27),
    23: (2026, 12, 11),
    24: (2026, 12, 25),
    25: (2027, 1, 8),
    26: (2027, 1, 22),
}

def register_paycycle_tasks():
    """Register all PayCycle tasks (PC-07 through PC-26)"""
    
    print("=" * 60)
    print("REGISTERING PAYCYCLE TASKS (PC-07 - PC-26)")
    print("=" * 60)
    print()
    
    # Get the Task Scheduler COM object
    try:
        scheduler = win32com.client.Dispatch("Schedule.Service")
        scheduler.Connect()
    except Exception as e:
        print(f"[ERROR] Failed to connect to Task Scheduler: {e}")
        print("[INFO] This likely requires admin PowerShell")
        return False
    
    success_count = 0
    failure_count = 0
    
    for pc_num, (year, month, day) in sorted(PAYCYCLE_DATES.items()):
        task_name = f"DC-EMAIL-PC-{pc_num:02d}-FY27"
        
        try:
            # Create task definition
            root_folder = scheduler.GetFolder("\\")
            task_def = scheduler.NewTask(0)
            
            # Set description
            task_def.RegistrationInfo.Description = f"DC Manager Change Email - PayCycle {pc_num}"
            
            # Add trigger (one-time at 6:00 AM on specified date)
            trigger = task_def.Triggers.Create(1)  # 1 = One-time trigger
            trigger.StartBoundary = f"{year:04d}-{month:02d}-{day:02d}T06:00:00"
            
            # Add action (run batch wrapper with PAYCYCLE_NUMBER argument)
            action = task_def.Actions.Create(0)  # 0 = Execute action
            action.Path = BATCH_WRAPPER
            action.Arguments = f'{pc_num}'
            
            # Set run-level to highest privilege
            task_def.Principal.RunLevel = 1  # 1 = Highest
            
            # Register the task
            root_folder.RegisterTaskDefinition(
                task_name,
                task_def,
                6,  # 6 = Create or update
                None,  # User (None = current user)
                None,  # Password
                0     # Logon type
            )
            
            print(f"[OK] PC-{pc_num}: {task_name}")
            print(f"     Scheduled: {year:04d}-{month:02d}-{day:02d} @ 06:00 AM")
            print(f"     Command: {BATCH_WRAPPER} {pc_num}")
            success_count += 1
            
        except Exception as e:
            print(f"[FAIL] PC-{pc_num}: {task_name}")
            print(f"       Error: {e}")
            failure_count += 1
    
    print()
    print("=" * 60)
    print(f"Results: {success_count} successful, {failure_count} failed")
    print("=" * 60)
    print()
    
    # Verify registration
    print("Verifying task registration...")
    print()
    
    verified_count = 0
    try:
        root_folder = scheduler.GetFolder("\\")
        for pc_num in sorted(PAYCYCLE_DATES.keys()):
            task_name = f"DC-EMAIL-PC-{pc_num:02d}-FY27"
            try:
                task = root_folder.GetTask(task_name)
                if task:
                    print(f"  ✓ PC-{pc_num}: Registered")
                    verified_count += 1
            except:
                pass
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
