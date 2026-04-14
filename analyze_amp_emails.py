#!/usr/bin/env python3
"""
AMP AutoFeed Email Analyzer
Shows what data is being extracted from each email
Useful for debugging and understanding the data flow
"""

import json
import sys
from pathlib import Path
from typing import Dict, List
from datetime import datetime

try:
    from amp_autofeed_validation import EmailFetcher, HTMLEmailParser
except ImportError:
    print("ERROR: Could not import validation modules")
    print("Make sure you're running from the correct directory")
    sys.exit(1)


def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def analyze_email(email_data: Dict, email_type: str):
    """Analyze and display email content"""
    
    print(f"\nEmail Type: {email_type}")
    print(f"Received: {email_data.get('received')}")
    print(f"Subject: {email_data.get('subject')}")
    print(f"From: {email_data.get('sender')}")
    
    # Parse HTML
    html_body = email_data.get('html_body') or email_data.get('body')
    
    if not html_body:
        print("ERROR: No HTML body found")
        return None
    
    parser = HTMLEmailParser()
    data = parser.extract_data_from_html(html_body)
    
    print(f"\n📊 Data Extracted:")
    
    # Tables
    tables = data.get('tables', [])
    print(f"\n  Tables: {len(tables)} found")
    
    for i, table in enumerate(tables[:2], 1):  # Show first 2 tables
        print(f"\n    Table {i}: {len(table)} rows")
        if table:
            # Show header
            print(f"      Headers: {table[0]}")
            # Show first data row
            if len(table) > 1:
                print(f"      Sample: {table[1]}")
    
    if len(tables) > 2:
        print(f"    ... and {len(tables)-2} more tables")
    
    # Lists
    lists = data.get('lists', [])
    print(f"\n  Lists: {len(lists)} found")
    
    for i, lst in enumerate(lists[:2], 1):
        print(f"\n    List {i}: {len(lst)} items")
        for item in lst[:3]:
            print(f"      - {item[:60]}")
        if len(lst) > 3:
            print(f"      ... and {len(lst)-3} more items")
    
    # Text blocks
    text = data.get('text_blocks', [])
    print(f"\n  Text Blocks: {len(text)} found")
    
    for i, block in enumerate(text[:2], 1):
        preview = block[:80]
        if len(block) > 80:
            preview += "..."
        print(f"    {i}. {preview}")
    
    # Summary stats (numbers)
    stats = data.get('summary_stats', {})
    if stats:
        print(f"\n  📈 Numeric Data Found:")
        for pattern, values in stats.items():
            unique_values = sorted(set(values))
            print(f"    - {pattern}: {unique_values}")
    
    return data


def compare_emails(qb_data: Dict, amp_data: Dict):
    """Compare data from both emails"""
    
    print_section("Comparison")
    
    # Extract numbers
    qb_nums = set()
    amp_nums = set()
    
    for values in qb_data.get('summary_stats', {}).values():
        qb_nums.update(values)
    
    for values in amp_data.get('summary_stats', {}).values():
        amp_nums.update(values)
    
    print(f"\nQuickBase Numbers: {sorted(qb_nums)}")
    print(f"AMP Numbers:       {sorted(amp_nums)}")
    
    if qb_nums == amp_nums:
        print("✓ Numeric data matches")
    else:
        print("✗ Numeric data DIFFERS")
        if qb_nums - amp_nums:
            print(f"  Only in QB: {qb_nums - amp_nums}")
        if amp_nums - qb_nums:
            print(f"  Only in AMP: {amp_nums - qb_nums}")
    
    # Compare table count
    qb_tables = len(qb_data.get('tables', []))
    amp_tables = len(amp_data.get('tables', []))
    
    print(f"\nQuickBase Tables: {qb_tables}")
    print(f"AMP Tables:       {amp_tables}")
    
    if qb_tables == amp_tables:
        print("✓ Table count matches")
    else:
        print("✗ Table count DIFFERS")
    
    # Compare list count
    qb_lists = len(qb_data.get('lists', []))
    amp_lists = len(amp_data.get('lists', []))
    
    print(f"\nQuickBase Lists: {qb_lists}")
    print(f"AMP Lists:       {amp_lists}")
    
    if qb_lists == amp_lists:
        print("✓ List count matches")
    else:
        print("✗ List count DIFFERS")
    
    # Overall status
    match = (qb_nums == amp_nums) and (qb_tables == amp_tables) and (qb_lists == amp_lists)
    
    print_section("Overall Result")
    if match:
        print("✓ Data appears to MATCH")
    else:
        print("✗ Data appears to DIFFER")
    
    return match


