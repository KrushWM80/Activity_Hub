"""
V.E.T. Executive Report - Test Email Script
Generates the report and sends a test email example
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from generate_ppt import TDAPowerPointGenerator
from email_service import VETEmailService
from sample_data import SAMPLE_DATA_49_PROJECTS


def get_current_walmart_week():
    """
    Determine current Walmart Week
    Walmart weeks run Saturday-Friday, typically WK01-WK53
    
    Returns:
        String in format "WK##" (e.g., "WK12")
    """
    # For now, calculate based on date. Walmart WK01 starts Saturday of first full week in February
    # This is a simplified calculation
    today = datetime.now().date()
    
    # Walmart fiscal year starts in February
    # WK01 is the first week starting on a Saturday after Feb 1
    if today.month >= 2:
        year_start = datetime(today.year, 2, 1).date()
    else:
        year_start = datetime(today.year - 1, 2, 1).date()
    
    # Find first Saturday
    days_until_saturday = (5 - year_start.weekday()) % 7  # 5 = Saturday
    first_saturday = year_start + timedelta(days=days_until_saturday)
    
    # Calculate week number
    days_diff = (today - first_saturday).days
    if days_diff < 0:
        # Before first week
        weeks = 0
    else:
        weeks = (days_diff // 7) + 1
    
    wk_num = max(1, weeks)
    return f"WK{wk_num:02d}"


def generate_report_and_send_email(recipient_email: str, test_mode: bool = False):
    """
    Generate V.E.T. Executive Report and send email
    
    Args:
        recipient_email: Email address to send to
        test_mode: If False, actually sends the email (not just draft)
    """
    
    print("=" * 80)
    print("V.E.T. EXECUTIVE REPORT - EMAIL GENERATOR")
    print("=" * 80)
    print()
    
    try:
        # Step 1: Initialize generator
        print("[1/4] Initializing PowerPoint Generator...")
        generator = TDAPowerPointGenerator()
        print("     ✓ Generator initialized")
        print()
        
        # Step 2: Fetch data (using sample data since BigQuery may not be available)
        print("[2/4] Loading sample project data...")
        generator.data = SAMPLE_DATA_49_PROJECTS
        print(f"     ✓ Loaded {len(generator.data)} sample projects")
        print()
        
        # Calculate statistics
        total_projects = len(generator.data)
        total_stores = sum([int(row.get('# of Stores', 0) or 0) for row in generator.data])
        on_track = sum(1 for row in generator.data if 'on track' in str(row.get('Health Status', '')).lower())
        at_risk = sum(1 for row in generator.data if 'at risk' in str(row.get('Health Status', '')).lower())
        off_track = total_projects - on_track - at_risk
        
        # Get current WM Week (today's week)
        current_wm_week = get_current_walmart_week()
        
        report_data = {
            'total_projects': total_projects,
            'total_stores': total_stores,
            'on_track': on_track,
            'at_risk': at_risk,
            'off_track': off_track,
            'wm_week': current_wm_week
        }
        
        print("     Report Statistics:")
        print(f"       • Total Initiatives: {report_data['total_projects']}")
        print(f"       • Stores Impacted: {report_data['total_stores']:,}")
        print(f"       • On Track: {report_data['on_track']}")
        print(f"       • At Risk: {report_data['at_risk']}")
        print(f"       • Off Track: {report_data['off_track']}")
        print(f"       • Current WM Week: {current_wm_week} (Today: {datetime.now().strftime('%B %d, %Y')})")
        print()
        
        # Step 3: Generate PowerPoint report
        print("[3/4] Generating PowerPoint report...")
        reports_dir = Path(__file__).parent / 'reports'
        reports_dir.mkdir(exist_ok=True)
        
        # Use timestamped filename for storage, but attach as VET_Executive_Report.pptx
        output_file = reports_dir / f"VET_Executive_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx"
        ppt_path = generator.generate_report(str(output_file))
        print(f"     ✓ PowerPoint generated: {Path(ppt_path).name}")
        print(f"     ✓ Location: {ppt_path}")
        print()
        
        # Step 4: Prepare and send email
        print("[4/4] Preparing and sending email...")
        email_service = VETEmailService()
        
        mode_text = "DRAFT MODE (saved to Outlook Drafts)" if test_mode else "SENDING NOW"
        print(f"     Email Configuration:")
        print(f"       • Mode: {mode_text}")
        print(f"       • Recipient: {recipient_email}")
        print(f"       • Subject: V.E.T. Executive Report")
        print(f"       • Attachment: VET_Executive_Report.pptx")
        print()
        
        # Send email
        success = email_service.send_report_email(
            to_recipients=[recipient_email],
            report_data=report_data,
            ppt_file_path=ppt_path,
            test_mode=test_mode
        )
        
        print()
        print("=" * 80)
        if success:
            if test_mode:
                print("✅ EMAIL PREPARED SUCCESSFULLY (DRAFT MODE)")
                print()
                print("   The email has been saved as a DRAFT in Outlook.")
                print("   You can review it and manually send it.")
            else:
                print("✅ EMAIL SENT SUCCESSFULLY")
                print()
                print(f"   Recipient: {recipient_email}")
                print(f"   Subject: V.E.T. Executive Report")
                print(f"   Timestamp: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
        else:
            print("❌ FAILED TO PREPARE/SEND EMAIL")
            print()
            print("   Check the error messages above for details.")
        
        print("=" * 80)
        
        return success
    
    except Exception as e:
        print()
        print("=" * 80)
        print(f"❌ ERROR: {e}")
        print("=" * 80)
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate V.E.T. Executive Report and send email')
    parser.add_argument('--email', default='kendall.rush@walmart.com', help='Recipient email address (default: kendall.rush@walmart.com)')
    parser.add_argument('--draft', action='store_true', help='Save as draft instead of sending')
    
    args = parser.parse_args()
    
    generate_report_and_send_email(args.email, test_mode=args.draft)
