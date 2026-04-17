#!/usr/bin/env python3
"""
Daily Weekly Messages Audio Status Email
==========================================
Sends a daily status email showing BQ data breakdown for the COMING WM week.
Partners can see how many messages are cached, summarized, and when BQ last refreshed.

Usage:
    python send_daily_status_email.py           # Send to partners (TO + CC)
    python send_daily_status_email.py --test    # Send to kendall.rush only
"""
import os
import sys
import logging
import argparse
from datetime import datetime
from pathlib import Path

# Ensure this script can import from the same directory
sys.path.insert(0, str(Path(__file__).parent))

from generate_weekly_audio import (
    get_coming_wm_week_fy,
    fetch_and_cache_bq_data,
    AMP_MSG_URL,
    logger,
)

# ── Recipients ──────────────────────────────────────────────────────────────

TO_RECIPIENTS = [
    'Collin.Claunch@walmart.com',
    'Sara.Elliott@walmart.com',
    'Matthew.Farnworth@walmart.com',
    'JohnC.Davis@walmart.com',
    'LeeAnne.Mills@walmart.com',
]

CC_RECIPIENTS = [
    'Tammy.Claunch@walmart.com',
    'kendall.rush@walmart.com',
]

TEST_RECIPIENT = 'kendall.rush@walmart.com'


# ── HTML Email Builder ──────────────────────────────────────────────────────

