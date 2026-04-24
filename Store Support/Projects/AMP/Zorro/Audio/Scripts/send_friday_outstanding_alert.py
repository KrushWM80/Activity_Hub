#!/usr/bin/env python3
"""
Friday 10:30 AM Outstanding Items Alert
=========================================
Sends a mid-morning email on Fridays if any Weekly Messages are still missing
a Summarized text.  Uses the SAME format as the Daily Status Email, with an
"Outstanding Items" section injected before the footer showing AMP links and
action instructions.

Usage:
    python send_friday_outstanding_alert.py           # Production (all recipients, only sends if outstanding > 0)
    python send_friday_outstanding_alert.py --test     # Test mode (kendall.rush only, sends even if 0 outstanding)

Scheduled: Fridays at 10:30 AM  (Activity_Hub_Friday_Outstanding_Alert)
"""
import os
import sys
import logging
import argparse
from datetime import datetime
from pathlib import Path

# ── Logging ─────────────────────────────────────────────────────────────────
LOG_FILE = Path(__file__).parent / 'daily_status_email.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler(LOG_FILE, encoding='utf-8')]
)
logger = logging.getLogger('weekly_audio')

# ── ADC ─────────────────────────────────────────────────────────────────────
ADC_PATH = Path(os.environ.get(
    'GOOGLE_APPLICATION_CREDENTIALS',
    os.path.expanduser('~') + r'\AppData\Roaming\gcloud\application_default_credentials.json'
))
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(ADC_PATH)
logger.info(f"ADC credentials: {ADC_PATH} (exists: {ADC_PATH.exists()})")

# ── Imports from sibling modules ────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent))
from generate_weekly_audio import get_coming_wm_week_fy, fetch_and_cache_bq_data, AMP_MSG_URL
from send_daily_status_email import (
    build_status_email_html,
    send_status_email,
    TO_RECIPIENTS,
    CC_RECIPIENTS,
    TEST_RECIPIENT,
)


# ── Outstanding Items Section ───────────────────────────────────────────────

