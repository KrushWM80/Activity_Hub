#!/usr/bin/env python3
"""
Activity Hub Projects - Scheduled Email Runner
Sends the right email type based on the day of the week:
  Monday    → Owner emails (all active projects)
  Wednesday → Owner emails (not-updated projects only)
  Thursday  → Leadership emails (director/sr_director summaries)

TEST MODE: Only sends to Kendall Rush, Matt Farnworth, Kristine Torres
All emails routed to kendall.rush@walmart.com during test.
"""

import os
import sys
import logging
from datetime import datetime

# Add parent directory so we can import send_projects_emails
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from send_projects_emails import (
    send_smtp_email,
    query_owner_projects,
    query_director_projects,
    generate_email_html,
    LEADERSHIP_HIERARCHY,
    logger,
)

# ── Configuration ────────────────────────────────────────────────────────────
TEST_MODE = True                          # True = only test recipients below

# Test scope: owner + director + sr_director
TEST_OWNERS = ['Kendall Rush']
TEST_DIRECTORS = ['Matt Farnworth']       # Director
TEST_SR_DIRECTORS = ['Kristine Torres']   # Sr. Director
# ─────────────────────────────────────────────────────────────────────────────


def get_recipient(person_name: str) -> str:
    """Return actual email for the person"""
    info = LEADERSHIP_HIERARCHY.get(person_name)
    if info:
        return info['email']
    # Fallback: construct from name
    parts = person_name.lower().split()
    return f"{parts[0]}.{parts[-1]}@walmart.com" if len(parts) >= 2 else None


def send_owner_emails(include_only_not_updated: bool = False):
    """Send Monday or Wednesday owner emails"""
    email_type = 'wednesday' if include_only_not_updated else 'monday'
    day_label = 'Wednesday (Not Updated)' if include_only_not_updated else 'Monday (All Projects)'

    logger.info(f"── {day_label} Owner Emails ──")

    for owner in TEST_OWNERS:
        projects = query_owner_projects(owner, include_only_not_updated=include_only_not_updated)
        if not projects and include_only_not_updated:
            logger.info(f"  {owner}: All projects updated — no email needed")
            continue

        html = generate_email_html(email_type, owner, projects, is_leadership=False)
        subject = f"Activity Hub Projects - {day_label} for {owner}"
        recipient = get_recipient(owner)
        logger.info(f"  {owner} → {recipient}  ({len(projects)} projects)")
        send_smtp_email(recipient, subject, html)


def send_leadership_emails():
    """Send Thursday leadership summary emails"""
    logger.info("── Thursday Leadership Emails ──")

    # Import the leadership HTML generator
    from send_projects_emails import generate_leadership_email_html

    for director in TEST_DIRECTORS + TEST_SR_DIRECTORS:
        projects = query_director_projects(director)
        if not projects:
            logger.info(f"  {director}: No team projects — skipping")
            continue

        html = generate_leadership_email_html(director, projects)
        subject = f"Activity Hub Projects - Leadership Summary for {director}"
        recipient = get_recipient(director)
        logger.info(f"  {director} → {recipient}  ({len(projects)} projects)")
        send_smtp_email(recipient, subject, html)


def run_for_today():
    """Determine today's day-of-week and send the right emails"""
    today = datetime.now()
    dow = today.strftime('%A')   # Monday, Tuesday, …

    logger.info("=" * 70)
    logger.info(f"ACTIVITY HUB EMAIL SCHEDULER - {today.strftime('%A %B %d, %Y %I:%M %p')}")
    logger.info(f"TEST MODE: {TEST_MODE}")
    if TEST_MODE:
        logger.info(f"  Owners:       {TEST_OWNERS}")
        logger.info(f"  Directors:    {TEST_DIRECTORS}")
        logger.info(f"  Sr Directors: {TEST_SR_DIRECTORS}")
    logger.info("=" * 70)

    if dow == 'Monday':
        send_owner_emails(include_only_not_updated=False)
    elif dow == 'Wednesday':
        send_owner_emails(include_only_not_updated=True)
    elif dow == 'Thursday':
        send_leadership_emails()
    else:
        logger.info(f"No emails scheduled for {dow}. "
                     "Email days: Monday (owner), Wednesday (owner), Thursday (leadership)")

    logger.info("=" * 70)
    logger.info("✓ SCHEDULER COMPLETE")
    logger.info("=" * 70)


if __name__ == '__main__':
    run_for_today()