def build_status_email_html(week, fy, cache_data):
    """Build an Outlook-safe HTML email with status breakdown table."""
    import html as html_mod

    status_breakdown = cache_data.get('status_breakdown', [])
    total_excl = cache_data.get('total_excl_denied', 0)
    summarized_count = cache_data.get('summarized_count', 0)
    event_count = cache_data.get('event_count', 0)
    bq_last_updated = cache_data.get('bq_last_updated', '')
    events_without = cache_data.get('events_without_summary', [])

    generated_at = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    missing_count = event_count - summarized_count

    # Format BQ timestamp
    bq_ts_display = ''
    if bq_last_updated:
        try:
            from datetime import timezone
            dt = datetime.fromisoformat(bq_last_updated)
            bq_ts_display = dt.strftime("%m/%d/%Y, %I:%M:%S %p")
        except Exception:
            bq_ts_display = str(bq_last_updated)

    # Status breakdown rows
    status_rows = ''
    for s in status_breakdown:
        status = html_mod.escape(s.get('status', ''))
        count = s.get('count', 0)
        is_excluded = 'Denied' in status or 'Expired' in status or status == 'Draft - Pending'
        if is_excluded:
            status_rows += (
                f'<tr>'
                f'<td style="padding:6px 12px;border-bottom:1px solid #E5E7EB;'
                f'color:#9CA3AF;text-decoration:line-through;">{status}</td>'
                f'<td style="padding:6px 12px;border-bottom:1px solid #E5E7EB;'
                f'text-align:right;font-weight:600;color:#9CA3AF;text-decoration:line-through;">{count}</td>'
                f'</tr>'
            )
        else:
            status_rows += (
                f'<tr>'
                f'<td style="padding:6px 12px;border-bottom:1px solid #E5E7EB;">{status}</td>'
                f'<td style="padding:6px 12px;border-bottom:1px solid #E5E7EB;'
                f'text-align:right;font-weight:600;">{count}</td>'
                f'</tr>'
            )

    # Ready or not-ready callout
    if total_excl == summarized_count and total_excl > 0:
        callout_html = (
            '<div style="background:#ECFDF5;border:1px solid #6EE7B7;border-radius:8px;'
            'padding:14px 16px;margin-top:16px;">'
            '<span style="font-size:16px;">&#9989;</span> '
            '<strong style="color:#065F46;">All messages have summaries</strong>'
            '<span style="color:#047857;"> &mdash; ready for audio generation!</span>'
            '</div>'
        )
    else:
        callout_html = (
            '<div style="background:#FFFBEB;border:1px solid #FCD34D;border-radius:8px;'
            'padding:14px 16px;margin-top:16px;">'
            '<span style="font-size:16px;">&#9888;&#65039;</span> '
            f'<strong style="color:#92400E;">{missing_count} message(s) missing summaries.</strong>'
            '<br><span style="color:#78716C;font-size:13px;">'
            'Once Total Count and Summarized match, the Final Audio Email will be sent.</span>'
            '</div>'
        )

    # Events without summary section
    missing_section = ''
    if events_without:
        missing_rows = ''
        for evt in events_without:
            eid = evt.get('event_id', '')
            title = html_mod.escape(evt.get('title', 'Unknown'))
            area = html_mod.escape(evt.get('area', 'Unknown'))
            msg_url = AMP_MSG_URL.format(event_id=eid, week=week, fy=fy)
            missing_rows += (
                f'<tr>'
                f'<td style="padding:6px 10px;border-bottom:1px solid #E5E7EB;font-size:12px;">{area}</td>'
                f'<td style="padding:6px 10px;border-bottom:1px solid #E5E7EB;font-size:12px;">{title}</td>'
                f'<td style="padding:6px 10px;border-bottom:1px solid #E5E7EB;font-size:12px;">'
                f'<a href="{msg_url}" style="color:#2563EB;">View</a></td>'
                f'</tr>'
            )
        missing_section = f"""
        <div style="margin-top:20px;">
            <h3 style="font-size:14px;color:#DC2626;margin-bottom:8px;">
                Messages Without &quot;Summarized:&quot; Text ({len(events_without)})
            </h3>
            <table style="width:100%;border-collapse:collapse;font-size:13px;">
                <thead>
                    <tr style="background:#FEF2F2;">
                        <th style="padding:6px 10px;text-align:left;border-bottom:2px solid #FECACA;">Area</th>
                        <th style="padding:6px 10px;text-align:left;border-bottom:2px solid #FECACA;">Title</th>
                        <th style="padding:6px 10px;text-align:left;border-bottom:2px solid #FECACA;">Link</th>
                    </tr>
                </thead>
                <tbody>{missing_rows}</tbody>
            </table>
        </div>"""

    email_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
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
                        WK{week} &bull; FY{fy} &bull; {generated_at}
                    </p>
                </td>
            </tr>
        </table>

        <div style="padding:24px 32px;">

            <!-- Summary Cards -->
            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:20px;">
                <tr>
                    <td width="33%" style="padding:0 4px 0 0;">
                        <div style="background:#EFF6FF;border-radius:8px;padding:14px;text-align:center;">
                            <div style="font-size:26px;font-weight:700;color:#1D4ED8;">{total_excl}</div>
                            <div style="font-size:11px;color:#6B7280;margin-top:2px;">Total (excl. Draft/Denied/Expired)</div>
                        </div>
                    </td>
                    <td width="33%" style="padding:0 2px;">
                        <div style="background:#ECFDF5;border-radius:8px;padding:14px;text-align:center;">
                            <div style="font-size:26px;font-weight:700;color:#059669;">{summarized_count}</div>
                            <div style="font-size:11px;color:#6B7280;margin-top:2px;">With Summarized Text</div>
                        </div>
                    </td>
                    <td width="33%" style="padding:0 0 0 4px;">
                        <div style="background:{'#ECFDF5' if missing_count == 0 else '#FEF2F2'};border-radius:8px;padding:14px;text-align:center;">
                            <div style="font-size:26px;font-weight:700;color:{'#059669' if missing_count == 0 else '#DC2626'};">{missing_count}</div>
                            <div style="font-size:11px;color:#6B7280;margin-top:2px;">Missing Summary</div>
                        </div>
                    </td>
                </tr>
            </table>

            <!-- Status Breakdown Table -->
            <h3 style="font-size:14px;color:#111827;margin-bottom:6px;">Status Breakdown</h3>
            <p style="font-size:12px;color:#6B7280;margin:0 0 8px;">
                Excludes: AMP PR Merchandise, Draft, Denied, Expired
            </p>
            <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:4px;">
                <thead>
                    <tr style="background:#EFF6FF;">
                        <th style="padding:8px 12px;text-align:left;border-bottom:2px solid #1D4ED8;font-weight:700;">Status</th>
                        <th style="padding:8px 12px;text-align:right;border-bottom:2px solid #1D4ED8;font-weight:700;">Count</th>
                    </tr>
                </thead>
                <tbody>
                    {status_rows}
                    <tr style="background:#F0F9FF;">
                        <td style="padding:8px 12px;font-weight:700;border-top:2px solid #1D4ED8;">Total (excl. Draft/Denied/Expired)</td>
                        <td style="padding:8px 12px;text-align:right;font-weight:700;border-top:2px solid #1D4ED8;">{total_excl}</td>
                    </tr>
                </tbody>
            </table>

            <!-- BQ Timestamp -->
            {'<p style="font-size:12px;color:#6B7280;margin-top:8px;">&#128340; AMP ALL 2 Last Refreshed: <strong>' + bq_ts_display + '</strong></p>' if bq_ts_display else ''}

            <!-- Ready / Not Ready Callout -->
            {callout_html}

            <!-- Missing Summary Detail -->
            {missing_section}

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

    return email_html


