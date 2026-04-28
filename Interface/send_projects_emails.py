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
import base64
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
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

# Logging - MUST BE BEFORE SPARK LOGO SETUP
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Spark Logo - Read dynamically at runtime (matching TDA Insights approach)
# Try multiple paths to find the logo
def _get_spark_logo_path():
    """Find Spark logo in multiple possible locations"""
    paths_to_try = [
        Path(__file__).parent / "Spark_Blank.png",  # Same directory as this script
        Path(__file__).parent.parent / "Interface" / "Spark_Blank.png",  # Up to Activity_Hub, then Interface
        Path(__file__).parent.parent.parent / "Interface" / "Spark_Blank.png",  # Go up further
        Path("C:/Users/krush/OneDrive - Walmart Inc/Documents/VSCode/Activity_Hub/Interface/Spark_Blank.png"),  # Absolute path
    ]
    
    for path in paths_to_try:
        if path.exists():
            logger.info(f"✓ Found Spark logo at: {path}")
            return path
    
    # If nothing found, log all paths checked
    logger.warning(f"Spark logo not found. Checked paths:")
    for path in paths_to_try:
        logger.warning(f"  - {path}")
    return None

SPARK_LOGO_PATH = _get_spark_logo_path()

# Set Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
    os.environ.get('APPDATA', ''), 'gcloud', 'application_default_credentials.json'
)


def get_spark_logo_base64() -> str:
    """Get Spark logo as base64 string, reading dynamically from PNG file like TDA Insights"""
    try:
        if SPARK_LOGO_PATH and SPARK_LOGO_PATH.exists():
            logo_b64 = base64.b64encode(SPARK_LOGO_PATH.read_bytes()).decode('ascii')
            if logo_b64:
                return logo_b64
        logger.warning("Spark logo not found or empty, emails will show placeholder")
        return ""
    except Exception as e:
        logger.error(f"Error reading Spark logo: {e}")
        return ""

def get_spark_logo_html(size: str = "44") -> str:
    """Generate HTML img tag for Spark logo using CID reference for email client compatibility"""
    # Use cid: reference - the actual image is attached in send_smtp_email()
    return f'<img src="cid:spark_logo" width="{size}" height="{size}" alt="Spark" style="display:block;"/>'


def get_project_url(project_id: str, project_source: str) -> tuple:
    """Generate proper URL and determine if should show link based on project source
    Returns: (url, should_show_link)"""
    if 'Intake' in project_source:
        # Intake Hub projects link to hoops.wal-mart.com
        return (f"https://hoops.wal-mart.com/intake-hub/projects/{project_id}", True)
    else:
        # Projects dashboard - link to Activity Hub projects page
        return (f"http://weus42608431466:8088/activity-hub/projects?id={project_id}", True)


def check_owner_missing_hierarchy(owner_name: str) -> dict:
    """Check if owner has projects with missing director/sr_director data"""
    client = bigquery.Client(project=BQ_PROJECT)
    
    query = f"""
    SELECT 
        COUNT(*) as total_projects,
        COUNTIF(director_id IS NULL) as missing_director,
        COUNTIF(sr_director_id IS NULL) as missing_sr_director,
        COUNTIF(director_id IS NULL OR sr_director_id IS NULL) as missing_either
    FROM `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE}`
    WHERE owner = @owner_name
    """
    
    job_config = bigquery.QueryJobConfig(query_parameters=[
        bigquery.ScalarQueryParameter("owner_name", "STRING", owner_name),
    ])
    
    results = list(client.query(query, job_config=job_config).result())
    if results:
        return {
            'total_projects': results[0].total_projects,
            'missing_director': results[0].missing_director,
            'missing_sr_director': results[0].missing_sr_director,
            'missing_either': results[0].missing_either
        }
    return {}


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
        ap.director_id,
        ap.sr_director_id,
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
            'url': url,
            'director_id': row.director_id,
            'sr_director_id': row.sr_director_id
        })
    
    return projects


