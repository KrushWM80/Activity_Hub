#!/usr/bin/env python3
"""
Activity Hub Project Owner Email System
Sends Monday and Wednesday emails to project owners and managers
- Monday: All projects
- Wednesday: Only not-updated projects

Uses Walmart internal SMTP (smtp-gw1.homeoffice.wal-mart.com)
Same pattern as TDA Insights and VET Dashboard (proven, working)
"""

import os
import sys
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from google.cloud import bigquery
import logging

# Configuration
SMTP_SERVER = "smtp-gw1.homeoffice.wal-mart.com"
SMTP_PORT = 25
FROM_EMAIL = "kendall.rush@walmart.com"  # Activity Hub system email
BQ_PROJECT = 'wmt-assetprotection-prod'
BQ_DATASET = 'Store_Support_Dev'
BQ_TABLE = 'AH_Projects'
ACTIVITY_HUB_URL = "http://localhost:8088/activity-hub/projects"

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Set Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
    os.environ.get('APPDATA', ''), 'gcloud', 'application_default_credentials.json'
)


def get_walmart_week():
    """Get current Walmart fiscal week"""
    today = datetime.now()
    fy_start = datetime(today.year if today.month >= 2 else today.year - 1, 2, 1)
    days_since = (today - fy_start).days
    return (days_since // 7) + 1


def query_owner_projects(owner_name: str, include_only_not_updated: bool = False) -> list:
    """Query BigQuery for projects owned by a specific person"""
    current_week = get_walmart_week()
    
    client = bigquery.Client(project=BQ_PROJECT)
    
    sql = f"""
    SELECT 
        project_id,
        title,
        owner,
        health,
        status,
        project_update,
        project_update_date,
        business_organization
    FROM `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE}`
    WHERE owner = @owner_name
    ORDER BY title ASC
    """
    
    job_config = bigquery.QueryJobConfig(query_parameters=[
        bigquery.ScalarQueryParameter("owner_name", "STRING", owner_name),
    ])
    
    results = list(client.query(sql, job_config=job_config).result())
    
    projects = []
    for row in results:
        # Check if updated this WM week
        is_updated = False
        if row.project_update_date:
            update_date = row.project_update_date
            fy_start = datetime(update_date.year if update_date.month >= 2 else update_date.year - 1, 2, 1)
            days_since = (update_date.replace(tzinfo=None) - fy_start).days
            update_wm_week = (days_since // 7) + 1
            is_updated = (update_wm_week == current_week)
        
        # Filter based on parameter
        if include_only_not_updated and is_updated:
            continue
        
        # Handle project_update note - show "No note provided" if empty
        project_note = row.project_update if row.project_update and row.project_update.strip() else 'No note provided'
        
        # Handle date display - show "None Provided" instead of "Never"
        update_date_str = row.project_update_date.strftime('%b %d, %Y') if row.project_update_date else 'None Provided'
        
        projects.append({
            'project_id': row.project_id,
            'title': row.title or 'N/A',
            'owner': row.owner or 'N/A',
            'health': row.health or 'Unknown',
            'status': row.status or 'Unknown',
            'project_update': project_note,
            'updated': is_updated,
            'update_date': update_date_str,
            'business_area': row.business_organization or 'N/A'
        })
    
    return projects


def get_all_project_owners() -> list:
    """Get all unique project owners from AH_Projects"""
    client = bigquery.Client(project=BQ_PROJECT)
    
    sql = f"""
    SELECT DISTINCT owner 
    FROM `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE}`
    WHERE owner IS NOT NULL AND owner != ''
    ORDER BY owner ASC
    """
    
    results = list(client.query(sql).result())
    return [row.owner for row in results]


def generate_owner_email_html(owner_name: str, projects: list, email_type: str = 'monday') -> str:
    """Generate professional HTML email for project owner (matches VET Dashboard style)"""
    
    day_text = "This Week's Project Update" if email_type == 'monday' else "Projects Needing Updates"
    action_text = (
        "Below are all your projects for this week. Please review and provide updates where needed."
        if email_type == 'monday'
        else "Below are your projects that have not been updated in this Walmart week. Please provide status updates."
    )
    
    if not projects:
        projects_table = """
        <tr>
            <td colspan="6" style="text-align: center; padding: 24px; color: #999; font-style: italic;">
                No projects to display
            </td>
        </tr>
        """
    else:
        project_rows = []
        for p in projects:
            status_badge = (
                '<span style="display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; '
                f'font-weight: 600; background-color: #d4edda; color: #155724;">✓ Updated</span>'
                if p['updated']
                else '<span style="display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; '
                'font-weight: 600; background-color: #ffeaa7; color: #d63031;">⚠ Not Updated</span>'
            )
            
            health_color = '#107C10' if p['health'] == 'On Track' else '#F7630C' if p['health'] == 'At Risk' else '#DC3545'
            update_note = p.get('project_update', 'No note provided')
            
            project_rows.append(f"""
            <tr style="border-bottom: 1px solid #e0e0e0;">
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; font-weight: 500;">{p['title']}</td>
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; font-weight: 600; color: {health_color};">{p['health']}</td>
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; color: #666; font-size: 13px;">{p['update_date']}</td>
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; font-size: 13px; line-height: 1.4;">{update_note}</td>
                <td style="padding: 12px; text-align: center;">{status_badge}</td>
            </tr>
            """)
        
        projects_table = ''.join(project_rows)
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Activity Hub Project Update</title>
</head>
<body style="font-family: 'Segoe UI', Arial, sans-serif; color: #333; margin: 0; padding: 0; background-color: #f5f5f5;">

<table style="width: 100%; max-width: 900px; margin: 0 auto; background-color: white; border-collapse: collapse;" cellpadding="0" cellspacing="0" border="0">
    
    <!-- HEADER -->
    <tr>
        <td style="background: linear-gradient(135deg, #0071CE 0%, #004C91 100%); padding: 32px 24px; text-align: left;">
            <table cellpadding="0" cellspacing="0" border="0" style="width: 100%;">
                <tr>
                    <td style="width: 50px; padding-right: 16px; vertical-align: middle;">
                        <div style="width: 48px; height: 48px; background-color: #FFC220; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 700; color: #0071CE; font-size: 24px;">
                            ✦
                        </div>
                    </td>
                    <td style="vertical-align: middle;">
                        <h1 style="margin: 0 0 4px 0; font-size: 22px; font-weight: 700; color: #ffffff; letter-spacing: -0.5px;">Activity Hub &gt; Projects</h1>
                        <p style="margin: 0; font-size: 13px; color: rgba(255,255,255,0.9); font-weight: 500;">{day_text}</p>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
    
    <!-- CONTENT -->
    <tr>
        <td style="padding: 32px 24px;">
            
            <!-- Greeting -->
            <p style="margin: 0 0 8px 0; font-size: 16px; font-weight: 500;">Hi {owner_name},</p>
            <p style="margin: 0 0 24px 0; font-size: 14px; color: #666; line-height: 1.6;">{action_text}</p>
            
            <!-- Project Count Badge -->
            <div style="background-color: #f0f7ff; border-left: 4px solid #0071CE; padding: 16px 20px; margin-bottom: 24px; border-radius: 4px;">
                <div style="font-size: 13px; font-weight: 600; color: #0071CE; text-transform: uppercase; letter-spacing: 0.5px;">Project Summary</div>
                <div style="font-size: 24px; font-weight: 700; color: #0071CE; margin-top: 4px;">
                    {len(projects)} Project{'s' if len(projects) != 1 else ''}
                </div>
            </div>
            
            <!-- Projects Table -->
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 24px; border: 1px solid #e0e0e0;" cellpadding="0" cellspacing="0" border="0">
                <thead>
                    <tr style="background-color: #f5f5f5; border-bottom: 2px solid #0071CE;">
                        <th style="padding: 12px; text-align: left; font-weight: 600; font-size: 13px; color: #333; text-transform: uppercase; letter-spacing: 0.5px; border-right: 1px solid #e0e0e0;">Project Title</th>
                        <th style="padding: 12px; text-align: left; font-weight: 600; font-size: 13px; color: #333; text-transform: uppercase; letter-spacing: 0.5px; border-right: 1px solid #e0e0e0;">Health</th>
                        <th style="padding: 12px; text-align: left; font-weight: 600; font-size: 13px; color: #333; text-transform: uppercase; letter-spacing: 0.5px; border-right: 1px solid #e0e0e0;">Last Updated</th>
                        <th style="padding: 12px; text-align: left; font-weight: 600; font-size: 13px; color: #333; text-transform: uppercase; letter-spacing: 0.5px; border-right: 1px solid #e0e0e0;">Project Update Note</th>
                        <th style="padding: 12px; text-align: center; font-weight: 600; font-size: 13px; color: #333; text-transform: uppercase; letter-spacing: 0.5px;">Status</th>
                    </tr>
                </thead>
                <tbody>
                    {projects_table}
                </tbody>
            </table>
            
            <!-- Call-to-Action Button -->
            <table style="margin: 24px 0;" cellpadding="0" cellspacing="0" border="0">
                <tr>
                    <td style="background: linear-gradient(135deg, #0071CE 0%, #004C91 100%); border-radius: 6px; padding: 14px 32px;">
                        <a href="{ACTIVITY_HUB_URL}" style="display: inline-block; color: white; text-decoration: none; font-weight: 600; font-size: 14px;">
                            → Go to Activity Hub Projects
                        </a>
                    </td>
                </tr>
            </table>
            
            <!-- Action Text -->
            <p style="margin: 24px 0 0 0; font-size: 13px; color: #666; line-height: 1.6; font-style: italic;">
                💡 Please log in to Activity Hub to provide project updates. Your updates help keep leadership informed on project status.
            </p>
            
        </td>
    </tr>
    
    <!-- FOOTER -->
    <tr>
        <td style="background-color: #f5f5f5; padding: 20px 24px; border-top: 1px solid #e0e0e0; text-align: center;">
            <p style="margin: 0; font-size: 12px; color: #999;">
                This is an automated email from Activity Hub. Please do not reply to this email.
            </p>
            <p style="margin: 8px 0 0 0; font-size: 12px; color: #999;">
                Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
            </p>
        </td>
    </tr>
    
</table>

</body>
</html>
"""
    
    return html


def send_smtp_email(recipient_email: str, subject: str, html_body: str) -> bool:
    """Send email via Walmart internal SMTP (same as TDA Insights & VET Dashboard)"""
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = FROM_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(html_body, 'html', 'utf-8'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
            server.sendmail(FROM_EMAIL, [recipient_email], msg.as_string())
        
        logger.info(f"✓ Email sent to {recipient_email}")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to send email to {recipient_email}: {e}")
        return False


def send_owner_emails(email_type: str = 'monday', test_mode: bool = False):
    """
    Send emails to all project owners
    
    Args:
        email_type: 'monday' (all projects) or 'wednesday' (not updated only)
        test_mode: If True, only send samples (2-3) to kendall.rush@walmart.com with details
    """
    
    logger.info("=" * 80)
    logger.info(f"Activity Hub Project Owner Emails - {email_type.upper()}")
    logger.info("=" * 80)
    
    # Get all owners
    logger.info("\n[1/3] Fetching all project owners...")
    owners = get_all_project_owners()
    logger.info(f"  Found {len(owners)} unique project owners")
    
    # Send emails
    logger.info(f"\n[2/3] Sending {email_type} emails...")
    sent_count = 0
    failed_count = 0
    
    # In test mode, sample 2-3 owners with different scenarios (some with projects, some without)
    if test_mode:
        sample_owners = owners[:3] if len(owners) >= 3 else owners  # Take first 3 or all if < 3
        logger.info(f"  [TEST MODE] Sampling {len(sample_owners)} owners for testing")
        test_owners = sample_owners
    else:
        test_owners = owners
    
    for owner in test_owners:
        # Get owner's projects
        include_only_not_updated = (email_type == 'wednesday')
        projects = query_owner_projects(owner, include_only_not_updated=include_only_not_updated)
        
        if not projects:
            logger.info(f"  ⊘ {owner}: No projects ({email_type})")
            continue
        
        # Generate email
        html_body = generate_owner_email_html(owner, projects, email_type)
        subject = f"Activity Hub - {owner}'s Projects ({email_type.capitalize()})"
        
        # Determine recipient
        if test_mode:
            recipient = 'kendall.rush@walmart.com'
            logger.info(f"  [TEST] {owner}: {len(projects)} project(s) → {recipient}")
        else:
            # In production, owner email would come from a lookup table
            # For now, skip non-test sends
            logger.info(f"  [SKIP] {owner}: {len(projects)} projects (test mode disabled)")
            continue
        
        # Send
        if send_smtp_email(recipient, subject, html_body):
            sent_count += 1
        else:
            failed_count += 1
    
    logger.info(f"\n[3/3] Email Summary")
    logger.info(f"  Sent: {sent_count}")
    logger.info(f"  Failed: {failed_count}")
    logger.info("=" * 80)


def generate_demo_email(owner_name: str = "Kendall Rush", email_type: str = 'monday'):
    """Generate a demo email for format review"""
    
    logger.info("=" * 80)
    logger.info(f"Generating Demo Email - {email_type.upper()}")
    logger.info("=" * 80)
    
    # Create sample projects
    if email_type == 'monday':
        projects = [
            {
                'project_id': 12345,
                'title': 'Project Management System Implementation',
                'owner': owner_name,
                'health': 'On Track',
                'status': 'In Progress',
                'project_update': 'Team completed Phase 2 design review. No blockers at this time.',
                'updated': True,
                'update_date': 'Apr 23, 2026',
                'business_area': 'Technology'
            },
            {
                'project_id': 12346,
                'title': 'Store Layout Optimization - Region 5',
                'owner': owner_name,
                'health': 'At Risk',
                'status': 'Pending Review',
                'project_update': 'Waiting for approval from regional leadership. Expected by end of week.',
                'updated': False,
                'update_date': 'None Provided',
                'business_area': 'Operations'
            },
            {
                'project_id': 12347,
                'title': 'Q2 Budget Forecasting Initiative',
                'owner': owner_name,
                'health': 'On Track',
                'status': 'In Progress',
                'project_update': 'Forecast model 90% complete. Finance team collaborating on review.',
                'updated': True,
                'update_date': 'Apr 22, 2026',
                'business_area': 'Finance'
            },
        ]
    else:
        # Wednesday: only not updated projects
        projects = [
            {
                'project_id': 12346,
                'title': 'Store Layout Optimization - Region 5',
                'owner': owner_name,
                'health': 'At Risk',
                'status': 'Pending Review',
                'project_update': 'Waiting for approval from regional leadership.',
                'updated': False,
                'update_date': 'None Provided',
                'business_area': 'Operations'
            },
        ]
    
    html_body = generate_owner_email_html(owner_name, projects, email_type)
    
    # Save to file
    output_file = Path(__file__).parent / f"demo_email_{email_type}.html"
    output_file.write_text(html_body, encoding='utf-8')
    
    logger.info(f"\n✓ Demo email saved to: {output_file}")
    logger.info(f"  Owner: {owner_name}")
    logger.info(f"  Type: {email_type.upper()}")
    logger.info(f"  Projects: {len(projects)}")
    logger.info(f"  Size: {len(html_body):,} bytes")
    logger.info("=" * 80)
    
    return output_file, html_body


def main():
    """Main entry point"""
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'demo':
            # Generate demo email
            email_type = sys.argv[2].lower() if len(sys.argv) > 2 else 'monday'
            output_file, _ = generate_demo_email('Kendall Rush', email_type)
            print(f"\n✓ Demo email generated: {output_file}")
            return
        
        elif command == 'monday':
            # Send Monday emails
            send_owner_emails('monday', test_mode=True)
            return
        
        elif command == 'wednesday':
            # Send Wednesday emails
            send_owner_emails('wednesday', test_mode=True)
            return
    
    # Default: show usage
    print("""
Usage:
  python send_projects_owner_emails.py demo [monday|wednesday]     # Generate demo email
  python send_projects_owner_emails.py monday                       # Send Monday emails
  python send_projects_owner_emails.py wednesday                    # Send Wednesday emails
    """)


if __name__ == '__main__':
    main()
