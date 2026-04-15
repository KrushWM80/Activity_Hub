#!/usr/bin/env python3
"""Test Outlook COM connection"""

import sys
import time

try:
    import win32com.client
    print("✓ win32com installed")
except ImportError as e:
    print(f"✗ win32com failed to import: {e}")
    sys.exit(1)

print("\nAttempting to connect to Outlook...")

# Try GetActiveObject first (running instance)
try:# Small delay to ensure initialization
    time.sleep(1)
    
    
    outlook = win32com.client.GetActiveObject("Outlook.Application")
    print("✓ Outlook.Application found (GetActiveObject)")
except Exception as e:
    print(f"  GetActiveObject failed: {e}")
    # Try Dispatch (create new instance if needed)
    try:
        outlook = win32com.client.Dispatch("Outlook.Application")
        print("✓ Outlook.Application found (Dispatch)")
    except Exception as e2:
        print(f"✗ Dispatch also failed: {e2}")
        sys.exit(1)
    
    namespace = outlook.GetNamespace("MAPI")
    print("✓ MAPI namespace initialized")
    
    # Try to access Inbox
    inbox = namespace.Folders.Item(1)
    print(f"✓ Default store accessed: {inbox.Name}")
    
    # Try to navigate to ATC folder
    try:
        atc = inbox.Folders.Item("ATC")
        print(f"✓ ATC folder found")
        
        # Try to navigate to Reports > AMP
        reports = atc.Folders.Item("Reports")
        print(f"✓ Reports folder found")
        
        amp = reports.Folders.Item("AMP")
        print(f"✓ AMP folder found")
        
        # List folders in AMP
        print("\n  Folders in AMP:")
        for folder in amp.Folders:
            print(f"    - {folder.Name}")
    except Exception as e:
        print(f"✗ Error navigating folders: {e}")
        print("\n  Available folders in ATC:")
        try:
            for f in inbox.Folders:
                print(f"    - {f.Name}")
        except:
            pass
    
    print("\n✓ Outlook connection successful!")
    
except Exception as e:
    print(f"✗ Failed to connect to Outlook: {e}")
    print("  Make sure Outlook is running")
    sys.exit(1)
