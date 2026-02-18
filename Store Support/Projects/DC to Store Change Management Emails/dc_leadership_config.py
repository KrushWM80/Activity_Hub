#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DC Leadership Distribution Lists
Auto-generates DC leadership emails based on standard naming convention.
"""

# ============================================================================
# DC LEADERSHIP ROLES
# ============================================================================

# Standard DC leadership roles that receive manager change notifications
DC_LEADERSHIP_ROLES = [
    'GM',   # General Manager
    'AGM',  # Assistant General Manager
]

# Email domain
DC_EMAIL_DOMAIN = 'email.wal-mart.com'

# ============================================================================
# NOTIFICATION RULES
# ============================================================================

# Which manager roles trigger DC notifications?
DC_NOTIFICATION_ROLES = {
    'Store Manager',     # Store-level changes
    'Market Manager',    # Market-level changes (affects multiple stores in DC territory)
    # 'Region Manager',  # Uncomment if you want DC teams notified of regional changes
}

# Minimum changes before sending email to DC?
MIN_CHANGES_FOR_DC_EMAIL = 1

# Send "no changes" confirmation to DCs?
SEND_DC_NO_CHANGE_EMAIL = False  # DCs only want to know about changes

# ============================================================================
# ADDITIONAL RECIPIENTS
# ============================================================================

# Always CC these emails on all DC notifications
GLOBAL_CC = [
    # 'your.email@homeoffice.wal-mart.com',
    # 'your.manager@homeoffice.wal-mart.com',
]

# ============================================================================
# EMAIL TEMPLATES
# ============================================================================

DC_EMAIL_SUBJECT = "Manager Changes in Your DC Territory - {date}"

DC_EMAIL_INTRO = """
The following manager changes were detected in stores/markets served by your DC.

These changes may impact your supply chain coordination and store relationships.
"""

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_dc_emails(dc_number, dc_type='Ambient'):
    """
    Generate email distribution list for a DC based on standard naming convention.
    
    Args:
        dc_number: DC number (int)
        dc_type: 'Ambient' or 'Perishable' (for logging/display only)
    
    Returns:
        List of email addresses
    
    Example:
        get_dc_emails(6020) returns:
        ['6020GM@email.wal-mart.com', '6020AGM@email.wal-mart.com']
    """
    emails = []
    
    for role in DC_LEADERSHIP_ROLES:
        email = f"{dc_number}{role}@{DC_EMAIL_DOMAIN}"
        emails.append(email)
    
    return emails

def get_all_dc_emails_for_store(store_number, dc_lookup):
    """
    Get all DC leadership emails for a store.
    Includes BOTH Ambient and Perishable DC teams.
    
    Args:
        store_number: Store number (int)
        dc_lookup: DC lookup dict from dc_to_stores_lookup.json
    
    Returns:
        Dict: {
            'ambient_dc': DC_number or None,
            'ambient_emails': [list of emails],
            'perishable_dc': DC_number or None,
            'perishable_emails': [list of emails],
            'all_emails': [combined list]
        }
    """
    result = {
        'ambient_dc': None,
        'ambient_emails': [],
        'perishable_dc': None,
        'perishable_emails': [],
        'all_emails': []
    }
    
    # Find which DCs serve this store
    for dc_num, dc_info in dc_lookup.items():
        dc_num = int(dc_num)
        if store_number in dc_info.get('stores', []):
            dc_type = dc_info.get('type', 'Unknown')
            emails = get_dc_emails(dc_num, dc_type)
            
            if dc_type == 'Ambient':
                result['ambient_dc'] = dc_num
                result['ambient_emails'] = emails
            elif dc_type == 'Perishable':
                result['perishable_dc'] = dc_num
                result['perishable_emails'] = emails
            
            result['all_emails'].extend(emails)
    
    # Remove duplicates while preserving order
    result['all_emails'] = list(dict.fromkeys(result['all_emails']))
    
    return result

def get_dc_display_name(dc_number, dc_type='DC'):
    """
    Get friendly display name for a DC.
    
    Args:
        dc_number: DC number (int)
        dc_type: 'Ambient', 'Perishable', or 'DC'
    
    Returns:
        Display name string
    """
    if dc_type == 'Ambient':
        return f"DC {dc_number} (Regional)"
    elif dc_type == 'Perishable':
        return f"DC {dc_number} (Food)"
    else:
        return f"DC {dc_number}"

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("\nDC Leadership Email Generator Test\n")
    print("="*60)
    
    # Test DC 6020
    print("\nExample: DC 6020")
    emails = get_dc_emails(6020)
    print(f"  Emails: {', '.join(emails)}")
    
    # Test DC 6082
    print("\nExample: DC 6082")
    emails = get_dc_emails(6082)
    print(f"  Emails: {', '.join(emails)}")
    
    # Test store with both
    print("\nExample: Store 1 (has both Ambient and Perishable DCs)")
    print("  Ambient DC 6094:")
    print(f"    {', '.join(get_dc_emails(6094, 'Ambient'))}")
    print("  Perishable DC 6082:")
    print(f"    {', '.join(get_dc_emails(6082, 'Perishable'))}")
    print(f"\n  Total: 4 emails sent for one store change")
    print("="*60 + "\n")
