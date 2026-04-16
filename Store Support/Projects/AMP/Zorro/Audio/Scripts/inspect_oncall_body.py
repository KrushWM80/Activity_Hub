#!/usr/bin/env python3
"""Inspect the most recent On Call email body."""
import pythoncom
import win32com.client

pythoncom.CoInitialize()
outlook = win32com.client.Dispatch('Outlook.Application')
ns = outlook.GetNamespace('MAPI')
inbox = ns.GetDefaultFolder(6)
messages = inbox.Items
messages.Sort('[ReceivedTime]', True)

for msg in messages:
    try:
        subject = msg.Subject or ''
        if 'on call' in subject.lower() and 'planner' not in subject.lower():
            print(f"Subject: {subject}")
            print(f"From: {msg.SenderName}")
            print(f"Received: {msg.ReceivedTime}")
            print(f"To: {msg.To}")
            body = msg.Body or ''
            print(f"Body length: {len(body)}")
            print("--- Body ---")
            print(body[:2000])
            print("--- End Body ---")
            html = msg.HTMLBody or ''
            print(f"\nHTML length: {len(html)}")
            if html:
                print("--- HTML (first 2000) ---")
                print(html[:2000])
                print("--- End HTML ---")
            break
    except Exception as e:
        print(f"Error: {e}")
        continue

pythoncom.CoUninitialize()
