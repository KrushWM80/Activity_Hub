#!/usr/bin/env python3
"""
On-Call Calendar Parser
========================
Parses the U.S. Comm On Call Planner from Outlook calendar.
Calendar entries follow the pattern: "{Name} On Call" spanning Friday-to-Friday.

Used by:
  - send_daily_status_email.py (Friday CC)
  - auto_generate_weekly_audio.py (Final audio email CC)
"""
import re
import logging
from datetime import datetime, timedelta

logger = logging.getLogger('weekly_audio')


def get_oncall_from_calendar(target_date=None):
    """Find the on-call person from calendar for the given date.

    Searches for calendar items matching '{Name} On Call' that span the target date.
    Default target: the coming Friday (or today if already Friday).

    Returns:
        dict with 'name', 'email', 'phone', 'start', 'end' — or None if not found.
    """
    import pythoncom
    import win32com.client

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
                days_until_friday = 7
            target_date = today + timedelta(days=days_until_friday)

        # Search window: 7 days before to 7 days after target
        search_start = (target_date - timedelta(days=7)).strftime('%m/%d/%Y')
        search_end = (target_date + timedelta(days=7)).strftime('%m/%d/%Y')

        items = cal.Items
        items.IncludeRecurrences = True
        items.Sort("[Start]")
        restriction = f"[Start] >= '{search_start}' AND [Start] <= '{search_end}'"
        restricted = items.Restrict(restriction)

        on_call_pattern = re.compile(r'^(.+?)\s+On[\s-]+Call\s*$', re.IGNORECASE)

        # Normalize target_date to a naive date for comparison
        target_day = target_date.date() if hasattr(target_date, 'date') else target_date

        candidates = []  # (start_date, entry_dict, spans_target)
        for item in restricted:
            try:
                subject = item.Subject or ''
                match = on_call_pattern.match(subject)
                if not match:
                    continue

                full_name = match.group(1).strip()
                parts = full_name.split()
                if len(parts) >= 2:
                    email = f"{parts[0]}.{parts[-1]}@walmart.com"
                else:
                    email = f"{full_name.replace(' ', '.')}@walmart.com"

                phone = getattr(item, 'Location', '') or ''

                # Parse start/end as naive dates for span check
                item_start = item.Start
                item_end = item.End
                start_d = item_start.date() if hasattr(item_start, 'date') else item_start
                end_d = item_end.date() if hasattr(item_end, 'date') else item_end

                # Entry spans target if start <= target < end, OR start == target
                spans = (start_d <= target_day < end_d) or (start_d == target_day)

                entry = {
                    'name': full_name,
                    'email': email,
                    'phone': phone,
                    'start': str(item_start),
                    'end': str(item_end),
                }
                candidates.append((start_d, entry, spans))
                logger.info(f"On-call candidate: {full_name} ({item_start} - {item_end}), spans target={spans}")
            except Exception:
                continue

        if not candidates:
            logger.info("No on-call calendar entry found for target date")
            return None

        # Prefer entry that spans the target date
        spanning = [c for c in candidates if c[2]]
        if spanning:
            # Pick the one with the latest start (most current)
            best = max(spanning, key=lambda c: c[0])
            logger.info(f"On-call found (spans target): {best[1]['name']} ({best[1]['email']})")
            return best[1]

        # Fallback: pick the most recent entry (closest start to target)
        candidates.sort(key=lambda c: abs((c[0] - target_day).days))
        best = candidates[0]
        logger.info(f"On-call found (nearest to target): {best[1]['name']} ({best[1]['email']})")
        return best[1]
    except Exception as e:
        logger.warning(f"On-call calendar lookup failed: {e}")
        return None
    finally:
        try:
            pythoncom.CoUninitialize()
        except Exception:
            pass
