#!/usr/bin/env python3
"""Check what accounts are available in Outlook"""

import win32com.client

print("Checking Outlook accounts...\n")

try:
    outlook = win32com.client.Dispatch('Outlook.Application')
    accounts = outlook.Session.Accounts
    
    print(f"Found {accounts.Count} account(s):\n")
    
    for i in range(1, accounts.Count + 1):
        account = accounts.Item(i)
        print(f"{i}. {account.DisplayName}")
        print(f"   Email: {account.SmtpAddress}")
        print(f"   Type: {account.AccountType}")
        print()
        
    # Check if shared mailbox is available
    shared_found = False
    for i in range(1, accounts.Count + 1):
        account = accounts.Item(i)
        if "supplychainops" in account.SmtpAddress.lower():
            shared_found = True
            print(f"✅ Shared mailbox FOUND: {account.SmtpAddress}")
            print(f"   Can use Outlook COM to send from this account!\n")
            break
    
    if not shared_found:
        print(f"❌ Shared mailbox NOT found in Outlook accounts")
        print(f"   Need to add supplychainops@email.wal-mart.com to Outlook\n")
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
