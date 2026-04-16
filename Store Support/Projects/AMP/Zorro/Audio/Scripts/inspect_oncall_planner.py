#!/usr/bin/env python3
"""
Inspect the U.S. Comm - On Call Planner email from Outlook.
Diagnostic script to understand the email format before building the parser.
"""
import pythoncom
import win32com.client
from datetime import datetime, timedelta

pythoncom.CoInitialize()
outlook = win32com.client.Dispatch('Outlook.Application')
ns = outlook.GetNamespace('MAPI')
inbox = ns.GetDefaultFolder(6)  # 6 = olFolderInbox

# Search for recent planner emails (last 14 days)
cutoff = (datetime.now() - timedelta(days=14)).strftime('%m/%d/%Y')
messages = inbox.Items
messages.Sort("[ReceivedTime]", True)  # newest first

print("=" * 70)
print("Searching for 'On Call Planner' emails in Inbox (last 14 days)...")
print("=" * 70)

found = 0
for msg in messages:
    try:
        received = msg.ReceivedTime
        if received.strftime('%Y-%m-%d') < (datetime.now() - timedelta(days=14)).strftime('%Y-%m-%d'):
            break
        subject = msg.Subject or ''
        if 'on call' in subject.lower() or 'planner' in subject.lower():
            found += 1
            print(f"\n--- Match #{found} ---")
            print(f"Subject:  {subject}")
            print(f"From:     {msg.SenderName} <{msg.SenderEmailAddress}>")
            print(f"Received: {received.strftime('%Y-%m-%d %I:%M %p')}")
            print(f"To:       {msg.To[:120] if msg.To else 'N/A'}...")
            print(f"\nBody (first 2000 chars):")
            print("-" * 50)
            body = msg.Body or ''
            print(body[:2000])
            print("-" * 50)
            
            # Also check HTML body for table structure
            html = msg.HTMLBody or ''
            if '<table' in html.lower():
                print(f"\n[HTML contains table(s) — {html.lower().count('<table')} table tag(s)]")
            
            if found >= 3:  # Show up to 3 matches
                break
    except Exception as e:
        continue

if found == 0:
    print("\nNo matching emails found. Trying broader search...")
    # Try searching all folders
    for msg in messages:
        try:
            subject = msg.Subject or ''
            if 'comm' in subject.lower() and ('call' in subject.lower() or 'plan' in subject.lower()):
                print(f"\n  Possible match: {subject}")
                print(f"  From: {msg.SenderName}")
                print(f"  Received: {msg.ReceivedTime.strftime('%Y-%m-%d')}")
                found += 1
                if found >= 5:
                    break
        except:
            continue

print(f"\n{'=' * 70}")
print(f"Total matches found: {found}")
pythoncom.CoUninitialize()
