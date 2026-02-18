"""
Quick User ID Lookup - Simple command line wrapper
Usage: python quick_lookup.py email1 [email2 email3 ...]
"""

import sys
from user_id_lookup import UserIDLookup

def main():
    if len(sys.argv) < 2:
        print("\nUsage: python quick_lookup.py <email1> [email2 email3 ...]")
        print("\nExample:")
        print("  python quick_lookup.py nathan.schmidt0@wal-mart.com")
        print("  python quick_lookup.py crystal.mcdonagh@walmart.com scott.lukomske@walmart.com")
        print("\nNote: Works with both @walmart.com and @wal-mart.com domains")
        sys.exit(1)
    
    # Get emails from command line arguments
    emails = sys.argv[1:]
    
    print("\n" + "=" * 100)
    print("USER ID LOOKUP")
    print("=" * 100)
    
    # Initialize lookup
    lookup = UserIDLookup()
    
    # Search for all emails
    results = lookup.search_multiple(emails)
    
    # Display results
    lookup.display_results(results, show_all_fields=False)
    
    # Summary
    print(f"\nSearched for {len(emails)} email(s), found {len(results)} match(es)")
    
    # List emails not found
    if len(results) < len(emails):
        found_emails = set(results[lookup.email_column].str.lower() if not results.empty else [])
        not_found = []
        for email in emails:
            email_base = email.lower().replace('@walmart.com', '').replace('@wal-mart.com', '')
            found = any(email_base in found_email.lower() for found_email in found_emails)
            if not found:
                not_found.append(email)
        
        if not_found:
            print("\nEmails not found:")
            for email in not_found:
                print(f"  ✗ {email}")

if __name__ == "__main__":
    main()
