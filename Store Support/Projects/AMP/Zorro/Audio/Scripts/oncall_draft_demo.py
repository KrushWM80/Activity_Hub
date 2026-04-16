#!/usr/bin/env python3
"""
On-Call Planner Parser + Draft Email Demo
==========================================
Demonstrates:
1. Parsing the U.S. Comm On Call calendar entry from Outlook
2. Extracting the on-call person's name and email
3. Creating a draft email (not sent) with them as a TO recipient

Usage:
    python oncall_draft_demo.py          # Create draft with real on-call person
    python oncall_draft_demo.py --test   # Dry run, print results only
"""
import pythoncom
import win32com.client
import re
import argparse
from datetime import datetime, timedelta


def get_oncall_from_calendar(target_date=None):
    """Find the on-call person from calendar for the given date (default: coming Friday).

    Searches for calendar items matching '{Name} On Call' that span the target date.

    Returns:
        dict with 'name', 'email', 'phone', 'start', 'end' or None if not found.
    """
    pythoncom.CoInitialize()
    try:
        outlook = win32com.client.Dispatch('Outlook.Application')
        ns = outlook.GetNamespace('MAPI')
        cal = ns.GetDefaultFolder(9)  # olFolderCalendar

        # Default: find the coming Friday (or today if already Friday)
        if target_date is None:
            today = datetime.now()
            days_until_friday = (4 - today.weekday()) % 7
            if days_until_friday == 0 and today.hour >= 18:
                days_until_friday = 7  # Next Friday if past 6pm on Friday
            target_date = today + timedelta(days=days_until_friday)

        # Search window: 7 days before to 7 days after target
        search_start = (target_date - timedelta(days=7)).strftime('%m/%d/%Y')
        search_end = (target_date + timedelta(days=7)).strftime('%m/%d/%Y')

        items = cal.Items
        items.IncludeRecurrences = True
        items.Sort("[Start]")
        restriction = f"[Start] >= '{search_start}' AND [Start] <= '{search_end}'"
        restricted = items.Restrict(restriction)

        on_call_pattern = re.compile(r'^(.+?)\s+On\s+Call$', re.IGNORECASE)

        for item in restricted:
            try:
                subject = item.Subject or ''
                match = on_call_pattern.match(subject)
                if not match:
                    continue

                # Check if this appointment spans our target date
                item_start = item.Start.replace(tzinfo=None) if hasattr(item.Start, 'replace') else item.Start
                item_end = item.End.replace(tzinfo=None) if hasattr(item.End, 'replace') else item.End
                target_naive = target_date.replace(hour=12, minute=0, second=0, microsecond=0)

                if hasattr(item_start, 'date'):
                    start_date = item_start.date() if hasattr(item_start, 'date') else item_start
                    end_date = item_end.date() if hasattr(item_end, 'date') else item_end
                else:
                    start_date = item_start
                    end_date = item_end

                full_name = match.group(1).strip()
                # Convert "First Last" → "First.Last@walmart.com"
                parts = full_name.split()
                if len(parts) >= 2:
                    email = f"{parts[0]}.{parts[-1]}@walmart.com"
                else:
                    email = f"{full_name.replace(' ', '.')}@walmart.com"

                phone = getattr(item, 'Location', '') or ''

                return {
                    'name': full_name,
                    'email': email,
                    'phone': phone,
                    'start': str(item.Start),
                    'end': str(item.End),
                }
            except Exception:
                continue

        return None
    finally:
        pythoncom.CoUninitialize()


