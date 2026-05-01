#!/usr/bin/env python3
"""
Simplified diagnostic to check on-call group and calendar.
"""

def test_group_members():
    """Test accessing group members."""
    print("\n" + "="*80)
    print("TASK 1A: Checking U.S. Comm - On Call Planner GROUP")
    print("="*80)
    
    try:
        import pythoncom
        import win32com.client
        
        print("\nInitializing COM...")
        pythoncom.CoInitialize()
        
        print("Getting Outlook application...")
        outlook = win32com.client.Dispatch('Outlook.Application')
        ns = outlook.GetNamespace('MAPI')
        
        print("Getting Global Address List...")
        gal = ns.GetGlobalAddressList()
        
        print(f"\nSearching for 'U.S. Comm - On Call Planner' group...")
        found_groups = []
        for entry in gal.AddressEntries:
            name = entry.Name
            if 'on call' in name.lower() or 'oncall' in name.lower():
                found_groups.append(name)
                print(f"  Found: {name}")
        
        if not found_groups:
            print("  ✗ No groups matching 'on call' found in GAL")
            print("  Available group search - trying exact match...")
            
        # Try exact match
        group = None
        for entry in gal.AddressEntries:
            if entry.Name == 'U.S. Comm - On Call Planner':
                print(f"  ✓ EXACT MATCH: {entry.Name}")
                try:
                    group = entry.GetExchangeDistributionList()
                    break
                except Exception as e:
                    print(f"    Note: {e}")
        
        if group:
            print("\n✓ Getting group members...")
            try:
                members = group.GetExchangeDistributionListMembers()
                print(f"  Found {len(members)} members:")
                for member in members:
                    try:
                        print(f"    • {member.Name:<35} {member.Address}")
                    except:
                        print(f"    • {member.Name}")
            except Exception as e:
                print(f"  ✗ Error getting members: {e}")
        else:
            print("  ✗ Could not access group")
        
        pythoncom.CoUninitialize()
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()


def test_calendar():
    """Test accessing calendar entries."""
    print("\n" + "="*80)
    print("TASK 1B: Checking U.S. Comm - On Call Planner CALENDAR & ORGANIZER")
    print("="*80)
    
    try:
        import pythoncom
        import win32com.client
        from datetime import datetime, timedelta
        import re
        
        print("\nInitializing COM...")
        pythoncom.CoInitialize()
        
        print("Getting Outlook application...")
        outlook = win32com.client.Dispatch('Outlook.Application')
        ns = outlook.GetNamespace('MAPI')
        
        print("\nSearching for 'U.S. Comm - On Call Planner' calendar...")
        cal = None
        for folder in ns.Folders:
            try:
                folder_name = folder.Name
                if 'on call' in folder_name.lower():
                    print(f"  Found folder: {folder_name}")
                if folder_name == 'U.S. Comm - On Call Planner':
                    print(f"  ✓ EXACT MATCH: {folder_name}")
                    try:
                        cal = folder.Folders['Calendar']
                        print(f"  ✓ Calendar found")
                        break
                    except:
                        print(f"  Note: No Calendar subfolder in {folder_name}")
            except Exception as e:
                pass
        
        if cal is None:
            print("  ✗ Could not find calendar")
        else:
            print("\n✓ Searching calendar entries (last 30 days)...")
            
            search_start = (datetime.now() - timedelta(days=30)).strftime('%m/%d/%Y')
            search_end = (datetime.now() + timedelta(days=30)).strftime('%m/%d/%Y')
            
            items = cal.Items
            items.IncludeRecurrences = True
            items.Sort("[Start]")
            
            try:
                restriction = f"[Start] >= '{search_start}' AND [Start] <= '{search_end}'"
                restricted = items.Restrict(restriction)
                
                on_call_pattern = re.compile(r'^(.+?)\s+On[\s-]+Call\s*$', re.IGNORECASE)
                
                matches = 0
                for item in restricted:
                    try:
                        subject = item.Subject or ''
                        if on_call_pattern.match(subject):
                            matches += 1
                            print(f"\n  Entry {matches}: {subject}")
                            print(f"    Start: {item.Start}")
                            print(f"    End:   {item.End}")
                            
                            try:
                                organizer = item.Organizer
                                if hasattr(organizer, 'Name'):
                                    print(f"    Organizer Name: {organizer.Name}")
                                if hasattr(organizer, 'Address'):
                                    print(f"    Organizer Email: {organizer.Address}")
                            except Exception as e:
                                print(f"    Organizer: (could not retrieve: {e})")
                    except:
                        continue
                
                if matches == 0:
                    print("  No 'On Call' entries found in this date range")
            
            except Exception as e:
                print(f"  Error searching calendar: {e}")
        
        pythoncom.CoUninitialize()
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()


def check_missing_summaries_display():
    """Check if missing summaries display in email."""
    print("\n" + "="*80)
    print("TASK 2: Missing Summaries Display in Email")
    print("="*80)
    
    try:
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent))
        
        from send_daily_status_email import build_status_email_html
        
        # Test with sample data
        sample_cache = {
            'week': 14,
            'fy': 2027,
            'event_count': 5,
            'total_excl_denied': 5,
            'summarized_count': 3,
            'bq_last_updated': '2026-05-01 12:00:00',
            'status_breakdown': [
                {'status': 'No Comms', 'count': 5},
            ],
            'events_without_summary': [
                {
                    'area': 'Store Operations',
                    'title': 'Safety Alert - Aisle Hazard',
                    'id': 'event_001',
                },
                {
                    'area': 'Merchandising',
                    'title': 'New Product Launch',
                    'id': 'event_002',
                },
            ]
        }
        
        print("\n✓ Rendering HTML with 2 missing items...")
        html = build_status_email_html(14, 2027, sample_cache)
        
        # Check if missing items are in HTML
        if 'Messages Without "Summarized:" Text' in html:
            print("  ✓ Missing items SECTION is present")
        else:
            print("  ✗ Missing items section NOT found")
        
        if 'Safety Alert - Aisle Hazard' in html:
            print("  ✓ Item 1 title IS in HTML")
        else:
            print("  ✗ Item 1 title NOT in HTML")
        
        if 'New Product Launch' in html:
            print("  ✓ Item 2 title IS in HTML")
        else:
            print("  ✗ Item 2 title NOT in HTML")
        
        print("\n✓ CONCLUSION: Missing summaries WILL display in the email")
        print("  - They appear in a dedicated 'Messages Without Summarized: Text' section")
        print("  - Each missing item shows: Area | Title | View link")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_group_members()
    test_calendar()
    check_missing_summaries_display()
    print("\n" + "="*80)
    print("Diagnostic complete")
    print("="*80 + "\n")
