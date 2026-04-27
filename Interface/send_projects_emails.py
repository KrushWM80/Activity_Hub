#!/usr/bin/env python3
"""
Activity Hub Projects Email System - All Three Email Types
1. Monday: All Active Projects for Each Owner
2. Wednesday: Not Updated Projects for Each Owner  
3. Leadership: All Direct Reports' Projects for Managers
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
BQ_PROJECT = 'wmt-assetprotection-prod'
BQ_DATASET = 'Store_Support_Dev'
BQ_TABLE = 'AH_Projects'
INTAKE_HUB_URL = "http://weus42608431466:8088/activity-hub/intake"
PROJECTS_URL = "http://weus42608431466:8088/activity-hub/projects"
PROJECTS_DASHBOARD = "http://weus42608431466:8088/activity-hub/projects"

# Organizational Hierarchy
LEADERSHIP_HIERARCHY = {
    'Kendall Rush': {
        'email': 'kendall.rush@walmart.com',
        'manager': 'Matt Farnworth',
        'direct_reports': []
    },
    'Matt Farnworth': {
        'email': 'matthew.farnworth@walmart.com',
        'manager': 'Kristine Torres',
        'direct_reports': ['Kendall Rush']  # People reporting to Matt
    },
    'Kristine Torres': {
        'email': 'kristine.torres@walmart.com',
        'manager': None,
        'direct_reports': ['Matt Farnworth']  # People reporting to Kristine
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


def get_project_url(project_id: str, project_source: str) -> tuple:
    """Generate proper URL and determine if should show link based on project source
    Returns: (url, should_show_link)"""
    if 'Intake' in project_source:
        # Intake Hub projects link to hoops.wal-mart.com
        return (f"https://hoops.wal-mart.com/intake-hub/projects/{project_id}", True)
    else:
        # Projects dashboard - link to Activity Hub projects page
        return (f"http://weus42608431466:8088/activity-hub/projects?id={project_id}", True)


def query_owner_projects(owner_name: str, include_only_not_updated: bool = False) -> list:
    """Query BigQuery for projects owned by a specific person"""
    
    client = bigquery.Client(project=BQ_PROJECT)
    
    # Use Cal_Dim_Data to determine current WM week
    week_query = """
    SELECT DISTINCT WM_WEEK_NBR, FISCAL_YEAR_NBR
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Cal_Dim_Data`
    WHERE CALENDAR_DATE = CURRENT_DATE()
    LIMIT 1
    """
    
    week_result = list(client.query(week_query).result())
    if week_result:
        current_wm_week = week_result[0]['WM_WEEK_NBR']
        current_fiscal_year = week_result[0]['FISCAL_YEAR_NBR']
    else:
        current_wm_week = 13
        current_fiscal_year = 2027
    
    sql = f"""
    SELECT 
        ap.project_id,
        ap.title,
        ap.owner,
        ap.health,
        ap.status,
        ap.project_update,
        ap.project_update_date,
        ap.business_organization,
        ap.project_source,
        c.WM_WEEK_NBR,
        c.FISCAL_YEAR_NBR
    FROM `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE}` ap
    LEFT JOIN `{BQ_PROJECT}.{BQ_DATASET}.Cal_Dim_Data` c
      ON CAST(ap.project_update_date AS DATE) = c.CALENDAR_DATE
    WHERE ap.owner = @owner_name
    ORDER BY ap.title ASC
    """
    
    job_config = bigquery.QueryJobConfig(query_parameters=[
        bigquery.ScalarQueryParameter("owner_name", "STRING", owner_name),
    ])
    
    results = list(client.query(sql, job_config=job_config).result())
    
    projects = []
    for row in results:
        # Check if updated this WM week
        is_updated = False
        if row.WM_WEEK_NBR == current_wm_week and row.FISCAL_YEAR_NBR == current_fiscal_year:
            is_updated = True
        
        # Filter based on parameter
        if include_only_not_updated and is_updated:
            continue
        
        # Handle project_update note
        project_note = row.project_update if row.project_update and row.project_update.strip() else 'No update provided'
        
        # Handle date display
        update_date_str = row.project_update_date.strftime('%b %d, %Y') if row.project_update_date else 'Not updated'
        
        # Get project URL and whether to show link
        url, show_link = get_project_url(row.project_id, row.project_source or 'Projects')
        
        projects.append({
            'project_id': row.project_id,
            'title': row.title or 'N/A',
            'owner': row.owner or 'N/A',
            'health': row.health or 'Unknown',
            'status': row.status or 'Unknown',
            'project_update': project_note,
            'updated': is_updated,
            'update_date': update_date_str,
            'business_area': row.business_organization or 'N/A',
            'project_source': row.project_source or 'Manual',
            'url': url
        })
    
    return projects


def generate_email_html(email_type: str, owner_name: str, projects: list, is_leadership: bool = False, manager_name: str = None) -> str:
    """Generate professional HTML email for project notifications"""
    
    # Determine email type text
    if is_leadership:
        day_text = f"Team Projects Summary - {owner_name}'s Direct Reports"
        action_text = f"Below are all projects for those directly reporting to you. Please review and provide guidance where needed."
    elif email_type == 'monday':
        day_text = "This Week's Project Updates"
        action_text = "Below are all your projects for this week. Please provide updates where needed."
    else:  # wednesday
        day_text = "Projects Needing Updates"
        action_text = "Below are your projects that have not been updated in this Walmart week. Please provide status updates."
    
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
            # Map health status to colors
            health_value = p['health'].lower() if p['health'] else 'unknown'
            if 'on track' in health_value:
                health_color = '#107C10'  # Green
            elif 'at risk' in health_value:
                health_color = '#F7630C'  # Orange
            elif 'off track' in health_value or 'paused' in health_value:
                health_color = '#DC3545'  # Red
            else:
                health_color = '#666666'  # Gray for unknown/other
            
            # Create clickable project title based on source
            if 'Intake' in p['project_source']:
                # Intake Hub projects link to hoops.wal-mart.com
                project_url = f"https://hoops.wal-mart.com/intake-hub/projects/{p['project_id']}"
            else:
                # Projects dashboard - link to Activity Hub projects page
                project_url = f"http://weus42608431466:8088/activity-hub/projects?id={p['project_id']}"
            
            project_title_html = f'<a href="{project_url}" style="color: #0071CE; text-decoration: none; font-weight: 500;" target="_blank">{p["title"]}</a>'
            
            project_rows.append(f"""
            <tr style="border-bottom: 1px solid #e0e0e0;">
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; font-weight: 500;">{project_title_html}</td>
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; font-weight: 600; color: {health_color};">{p['health']}</td>
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; color: #666; font-size: 13px;">{p['business_area']}</td>
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; color: #666; font-size: 13px;">{p['update_date']}</td>
                <td style="padding: 12px; font-size: 13px; line-height: 1.4; max-width: 300px; word-wrap: break-word;">{p['project_update']}</td>
            </tr>
            """)
        
        projects_table = ''.join(project_rows)
    
    # Spark logo as base64
    spark_logo_base64 = "iVBORw0KGgoAAAANSUhEUgAAAHgAAAB4CAYAAAA5ZDbSAAAACXBIWXMAAA7DAAAOwwHHb6thAAADYElEQVR4nO2dMU7kQBCFXXCBgMSBA5wgwwGYkZjhmBnGhBvESNwgJGbGS0BAVOQwMIGsADeQmBFgBGZGYkbg6VJ3bXudu2M7M/PVV/O/F3i1M+6e/k9P/1v+MTAZQgh4WRCWKlKqKlKqKlKqKlKqKlKqKlKqKlKqKlKqKlKqKlKqKlKqKlKqKlKqKlKqKlKqKvJfI8Symj5VVV0uFgvzfr/N9/t9ur6+vpqZmW1ubtzOzs7ZbrezDIfDi9/vZ6enp1fX13fN5eXlEZqZfb1ex+Px2Ox2O3t9fb27ubmxs7MzGwwGdn19ber1ul1dXVk4HJrnx2Nx+Pj4aJPJRHU6HbtYLMxmszGdTseMMXY2m6nJZKLKkiSJ6vV60eFwUCXJN2VZqMFgYJRlYXq9nsKBNpvN1GazMXXhw+FgfD6furu7U2qCmUxGXV5eqslkotRt6XQ6RP0fFGWhLi8v1dPTkyrJRFGUKk+S6PV6DgYDg1wt6vfhcKB8Pp9yOp3K6/UqxOdzPJQqyFUlmSjLQrlcLjObzSqn06lcLpc6HA5qvV4rr9er+v2+6vV6anNzWzkcDhV/PuQ5oQA9Ho/yeDyqXq8rj8ej/H6/Ug6HQ/lcLpXJZNT5+blKpVLK5XKp5XKpPB6PCgaDCofDocLhsBoNBkrJsuHhsNBkMlH/F/wwGqPxwHB8f3+v/H6/gm6Pb28Kdq1eowqFArb8wWDg+MrpjvAdj8f29fV1PYVWXIrFou1tbwV6PQ2YL+vc2Zm/PgXv3/B9BYZhMBqN1A/y3C4F7xJx8Jv3A+XTfX5+qtwulwoEAsZGo5H5/X6z3W7/Pd+J6XT63xY3N+pXCfk8T7cYBZx/7AqOlPL5rG3S+0Y3PGW/xPJWbHEbsxyOhJv0h1eGGZfCvGt+jOuqWrH2nH8ZMFBENz/M8xwT9WHj0s1qBGhm5pP0hzHg2dMPnbhHEFGU3VLOkZzOvCrXbq7uWe0qN0Fs7hEUjcr8b0/aTLN7Uo3dHnlS3dIW3SXYIEjdHYYEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZX7f/oMyJPfAcUVw9QAAAAASUVORK5CYII="
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Activity Hub Projects</title>
</head>
<body style="font-family: 'Segoe UI', Arial, sans-serif; color: #333; margin: 0; padding: 0; background-color: #f5f5f5;">

<table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 24px;">
<tr>
<td bgcolor="#004C91" style="background-color:#004C91; padding: 24px 30px;">
    <table cellpadding="0" cellspacing="0" border="0">
    <tr>
    <td style="padding-right: 20px; vertical-align: middle; font-size: 32px; font-weight: bold; color: #0071CE; width: 60px; text-align: center; background: white; border-radius: 4px; height: 48px; line-height: 48px;">W</td>
    <td style="vertical-align: middle;">
        <div style="color: white; font-size: 26px; font-weight: 700;">Projects</div>
        <div style="color: #cccccc; font-size: 13px; margin-top: 2px;">by Activity Hub</div>
    </td>
    </tr></table>
</td>
</tr>
</table>

<!-- GO TO PROJECTS BUTTON -->
<table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 24px;">
<tr>
<td style="text-align: center; padding: 20px;">
    <a href="http://weus42608431466:8088/activity-hub/projects" style="display: inline-block; background: #0071CE; color: white; text-decoration: none; font-weight: 600; font-size: 14px; padding: 12px 24px; border-radius: 4px; font-family: Arial, sans-serif;">
        → Go to Projects Dashboard
    </a>
</td>
</tr>
</table>
    
    <!-- CONTENT AREA -->
    <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 24px; max-width: 1000px; margin-left: auto; margin-right: auto;">
    <tr>
    <td bgcolor="#ffffff" style="background-color:#ffffff; padding: 24px 30px;">
        <p style="margin: 0 0 8px 0; font-size: 16px; font-weight: 500; color: #333;">Hi {owner_name},</p>
        <p style="margin: 0 0 24px 0; font-size: 14px; color: #666; line-height: 1.6;">{action_text}</p>
        
        <!-- Projects Count Badge -->
        <div style="background-color: #f0f7ff; border-left: 4px solid #0071CE; padding: 16px 20px; margin-bottom: 24px; border-radius: 4px;">
            <div style="font-size: 11px; font-weight: 700; color: #0071CE; text-transform: uppercase; letter-spacing: 0.5px;">Project Summary</div>
            <div style="font-size: 24px; font-weight: 700; color: #0071CE; margin-top: 8px;">{len(projects)} Project{'s' if len(projects) != 1 else ''}</div>
        </div>
        
        <!-- Projects Table -->
        <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse: collapse; margin-bottom: 24px; border: 1px solid #e0e0e0;">
            <thead>
            <tr style="background-color: #f5f5f5;">
                <th style="padding: 12px; text-align: left; font-weight: 700; font-size: 12px; color: #333; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #0071CE; border-right: 1px solid #e0e0e0; width: 35%;">Project Title</th>
                <th style="padding: 12px; text-align: left; font-weight: 700; font-size: 12px; color: #333; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #0071CE; border-right: 1px solid #e0e0e0; width: 12%;">Health</th>
                <th style="padding: 12px; text-align: left; font-weight: 700; font-size: 12px; color: #333; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #0071CE; border-right: 1px solid #e0e0e0; width: 18%;">Business Area</th>
                <th style="padding: 12px; text-align: left; font-weight: 700; font-size: 12px; color: #333; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #0071CE; border-right: 1px solid #e0e0e0; width: 12%;">Update Date</th>
                <th style="padding: 12px; text-align: left; font-weight: 700; font-size: 12px; color: #333; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #0071CE; width: 23%;">Latest Update</th>
            </tr>
            </thead>
            <tbody>
                {projects_table}
            </tbody>
        </table>
    </td>
    </tr>
    </table>
    
    <!-- FOOTER -->
    <table width="100%" cellpadding="0" cellspacing="0" style="margin-top: 24px; max-width: 1000px; margin-left: auto; margin-right: auto;">
    <tr>
    <td bgcolor="#f5f5f5" style="background-color: #f5f5f5; padding: 16px 30px; border-top: 1px solid #e0e0e0; text-align: center;">
        <p style="margin: 0; font-size: 12px; color: #999;">
            This is an automated email from Activity Hub. Project titles are clickable links to view details.
        </p>
        <p style="margin: 8px 0 0 0; font-size: 12px; color: #999;">
            Generated: {datetime.now().strftime('%B %d, %Y')}
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


def send_monday_email_test():
    """Send Monday email test (all projects for one owner)"""
    logger.info("\n" + "=" * 80)
    logger.info("MONDAY EMAIL - ALL ACTIVE PROJECTS")
    logger.info("=" * 80)
    
    owner_name = 'Kendall Rush'
    projects = query_owner_projects(owner_name, include_only_not_updated=False)
    
    logger.info(f"Found {len(projects)} projects for {owner_name}")
    
    html_body = generate_email_html('monday', owner_name, projects, is_leadership=False)
    subject = f"Activity Hub Projects - Monday Update for {owner_name}"
    
    recipient = 'kendall.rush@walmart.com'
    logger.info(f"Sending to: {recipient}")
    
    if send_smtp_email(recipient, subject, html_body):
        logger.info("✓ Monday email sent successfully!")
        return True
    return False


def send_wednesday_email_test():
    """Send Wednesday email test (not updated projects for one owner)"""
    logger.info("\n" + "=" * 80)
    logger.info("WEDNESDAY EMAIL - NOT UPDATED PROJECTS")
    logger.info("=" * 80)
    
    owner_name = 'Kendall Rush'
    projects = query_owner_projects(owner_name, include_only_not_updated=True)
    
    logger.info(f"Found {len(projects)} not-updated projects for {owner_name}")
    
    if not projects:
        logger.info("✓ No not-updated projects, so no email would be sent")
        return True
    
    html_body = generate_email_html('wednesday', owner_name, projects, is_leadership=False)
    subject = f"Activity Hub Projects - Wednesday Update Needed for {owner_name}"
    
    recipient = 'kendall.rush@walmart.com'
    logger.info(f"Sending to: {recipient}")
    
    if send_smtp_email(recipient, subject, html_body):
        logger.info("✓ Wednesday email sent successfully!")
        return True
    return False


def get_all_direct_reports_projects(manager_name: str) -> list:
    """Get all projects for manager and all downstream direct reports (recursive)"""
    
    def get_team_projects_recursive(person_name: str) -> list:
        """Recursively get all projects from person and all their direct reports"""
        all_projects = []
        
        # Get this person's projects
        person_projects = query_owner_projects(person_name, include_only_not_updated=False)
        for p in person_projects:
            p['project_owner'] = person_name
            all_projects.append(p)
        
        # Get their direct reports' projects recursively
        direct_reports = LEADERSHIP_HIERARCHY.get(person_name, {}).get('direct_reports', [])
        for report in direct_reports:
            report_projects = get_team_projects_recursive(report)
            all_projects.extend(report_projects)
        
        return all_projects
    
    # Start recursion from the manager
    all_projects = get_team_projects_recursive(manager_name)
    
    # Sort by owner then by title
    all_projects.sort(key=lambda x: (x['project_owner'], x['title']))
    
    return all_projects


def generate_leadership_email_html(manager_name: str, projects: list) -> str:
    """Generate leadership email with team projects organized by owner"""
    
    # Group projects by owner
    projects_by_owner = {}
    for p in projects:
        owner = p['project_owner']
        if owner not in projects_by_owner:
            projects_by_owner[owner] = []
        projects_by_owner[owner].append(p)
    
    # Build projects table with owner sections
    projects_html = ""
    
    for owner in sorted(projects_by_owner.keys()):
        owner_projects = projects_by_owner[owner]
        projects_html += f"""
        <tr>
            <td colspan="5" style="padding: 16px 12px; background-color: #e8f4f8; font-weight: 600; color: #0071CE; border-top: 2px solid #0071CE;">
                {owner} ({len(owner_projects)} project{'s' if len(owner_projects) != 1 else ''})
            </td>
        </tr>
        """
        
        for p in owner_projects:
            # Map health status to colors
            health_value = p['health'].lower() if p['health'] else 'unknown'
            if 'on track' in health_value:
                health_color = '#107C10'  # Green
            elif 'at risk' in health_value:
                health_color = '#F7630C'  # Orange
            elif 'off track' in health_value or 'paused' in health_value:
                health_color = '#DC3545'  # Red
            else:
                health_color = '#666666'  # Gray for unknown/other
            
            # Create clickable project title based on source
            if 'Intake' in p['project_source']:
                # Intake Hub projects link to hoops.wal-mart.com
                project_url = f"https://hoops.wal-mart.com/intake-hub/projects/{p['project_id']}"
            else:
                # Projects dashboard - link to Activity Hub projects page
                project_url = f"http://weus42608431466:8088/activity-hub/projects?id={p['project_id']}"
            
            project_title_html = f'<a href="{project_url}" style="color: #0071CE; text-decoration: none; font-weight: 500;" target="_blank">{p["title"]}</a>'
            
            projects_html += f"""
            <tr style="border-bottom: 1px solid #e0e0e0;">
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; font-weight: 500;">{project_title_html}</td>
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; font-weight: 600; color: {health_color};">{p['health']}</td>
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; color: #666; font-size: 13px;">{p['business_area']}</td>
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; color: #666; font-size: 13px;">{p['update_date']}</td>
                <td style="padding: 12px; font-size: 13px; line-height: 1.4; max-width: 300px; word-wrap: break-word;">{p['project_update']}</td>
            </tr>
            """
    
    if not projects_html:
        projects_html = """
        <tr>
            <td colspan="5" style="text-align: center; padding: 24px; color: #999; font-style: italic;">
                No projects to display
            </td>
        </tr>
        """
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Activity Hub Projects - Leadership Summary</title>
</head>
<body style="font-family: 'Segoe UI', Arial, sans-serif; color: #333; margin: 0; padding: 0; background-color: #f5f5f5;">

<table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 24px;">
<tr>
<td bgcolor="#004C91" style="background-color:#004C91; padding: 24px 30px;">
    <table cellpadding="0" cellspacing="0" border="0">
    <tr>
    <td style="padding-right: 20px; vertical-align: middle; font-size: 32px; font-weight: bold; color: #0071CE; width: 60px; text-align: center; background: white; border-radius: 4px; height: 48px; line-height: 48px;">W</td>
    <td style="vertical-align: middle;">
        <div style="color: white; font-size: 26px; font-weight: 700;">Projects</div>
        <div style="color: #cccccc; font-size: 13px; margin-top: 2px;">by Activity Hub</div>
    </td>
    </tr></table>
</td>
</tr>
</table>

<!-- GO TO PROJECTS BUTTON -->
<table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 24px;">
<tr>
<td style="text-align: center; padding: 20px;">
    <a href="http://weus42608431466:8088/activity-hub/projects" style="display: inline-block; background: #0071CE; color: white; text-decoration: none; font-weight: 600; font-size: 14px; padding: 12px 24px; border-radius: 4px; font-family: Arial, sans-serif;">
        → Go to Projects Dashboard
    </a>
</td>
</tr>
</table>

    <!-- CONTENT AREA -->
    <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 24px; max-width: 1000px; margin-left: auto; margin-right: auto;">
    <tr>
    <td bgcolor="#ffffff" style="background-color:#ffffff; padding: 24px 30px;">
        <p style="margin: 0 0 8px 0; font-size: 16px; font-weight: 500; color: #333;">Hi {manager_name},</p>
        <p style="margin: 0 0 24px 0; font-size: 14px; color: #666; line-height: 1.6;">Below is a summary of all projects for your team, including your direct reports. This will help you stay informed on team project status and identify any areas needing attention.</p>
        
        <!-- Projects Count Badge -->
        <div style="background-color: #f0f7ff; border-left: 4px solid #0071CE; padding: 16px 20px; margin-bottom: 24px; border-radius: 4px;">
            <div style="font-size: 11px; font-weight: 700; color: #0071CE; text-transform: uppercase; letter-spacing: 0.5px;">Team Project Summary</div>
            <div style="font-size: 24px; font-weight: 700; color: #0071CE; margin-top: 8px;">{len(projects)} Total Project{'s' if len(projects) != 1 else ''}</div>
        </div>
        
        <!-- Projects Table -->
        <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse: collapse; margin-bottom: 24px; border: 1px solid #e0e0e0;">
            <thead>
            <tr style="background-color: #f5f5f5;">
                <th style="padding: 12px; text-align: left; font-weight: 700; font-size: 12px; color: #333; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #0071CE; border-right: 1px solid #e0e0e0; width: 35%;">Project Title</th>
                <th style="padding: 12px; text-align: left; font-weight: 700; font-size: 12px; color: #333; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #0071CE; border-right: 1px solid #e0e0e0; width: 12%;">Health</th>
                <th style="padding: 12px; text-align: left; font-weight: 700; font-size: 12px; color: #333; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #0071CE; border-right: 1px solid #e0e0e0; width: 18%;">Business Area</th>
                <th style="padding: 12px; text-align: left; font-weight: 700; font-size: 12px; color: #333; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #0071CE; border-right: 1px solid #e0e0e0; width: 12%;">Update Date</th>
                <th style="padding: 12px; text-align: left; font-weight: 700; font-size: 12px; color: #333; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #0071CE; width: 23%;">Latest Update</th>
            </tr>
            </thead>
            <tbody>
                {projects_html}
            </tbody>
        </table>
    </td>
    </tr>
    </table>
    
    <!-- FOOTER -->
    <table width="100%" cellpadding="0" cellspacing="0" style="margin-top: 24px; max-width: 1000px; margin-left: auto; margin-right: auto;">
    <tr>
    <td bgcolor="#f5f5f5" style="background-color: #f5f5f5; padding: 16px 30px; border-top: 1px solid #e0e0e0; text-align: center;">
        <p style="margin: 0; font-size: 12px; color: #999;">
            This is an automated leadership summary from Activity Hub. Project titles are clickable links to view details.
        </p>
        <p style="margin: 8px 0 0 0; font-size: 12px; color: #999;">
            Generated: {datetime.now().strftime('%B %d, %Y')}
        </p>
    </td>
    </tr>
    </table>

</body>
</html>
"""
    
    return html


def send_leadership_email_test(manager_name: str):
    """Send leadership email test - all test emails go to kendall.rush@walmart.com"""
    logger.info(f"\nSending leadership email for {manager_name}...")
    logger.info("-" * 80)
    
    # Special handling for Kristine - get all 28 projects from Intake Hub directly
    if manager_name == 'Kristine Torres':
        kristine_projects = query_kristine_all_projects()
        if not kristine_projects:
            logger.warning("No projects found for Kristine Torres")
            return False
        
        logger.info(f"Found {len(kristine_projects)} projects for Kristine Torres")
        
        # Format projects for leadership email - group by director
        projects_by_director = {}
        for p in kristine_projects:
            director = p['director']
            if director not in projects_by_director:
                projects_by_director[director] = []
            # Add project_owner for grouping in email
            p['project_owner'] = director
            projects_by_director[director].append(p)
        
        # Flatten back to list for email generation
        formatted_projects = []
        for director in sorted(projects_by_director.keys()):
            formatted_projects.extend(projects_by_director[director])
        
        html_body = generate_leadership_email_html(manager_name, formatted_projects)
    else:
        # Regular hierarchical approach for other managers
        projects = get_all_direct_reports_projects(manager_name)
        logger.info(f"Found {len(projects)} total team projects for {manager_name}")
        
        html_body = generate_leadership_email_html(manager_name, projects)
    
    subject = f"Activity Hub Projects - Team Summary for {manager_name}"
    
    # For testing, send all leadership emails to Kendall
    recipient = 'kendall.rush@walmart.com'
    logger.info(f"Sending to: {recipient}")
    
    if send_smtp_email(recipient, subject, html_body):
        logger.info(f"✓ Leadership email sent successfully for {manager_name}!")
        return True
    return False


def query_kristine_all_projects() -> list:
    """Query all 28 projects where Kristine Torres is director or sr_director from Intake Hub"""
    
    client = bigquery.Client(project=BQ_PROJECT)
    
    # Query Intake Hub data for all projects with Kristine as director or sr_director
    sql = """
    SELECT 
        Intake_Card_Nbr as project_id,
        Project_Title as title,
        Owner as owner,
        Business_Owner_Area as business_area,
        Project_Update as project_update,
        Project_Update_Date as update_date,
        Health_Update as health,
        Status as status,
        PROJECT_DIRECTOR as director,
        PROJECT_DIRECTOR_ID as director_id,
        'Intake' as project_source
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
    WHERE PROJECT_SR_DIRECTOR = 'Kristine Torres'
       OR PROJECT_DIRECTOR = 'Kristine Torres'
    ORDER BY PROJECT_DIRECTOR, Project_Title
    """
    
    results = list(client.query(sql).result())
    projects = []
    for row in results:
        projects.append({
            'project_id': str(row.project_id),
            'title': row.title or 'N/A',
            'owner': row.owner or 'N/A',
            'health': row.health or 'Unknown',
            'status': row.status or 'Unknown',
            'project_update': row.project_update if row.project_update and row.project_update.strip() else 'No update provided',
            'update_date': row.update_date.strftime('%b %d, %Y') if row.update_date else 'Not updated',
            'business_area': row.business_area or 'N/A',
            'project_source': row.project_source,
            'director': row.director or 'No Director Assigned',
            'url': f"https://hoops.wal-mart.com/intake-hub/projects/{row.project_id}"
        })
    
    return projects


def generate_kristine_comprehensive_email(projects: list) -> str:
    """Generate comprehensive email for Kristine showing all 28 projects grouped by director"""
    
    # Group projects by director
    projects_by_director = {}
    for p in projects:
        director = p['director']
        if director not in projects_by_director:
            projects_by_director[director] = []
        projects_by_director[director].append(p)
    
    # Build projects table with director sections
    projects_html = ""
    
    # Spark logo as base64
    spark_logo_base64 = "iVBORw0KGgoAAAANSUhEUgAAAHgAAAB4CAYAAAA5ZDbSAAAACXBIWXMAAA7DAAAOwwHHb6thAAADYElEQVR4nO2dMU7kQBCFXXCBgMSBA5wgwwGYkZjhmBnGhBvESNwgJGbGS0BAVOQwMIGsADeQmBFgBGZGYkbg6VJ3bXudu2M7M/PVV/O/F3i1M+6e/k9P/1v+MTAZQgh4WRCWKlKqKlKqKlKqKlKqKlKqKlKqKlKqKlKqKlKqKlKqKlKqKlKqKlKqKlKqKvJfI8Symj5VVV0uFgvzfr/N9/t9ur6+vpqZmW1ubtzOzs7ZbrezDIfDi9/vZ6enp1fX13fN5eXlEZqZfb1ex+Px2Ox2O3t9fb27ubmxs7MzGwwGdn19ber1ul1dXVk4HJrnx2Nx+Pj4aJPJRHU6HbtYLMxmszGdTseMMXY2m6nJZKLKkiSJ6vV60eFwUCXJN2VZqMFgYJRlYXq9nsKBNpvN1GazMXXhw+FgfD6fuju7U2qCmUxGXV5eqslkotRt6XQ6RP0fFGWhLi8v1dPTkyrJRFGUKk+S6PV6DgYDg1wt6vfhcKB8Pp9yOp3K6/UqxOdzPJQqyFUlmSjLQrlcLjObzSqn06lcLpc6HA5qvV4rr9er+v2+6vV6anNzWzkcDhV/PuQ5oQA9Ho/yeDyqXq8rj8ej/H6/Ug6HQ/lcLpXJZNT5+blKpVLK5XKp5XKpPB6PCgaDCofDocLhsBoNBkrJsuHhsNBkMlH/F/wwGqPxwHB8f3+v/H6/gm6Pb28Kdq1eowqFArb8wWDg+MrpjvAdj8f29fV1PYVWXIrFou1tbwV6PQ2YL+vc2Zm/PgXv3/B9BYZhMBqN1A/y3C4F7xJx8Jv3A+XTfX5+qtwulwoEAsZGo5H5/X6z3W7/Pd+J6XT63xY3N+pXCfk8T7cYBZx/7AqOlPL5rG3S+0Y3PGW/xPJWbHEbsxyOhJv0h1eGGZfCvGt+jOuqWrH2nH8ZMFBENz/M8xwT9WHj0s1qBGhm5pP0hzHg2dMPnbhHEFGU3VLOkZzOvCrXbq7uWe0qN0Fs7hEUjcr8b0/aTLN7Uo3dHnlS3dIW3SXYIEjdHYYEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZX7f/oMyJPfAcUVw9QAAAAASUVORK5CYII="
    
    for director in sorted(projects_by_director.keys()):
        director_projects = projects_by_director[director]
        projects_html += f"""
        <tr>
            <td colspan="5" style="padding: 14px 12px; background-color: #e8f4f8; font-weight: 700; color: #0071CE; border-top: 2px solid #0071CE; border-bottom: 1px solid #d0e8f0;">
                {director} ({len(director_projects)} project{'s' if len(director_projects) != 1 else ''})
            </td>
        </tr>
        """
        
        for p in director_projects:
            # Map health status to colors
            health_value = p['health'].lower() if p['health'] else 'unknown'
            if 'on track' in health_value:
                health_color = '#107C10'  # Green
            elif 'at risk' in health_value:
                health_color = '#F7630C'  # Orange
            elif 'off track' in health_value or 'paused' in health_value:
                health_color = '#DC3545'  # Red
            else:
                health_color = '#666666'  # Gray for unknown
            
            project_title_html = f'<a href="{p["url"]}" style="color: #0071CE; text-decoration: none; font-weight: 500;" target="_blank">{p["title"]}</a>'
            
            projects_html += f"""
            <tr style="border-bottom: 1px solid #e0e0e0;">
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; font-weight: 500;">{project_title_html}</td>
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; font-weight: 600; color: {health_color};">{p['health']}</td>
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; color: #666; font-size: 13px;">{p['business_area']}</td>
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; color: #666; font-size: 13px;">{p['update_date']}</td>
                <td style="padding: 12px; font-size: 13px; line-height: 1.4; max-width: 300px; word-wrap: break-word;">{p['project_update']}</td>
            </tr>
            """
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Activity Hub Projects - Kristine Torres Leadership Portfolio</title>
</head>
<body style="font-family: 'Segoe UI', Arial, sans-serif; color: #333; margin: 0; padding: 0; background-color: #f5f5f5;">

<table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 24px;">
<tr>
<td bgcolor="#004C91" style="background-color:#004C91; padding: 24px 30px;">
    <table cellpadding="0" cellspacing="0" border="0">
    <tr>
    <td style="padding-right: 15px; vertical-align: middle;">
        <img src="data:image/png;base64,{spark_logo_base64}" width="48" height="48" alt="Spark" style="display:block;"/>
    </td>
    <td style="vertical-align: middle;">
        <div style="color: white; font-size: 26px; font-weight: 700;">Projects</div>
        <div style="color: #cccccc; font-size: 13px; margin-top: 2px;">by Activity Hub</div>
    </td>
    </tr></table>
</td>
</tr>
</table>

<!-- GO TO PROJECTS BUTTON -->
<table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 24px;">
<tr>
<td style="text-align: center; padding: 20px;">
    <a href="http://weus42608431466:8088/activity-hub/projects" style="display: inline-block; background: #0071CE; color: white; text-decoration: none; font-weight: 600; font-size: 14px; padding: 12px 24px; border-radius: 4px; font-family: Arial, sans-serif;">
        → Go to Projects Dashboard
    </a>
</td>
</tr>
</table>

    <!-- CONTENT AREA -->
    <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 24px; max-width: 1000px; margin-left: auto; margin-right: auto;">
    <tr>
    <td bgcolor="#ffffff" style="background-color:#ffffff; padding: 24px 30px;">
        <p style="margin: 0 0 8px 0; font-size: 16px; font-weight: 500; color: #333;">Hi Kristine,</p>
        <p style="margin: 0 0 24px 0; font-size: 14px; color: #666; line-height: 1.6;">Below is a comprehensive summary of all projects you oversee as Senior Director, organized by Project Director. This includes all initiatives under your leadership chain.</p>
        
        <!-- Projects Count Badge -->
        <div style="background-color: #f0f7ff; border-left: 4px solid #0071CE; padding: 16px 20px; margin-bottom: 24px; border-radius: 4px;">
            <div style="font-size: 11px; font-weight: 700; color: #0071CE; text-transform: uppercase; letter-spacing: 0.5px;">Leadership Portfolio</div>
            <div style="font-size: 24px; font-weight: 700; color: #0071CE; margin-top: 8px;">{len(projects)} Total Projects</div>
        </div>
        
        <!-- Projects Table -->
        <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse: collapse; margin-bottom: 24px; border: 1px solid #e0e0e0;">
            <thead>
            <tr style="background-color: #f5f5f5;">
                <th style="padding: 12px; text-align: left; font-weight: 700; font-size: 12px; color: #333; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #0071CE; border-right: 1px solid #e0e0e0; width: 35%;">Project Title</th>
                <th style="padding: 12px; text-align: left; font-weight: 700; font-size: 12px; color: #333; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #0071CE; border-right: 1px solid #e0e0e0; width: 12%;">Health</th>
                <th style="padding: 12px; text-align: left; font-weight: 700; font-size: 12px; color: #333; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #0071CE; border-right: 1px solid #e0e0e0; width: 18%;">Business Area</th>
                <th style="padding: 12px; text-align: left; font-weight: 700; font-size: 12px; color: #333; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #0071CE; border-right: 1px solid #e0e0e0; width: 12%;">Update Date</th>
                <th style="padding: 12px; text-align: left; font-weight: 700; font-size: 12px; color: #333; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #0071CE; width: 23%;">Latest Update</th>
            </tr>
            </thead>
            <tbody>
                {projects_html}
            </tbody>
        </table>
    </td>
    </tr>
    </table>
    
    <!-- FOOTER -->
    <table width="100%" cellpadding="0" cellspacing="0" style="margin-top: 24px; max-width: 1000px; margin-left: auto; margin-right: auto;">
    <tr>
    <td bgcolor="#f5f5f5" style="background-color: #f5f5f5; padding: 16px 30px; border-top: 1px solid #e0e0e0; text-align: center;">
        <p style="margin: 0; font-size: 12px; color: #999;">
            This is an automated leadership summary from Activity Hub. Project titles are clickable links to view details in Intake Hub.
        </p>
        <p style="margin: 8px 0 0 0; font-size: 12px; color: #999;">
            Generated: {datetime.now().strftime('%B %d, %Y')}
        </p>
    </td>
    </tr>
    </table>

</body>
</html>
"""
    
    return html


def send_kristine_comprehensive_email_test():
    """Send Kristine a comprehensive email with all 28 projects grouped by director"""
    
    logger.info("\n" + "=" * 80)
    logger.info("KRISTINE TORRES - COMPREHENSIVE LEADERSHIP EMAIL (28 Projects)")
    logger.info("=" * 80)
    
    projects = query_kristine_all_projects()
    
    if not projects:
        logger.warning("No projects found for Kristine Torres")
        return False
    
    logger.info(f"Found {len(projects)} projects for Kristine Torres")
    
    html_body = generate_kristine_comprehensive_email(projects)
    subject = "Activity Hub Projects - Complete Leadership Portfolio for Kristine Torres"
    
    # For testing, send to Kendall
    recipient = 'kendall.rush@walmart.com'
    logger.info(f"Sending comprehensive Kristine email to: {recipient}")
    
    if send_smtp_email(recipient, subject, html_body):
        logger.info(f"✓ Kristine comprehensive email sent successfully!")
        return True
    return False


def main():
    logger.info("=" * 80)
    logger.info("ACTIVITY HUB PROJECTS - EMAIL SYSTEM TEST")
    logger.info("=" * 80)
    logger.info("SENDING TEST EMAILS TO KENDALL RUSH ONLY")
    logger.info("=" * 80)
    
    # Test Monday email
    send_monday_email_test()
    
    # Test Wednesday email
    send_wednesday_email_test()
    
    # Test leadership emails to Kendall
    logger.info("\n" + "=" * 80)
    logger.info("LEADERSHIP EMAILS - TESTING")
    logger.info("=" * 80)
    
    # Send Kendall's own leadership email (her team)
    send_leadership_email_test('Kendall Rush')
    
    # Send Matt's leadership email to Kendall (to see what Matt would get)
    send_leadership_email_test('Matt Farnworth')
    
    # Send Kristine's leadership email to Kendall (to see what Kristine would get)
    send_leadership_email_test('Kristine Torres')
    
    # Send Kristine's comprehensive email (all 28 projects from Intake Hub)
    send_kristine_comprehensive_email_test()
    
    logger.info("\n" + "=" * 80)
    logger.info("✓ ALL TEST EMAILS SENT")
    logger.info("=" * 80)
    
    logger.info("\n" + "=" * 80)
    logger.info("✓ ALL TEST EMAILS SENT")
    logger.info("=" * 80)


if __name__ == '__main__':
    main()