def create_draft_email(oncall_info, week, fy):
    """Create a draft email in Outlook with the on-call person as a TO recipient."""
    pythoncom.CoInitialize()
    try:
        outlook = win32com.client.Dispatch('Outlook.Application')
        mail = outlook.CreateItem(0)

        # Regular TO recipients
        to_list = [
            'Collin.Claunch@walmart.com',
            'Sara.Elliott@walmart.com',
            'Matthew.Farnworth@walmart.com',
            'JohnC.Davis@walmart.com',
            'LeeAnne.Mills@walmart.com',
        ]

        # Add on-call person to CC
        if oncall_info:
            oncall_email = oncall_info['email']
            if oncall_email.lower() not in [e.lower() for e in cc_list]:
                cc_list.append(oncall_email)

        mail.To = '; '.join(to_list)
        mail.CC = '; '.join(cc_list)

        today_str = datetime.now().strftime('%m/%d/%Y')
        mail.Subject = f"Weekly Messages Audio Status \u2014 WK{week} FY{fy} \u2014 {today_str}"

        oncall_banner = ''
        if oncall_info:
            oncall_banner = f"""
            <div style="background:#DBEAFE;border:1px solid #93C5FD;border-radius:8px;
                        padding:12px 16px;margin-bottom:16px;">
                <span style="font-size:15px;">&#128222;</span>
                <strong style="color:#1E40AF;">On Call This Week:</strong>
                <span style="color:#1E3A8A;">{oncall_info['name']}</span>
                {f' &mdash; <span style="color:#6B7280;">{oncall_info["phone"]}</span>' if oncall_info.get('phone') else ''}
            </div>"""

        mail.HTMLBody = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#F3F4F6;">
    <div style="max-width:660px;margin:20px auto;background:white;border-radius:12px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.1);">

        <!-- Header -->
        <table width="100%" cellpadding="0" cellspacing="0" border="0">
            <tr>
                <td align="center" style="padding:24px 32px;border-bottom:4px solid #1D4ED8;background-color:#EFF6FF;">
                    <h1 style="font-size:20px;font-weight:700;margin:0;color:#1E3A8A;">
                        Weekly Messages Audio Status
                    </h1>
                    <p style="font-size:14px;margin:6px 0 0;color:#4B5563;">
                        WK{week} &bull; FY{fy} &bull; {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
                    </p>
                </td>
            </tr>
        </table>

        <div style="padding:24px 32px;">

            {oncall_banner}

            <!-- Placeholder content -->
            <div style="background:#F9FAFB;border:1px solid #E5E7EB;border-radius:8px;padding:20px;text-align:center;color:#6B7280;">
                <p style="margin:0;font-size:14px;">
                    &#128204; <strong>DRAFT PREVIEW</strong><br><br>
                    This is a draft to demonstrate the on-call integration.<br>
                    The actual email will include the full status breakdown table,<br>
                    summary cards, and missing summary details.
                </p>
            </div>

        </div>

        <!-- Footer -->
        <div style="background:#F9FAFB;padding:14px 32px;text-align:center;border-top:1px solid #E5E7EB;">
            <p style="font-size:11px;color:#9CA3AF;margin:0;">
                Automated Daily Status &bull; Zorro Activity Hub &bull; Audio Message Hub
            </p>
        </div>
    </div>
</body>
</html>"""

        mail.Save()  # Save as draft (not send)
        return {
            'success': True,
            'to': mail.To,
            'cc': mail.CC,
            'subject': mail.Subject,
            'oncall': oncall_info,
        }
    finally:
        pythoncom.CoUninitialize()


def main():
    parser = argparse.ArgumentParser(description="On-Call Planner Parser Demo")
    parser.add_argument("--test", action="store_true", help="Dry run — don't create draft")
    args = parser.parse_args()

    print("=" * 60)
    print("On-Call Planner Parser")
    print("=" * 60)

    # Step 1: Parse on-call from calendar
    print("\nStep 1: Searching calendar for on-call appointment...")
    oncall = get_oncall_from_calendar()

    if oncall:
        print(f"  Found: {oncall['name']}")
        print(f"  Email: {oncall['email']}")
        print(f"  Phone: {oncall.get('phone', 'N/A')}")
        print(f"  Period: {oncall['start']} to {oncall['end']}")
    else:
        print("  No on-call appointment found for the coming Friday.")
        print("  The email will be sent without an on-call recipient.")

    # Step 2: Create draft
    week, fy = 12, 2027  # Placeholder — would use get_coming_wm_week_fy() in production

    if args.test:
        print(f"\nStep 2: [DRY RUN] Would create draft for WK{week} FY{fy}")
        if oncall:
            print(f"  On-call '{oncall['name']}' ({oncall['email']}) would be added to TO")
        return

    print(f"\nStep 2: Creating draft email for WK{week} FY{fy}...")
    result = create_draft_email(oncall, week, fy)

    if result['success']:
        print(f"\n  Draft saved to Outlook Drafts folder!")
        print(f"  Subject: {result['subject']}")
        print(f"  TO: {result['to']}")
        print(f"  CC: {result['cc']}")
        if result['oncall']:
            print(f"  On-Call: {result['oncall']['name']} ({result['oncall']['email']})")
    else:
        print(f"  Failed: {result.get('error')}")


if __name__ == "__main__":
    main()
