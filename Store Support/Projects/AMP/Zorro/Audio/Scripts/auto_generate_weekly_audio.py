#!/usr/bin/env python3
"""
Auto-Generate Weekly Audio
============================
Monitors BQ for the coming week's messages. When Total (excl. Denied/Expired)
equals the Summarized count, automatically generates the audio MP4 and sends
the Final Weekly Message Audio email.

Scheduled: Fridays, hourly after 6 AM daily email, until processed.

Flow:
  1. Check BQ: Total == Summarized?  → If no, exit silently.
  2. Check lock file: already processed this week?  → If yes, exit.
  3. Switch WiFi: Eagle → Walmartwifi (off VPN for edge-tts)
  4. Synthesize audio from cache → MP4 with Jenny Neural
  5. Switch WiFi: Walmartwifi → Eagle (disconnect, auto-reconnects)
  6. Send Final Audio Report email (TO + CC + on-call)

Usage:
    python auto_generate_weekly_audio.py           # Production run
    python auto_generate_weekly_audio.py --test    # Dry run, no WiFi switch or email
    python auto_generate_weekly_audio.py --force   # Ignore lock, re-process
"""
import os
import sys
import json
import time
import logging
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

# Ensure imports work from this directory
sys.path.insert(0, str(Path(__file__).parent))

from generate_weekly_audio import (
    get_coming_wm_week_fy,
    fetch_and_cache_bq_data,
    synthesize_from_cache,
    send_audio_report_email,
    logger,
)
from oncall_parser import get_oncall_from_calendar

# ── Configuration ───────────────────────────────────────────────────────────

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

LOCK_DIR = Path(__file__).parent / 'cache'
EAGLE_IP_PREFIX = '10.97.'
WALMARTWIFI_NAME = 'Walmartwifi'


# ── WiFi Switching ──────────────────────────────────────────────────────────

