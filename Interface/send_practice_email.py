#!/usr/bin/env python3
"""
Activity Hub Practice Email - Leadership Chain
Sends test email to kendall.rush@walmart.com with:
- Kendall Rush (Owner)
- Kendall's Boss (Manager)
- Kendall's Boss's Boss (Skip-level Manager)

Usage: python send_practice_email.py
"""

import os
import sys
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from google.cloud import bigquery
import logging

# Configuration
SMTP_SERVER = "smtp-gw1.homeoffice.wal-mart.com"
SMTP_PORT = 25
FROM_EMAIL = "kendall.rush@walmart.com"
TEST_RECIPIENT = "kendall.rush@walmart.com"  # Send test email here
BQ_PROJECT = 'wmt-assetprotection-prod'
BQ_DATASET = 'Store_Support_Dev'
BQ_TABLE = 'AH_Projects'
ACTIVITY_HUB_URL = "http://localhost:8088/activity-hub/projects"

# Leadership Chain - Activity Hub Projects
LEADERSHIP_CHAIN = {
    'owner': {
        'name': 'Kendall Rush',
        'email': 'kendall.rush@walmart.com',
        'role': 'Project Owner'
    },
    'manager': {
        'name': 'Matt Farnworth',
        'email': 'matt.farnworth@walmart.com',
        'role': 'Direct Manager'
    },
    'skip_level': {
        'name': 'Kristine Torres',
        'email': 'kristine.torres@walmart.com',
        'role': 'Skip-Level Manager'
    }
}

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


