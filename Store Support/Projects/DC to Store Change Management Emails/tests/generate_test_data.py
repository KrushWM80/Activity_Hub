#!/usr/bin/env python3
"""
Test Data Generator for Dashboard
Simulates email sends for testing the dashboard without running the full email system.

Usage:
    python tests/generate_test_data.py                  # Generate sample data
    python tests/generate_test_data.py --clear          # Clear database first
    python tests/generate_test_data.py --daily-report   # Generate realistic daily data
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import random

# Add parent directory to path so we can import email_history_logger
sys.path.insert(0, str(Path(__file__).parent.parent))

from email_history_logger import EmailHistoryLogger


def generate_sample_data():
    """Generate realistic sample email data"""
    logger = EmailHistoryLogger()
    
    print("\n" + "="*80)
    print("GENERATING TEST DATA FOR DASHBOARD")
    print("="*80 + "\n")
    
    # DC information
    dcs = [
        (6020, 'Ambient'),
        (6040, 'Perishable'),
        (6080, 'Ambient'),
        (6090, 'Perishable'),
        (6120, 'Ambient'),
    ]
    
    # Generate data for last 30 days
    for day_offset in range(30, 0, -1):
        date = (datetime.now() - timedelta(days=day_offset)).strftime("%Y-%m-%d")
        
        # 70% chance of emails on any given day
        if random.random() < 0.7:
            # 1-3 DCs might have changes on a given day
            dcs_with_changes = random.sample(dcs, k=random.randint(1, 3))
            
            for dc_number, dc_type in dcs_with_changes:
                # Random change counts
                store_manager = random.randint(0, 8)
                market_manager = random.randint(0, 4)
                region_manager = random.randint(0, 2)
                stores_affected = store_manager + random.randint(2, 8)
                
                # Only log if there are changes
                if store_manager + market_manager + region_manager > 0:
                    recipients = [
                        f"{dc_number}GM@email.wal-mart.com",
                        f"{dc_number}AGM@email.wal-mart.com"
                    ]
                    
                    subject = f"Manager Changes in Your DC Territory - {date}"
                    
                    changes = {
                        'store_manager': store_manager,
                        'market_manager': market_manager,
                        'region_manager': region_manager,
                        'stores_affected': stores_affected
                    }
                    
                    email_id = logger.log_email_send(
                        dc_number=dc_number,
                        dc_type=dc_type,
                        recipients=recipients,
                        subject=subject,
                        changes=changes,
                        test_mode=True,
                        status='sent'
                    )
                    
                    print(f"✓ {date} - DC {dc_number} ({dc_type}): {store_manager+market_manager+region_manager} changes - Record ID: {email_id}")
    
    print("\n" + "="*80)
    print("✅ TEST DATA GENERATED SUCCESSFULLY!")
    print("="*80)
    print("\nNow run: python dashboard.py")
    print("Then visit: http://localhost:5000\n")


def clear_database():
    """Clear the database (careful!)"""
    import os
    db_path = Path(__file__).parent.parent / "email_history.db"
    
    if db_path.exists():
        print(f"\nClearing database: {db_path}")
        os.remove(db_path)
        print("✓ Database cleared\n")
    else:
        print(f"\nDatabase not found: {db_path}\n")


def generate_realistic_daily():
    """Generate realistic daily data (like actual emails would)"""
    logger = EmailHistoryLogger()
    today = datetime.now().strftime("%Y-%m-%d")
    
    print("\n" + "="*80)
    print(f"GENERATING TODAY'S EMAIL DATA ({today})")
    print("="*80 + "\n")
    
    dcs = [
        (6020, 'Ambient'),
        (6040, 'Perishable'),
        (6080, 'Ambient'),
    ]
    
    for dc_number, dc_type in dcs:
        store_manager = random.randint(1, 5)
        market_manager = random.randint(0, 2)
        stores_affected = random.randint(4, 12)
        
        recipients = [
            f"{dc_number}GM@email.wal-mart.com",
            f"{dc_number}AGM@email.wal-mart.com"
        ]
        
        changes = {
            'store_manager': store_manager,
            'market_manager': market_manager,
            'region_manager': 0,
            'stores_affected': stores_affected
        }
        
        email_id = logger.log_email_send(
            dc_number=dc_number,
            dc_type=dc_type,
            recipients=recipients,
            subject=f"Manager Changes - {today}",
            changes=changes,
            test_mode=True,
            status='sent'
        )
        
        print(f"✓ DC {dc_number} ({dc_type}): {store_manager + market_manager} changes to {stores_affected} stores - Record ID: {email_id}")
    
    print("\n" + "="*80)
    print("✅ TODAY'S DATA GENERATED!")
    print("="*80)
    print("\nRefresh dashboard to see updates: http://localhost:5000\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--clear":
            clear_database()
        elif sys.argv[1] == "--daily-report":
            generate_realistic_daily()
    else:
        generate_sample_data()