def _get_current_ip():
    """Get the current WiFi IPv4 address."""
    try:
        result = subprocess.run(
            ['powershell', '-Command',
             "Get-NetIPConfiguration | Where-Object { $_.InterfaceAlias -eq 'Wi-Fi' } "
             "| Select-Object -ExpandProperty IPv4Address | Select-Object -ExpandProperty IPAddress"],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip()
    except Exception as e:
        logger.warning(f"Could not get IP: {e}")
        return ''


def _switch_to_walmartwifi():
    """Switch WiFi to Walmartwifi (off VPN, enables edge-tts).
    No elevation needed — netsh wlan connect works for saved profiles.
    """
    logger.info("Switching WiFi: Eagle → Walmartwifi...")
    try:
        result = subprocess.run(
            ['netsh', 'wlan', 'connect', f'name={WALMARTWIFI_NAME}'],
            capture_output=True, text=True, timeout=15
        )
        logger.info(f"netsh connect result: {result.stdout.strip()}")
        # Wait for connection to establish
        for attempt in range(10):
            time.sleep(3)
            ip = _get_current_ip()
            if ip and not ip.startswith(EAGLE_IP_PREFIX):
                logger.info(f"Connected to Walmartwifi (IP: {ip})")
                return True
            logger.info(f"Waiting for Walmartwifi connection (attempt {attempt + 1}/10)...")
        logger.error("Failed to connect to Walmartwifi after 30s")
        return False
    except Exception as e:
        logger.error(f"WiFi switch failed: {e}")
        return False


def _switch_to_eagle():
    """Switch WiFi back to Eagle by disconnecting (auto-reconnects via group policy).
    No elevation needed.
    """
    logger.info("Switching WiFi: Walmartwifi → Eagle (disconnect + auto-reconnect)...")
    try:
        result = subprocess.run(
            ['netsh', 'wlan', 'disconnect'],
            capture_output=True, text=True, timeout=15
        )
        # Wait for Eagle to auto-reconnect
        for attempt in range(15):
            time.sleep(3)
            ip = _get_current_ip()
            if ip and ip.startswith(EAGLE_IP_PREFIX):
                logger.info(f"Reconnected to Eagle (IP: {ip})")
                return True
            logger.info(f"Waiting for Eagle auto-reconnect (attempt {attempt + 1}/15)...")
        logger.warning("Eagle did not auto-reconnect within 45s — may need manual reconnect")
        return False
    except Exception as e:
        logger.error(f"WiFi switch-back failed: {e}")
        return False


# ── Lock File ───────────────────────────────────────────────────────────────

def _lock_file(week, fy):
    return LOCK_DIR / f'auto_generated_week_{week}_fy{fy}.lock'


def _is_already_processed(week, fy):
    return _lock_file(week, fy).exists()


def _mark_processed(week, fy):
    LOCK_DIR.mkdir(parents=True, exist_ok=True)
    _lock_file(week, fy).write_text(json.dumps({
        'processed_at': datetime.now().isoformat(),
        'week': week,
        'fy': fy,
    }))


# ── End-of-Day Alert ────────────────────────────────────────────────────────

def _send_eod_alert(week, fy):
    """Send an alert email when audio was not generated by end of day Friday."""
    import pythoncom
    import win32com.client as win32

    today_str = datetime.now().strftime('%m/%d/%Y')
    subject = f"⚠ Weekly Audio NOT Generated — WK{week} FY{fy} — {today_str}"

    # Fetch latest BQ counts for context
    total, summarized = '?', '?'
    try:
        cache_data = fetch_and_cache_bq_data(week, fy)
        if 'error' not in cache_data:
            total = cache_data.get('total_excl_denied', '?')
            summarized = cache_data.get('summarized_count', '?')
    except Exception:
        pass

    html_body = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#F3F4F6;">
<div style="max-width:560px;margin:20px auto;background:white;border-radius:12px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.1);">
    <div style="padding:24px 32px;border-bottom:4px solid #DC2626;background:#FEF2F2;text-align:center;">
        <h1 style="font-size:18px;color:#991B1B;margin:0;">Weekly Audio Not Generated</h1>
        <p style="font-size:13px;color:#6B7280;margin:6px 0 0;">WK{week} FY{fy} &bull; {today_str}</p>
    </div>
    <div style="padding:24px 32px;">
        <p style="font-size:14px;color:#374151;">
            The automated Friday hourly checks (7 AM – 5 PM) did not detect a
            <strong>Total = Summarized</strong> match for WK{week} FY{fy}.
        </p>
        <table style="margin:16px 0;font-size:14px;">
            <tr><td style="padding:4px 12px 4px 0;color:#6B7280;">Total (excl. Denied/Expired):</td>
                <td style="font-weight:700;">{total}</td></tr>
            <tr><td style="padding:4px 12px 4px 0;color:#6B7280;">With Summarized Text:</td>
                <td style="font-weight:700;">{summarized}</td></tr>
        </table>
        <p style="font-size:13px;color:#6B7280;">
            The audio will need to be generated manually via the
            <a href="http://weus42608431466:8888/Zorro/Audio_Message_Hub" style="color:#2563EB;">Audio Message Hub</a>
            dashboard once all summaries are in place.
        </p>
    </div>
    <div style="background:#F9FAFB;padding:12px 32px;text-align:center;border-top:1px solid #E5E7EB;">
        <p style="font-size:11px;color:#9CA3AF;margin:0;">Automated Alert &bull; Zorro Activity Hub</p>
    </div>
</div>
</body></html>"""

    try:
        pythoncom.CoInitialize()
        outlook = win32.Dispatch('Outlook.Application')
        mail = outlook.CreateItem(0)
        mail.To = TEST_RECIPIENT  # kendall.rush@walmart.com
        mail.Subject = subject
        mail.HTMLBody = html_body
        mail.Send()
        logger.info(f"EOD alert sent to {TEST_RECIPIENT}")
    except Exception as e:
        logger.error(f"EOD alert email failed: {e}")
    finally:
        try:
            pythoncom.CoUninitialize()
        except Exception:
            pass


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Auto-generate weekly audio when Total = Summarized")
    parser.add_argument("--test", action="store_true", help="Dry run — check BQ but don't generate or send")
    parser.add_argument("--force", action="store_true", help="Ignore lock file, re-process")
    parser.add_argument("--eod-check", action="store_true",
                        help="End-of-day check — if audio not generated, send alert email")
    parser.add_argument("--week", type=int, default=None)
    parser.add_argument("--fy", type=int, default=None)
    args = parser.parse_args()

    # Determine week/fy early (needed by eod-check)
    if args.week and args.fy:
        week, fy = args.week, args.fy
    else:
        week, fy = get_coming_wm_week_fy()

    # End-of-day check: if not processed by 5 PM, send alert
    if args.eod_check:
        logger.info(f"End-of-day check for WK{week} FY{fy}")
        if _is_already_processed(week, fy):
            logger.info(f"WK{week} FY{fy} was already generated — no alert needed")
            return
        logger.warning(f"WK{week} FY{fy} NOT generated by end of day — sending alert")
        _send_eod_alert(week, fy)
        return

    logger.info("=" * 60)
    logger.info("Auto-Generate Weekly Audio — Starting")
    logger.info("=" * 60)
    logger.info(f"Target: WK{week} FY{fy}")

    # Check lock
    if _is_already_processed(week, fy) and not args.force:
        logger.info(f"WK{week} FY{fy} already processed — exiting")
        return

    # Step 1: Fetch BQ data (on Eagle/VPN)
    logger.info("Step 1: Fetching BQ data...")
    cache_data = fetch_and_cache_bq_data(week, fy)

    if 'error' in cache_data:
        logger.info(f"BQ fetch: {cache_data['error']} — not ready yet, exiting")
        return

    total = cache_data.get('total_excl_denied', 0)
    summarized = cache_data.get('summarized_count', 0)
    logger.info(f"Total (excl. Denied/Expired): {total}, Summarized: {summarized}")

    # Check trigger: Total == Summarized
    if total != summarized or total == 0:
        logger.info(f"Not ready — Total ({total}) != Summarized ({summarized}). Exiting.")
        return

    logger.info(f"TRIGGER: Total ({total}) == Summarized ({summarized}) — starting audio generation!")

    if args.test:
        logger.info("[DRY RUN] Would switch WiFi, synthesize, and send email. Exiting.")
        return

    # Step 2: Switch to Walmartwifi for edge-tts
    if not _switch_to_walmartwifi():
        logger.error("Cannot switch to Walmartwifi — aborting")
        return

    # Step 3: Synthesize audio from cache
    logger.info("Step 3: Synthesizing audio (Jenny Neural)...")
    try:
        synth_result = synthesize_from_cache(week, fy, voice="Jenny", rate=0.95)
    except Exception as e:
        logger.error(f"Synthesis failed: {e}")
        _switch_to_eagle()
        return

    # Step 4: Switch back to Eagle
    _switch_to_eagle()
    time.sleep(5)  # Give Eagle time to fully reconnect

    if not synth_result.get('success'):
        logger.error(f"Synthesis failed: {synth_result.get('error')}")
        return

    logger.info(f"Audio generated: {synth_result.get('output_file')}")

    # Step 5: Build recipient list (TO + CC + on-call)
    to = list(TO_RECIPIENTS)
    cc = list(CC_RECIPIENTS)

    try:
        oncall = get_oncall_from_calendar()
        if oncall:
            oncall_email = oncall['email']
            all_existing = [e.lower() for e in to + cc]
            if oncall_email.lower() not in all_existing:
                cc.append(oncall_email)
                logger.info(f"Added on-call {oncall['name']} ({oncall_email}) to CC")
    except Exception as e:
        logger.warning(f"On-call lookup failed: {e}")

    # Step 6: Send Final Audio Report email
    logger.info("Step 6: Sending Final Weekly Message Audio email...")
    email_result = send_audio_report_email(week, fy, to_recipients=to, cc_recipients=cc)

    if email_result.get('success'):
        logger.info(f"Email sent: {email_result['message']}")
        _mark_processed(week, fy)
        logger.info(f"Marked WK{week} FY{fy} as processed (lock file created)")
    else:
        logger.error(f"Email failed: {email_result.get('error')}")

    logger.info("=" * 60)
    logger.info("Auto-Generate Weekly Audio — Complete")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