# ── Email Sender ────────────────────────────────────────────────────────────

def send_status_email(week, fy, html_body, to_recipients, cc_recipients=None):
    """Send the status email via Outlook COM with retry logic."""
    import pythoncom
    import time

    subject = f"Weekly Messages Audio Status \u2014 WK{week} FY{fy} \u2014 {datetime.now().strftime('%m/%d/%Y')}"

    try:
        pythoncom.CoInitialize()
        import win32com.client

        max_retries = 4
        for attempt in range(max_retries):
            try:
                outlook = win32com.client.Dispatch('Outlook.Application')
                mail = outlook.CreateItem(0)
                mail.To = '; '.join(to_recipients)
                if cc_recipients:
                    mail.CC = '; '.join(cc_recipients)
                mail.Subject = subject
                mail.HTMLBody = html_body
                mail.Send()
                logger.info(f"Email sent — TO: {', '.join(to_recipients)}"
                            f"{' CC: ' + ', '.join(cc_recipients) if cc_recipients else ''}")
                return {'success': True, 'message': f'Email sent to {", ".join(to_recipients)}'}
            except pythoncom.com_error as ce:
                if ce.args[0] == -2147418111 and attempt < max_retries - 1:
                    wait = 2 * (attempt + 1)
                    logger.warning(f"Outlook busy, retrying in {wait}s (attempt {attempt + 1}/{max_retries})...")
                    time.sleep(wait)
                else:
                    raise
    except ImportError:
        return {'success': False, 'error': 'pywin32 not installed. Run: pip install pywin32'}
    except Exception as e:
        logger.error(f"Email send failed: {e}")
        return {'success': False, 'error': str(e)}
    finally:
        try:
            pythoncom.CoUninitialize()
        except Exception:
            pass


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Send daily Weekly Messages Audio status email")
    parser.add_argument("--test", action="store_true", help="Send to kendall.rush only (no CC)")
    parser.add_argument("--week", type=int, default=None, help="Override WM week")
    parser.add_argument("--fy", type=int, default=None, help="Override fiscal year")
    args = parser.parse_args()

    # Determine week/fy
    if args.week and args.fy:
        week, fy = args.week, args.fy
    else:
        week, fy = get_coming_wm_week_fy()
    logger.info(f"Daily status email for coming week: WK{week} FY{fy}")

    # Fetch fresh BQ data
    logger.info("Fetching BQ data...")
    cache_data = fetch_and_cache_bq_data(week, fy)

    # If no events exist yet for the coming week, build an empty dataset
    # (this is normal early in the prep cycle)
    if 'error' in cache_data and 'No Weekly Messages' in cache_data.get('error', ''):
        logger.info(f"No events for WK{week} FY{fy} yet — sending status email with zero counts")
        cache_data = {
            'event_count': 0,
            'total_excl_denied': 0,
            'summarized_count': 0,
            'status_breakdown': [],
            'events_without_summary': [],
            'bq_last_updated': '',
        }
    elif 'error' in cache_data:
        logger.error(f"BQ fetch failed: {cache_data['error']}")
        sys.exit(1)

    # Build email
    html_body = build_status_email_html(week, fy, cache_data)

    # Determine recipients
    if args.test:
        to = [TEST_RECIPIENT]
        cc = None
        logger.info(f"TEST MODE — sending to {TEST_RECIPIENT} only")
    else:
        to = list(TO_RECIPIENTS)
        cc = list(CC_RECIPIENTS)

        # On Fridays, add the on-call person to CC
        if datetime.now().weekday() == 4:  # 4 = Friday
            try:
                from oncall_parser import get_oncall_from_calendar
                oncall = get_oncall_from_calendar()
                if oncall:
                    oncall_email = oncall['email']
                    all_existing = [e.lower() for e in to + cc]
                    if oncall_email.lower() not in all_existing:
                        cc.append(oncall_email)
                        logger.info(f"Friday — added on-call {oncall['name']} ({oncall_email}) to CC")
                    else:
                        logger.info(f"Friday — on-call {oncall['name']} already in recipients")
                else:
                    logger.info("Friday — no on-call calendar entry found")
            except Exception as e:
                logger.warning(f"On-call lookup failed: {e}")

    # Send
    result = send_status_email(week, fy, html_body, to, cc)
    if result.get('success'):
        logger.info(f"Done: {result['message']}")
    else:
        logger.error(f"Failed: {result.get('error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
