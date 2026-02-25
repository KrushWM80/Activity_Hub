#!/usr/bin/env python3
"""
PayCycle Email Management Utility
Manage recipients, track sends, and monitor PayCycle schedule
"""

import json
from pathlib import Path
from datetime import datetime
import sys


class PayCycleManager:
    def __init__(self):
        self.tracking_file = Path("paycycle_tracking.json")
        self.recipients_file = Path("email_recipients.json")
        
    def load_tracking(self):
        """Load tracking data"""
        with open(self.tracking_file, 'r') as f:
            return json.load(f)
    
    def load_recipients(self):
        """Load recipients configuration"""
        with open(self.recipients_file, 'r') as f:
            return json.load(f)
    
    def save_tracking(self, data):
        """Save tracking data"""
        with open(self.tracking_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✓ Tracking updated: {self.tracking_file}")
    
    def save_recipients(self, data):
        """Save recipients configuration"""
        with open(self.recipients_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✓ Recipients updated: {self.recipients_file}")
    
    def show_schedule(self):
        """Display full PayCycle schedule"""
        tracking = self.load_tracking()
        
        print("\n" + "="*80)
        print("PAYCYCLE SCHEDULE - 2026 & 2027")
        print("="*80 + "\n")
        
        for cycle in tracking['paycycles']:
            date = cycle['paycycle_date']
            status = cycle['status'].upper()
            status_symbol = "✓" if status == "COMPLETED" else "→" if status == "SCHEDULED" else "✗"
            
            print(f"{status_symbol} PC {cycle['pc_number']:02d} | {date} @ {cycle['scheduled_send_time']} | Status: {status:12} | {cycle.get('notes', '')}")
        
        print("\n" + "="*80)
        print(f"Summary: {tracking['summary']['completed']} completed, {tracking['summary']['scheduled']} scheduled")
        print("="*80 + "\n")
    
    def show_recipients(self):
        """Display current recipients configuration"""
        recipients = self.load_recipients()
        mode = recipients['active_mode']
        
        print("\n" + "="*80)
        print(f"EMAIL RECIPIENTS - Active Mode: {mode.upper()}")
        print("="*80 + "\n")
        
        for mode_name, mode_config in recipients['modes'].items():
            if mode_config['active']:
                print(f"[ACTIVE] {mode_name.upper()} Mode")
                print(f"Description: {mode_config['description']}")
                print(f"Total Recipients: {len([r for r in mode_config['recipients'] if r['active']])}/{len(mode_config['recipients'])}\n")
                
                for recipient in mode_config['recipients']:
                    active = "✓" if recipient['active'] else "✗"
                    print(f"  {active} {recipient['email']:40} ({recipient['role']})")
                    if recipient.get('notes'):
                        print(f"     Note: {recipient['notes']}")
                print()
        
        print("="*80 + "\n")
    
    def add_recipient(self, mode, email, name, role):
        """Add a new recipient"""
        recipients = self.load_recipients()
        
        if mode not in recipients['modes']:
            print(f"✗ Mode '{mode}' not found. Use 'test' or 'production'.")
            return False
        
        # Check if already exists
        existing = [r for r in recipients['modes'][mode]['recipients'] if r['email'] == email]
        if existing:
            print(f"✗ {email} already exists in {mode} mode")
            return False
        
        # Add new recipient
        recipients['modes'][mode]['recipients'].append({
            "name": name,
            "email": email,
            "role": role,
            "active": True
        })
        
        recipients['modes'][mode]['total_count'] = len(recipients['modes'][mode]['recipients'])
        recipients['modes'][mode]['last_updated'] = datetime.now().isoformat()
        
        self.save_recipients(recipients)
        print(f"✓ Added {email} to {mode} mode")
        return True
    
    def remove_recipient(self, mode, email):
        """Remove a recipient"""
        recipients = self.load_recipients()
        
        if mode not in recipients['modes']:
            print(f"✗ Mode '{mode}' not found")
            return False
        
        # Find and remove
        before = len(recipients['modes'][mode]['recipients'])
        recipients['modes'][mode]['recipients'] = [
            r for r in recipients['modes'][mode]['recipients'] if r['email'] != email
        ]
        after = len(recipients['modes'][mode]['recipients'])
        
        if after < before:
            recipients['modes'][mode]['total_count'] = after
            recipients['modes'][mode]['last_updated'] = datetime.now().isoformat()
            self.save_recipients(recipients)
            print(f"✓ Removed {email} from {mode} mode")
            return True
        else:
            print(f"✗ {email} not found in {mode} mode")
            return False
    
    def toggle_mode(self, new_mode):
        """Switch between test and production mode"""
        recipients = self.load_recipients()
        
        if new_mode not in recipients['modes']:
            print(f"✗ Mode must be 'test' or 'production'")
            return False
        
        recipients['active_mode'] = new_mode
        recipients['modes'][new_mode]['last_updated'] = datetime.now().isoformat()
        
        self.save_recipients(recipients)
        print(f"✓ Switched to {new_mode} mode")
        return True
    
    def record_send(self, pc_number, success=True, error_msg=None, recipients_count=3):
        """Record a PayCycle send"""
        tracking = self.load_tracking()
        
        # Find PayCycle
        cycle = None
        for c in tracking['paycycles']:
            if c['pc_number'] == pc_number:
                cycle = c
                break
        
        if not cycle:
            print(f"✗ PayCycle {pc_number} not found")
            return False
        
        # Update record
        cycle['actual_send_time'] = datetime.now().strftime("%H:%M:%S")
        cycle['actual_send_datetime'] = datetime.now().isoformat()
        cycle['status'] = 'completed' if success else 'failed'
        cycle['recipients_count'] = recipients_count
        cycle['error_message'] = error_msg
        
        # Update summary
        tracking['summary']['completed'] = len([c for c in tracking['paycycles'] if c['status'] == 'completed'])
        tracking['summary']['failed'] = len([c for c in tracking['paycycles'] if c['status'] == 'failed'])
        tracking['summary']['last_updated'] = datetime.now().isoformat()
        
        self.save_tracking(tracking)
        status = "✓ SENT" if success else "✗ FAILED"
        print(f"{status} PC {pc_number:02d} at {cycle['actual_send_time']}")
        return True
    
    def get_active_recipients(self):
        """Get active recipient emails (useful for integration with email system)"""
        recipients = self.load_recipients()
        mode = recipients['active_mode']
        
        emails = [
            r['email'] for r in recipients['modes'][mode]['recipients']
            if r['active'] and r['email'] != '[TO_BE_ADDED]'
        ]
        return emails


def main():
    """CLI interface for PayCycle management"""
    
    manager = PayCycleManager()
    
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'schedule':
        manager.show_schedule()
    
    elif command == 'recipients':
        manager.show_recipients()
    
    elif command == 'add-recipient':
        # Usage: add-recipient <mode> <email> <name> <role>
        if len(sys.argv) < 6:
            print("Usage: python manage_paycycle.py add-recipient <mode> <email> <name> <role>")
            print('Example: python manage_paycycle.py add-recipient production john.doe@walmart.com "John Doe" "Store Manager"')
            return
        
        mode = sys.argv[2]
        email = sys.argv[3]
        name = sys.argv[4]
        role = sys.argv[5]
        
        manager.add_recipient(mode, email, name, role)
    
    elif command == 'remove-recipient':
        # Usage: remove-recipient <mode> <email>
        if len(sys.argv) < 4:
            print("Usage: python manage_paycycle.py remove-recipient <mode> <email>")
            return
        
        mode = sys.argv[2]
        email = sys.argv[3]
        manager.remove_recipient(mode, email)
    
    elif command == 'switch-mode':
        # Usage: switch-mode <mode>
        if len(sys.argv) < 3:
            print("Usage: python manage_paycycle.py switch-mode <mode>")
            return
        
        new_mode = sys.argv[2]
        manager.toggle_mode(new_mode)
    
    elif command == 'record-send':
        # Usage: record-send <pc_number> [success] [error_msg] [recipients_count]
        if len(sys.argv) < 3:
            print("Usage: python manage_paycycle.py record-send <pc_number> [success|failed] [error_msg] [count]")
            return
        
        pc_number = int(sys.argv[2])
        success = sys.argv[3].lower() != 'failed' if len(sys.argv) > 3 else True
        error_msg = sys.argv[4] if len(sys.argv) > 4 else None
        recipients_count = int(sys.argv[5]) if len(sys.argv) > 5 else 3
        
        manager.record_send(pc_number, success, error_msg, recipients_count)
    
    elif command == 'get-emails':
        # Returns active recipient emails as JSON
        emails = manager.get_active_recipients()
        print(json.dumps(emails))
    
    elif command == 'help':
        show_help()
    
    else:
        print(f"Unknown command: {command}")
        show_help()


def show_help():
    """Show help message"""
    print("""
PayCycle Email Management Utility

USAGE:
    python manage_paycycle.py <command> [args]

COMMANDS:

  schedule
    Display all 26 PayCycle dates and their status
    Usage: python manage_paycycle.py schedule

  recipients
    Show current active recipients configuration
    Usage: python manage_paycycle.py recipients

  add-recipient <mode> <email> <name> <role>
    Add a new recipient to test or production mode
    Usage: python manage_paycycle.py add-recipient production john@walmart.com "John Doe" "Store Manager"

  remove-recipient <mode> <email>
    Remove a recipient from test or production mode
    Usage: python manage_paycycle.py remove-recipient production john@walmart.com

  switch-mode <mode>
    Switch between 'test' and 'production' modes
    Usage: python manage_paycycle.py switch-mode production

  record-send <pc_number> [success|failed]
    Record that a PayCycle send was completed
    Usage: python manage_paycycle.py record-send 3 success

  get-emails
    Get list of active recipient emails (JSON format, useful for scripts)
    Usage: python manage_paycycle.py get-emails

  help
    Show this help message
    Usage: python manage_paycycle.py help

EXAMPLES:

  # View schedule
  python manage_paycycle.py schedule

  # View current recipients
  python manage_paycycle.py recipients

  # Add a DC manager to production
  python manage_paycycle.py add-recipient production dc.manager@walmart.com "DC Manager" "Distribution Manager"

  # Switch to production
  python manage_paycycle.py switch-mode production

  # Record successful send for PC 03
  python manage_paycycle.py record-send 3 success

  # Get emails for external script
  python manage_paycycle.py get-emails

FILES:
  paycycle_tracking.json    - Tracks when emails are sent
  email_recipients.json     - Manages test and production recipients

WORKFLOW:
  1. Start in TEST mode with 3 testers
  2. Add actual DC recipients to PRODUCTION section
  3. Run: python manage_paycycle.py switch-mode production
  4. System sends to production recipients on next PayCycle
""")


if __name__ == '__main__':
    main()
