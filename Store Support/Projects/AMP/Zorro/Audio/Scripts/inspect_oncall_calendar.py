#!/usr/bin/env python3
"""Search calendar for On Call entries and inbox for the planner pattern."""
import pythoncom
import win32com.client
from datetime import datetime, timedelta

pythoncom.CoInitialize()
outlook = win32com.client.Dispatch('Outlook.Application')
ns = outlook.GetNamespace('MAPI')

# --- Search Calendar for On Call items ---
print("=" * 70)
print("CALENDAR - On Call items (next 14 days)")
print("=" * 70)

cal = ns.GetDefaultFolder(9)  # 9 = olFolderCalendar
items = cal.Items
items.IncludeRecurrences = True
items.Sort("[Start]")

start_date = datetime.now().strftime('%m/%d/%Y')
end_date = (datetime.now() + timedelta(days=14)).strftime('%m/%d/%Y')
restriction = f"[Start] >= '{start_date}' AND [Start] <= '{end_date}'"
restricted = items.Restrict(restriction)

found_cal = 0
for item in restricted:
    try:
        subject = item.Subject or ''
        if 'on call' in subject.lower() or 'comm' in subject.lower():
            found_cal += 1
            print(f"\n--- Calendar #{found_cal} ---")
            print(f"Subject:   {subject}")
            print(f"Start:     {item.Start}")
            print(f"End:       {item.End}")
            print(f"Organizer: {item.Organizer}")
            print(f"Location:  {item.Location}")
            body = item.Body or ''
            print(f"Body length: {len(body)}")
            if body.strip():
                print(f"Body preview: {body[:500]}")
            if found_cal >= 10:
                break
    except Exception as e:
        continue

print(f"\nCalendar matches: {found_cal}")

# --- Search Inbox for meeting requests with On Call ---
print("\n" + "=" * 70)
print("INBOX - Meeting requests with 'On Call' (last 30 days)")
print("=" * 70)

inbox = ns.GetDefaultFolder(6)
messages = inbox.Items
messages.Sort('[ReceivedTime]', True)

found_inbox = 0
cutoff = datetime.now() - timedelta(days=30)
for msg in messages:
    try:
        received = msg.ReceivedTime
        if received.replace(tzinfo=None) < cutoff:
            break
        subject = msg.Subject or ''
        mc = getattr(msg, 'MessageClass', '')
        if 'on call' in subject.lower():
            found_inbox += 1
            print(f"\n--- Inbox #{found_inbox} ---")
            print(f"Subject:      {subject}")
            print(f"MessageClass: {mc}")
            print(f"From:         {msg.SenderName}")
            print(f"Received:     {received}")
            body = msg.Body or ''
            if body.strip():
                print(f"Body: {body[:300]}")
            if found_inbox >= 10:
                break
    except:
        continue

print(f"\nInbox meeting request matches: {found_inbox}")

pythoncom.CoUninitialize()