def save_analysis(qb_email: Dict, amp_email: Dict, qb_data: Dict, amp_data: Dict, match: bool):
    """Save analysis results"""
    
    analysis = {
        'timestamp': datetime.now().isoformat(),
        'match': match,
        'quickbase': {
            'subject': qb_email.get('subject'),
            'received': str(qb_email.get('received')),
            'tables_found': len(qb_data.get('tables', [])),
            'lists_found': len(qb_data.get('lists', [])),
            'text_blocks_found': len(qb_data.get('text_blocks', [])),
            'numbers_found': list(set(
                num for values in qb_data.get('summary_stats', {}).values()
                for num in values
            )),
        },
        'amp': {
            'subject': amp_email.get('subject'),
            'received': str(amp_email.get('received')),
            'tables_found': len(amp_data.get('tables', [])),
            'lists_found': len(amp_data.get('lists', [])),
            'text_blocks_found': len(amp_data.get('text_blocks', [])),
            'numbers_found': list(set(
                num for values in amp_data.get('summary_stats', {}).values()
                for num in values
            )),
        }
    }
    
    log_dir = Path("amp_validation_logs")
    log_dir.mkdir(exist_ok=True)
    
    analysis_file = log_dir / f"email_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(analysis_file, 'w') as f:
        json.dump(analysis, f, indent=2, default=str)
    
    print(f"\n✓ Analysis saved to: {analysis_file}")
    
    return analysis_file


def main():
    """Main analysis function"""
    
    print("\n" + "="*70)
    print("  AMP AutoFeed Email Analyzer")
    print("="*70)
    print("This tool analyzes your QuickBase and AMP emails")
    print("to show what data is being compared.\n")
    
    try:
        # Fetch emails
        print("Connecting to Outlook...")
        fetcher = EmailFetcher()
        
        print("Fetching QuickBase API Response email...")
        qb_emails = fetcher.get_email_by_subject("", days_back=1, folder_name="Quick Base API Response Data")
        
        if not qb_emails:
            print("✗ QuickBase email not found")
            print("  Make sure it exists in your Inbox > ATC > Reports > AMP > Quick Base API Response Data folder")
            return 1
        
        qb_email = qb_emails[0]
        
        print("Fetching AMP AutoFeed Details email...")
        amp_emails = fetcher.get_email_by_subject("", days_back=1, folder_name="Auto Feed")
        
        if not amp_emails:
            print("✗ AMP email not found")
            print("  Make sure it exists in your Inbox > ATC > Reports > AMP > Auto Feed folder")
            return 1
        
        amp_email = amp_emails[0]
        
        # Analyze emails
        print_section("QuickBase Email Analysis")
        qb_data = analyze_email(qb_email, "QuickBase API Response")
        
        print_section("AMP Email Analysis")
        amp_data = analyze_email(amp_email, "Processed AutoFeed Details")
        
        # Compare
        match = compare_emails(qb_data, amp_data)
        
        # Save analysis
        save_analysis(qb_email, amp_email, qb_data, amp_data, match)
        
        print("\n" + "="*70)
        
        if match:
            print("✓ Analysis complete - Data appears consistent")
            return 0
        else:
            print("⚠ Analysis complete - Data differences detected")
            print("\nNext steps:")
            print("1. Review the specific differences above")
            print("2. Check if this is expected (e.g., timing differences)")
            print("3. If unexpected, investigate the email generation process")
            return 1
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
