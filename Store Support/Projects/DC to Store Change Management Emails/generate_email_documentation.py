#!/usr/bin/env python3
"""
Email Flow Demonstration & Real Example Generator
Shows how emails are created, who receives them, and the complete process flow.
"""

import json
from datetime import datetime
from pathlib import Path

# Email Flow Documentation
EMAIL_FLOW_DOCUMENTATION = """
╔════════════════════════════════════════════════════════════════════════════════╗
║               DC TO STORE CHANGE MANAGEMENT - EMAIL FLOW PROCESS               ║
╚════════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────────────┐
│ STEP 1: HOURLY TRIGGER                                                          │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│ ✓ Windows Task Scheduler runs: daily_check_smart.py (Every hour)               │
│   └─ Execution: 2:00 AM + every hour after                                      │
│                                                                                  │
│ ✓ Script checks: "Do we have today's snapshot?"                                │
│   └─ If YES: Exit (already processed once today)                               │
│   └─ If NO: Proceed to create snapshot                                         │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│ STEP 2: DATA COLLECTION (IF FIRST RUN OF THE DAY)                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│ ✓ Check VPN connection (required for SDL access)                               │
│                                                                                  │
│ ✓ If VPN connected:                                                            │
│   ├─ Scrape SDL (Store Directory Lookup): ~5,200 locations                     │
│   ├─ Export manager data in JSON format                                         │
│   └─ Save as: snapshots_local/manager_snapshot_YYYY-MM-DD.json                │
│                                                                                  │
│ ✓ If VPN NOT connected:                                                        │
│   ├─ Log retry attempt                                                         │
│   ├─ Check if 7-day retry limit exceeded                                      │
│   └─ If exceeded: Send error email to admin                                    │
│                                                                                  │
│ ✓ 7-Day Retry Logic:                                                           │
│   ├─ Keeps retrying hourly for up to 7 days                                    │
│   ├─ Tracks attempt in: vpn_retry_tracker.json                                │
│   └─ Only sends error email AFTER 7 days with no VPN                          │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│ STEP 3: CHANGE DETECTION                                                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│ ✓ Compare with previous day's snapshot:                                        │
│   ├─ Today's snapshot:   snapshots_local/manager_snapshot_2026-01-22.json      │
│   └─ Yesterday's snap:   snapshots_local/manager_snapshot_2026-01-21.json      │
│                                                                                  │
│ ✓ Detect changes in 3 categories:                                              │
│   ├─ STORE MANAGER changes (affects individual stores)                        │
│   ├─ MARKET MANAGER changes (affects multiple stores in market)               │
│   └─ REGION MANAGER changes (affects entire region)                           │
│                                                                                  │
│ ✓ Changes stored in: ManagerChange objects with:                              │
│   ├─ Location ID (store/market/region number)                                 │
│   ├─ Location Name                                                             │
│   ├─ Previous Manager Name → New Manager Name                                 │
│   ├─ New Manager Email                                                         │
│   ├─ Market/Region context                                                     │
│   └─ Role type                                                                  │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│ STEP 4: GROUP BY DC (DISTRIBUTION CENTER)                                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│ ✓ Use DC-to-Store lookup: dc_to_stores_lookup.json                            │
│   ├─ Maps each store to its serving DC(s)                                      │
│   └─ Stores can be served by multiple DCs (Ambient + Perishable)              │
│                                                                                  │
│ ✓ Group all detected changes by DC:                                           │
│   ├─ DC 6020 (Ambient): [Manager Change 1, Manager Change 3, ...]            │
│   ├─ DC 6020 (Perishable): [Manager Change 5, ...]                           │
│   ├─ DC 6080 (Ambient): [Manager Change 2, ...]                              │
│   └─ [Continue for all affected DCs]                                           │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│ STEP 5: EMAIL GENERATION                                                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│ ✓ For each DC with changes, generate HTML email:                              │
│   ├─ Header: "Recent Field Leadership Updates" (Walmart Green theme)           │
│   ├─ Recipients Box: Shows who would receive in production                     │
│   ├─ Change Details: Organized by role type                                    │
│   │   ├─ STORE MANAGER (X changes)                                            │
│   │   │   └─ Card per store: old mgr → new mgr, market, email               │
│   │   ├─ MARKET MANAGER (X changes)                                           │
│   │   │   └─ Card per market: old mgr → new mgr, email                       │
│   │   └─ REGION MANAGER (X changes)                                           │
│   │       └─ Card per region: old mgr → new mgr, email                       │
│   ├─ Summary: Total changes, DC recipients count                              │
│   └─ Footer: Disclaimer, no-reply notice                                      │
│                                                                                  │
│ ✓ Styling features:                                                            │
│   ├─ Walmart brand colors (Green header, Blue accents)                        │
│   ├─ Responsive design (mobile-friendly)                                       │
│   ├─ Strikethrough old managers (red), green new managers                     │
│   ├─ Clickable SDL links (Store numbers link to SDL lookup)                   │
│   └─ Card-based layout for easy scanning                                       │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│ STEP 6: DETERMINE RECIPIENTS (TEST MODE vs PRODUCTION)                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│ ➤ TEST MODE (Current - config.TEST_MODE = True)                               │
│   ├─ Test Email Address: kendall.rush@walmart.com                             │
│   ├─ Email SENDS TO: kendall.rush@walmart.com                                │
│   ├─ Email SHOWS: Production recipients list (for visibility)                 │
│   └─ Purpose: Test entire flow without affecting DC leaders                  │
│                                                                                  │
│ ➤ PRODUCTION MODE (Future - config.TEST_MODE = False)                         │
│   ├─ Email SENDS TO: DC leadership distribution lists (BCC)                   │
│   ├─ DC Leadership emails: <DC#>GM@email.wal-mart.com (General Manager)       │
│   │                        <DC#>AGM@email.wal-mart.com (Assistant GM)         │
│   ├─ Example recipients for DC 6020:                                          │
│   │   ├─ 6020GM@email.wal-mart.com                                            │
│   │   └─ 6020AGM@email.wal-mart.com                                           │
│   └─ Example recipients for DC 6080:                                          │
│       ├─ 6080GM@email.wal-mart.com                                            │
│       └─ 6080AGM@email.wal-mart.com                                           │
│                                                                                  │
│ ➤ RECIPIENT CALCULATION                                                        │
│   ├─ For each DC number served by a store with changes:                       │
│   │   └─ Add that DC's GM and AGM to distribution list                        │
│   ├─ Remove duplicates (stores may be in multiple markets)                    │
│   ├─ Add GLOBAL_CC addresses (if configured)                                   │
│   └─ Use BCC to hide other recipients from each person                        │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│ STEP 7: EMAIL SENDING                                                           │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│ ✓ Send via Microsoft Graph (or Outlook COM):                                   │
│   ├─ From: supplychainops@email.wal-mart.com                                  │
│   ├─ Subject: "Manager Changes in Your DC Territory - YYYY-MM-DD"             │
│   ├─ Body: [Beautiful HTML email generated in STEP 5]                         │
│   ├─ BCC: [All DC leadership recipients from STEP 6]                          │
│   ├─ Reply-To: [Configured - typically no-reply to prevent responses]         │
│   └─ Headers: Auto-Submitted, Precedence: bulk (to suppress auto-replies)    │
│                                                                                  │
│ ✓ Email History Logging:                                                       │
│   ├─ Date Sent                                                                 │
│   ├─ Recipients Count                                                          │
│   ├─ Changes Count                                                             │
│   ├─ DC Territory                                                              │
│   ├─ Change Types (Store/Market/Region Manager counts)                        │
│   └─ Email Delivery Status                                                     │
│                                                                                  │
│ ✓ If no changes detected:                                                      │
│   └─ NO EMAIL SENT (saves mailboxes from noise)                               │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│ STEP 8: CYCLE COMPLETION                                                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│ ✓ Current Schedule: HOURLY (for development/testing)                           │
│   └─ Task runs every hour to check for changes (idempotent - only acts once)   │
│                                                                                  │
│ ➤ Future Schedule: BI-WEEKLY (aligned with pay cycles)                        │
│   ├─ Will adjust Task Scheduler to run on pay cycle dates                     │
│   ├─ Likely: Every other Friday or specific date                              │
│   └─ Can reduce email noise while still tracking leadership changes           │
│                                                                                  │
│ ✓ Cleanup tasks:                                                               │
│   ├─ Clear VPN retry tracker (if successful)                                  │
│   └─ Archive old snapshots after 30 days (optional)                           │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

╔════════════════════════════════════════════════════════════════════════════════╗
║                              CONFIGURATION NOTES                               ║
╚════════════════════════════════════════════════════════════════════════════════╝

📁 KEY FILES & FOLDERS:
├─ snapshots_local/                  ← Daily manager snapshots (JSON files)
├─ emails_pending/                   ← Queued emails awaiting send
├─ reports/                          ← Generated reports and metrics
├─ dc_to_stores_lookup.json          ← DC-to-Store mapping (from LAS API)
├─ config.py                         ← Main configuration (TEST_EMAIL, roles, etc.)
├─ dc_email_config.py                ← Email-specific config (TEST_MODE, sender, etc.)
├─ dc_leadership_config.py           ← DC recipient distribution lists
└─ vpn_retry_tracker.json            ← VPN retry state (created as needed)

⚙️ CURRENT SETTINGS:
├─ TEST_MODE: True
│   └─ All emails go to: kendall.rush@walmart.com
├─ TEST_EMAIL: kendall.rush@walmart.com
├─ SEND_FROM_EMAIL: supplychainops@email.wal-mart.com
├─ USE_BCC: True (hides recipients from each other)
├─ VPN_RETRY_ENABLED: True (7-day retry on VPN disconnect)
├─ EMAIL_ENABLED: True
└─ EMAIL_METHOD: MSGRAPH (Microsoft Graph API)

🔧 TO SWITCH TO PRODUCTION MODE:
   1. config.py          → Set TEST_MODE = False
   2. dc_email_config.py → Set TEST_MODE = False
   3. Then emails will send to DC leadership emails automatically

📊 FUTURE DASHBOARD WILL TRACK:
├─ Email sending history (when, to whom, count)
├─ Change metrics by DC, by role type
├─ Email delivery confirmations
├─ Trends and patterns over time
└─ Impact analysis (which stores/markets had most changes)

"""