def get_owner_projects(owner_name: str) -> list:
    """Query BigQuery for projects owned by Kendall Rush"""
    
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
    LIMIT 10
    """
    
    job_config = bigquery.QueryJobConfig(query_parameters=[
        bigquery.ScalarQueryParameter("owner_name", "STRING", owner_name),
    ])
    
    results = list(client.query(sql, job_config=job_config).result())
    
    projects = []
    for row in results:
        # Handle date display
        update_date_str = row.project_update_date.strftime('%b %d, %Y') if row.project_update_date else 'Not updated'
        
        # Handle project update note
        project_note = row.project_update if row.project_update and row.project_update.strip() else 'No note provided'
        
        projects.append({
            'project_id': row.project_id,
            'title': row.title or 'N/A',
            'owner': row.owner or 'N/A',
            'health': row.health or 'Unknown',
            'status': row.status or 'Unknown',
            'project_update': project_note,
            'update_date': update_date_str,
            'business_area': row.business_organization or 'N/A'
        })
    
    return projects


def generate_leadership_email_html(projects: list) -> str:
    """Generate HTML email showing leadership chain"""
    
    if not projects:
        projects_table = """
        <tr>
            <td colspan="5" style="text-align: center; padding: 24px; color: #999; font-style: italic;">
                No projects to display
            </td>
        </tr>
        """
    else:
        project_rows = []
        for p in projects:
            health_color = '#107C10' if p['health'] == 'On Track' else '#F7630C' if p['health'] == 'At Risk' else '#DC3545'
            
            project_rows.append(f"""
            <tr style="border-bottom: 1px solid #e0e0e0;">
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; font-weight: 500;">{p['title']}</td>
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; font-weight: 600; color: {health_color};">{p['health']}</td>
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; color: #666; font-size: 13px;">{p['business_area']}</td>
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; color: #666; font-size: 13px;">{p['update_date']}</td>
                <td style="padding: 12px; font-size: 13px; line-height: 1.4;">{p['project_update']}</td>
            </tr>
            """)
        
        projects_table = ''.join(project_rows)
    
    # Build leadership recipients list
    leadership_html = ""
    for key, person in LEADERSHIP_CHAIN.items():
        leadership_html += f"""
        <tr style="border-bottom: 1px solid #e0e0e0;">
            <td style="padding: 12px; width: 30%; font-weight: 600; color: #0071CE;">{person['role']}</td>
            <td style="padding: 12px;">{person['name']}</td>
            <td style="padding: 12px; font-family: monospace; font-size: 12px; color: #666;">{person['email']}</td>
        </tr>
        """
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Activity Hub Practice Email - Leadership Chain</title>
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
                            ⚡
                        </div>
                    </td>
                    <td style="vertical-align: middle;">
                        <h1 style="margin: 0 0 4px 0; font-size: 22px; font-weight: 700; color: #ffffff; letter-spacing: -0.5px;">Activity Hub &gt; Practice Email</h1>
                        <p style="margin: 0; font-size: 13px; color: rgba(255,255,255,0.9); font-weight: 500;">Leadership Chain Test</p>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
    
    <!-- CONTENT -->
    <tr>
        <td style="padding: 32px 24px;">
            
            <!-- Greeting -->
            <p style="margin: 0 0 8px 0; font-size: 16px; font-weight: 500;">Hi Team,</p>
            <p style="margin: 0 0 24px 0; font-size: 14px; color: #666; line-height: 1.6;">This is a practice email demonstrating the leadership chain notification system for Activity Hub projects. Below is the distribution list for {LEADERSHIP_CHAIN['owner']['name']}'s projects.</p>
            
            <!-- Leadership Chain Section -->
            <div style="background-color: #f0f7ff; border-left: 4px solid #0071CE; padding: 20px; margin-bottom: 24px; border-radius: 4px;">
                <h3 style="margin: 0 0 16px 0; font-size: 14px; font-weight: 600; color: #0071CE; text-transform: uppercase; letter-spacing: 0.5px;">📋 Leadership Chain Recipients</h3>
                
                <table style="width: 100%; border-collapse: collapse;" cellpadding="0" cellspacing="0" border="0">
                    <tr style="background-color: #e8f4f8;">
                        <th style="padding: 10px; text-align: left; font-weight: 600; font-size: 12px; color: #0071CE; border-right: 1px solid #cce5f1;">Role</th>
                        <th style="padding: 10px; text-align: left; font-weight: 600; font-size: 12px; color: #0071CE; border-right: 1px solid #cce5f1;">Name</th>
                        <th style="padding: 10px; text-align: left; font-weight: 600; font-size: 12px; color: #0071CE;">Email</th>
                    </tr>
                    {leadership_html}
                </table>
            </div>
            
            <!-- Project Count Badge -->
            <div style="background-color: #fff8f0; border-left: 4px solid #F7630C; padding: 16px 20px; margin-bottom: 24px; border-radius: 4px;">
                <div style="font-size: 13px; font-weight: 600; color: #F7630C; text-transform: uppercase; letter-spacing: 0.5px;">📊 Sample Projects Summary</div>
                <div style="font-size: 24px; font-weight: 700; color: #F7630C; margin-top: 4px;">
                    {len(projects)} Project{'s' if len(projects) != 1 else ''}
                </div>
            </div>
            
            <!-- Projects Table -->
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 24px; border: 1px solid #e0e0e0;" cellpadding="0" cellspacing="0" border="0">
                <thead>
                    <tr style="background-color: #f5f5f5; border-bottom: 2px solid #0071CE;">
                        <th style="padding: 12px; text-align: left; font-weight: 600; font-size: 13px; color: #333; text-transform: uppercase; letter-spacing: 0.5px; border-right: 1px solid #e0e0e0;">Project Title</th>
                        <th style="padding: 12px; text-align: left; font-weight: 600; font-size: 13px; color: #333; text-transform: uppercase; letter-spacing: 0.5px; border-right: 1px solid #e0e0e0;">Health</th>
                        <th style="padding: 12px; text-align: left; font-weight: 600; font-size: 13px; color: #333; text-transform: uppercase; letter-spacing: 0.5px; border-right: 1px solid #e0e0e0;">Business Area</th>
                        <th style="padding: 12px; text-align: left; font-weight: 600; font-size: 13px; color: #333; text-transform: uppercase; letter-spacing: 0.5px; border-right: 1px solid #e0e0e0;">Last Updated</th>
                        <th style="padding: 12px; text-align: left; font-weight: 600; font-size: 13px; color: #333; text-transform: uppercase; letter-spacing: 0.5px;">Latest Update Note</th>
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
                            → View All Projects in Activity Hub
                        </a>
                    </td>
                </tr>
            </table>
            
            <!-- Notes -->
            <div style="background-color: #fffbf0; border-left: 4px solid #FFB81C; padding: 16px 20px; margin: 24px 0; border-radius: 4px;">
                <p style="margin: 0; font-size: 13px; color: #666; line-height: 1.6;">
                    <strong>✓ Practice Email Note:</strong> This is a test email demonstrating how automated notifications will be sent to the leadership chain. 
                    Actual production emails will be sent to all recipients listed above automatically according to the configured schedule.
                </p>
            </div>
            
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
    """Send email via Walmart internal SMTP"""
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


def main():
    """Main entry point"""
    
    logger.info("=" * 80)
    logger.info("ACTIVITY HUB - PRACTICE EMAIL (LEADERSHIP CHAIN)")
    logger.info("=" * 80)
    
    logger.info("\n[1/3] Fetching projects for Kendall Rush...")
    projects = get_owner_projects('Kendall Rush')
    logger.info(f"  Found {len(projects)} projects")
    
    if not projects:
        logger.warning("  No projects found for Kendall Rush")
    
    logger.info("\n[2/3] Generating email...")
    html_body = generate_leadership_email_html(projects)
    subject = "Activity Hub - Practice Email: Leadership Chain for Kendall Rush"
    
    logger.info(f"\n[3/3] Sending test email to {TEST_RECIPIENT}...")
    if send_smtp_email(TEST_RECIPIENT, subject, html_body):
        logger.info("\n" + "=" * 80)
        logger.info("✓ PRACTICE EMAIL SENT SUCCESSFULLY")
        logger.info("=" * 80)
        logger.info("\nEmail Details:")
        logger.info(f"  FROM: {FROM_EMAIL}")
        logger.info(f"  TO: {TEST_RECIPIENT}")
        logger.info(f"  SUBJECT: {subject}")
        logger.info(f"  PROJECTS: {len(projects)}")
        logger.info(f"\nLeadership Chain Recipients:")
        for key, person in LEADERSHIP_CHAIN.items():
            logger.info(f"  • {person['role']}: {person['name']} ({person['email']})")
    else:
        logger.error("\n" + "=" * 80)
        logger.error("✗ FAILED TO SEND PRACTICE EMAIL")
        logger.error("=" * 80)


if __name__ == '__main__':
    main()