def query_director_projects(director_name: str, include_only_not_updated: bool = False) -> list:
    """Query BigQuery for all projects where person is director or sr_director"""
    
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
        ap.director_id,
        ap.sr_director_id,
        c.WM_WEEK_NBR,
        c.FISCAL_YEAR_NBR
    FROM `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE}` ap
    LEFT JOIN `{BQ_PROJECT}.{BQ_DATASET}.Cal_Dim_Data` c
      ON CAST(ap.project_update_date AS DATE) = c.CALENDAR_DATE
    WHERE ap.sr_director_id = @director_name OR ap.director_id = @director_name
    ORDER BY ap.title ASC
    """
    
    job_config = bigquery.QueryJobConfig(query_parameters=[
        bigquery.ScalarQueryParameter("director_name", "STRING", director_name),
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
            'project_owner': row.owner or 'N/A',  # Add project_owner for leadership email compatibility
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
    
    # Check for missing director/sr_director data (only for owner emails, not leadership)
    missing_callout = ""
    if not is_leadership:
        hierarchy_check = check_owner_missing_hierarchy(owner_name)
        has_missing_hierarchy = hierarchy_check.get('missing_either', 0) > 0
        
        if has_missing_hierarchy:
            missing_callout = f"""
        <!-- MISSING CONTACT DATA CALLOUT -->
        <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 24px; background-color: #fff4e6; border-left: 4px solid #f7630c; padding: 16px 20px; border-radius: 4px; box-sizing: border-box;">
        <tr>
        <td>
            <div style="font-size: 13px; font-weight: 700; color: #f7630c; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">⚠️ ACTION NEEDED: Update Your Contact Information</div>
            <div style="font-size: 13px; color: #333; line-height: 1.5;">
                We detected that <strong>{hierarchy_check.get('missing_either', 0)} of your {hierarchy_check.get('total_projects', 0)} project(s)</strong> are missing <strong>Director</strong> and/or <strong>Sr. Director</strong> contact information.
                <br><br>
                This information is critical for:
                <ul style="margin: 10px 0; padding-left: 20px;">
                    <li>Routing escalations to the right leadership</li>
                    <li>Ensuring visibility in leadership dashboards</li>
                    <li>Proper project approvals and oversight</li>
                </ul>
                
                <strong>Quick Fix:</strong>
                <ol style="margin: 10px 0; padding-left: 20px;">
                    <li>Go to <a href="http://weus42608431466:8088/activity-hub/projects" style="color: #f7630c; text-decoration: underline;">Activity Hub Projects</a></li>
                    <li>Click on each project and update <strong>Director</strong> and <strong>Sr. Director</strong> fields</li>
                    <li>Or update in <a href="https://hoops.wal-mart.com/intake-hub" style="color: #f7630c; text-decoration: underline;">Intake Hub</a> if projects originated there</li>
                </ol>
                
                <strong>Need help?</strong> See the notification in your Activity Hub inbox or contact the Activity Hub support team.
            </div>
        </td>
        </tr>
        </table>
        """
    
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
            
            # Add missing indicator if director/sr_director is missing
            missing_indicator = ""
            if p.get('director_id') is None or p.get('sr_director_id') is None:
                missing_indicator = " ⚠️"
            
            project_rows.append(f"""
            <tr style="border-bottom: 1px solid #e0e0e0;">
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; font-weight: 500;">{project_title_html}{missing_indicator}</td>
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; font-weight: 600; color: {health_color};">{p['health']}</td>
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; color: #666; font-size: 13px;">{p['business_area']}</td>
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; color: #666; font-size: 13px;">{p['update_date']}</td>
                <td style="padding: 12px; font-size: 13px; line-height: 1.4; max-width: 300px; word-wrap: break-word;">{p['project_update']}</td>
            </tr>
            """)
        
        projects_table = ''.join(project_rows)
    
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
    <td style="padding-right: 15px; vertical-align: middle;">
        {get_spark_logo_html("48")}
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
        <p style="margin: 0 0 8px 0; font-size: 16px; font-weight: 500; color: #333;">Hi {owner_name},</p>
        <p style="margin: 0 0 24px 0; font-size: 14px; color: #666; line-height: 1.6;">{action_text}</p>
        
        <!-- MISSING CONTACT CALLOUT (if needed) -->
        {missing_callout}
        
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
        
        <p style="margin: 0; font-size: 12px; color: #999; font-style: italic;">
            ⚠️ = Projects missing Director and/or Sr. Director contact information
        </p>
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
    """Send email via Walmart internal SMTP with embedded Spark logo as CID attachment"""
    try:
        # Use 'related' so inline images (CID) are bundled with the HTML
        msg = MIMEMultipart('related')
        msg['From'] = FROM_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Wrap HTML in an 'alternative' sub-part
        msg_alt = MIMEMultipart('alternative')
        msg_alt.attach(MIMEText(html_body, 'html', 'utf-8'))
        msg.attach(msg_alt)
        
        # Attach Spark logo as inline CID image
        if SPARK_LOGO_PATH and SPARK_LOGO_PATH.exists():
            with open(SPARK_LOGO_PATH, 'rb') as f:
                logo_data = f.read()
            logo_img = MIMEImage(logo_data, _subtype='png')
            logo_img.add_header('Content-ID', '<spark_logo>')
            logo_img.add_header('Content-Disposition', 'inline', filename='Spark_Blank.png')
            msg.attach(logo_img)
        
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
    <td style="padding-right: 15px; vertical-align: middle;">
        {get_spark_logo_html("48")}
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
    
    # Special case for Kristine: use director query instead of hierarchical approach
    if manager_name == 'Kristine Torres':
        projects = query_director_projects('Kristine Torres', include_only_not_updated=False)
        logger.info(f"Found {len(projects)} total projects where Kristine Torres is director/sr_director")
    else:
        # Get all direct reports projects using hierarchical approach
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
        {get_spark_logo_html("48")}
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
    
    logger.info("\n" + "=" * 80)
    logger.info("✓ ALL TEST EMAILS SENT")
    logger.info("=" * 80)
    
    logger.info("\n" + "=" * 80)
    logger.info("✓ ALL TEST EMAILS SENT")
    logger.info("=" * 80)


if __name__ == '__main__':
    main()