# Create the documentation file
def create_email_flow_documentation():
    """Create email flow documentation"""
    doc_file = Path("EMAIL_FLOW_DOCUMENTATION.txt")
    with open(doc_file, 'w', encoding='utf-8') as f:
        f.write(EMAIL_FLOW_DOCUMENTATION)
    print(f"✓ Created: {doc_file}\n")


# Create sample data for example email
def create_sample_data_for_email():
    """Create sample snapshot data to demonstrate email generation"""
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Sample snapshot data (what SDL would return)
    sample_snapshot = {
        "date": today,
        "source": "SDL Export",
        "locations": [
            {
                "location_id": "1234",
                "location_name": "PLANO, TX",
                "location_type": "Walmart Supercenter",
                "store_manager": "Sarah Johnson",
                "store_manager_email": "sarah.johnson@walmart.com",
                "market": "Dallas/Fort Worth",
                "region": "Texas",
                "division": "WAL-MART STORES INC.",
                "banner": "WM Supercenter",
                "operating_status": 1
            },
            {
                "location_id": "5678",
                "location_name": "ARLINGTON, TX",
                "location_type": "Walmart Supercenter",
                "store_manager": "David Martinez",
                "store_manager_email": "david.martinez@walmart.com",
                "market": "Dallas/Fort Worth",
                "region": "Texas",
                "division": "WAL-MART STORES INC.",
                "banner": "WM Supercenter",
                "operating_status": 1
            },
            {
                "location_id": "9012",
                "location_name": "HOUSTON, TX",
                "location_type": "Walmart Supercenter",
                "store_manager": "Robert Williams",
                "store_manager_email": "robert.williams@walmart.com",
                "market": "Houston",
                "region": "Texas",
                "division": "WAL-MART STORES INC.",
                "banner": "WM Supercenter",
                "operating_status": 1
            },
            {
                "location_id": "3456",
                "location_name": "AUSTIN, TX",
                "location_type": "Walmart Supercenter",
                "store_manager": "Christopher Brown",
                "store_manager_email": "christopher.brown@walmart.com",
                "market": "Austin",
                "region": "Texas",
                "division": "WAL-MART STORES INC.",
                "banner": "WM Supercenter",
                "operating_status": 1
            },
            {
                "location_id": "DFW_MARKET",
                "location_name": "Dallas/Fort Worth Market",
                "location_type": "Market",
                "market_manager": "Amanda Foster",
                "market_manager_email": "amanda.foster@walmart.com",
                "region": "Texas",
                "market_type": "Distribution Market"
            },
            {
                "location_id": "HOU_MARKET",
                "location_name": "Houston Market",
                "location_type": "Market",
                "market_manager": "Patricia Rivera",
                "market_manager_email": "patricia.rivera@walmart.com",
                "region": "Texas",
                "market_type": "Distribution Market"
            }
        ],
        "total_locations": 6,
        "summary": {
            "store_managers": 4,
            "market_managers": 2,
            "by_market": {
                "Dallas/Fort Worth": 2,
                "Houston": 2,
                "Austin": 1
            }
        }
    }
    
    sample_file = Path(f"snapshots_local/manager_snapshot_{today}_SAMPLE.json")
    sample_file.parent.mkdir(exist_ok=True)
    
    with open(sample_file, 'w') as f:
        json.dump(sample_snapshot, f, indent=2)
    
    print(f"✓ Created sample snapshot: {sample_file}\n")
    
    return sample_snapshot