def _build_outstanding_section(events_without, week, fy):
    """Return HTML block for the Outstanding Items table + action instructions."""
    import html as html_mod

    if not events_without:
        return ''

    count = len(events_without)

    # Build event rows
    event_rows = ''
    for evt in events_without:
        eid = evt.get('event_id', '')
        title = html_mod.escape(evt.get('title', 'Unknown'))
        area = html_mod.escape(evt.get('area', 'Unknown'))
        msg_url = AMP_MSG_URL.format(event_id=eid, week=week, fy=fy)
        event_rows += (
            f'<tr>'
            f'<td style="padding:8px 12px;border-bottom:1px solid #E5E7EB;font-size:13px;">{area}</td>'
            f'<td style="padding:8px 12px;border-bottom:1px solid #E5E7EB;font-size:13px;">{title}</td>'
            f'<td style="padding:8px 12px;border-bottom:1px solid #E5E7EB;font-size:13px;">'
            f'<a href="{msg_url}" style="color:#2563EB;text-decoration:none;">Open in AMP</a></td>'
            f'</tr>'
        )

    return f"""
        <div style="margin-top:24px;padding-top:20px;border-top:2px solid #FDE68A;">
            <h3 style="font-size:15px;color:#DC2626;margin:0 0 8px;">
                &#9888;&#65039; Outstanding Items ({count})
            </h3>
            <p style="font-size:13px;color:#6B7280;margin:0 0 12px;">
                These events do not have a &ldquo;Summarized:&rdquo; section in their AMP message body.
                The audio cannot be generated until all messages have summaries.
            </p>
            <table style="width:100%;border-collapse:collapse;">
                <thead>
                    <tr style="background:#FEF3C7;">
                        <th style="padding:8px 12px;text-align:left;border-bottom:2px solid #FDE68A;font-size:13px;font-weight:700;">Area</th>
                        <th style="padding:8px 12px;text-align:left;border-bottom:2px solid #FDE68A;font-size:13px;font-weight:700;">Event Title</th>
                        <th style="padding:8px 12px;text-align:left;border-bottom:2px solid #FDE68A;font-size:13px;font-weight:700;">AMP Link</th>
                    </tr>
                </thead>
                <tbody>{event_rows}</tbody>
            </table>

            <!-- Action Instructions -->
            <div style="margin-top:16px;padding:14px 16px;background:#FEF3C7;border-radius:8px;border:1px solid #FDE68A;">
                <p style="font-size:13px;color:#92400E;margin:0 0 6px;font-weight:700;">Action Required:</p>
                <ul style="font-size:13px;color:#78716C;margin:0;padding-left:20px;">
                    <li style="margin-bottom:4px;">If there are any AMP Activities listed above, please update the Message Body with a &ldquo;Summarized:&rdquo; section.</li>
                    <li style="margin-bottom:4px;">If these messages need to be moved out to another week or denied, please update accordingly.</li>
                    <li>If there is an update in the Message Body, the data will update automatically with the next cycle.</li>
                </ul>
            </div>
        </div>"""


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Friday Outstanding Items Alert')
    parser.add_argument('--test', action='store_true', help='Send to kendall.rush only')
    parser.add_argument('--use-cache', action='store_true', help='Use cached BQ data instead of live fetch')
    args = parser.parse_args()

    # Get coming week
    week, fy = get_coming_wm_week_fy()
    logger.info(f"Outstanding items check for WK{week} FY{fy}")

    # Fetch BQ data (live or from cache)
    import json
    cache_file = Path(__file__).parent / 'cache' / f'week_{week}_fy{fy}.json'

    if args.use_cache:
        if not cache_file.exists():
            logger.error(f"No cache file found: {cache_file}")
            sys.exit(1)
        logger.info(f"Using cached data: {cache_file}")
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
    else:
        logger.info("Fetching BQ data...")
        try:
            cache_data = fetch_and_cache_bq_data(week, fy)
        except Exception as e:
            logger.error(f"BQ fetch failed: {e}")
            if cache_file.exists():
                logger.info(f"Falling back to cached data: {cache_file}")
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
            else:
                sys.exit(1)

    events_without = cache_data.get('events_without_summary', [])
    outstanding = len(events_without)
    total = cache_data.get('total_excl_denied', 0)
    summarized = cache_data.get('summarized_count', 0)

    logger.info(f"Total: {total}, Summarized: {summarized}, Outstanding: {outstanding}")

    # In production mode, only send if there are outstanding items
    if not args.test and outstanding == 0:
        logger.info("No outstanding items — skipping email (all summarized)")
        return

    # ── Build the Daily Email HTML, then inject Outstanding section ──────
    html_body = build_status_email_html(week, fy, cache_data)

    outstanding_section = _build_outstanding_section(events_without, week, fy)
    if outstanding_section:
        footer_marker = '<!-- Footer -->'
        if footer_marker in html_body:
            html_body = html_body.replace(footer_marker, outstanding_section + '\n\n        ' + footer_marker, 1)

    # ── Subject line ────────────────────────────────────────────────────
    tag = f"\u26a0\ufe0f {outstanding} Outstanding" if outstanding > 0 else "\u2705 All Summarized"
    subject = (
        f"{'[TEST] ' if args.test else ''}"
        f"Weekly Messages Audio Status \u2014 {tag} \u2014 WK{week} FY{fy}"
    )

    # ── Recipients ──────────────────────────────────────────────────────
    if args.test:
        to = [TEST_RECIPIENT]
        cc = None
        logger.info(f"TEST MODE — sending to {TEST_RECIPIENT}")
    else:
        to = list(TO_RECIPIENTS)
        cc = list(CC_RECIPIENTS)

        # Add on-call person to CC
        try:
            from oncall_parser import get_oncall_from_calendar
            oncall = get_oncall_from_calendar()
            if oncall:
                oncall_email = oncall['email']
                all_existing = [e.lower() for e in to + cc]
                if oncall_email.lower() not in all_existing:
                    cc.append(oncall_email)
                    logger.info(f"Added on-call {oncall['name']} ({oncall_email}) to CC")
                else:
                    logger.info(f"On-call {oncall['name']} already in recipients")
            else:
                logger.info("No on-call calendar entry found")
        except Exception as e:
            logger.warning(f"On-call lookup failed: {e}")

    # ── Send via Outlook (reuses send_status_email but override subject) ─
    import pythoncom
    import time

    try:
        pythoncom.CoInitialize()
        import win32com.client

        max_retries = 4
        for attempt in range(max_retries):
            try:
                outlook = win32com.client.Dispatch('Outlook.Application')
                mail = outlook.CreateItem(0)
                mail.To = '; '.join(to)
                if cc:
                    mail.CC = '; '.join(cc)
                mail.Subject = subject
                mail.HTMLBody = html_body
                mail.Send()
                logger.info(f"Email sent — TO: {', '.join(to)}"
                            f"{' CC: ' + ', '.join(cc) if cc else ''}")
                logger.info("Outstanding items alert sent successfully")
                return
            except pythoncom.com_error as ce:
                if ce.args[0] == -2147418111 and attempt < max_retries - 1:
                    wait = 2 * (attempt + 1)
                    logger.warning(f"Outlook busy, retrying in {wait}s...")
                    time.sleep(wait)
                else:
                    raise
    except Exception as e:
        logger.error(f"Email send failed: {e}")
        sys.exit(1)
    finally:
        try:
            pythoncom.CoUninitialize()
        except Exception:
            pass


if __name__ == '__main__':
    main()
