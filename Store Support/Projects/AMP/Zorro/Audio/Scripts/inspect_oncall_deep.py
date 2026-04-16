#!/usr/bin/env python3
"""Deep inspect the Dana Mason On Call item."""
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
        if subject == 'Dana Mason On Call':
            print(f"Subject: {subject}")
            print(f"Class: {msg.Class}")  # 43=mail, 26=appointment, etc.
            print(f"MessageClass: {msg.MessageClass}")
            print(f"From: {msg.SenderName}")
            print(f"Received: {msg.ReceivedTime}")
            
            body = msg.Body or ''
            print(f"Body length: {len(body)}")
            print("--- Body ---")
            print(body[:3000])
            print("--- End Body ---")
            
            html = msg.HTMLBody or ''
            print(f"\nHTML length: {len(html)}")
            print("--- HTML (first 3000) ---")
            print(html[:3000])
            print("--- End HTML ---")
            
            # Try common properties safely
            for attr in ['Categories', 'SenderEmailAddress', 'CC', 'BCC']:
                try:
                    val = getattr(msg, attr, 'N/A')
                    print(f"{attr}: {val}")
                except:
                    print(f"{attr}: (error)")
            break
    except Exception as e:
        print(f"Error on item: {e}")
        continue

pythoncom.CoUninitialize()
