#!/usr/bin/env python3
"""
Diagnostic script to inspect the U.S. Comm - On Call Planner group and calendar.
"""
import pythoncom
import win32com.client
from datetime import datetime, timedelta

def inspect_oncall_group():
    """Pull all members of the U.S. Comm - On Call Planner group."""
    print("\n" + "="*80)
    print("TASK 1: Inspecting U.S. Comm - On Call Planner GROUP MEMBERS")
    print("="*80)
    
    pythoncom.CoInitialize()
    try:
        outlook = win32com.client.Dispatch('Outlook.Application')
        ns = outlook.GetNamespace('MAPI')
        
        # Find the group
        gal = ns.GetGlobalAddressList()
        group = None
        
        for entry in gal.AddressEntries:
            if entry.Name == 'U.S. Comm - On Call Planner':
                group = entry.GetExchangeDistributionList()
                print(f"\n✓ Found group: {entry.Name}")
                break
        
        if not group:
            print("✗ Could not find 'U.S. Comm - On Call Planner' group")
            return
        
        # Get members
        members = group.GetExchangeDistributionListMembers()
        print(f"\nGroup Members ({len(members)} total):")
        print("-" * 80)
        
        for member in members:
            try:
                print(f"  • {member.Name:<30} | {member.Address}")
            except:
                print(f"  • {member.Name}")
    
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        try:
            pythoncom.CoUninitialize()
        except:
            pass


def inspect_oncall_calendar():
    """Pull all on-call calendar entries and their organizers."""
    print("\n" + "="*80)
    print("TASK 1: Inspecting U.S. Comm - On Call Planner CALENDAR ENTRIES")
    print("="*80)
    
    pythoncom.CoInitialize()
    try:
        outlook = win32com.client.Dispatch('Outlook.Application')
        ns = outlook.GetNamespace('MAPI')
        
        # Find the shared calendar
        cal = None
        for folder in ns.Folders:
            try:
                if folder.Name == 'U.S. Comm - On Call Planner':
                    cal = folder.Folders['Calendar']
                    print(f"\n✓ Found calendar: {folder.Name}")
                    break
            except:
                continue
        
        if cal is None:
            print("✗ Could not find 'U.S. Comm - On Call Planner' calendar")
            return
        
        # Search for last 60 days of entries
        search_start = (datetime.now() - timedelta(days=60)).strftime('%m/%d/%Y')
        search_end = (datetime.now() + timedelta(days=60)).strftime('%m/%d/%Y')
        
        items = cal.Items
        items.IncludeRecurrences = True
        items.Sort("[Start]")
        restriction = f"[Start] >= '{search_start}' AND [Start] <= '{search_end}'"
        restricted = items.Restrict(restriction)
        
        print(f"\nCalendar Entries (from {search_start} to {search_end}):")
        print("-" * 80)
        
        for item in restricted:
            try:
                subject = item.Subject or '(no subject)'
                start = item.Start
                end = item.End
                
                # Try to get organizer email
                try:
                    organizer = item.Organizer
                    org_email = organizer.Address if hasattr(organizer, 'Address') else str(organizer)
                    org_name = organizer.Name if hasattr(organizer, 'Name') else str(organizer)
                except:
                    org_email = "(no organizer)"
                    org_name = "(no organizer)"
                
                print(f"\n  Subject: {subject}")
                print(f"    Start:     {start}")
                print(f"    End:       {end}")
                print(f"    Organizer: {org_name} ({org_email})")
                
            except Exception as e:
                print(f"  Error reading entry: {e}")
    
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        try:
            pythoncom.CoUninitialize()
        except:
            pass


def check_missing_summaries():
    """Check if missing summaries show in the test email."""
    print("\n" + "="*80)
    print("TASK 2: Checking Missing Summaries Display Logic")
    print("="*80)
    
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    
    try:
        from generate_weekly_audio import get_coming_wm_week_fy, fetch_and_cache_bq_data
        from send_daily_status_email import build_status_email_html
        
        week, fy = get_coming_wm_week_fy()
        print(f"\nComing WM Week: WK{week} FY{fy}")
        
        # Fetch cache
        cache_data = fetch_and_cache_bq_data(week, fy)
        
        if 'error' in cache_data:
            print(f"Note: {cache_data['error']}")
            cache_data = {
                'event_count': 0,
                'total_excl_denied': 0,
                'summarized_count': 0,
                'status_breakdown': [],
                'events_without_summary': [],
                'bq_last_updated': '',
            }
        
        # Check the data
        total_excl = cache_data.get('total_excl_denied', 0)
        summarized = cache_data.get('summarized_count', 0)
        missing_list = cache_data.get('events_without_summary', [])
        missing_count = total_excl - summarized
        
        print(f"\nSummary Counts:")
        print(f"  Total (excl. Denied/Expired): {total_excl}")
        print(f"  With 'Summarized:' text:      {summarized}")
        print(f"  Missing count (calculated):  {missing_count}")
        print(f"  Missing items in list:       {len(missing_list)}")
        
        print(f"\n✓ Logic Check:")
        if missing_count == len(missing_list):
            print(f"  ✓ PASS: Missing count matches list length ({missing_count} items)")
        else:
            print(f"  ⚠ WARNING: Mismatch - calculated {missing_count} but list has {len(missing_list)}")
        
        if len(missing_list) > 0:
            print(f"\n✓ Missing Items WILL Show in Email:")
            print(f"  The events_without_summary list has {len(missing_list)} items")
            print(f"  These will display in the 'Messages Without Summarized: Text' section")
            for i, item in enumerate(missing_list[:3], 1):
                title = item.get('title', '(no title)')
                area = item.get('area', '(no area)')
                print(f"    {i}. [{area}] {title}")
            if len(missing_list) > 3:
                print(f"    ... and {len(missing_list) - 3} more")
        else:
            print(f"\n✓ No Missing Items Currently")
            print(f"  All {summarized} messages have 'Summarized:' text")
            print(f"  'Messages Without Summarized: Text' section will be empty")
    
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    inspect_oncall_group()
    inspect_oncall_calendar()
    check_missing_summaries()
    print("\n" + "="*80)
    print("Inspection complete")
    print("="*80 + "\n")