def create_recipients_reference_document():
    """Create document explaining recipient logic"""
    
    recipients_doc = """
╔════════════════════════════════════════════════════════════════════════════════╗
║                     EMAIL RECIPIENTS REFERENCE GUIDE                           ║
╚════════════════════════════════════════════════════════════════════════════════╝

CURRENT TEST MODE (TEST_MODE = True)
====================================

All emails currently go to: kendall.rush@walmart.com

The "Production Distribution List" box in each email shows WHO WOULD RECEIVE
the email in production mode, so you can see the full recipient list without
actually sending to them.


PRODUCTION MODE (When TEST_MODE = False)
=========================================

Email Recipients are AUTOMATICALLY DETERMINED based on which DCs serve the
stores with detected changes.

EXAMPLE SCENARIO:
─────────────────

Suppose we detect manager changes at:
  • Store 1234 (PLANO, TX) - Served by DC 6020
  • Store 5678 (ARLINGTON, TX) - Served by DC 6020
  • Store 9012 (HOUSTON, TX) - Served by DC 6080

The system will:

  1. Look up DC assignments:
     ✓ Store 1234 → DC 6020 (Ambient) + DC 6040 (Perishable)
     ✓ Store 5678 → DC 6020 (Ambient) + DC 6040 (Perishable)
     ✓ Store 9012 → DC 6080 (Ambient) + DC 6090 (Perishable)

  2. Create recipient lists for affected DCs:
     ✓ DC 6020 Changes (4 changes total)
     ✓ DC 6040 Changes (4 changes total)
     ✓ DC 6080 Changes (1 change)
     ✓ DC 6090 Changes (1 change)

  3. For DC 6020, send email to:
     • 6020GM@email.wal-mart.com (DC 6020 General Manager)
     • 6020AGM@email.wal-mart.com (DC 6020 Assistant General Manager)

  4. For DC 6040, send email to:
     • 6040GM@email.wal-mart.com (DC 6040 General Manager)
     • 6040AGM@email.wal-mart.com (DC 6040 Assistant General Manager)

  5. For DC 6080, send email to:
     • 6080GM@email.wal-mart.com (DC 6080 General Manager)
     • 6080AGM@email.wal-mart.com (DC 6080 Assistant General Manager)

  6. For DC 6090, send email to:
     • 6090GM@email.wal-mart.com (DC 6090 General Manager)
     • 6090AGM@email.wal-mart.com (DC 6090 Assistant General Manager)

  ⚠️ NOTE: Each email is sent separately to each DC's team
     (Uses BCC so recipients don't see each other)


DC RECIPIENT PATTERN
====================

All DC recipients follow this pattern:

  Format: <DC_NUMBER><ROLE>@email.wal-mart.com

  Examples:
    6020GM  = DC 6020 General Manager
    6020AGM = DC 6020 Assistant General Manager
    6080GM  = DC 6080 General Manager
    6080AGM = DC 6080 Assistant General Manager

  DC Numbers: 6020, 6040, 6080, 6090, 6120, 6140, etc.
  Roles: GM (General Manager), AGM (Assistant General Manager)


ADDITIONAL RECIPIENTS (GLOBAL CC)
=================================

The system can also add additional recipients who should always get emails:

  • Set in: dc_leadership_config.py → GLOBAL_CC list
  • Example: GLOBAL_CC = ['supply.ops@walmart.com', 'ops.manager@walmart.com']
  • These will receive a BCC copy of EVERY email


HOW TO MODIFY RECIPIENTS
========================

To customize which managers receive notifications:

  1. Change DC Leadership Roles:
     File: dc_leadership_config.py → DC_LEADERSHIP_ROLES
     Default: ['GM', 'AGM']
     Can add: ['AGM', 'Operations Director'] etc.

  2. Change DC Email Domain:
     File: dc_leadership_config.py → DC_EMAIL_DOMAIN
     Default: 'email.wal-mart.com'
     Can change if domain updates

  3. Add Global Recipients:
     File: dc_leadership_config.py → GLOBAL_CC
     Add emails that should receive ALL notifications

  4. Filter by Manager Type:
     File: dc_leadership_config.py → DC_NOTIFICATION_ROLES
     Currently: {'Store Manager', 'Market Manager'}
     Add: 'Region Manager' if needed

  5. Minimum Changes Threshold:
     File: dc_leadership_config.py → MIN_CHANGES_FOR_DC_EMAIL
     Currently: 1 (send email if ANY change detected)
     Can change to: 5 (only send if 5+ changes)


TESTING EMAIL RECIPIENTS
========================

To see what recipients WOULD receive in production:

  1. Open any received email in test mode
  2. Look for: "Production Distribution List" box (yellow)
  3. This shows all the DCs and their GMs/AGMs that would get the email

Example Production Distribution List:
  • kendall.rush@walmart.com (TEST RECIPIENT - YOU)
  • 6020GM@email.wal-mart.com
  • 6020AGM@email.wal-mart.com
  • 6080GM@email.wal-mart.com
  • 6080AGM@email.wal-mart.com
  • 6040GM@email.wal-mart.com
  • 6040AGM@email.wal-mart.com


SWITCHING TO PRODUCTION MODE
============================

When ready to switch from test mode to production:

  1. Open: config.py
  2. Set: TEST_MODE = False

  3. Open: dc_email_config.py
  4. Set: TEST_MODE = False

  5. Verify: DC recipient emails look correct:
     $ python -c "from dc_leadership_config import get_dc_emails; print(get_dc_emails(6020))"
     Output: ['6020GM@email.wal-mart.com', '6020AGM@email.wal-mart.com']

  6. Test with one DC first (modify daily_check_smart.py to skip others)
  7. Monitor: Check Outlook to verify emails arrive
  8. Once confirmed: Remove test skip logic and run normally


TROUBLESHOOTING RECIPIENTS
==========================

Issue: "Email sent to wrong people"
  → Check: dc_to_stores_lookup.json (DC assignments)
  → Verify: Store is mapped to correct DC number

Issue: "DC emails have typos (6020G instead of 6020GM)"
  → Check: dc_leadership_config.py → DC_LEADERSHIP_ROLES format
  → Ensure: Role names are correct (GM, AGM, etc.)

Issue: "Some DCs not getting emails"
  → Check: Are stores served by those DCs in the changed list?
  → Verify: dc_to_stores_lookup.json includes those stores
  → Confirm: MIN_CHANGES_FOR_DC_EMAIL threshold met

Issue: "Same person getting multiple emails"
  → This is normal if they serve multiple DCs
  → Each DC gets a separate email with their territory's changes
  → Solution: Add deduplication logic if needed (contact admin)

"""
    
    recipients_file = Path("RECIPIENTS_REFERENCE.txt")
    with open(recipients_file, 'w', encoding='utf-8') as f:
        f.write(recipients_doc)
    print(f"✓ Created: {recipients_file}\n")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("EMAIL FLOW DOCUMENTATION & RECIPIENTS GUIDE GENERATOR")
    print("="*80 + "\n")
    
    # Create all documentation
    create_email_flow_documentation()
    create_recipients_reference_document()
    create_sample_data_for_email()
    
    print("="*80)
    print("DOCUMENTATION COMPLETE!")
    print("="*80)
    print("\n📄 Files created:\n")
    print("  1. EMAIL_FLOW_DOCUMENTATION.txt")
    print("     └─ Complete step-by-step breakdown of how emails are created")
    print("\n  2. RECIPIENTS_REFERENCE.txt")
    print("     └─ Detailed guide on who receives emails and why")
    print("\n  3. snapshots_local/manager_snapshot_<date>_SAMPLE.json")
    print("     └─ Sample data demonstrating the email generation process")
    print("\nOpen these files to understand the complete email flow!\n")
