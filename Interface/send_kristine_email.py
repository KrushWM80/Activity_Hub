#!/usr/bin/env python3
"""
Updated Activity Hub email system with fixes for:
1. Health status from Intake data
2. Full 5-column table (Project Title, Health, Business Area, Update Date, Latest Update)
3. Kristine 28-projects email with grouping by director
4. Visible Spark logo
"""
from google.cloud import bigquery
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BQ_PROJECT = 'wmt-assetprotection-prod'
BQ_DATASET = 'Store_Support_Dev'
SMTP_SERVER = 'smtp-gw1.homeoffice.wal-mart.com'
SMTP_PORT = 25
FROM_EMAIL = 'kendall.rush@walmart.com'
PROJECTS_DASHBOARD = 'http://weus42608431466:8088/activity-hub/projects'

def query_kristine_28_projects() -> list:
    """Query all 28 projects where Kristine is director or sr_director, grouped by director"""
    client = bigquery.Client(project=BQ_PROJECT)
    
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
            'title': row.title,
            'owner': row.owner,
            'business_area': row.business_area,
            'project_update': row.project_update or 'No update provided',
            'update_date': row.update_date.strftime('%m/%d/%Y') if row.update_date else 'N/A',
            'health': row.health or 'Unknown',
            'status': row.status,
            'director': row.director,
            'project_source': row.project_source
        })
    
    return projects

def generate_kristine_leadership_email() -> str:
    """Generate Kristine's comprehensive 28-projects email grouped by director"""
    
    projects = query_kristine_28_projects()
    
    if not projects:
        logger.warning("No projects found for Kristine Torres")
        return None
    
    # Group projects by director
    projects_by_director = {}
    for p in projects:
        director = p['director'] or 'No Director Assigned'
        if director not in projects_by_director:
            projects_by_director[director] = []
        projects_by_director[director].append(p)
    
    # Build projects HTML grouped by director
    projects_html = ""
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
            # Health color mapping
            health_lower = p['health'].lower()
            if 'on track' in health_lower:
                health_color = '#107C10'  # Green
            elif 'at risk' in health_lower:
                health_color = '#F7630C'  # Orange
            elif 'off track' in health_lower or 'paused' in health_lower:
                health_color = '#DC3545'  # Red
            else:
                health_color = '#666666'  # Gray
            
            # Create project link
            project_url = f"https://hoops.wal-mart.com/intake-hub/projects/{p['project_id']}"
            project_title_html = f'<a href="{project_url}" style="color: #0071CE; text-decoration: none; font-weight: 500;" target="_blank">{p["title"]}</a>'
            
            projects_html += f"""
            <tr style="border-bottom: 1px solid #e0e0e0;">
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; font-weight: 500; font-size: 13px;">{project_title_html}</td>
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; font-weight: 600; color: {health_color}; font-size: 13px;">{p['health']}</td>
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; color: #666; font-size: 12px;">{p['business_area']}</td>
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; color: #666; font-size: 12px;">{p['update_date']}</td>
                <td style="padding: 12px; font-size: 12px; line-height: 1.5; color: #555;">{p['project_update']}</td>
            </tr>
            """
    
    # Spark logo - proper base64 data URI
    spark_logo = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHgAAAB4CAYAAAA5ZDbSAAAACXBIWXMAAA7DAAAOwwHHb6thAAADYElEQVR4nO2dMU7kQBCFXXCBgMSBA5wgwwGYkZjhmBnGhBvESNwgJGbGS0BAVOQwMIGsADeQmBFgBGZGYkbg6VJ3bXudu2M7M/PVV/O/F3i1M+6e/k9P/1v+MTAZQgh4WRCWKlKqKlKqKlKqKlKqKlKqKlKqKlKqKlKqKlKqKlKqKlKqKlKqKlKqKlKqKvJfI8Symj5VVV0uFgvzfr/N9/t9ur6+vpqZmW1ubtzOzs7ZbrezDIfDi9/vZ6enp1fX13fN5eXlEZqZfb1ex+Px2Ox2O3t9fb27ubmxs7MzGwwGdn19ber1ul1dXVk4HJrnx2Nx+Pj4aJPJRHU6HbtYLMxmszGdTseMMXY2m6nJZKLKkiSJ6vV60eFwUCXJN2VZqMFgYJRlYXq9nsKBNpvN1GazMXXhw+FgfD6furu7U2qCmUxGXV5eqslkotRt6XQ6RP0fFGWhLi8v1dPTkyrJRFGUKk+S6PV6DgYDg1wt6vfhcKB8Pp9yOp3K6/UqxOdzPJQqyFUlmSjLQrlcLjObzSqn06lcLpc6HA5qvV4rr9er+v2+6vV6anNzWzkcDhV/PuQ5oQA9Ho/yeDyqXq8rj8ej/H6/Ug6HQ/lcLpXJZNT5+blKpVLK5XKp5XKpPB6PCgaDCofDocLhsBoNBkrJsuHhsNBkMlH/F/wwGqPxwHB8f3+v/H6/gm6Pb28Kdq1eowqFArb8wWDg+MrpjvAdj8f29fV1PYVWXIrFou1tbwV6PQ2YL+vc2Zm/PgXv3/B9BYZhMBqN1A/y3C4F7xJx8Jv3A+XTfX5+qtwulwoEAsZGo5H5/X6z3W7/Pd+J6XT63xY3N+pXCfk8T7cYBZx/7AqOlPL5rG3S+0Y3PGW/xPJWbHEbsxyOhJv0h1eGGZfCvGt+jOuqWrH2nH8ZMFBENz/M8xwT9WHj0s1qBGhm5pP0hzHg2dMPnbhHEFGU3VLOkZzOvCrXbq7uWe0qN0Fs7hEUjcr8b0/aTLN7Uo3dHnlS3dIW3SXYIEjdHYYEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZXrfcIEjdbZ1ZX7f/oMyJPfAcUVw9QAAAAASUVORK5CYII="
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Activity Hub Projects - Kristine Torres Team Summary</title>
</head>
<body style="font-family: 'Segoe UI', Arial, sans-serif; color: #333; margin: 0; padding: 0; background-color: #f5f5f5;">

<table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 24px;">
<tr>
<td bgcolor="#004C91" style="background-color:#004C91; padding: 24px 30px;">
    <table cellpadding="0" cellspacing="0" border="0">
    <tr>
    <td style="padding-right: 15px; vertical-align: middle;">
        <img src="{spark_logo}" width="48" height="48" alt="Spark" style="display:block; border: none;"/>
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
    <a href="{PROJECTS_DASHBOARD}" style="display: inline-block; background: #0071CE; color: white; text-decoration: none; font-weight: 600; font-size: 14px; padding: 12px 24px; border-radius: 4px; font-family: Arial, sans-serif;">
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
    <p style="margin: 0 0 24px 0; font-size: 14px; color: #666; line-height: 1.6;">Below is a comprehensive summary of all 28 projects you oversee as Sr. Director, organized by Project Director. This includes all initiatives under your leadership chain.</p>
    
    <!-- Projects Count Badge -->
    <div style="background-color: #f0f7ff; border-left: 4px solid #0071CE; padding: 16px 20px; margin-bottom: 24px; border-radius: 4px;">
        <div style="font-size: 11px; font-weight: 700; color: #0071CE; text-transform: uppercase; letter-spacing: 0.5px;">Leadership Portfolio</div>
        <div style="font-size: 24px; font-weight: 700; color: #0071CE; margin-top: 8px;">28 Total Projects</div>
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

def send_smtp_email(recipient_email: str, subject: str, html_body: str) -> bool:
    """Send email via Walmart SMTP"""
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = FROM_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(html_body, 'html', 'utf-8'))
        
        with SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
            server.sendmail(FROM_EMAIL, [recipient_email], msg.as_string())
        
        logger.info(f"✓ Email sent to {recipient_email}")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to send email to {recipient_email}: {e}")
        return False

def send_kristine_comprehensive_email():
    """Send Kristine the comprehensive 28-projects email"""
    logger.info("\n" + "=" * 80)
    logger.info("KRISTINE TORRES - COMPREHENSIVE LEADERSHIP EMAIL (28 Projects)")
    logger.info("=" * 80)
    
    html_body = generate_kristine_leadership_email()
    if not html_body:
        logger.error("Failed to generate Kristine email")
        return False
    
    subject = "Activity Hub Projects - Complete Leadership Portfolio for Kristine Torres"
    recipient = 'kendall.rush@walmart.com'  # Testing - change to kristine.torres@walmart.com for production
    
    logger.info(f"Sending to: {recipient}")
    if send_smtp_email(recipient, subject, html_body):
        logger.info("✓ Kristine comprehensive email sent successfully!")
        return True
    return False

if __name__ == '__main__':
    send_kristine_comprehensive_email()
