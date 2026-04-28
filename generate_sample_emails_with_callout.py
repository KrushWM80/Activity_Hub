#!/usr/bin/env python3
"""
Generate sample Monday, Wednesday, and Thursday Leader emails with missing contact callout
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from google.cloud import bigquery

# Configuration
BQ_PROJECT = 'wmt-assetprotection-prod'
BQ_DATASET = 'Store_Support_Dev'
BQ_TABLE = 'AH_Projects'

# Set Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
    os.environ.get('APPDATA', ''), 'gcloud', 'application_default_credentials.json'
)

client = bigquery.Client(project=BQ_PROJECT)

def get_spark_logo_base64() -> str:
    """Get Spark logo as base64"""
    logo_path = Path("c:/Users/krush/OneDrive - Walmart Inc/Documents/VSCode/Activity_Hub/Interface/Spark_Blank.png")
    try:
        if logo_path.exists():
            import base64
            return base64.b64encode(logo_path.read_bytes()).decode('ascii')
    except:
        pass
    return ""

def get_spark_logo_html(size: str = "44") -> str:
    """Generate HTML img tag for Spark logo"""
    spark_b64 = get_spark_logo_base64()
    if spark_b64:
        return f'<img src="data:image/png;base64,{spark_b64}" width="{size}" height="{size}" alt="Spark" style="display:block;"/>'
    return '&#10058;'

def check_owner_missing_hierarchy(owner_name: str) -> dict:
    """Check if owner has projects with missing director/sr_director data"""
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

def query_owner_projects(owner_name: str, not_updated_only: bool = False) -> list:
    """Query projects for owner"""
    
    # Get current WM week
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
        is_updated = False
        if row.WM_WEEK_NBR == current_wm_week and row.FISCAL_YEAR_NBR == current_fiscal_year:
            is_updated = True
        
        if not_updated_only and is_updated:
            continue
        
        project_note = row.project_update if row.project_update and row.project_update.strip() else 'No update provided'
        update_date_str = row.project_update_date.strftime('%b %d, %Y') if row.project_update_date else 'Not updated'
        
        if 'Intake' in (row.project_source or 'Projects'):
            project_url = f"https://hoops.wal-mart.com/intake-hub/projects/{row.project_id}"
        else:
            project_url = f"http://weus42608431466:8088/activity-hub/projects?id={row.project_id}"
        
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
            'url': project_url,
            'director_id': row.director_id,
            'sr_director_id': row.sr_director_id
        })
    
    return projects

def generate_owner_email_html(email_type: str, owner_name: str, projects: list) -> str:
    """Generate owner email with missing contact callout"""
    
    if email_type == 'monday':
        day_text = "This Week's Project Updates"
        action_text = "Below are all your projects for this week. Please provide updates where needed."
    else:  # wednesday
        day_text = "Projects Needing Updates"
        action_text = "Below are your projects that have not been updated in this Walmart week. Please provide status updates."
    
    # Check for missing director/sr_director
    hierarchy_check = check_owner_missing_hierarchy(owner_name)
    has_missing_hierarchy = hierarchy_check.get('missing_either', 0) > 0
    
    missing_callout = ""
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
            health_value = p['health'].lower() if p['health'] else 'unknown'
            if 'on track' in health_value:
                health_color = '#107C10'  # Green
            elif 'at risk' in health_value:
                health_color = '#F7630C'  # Orange
            elif 'off track' in health_value or 'paused' in health_value:
                health_color = '#DC3545'  # Red
            else:
                health_color = '#666666'  # Gray
            
            project_title_html = f'<a href="{p["url"]}" style="color: #0071CE; text-decoration: none; font-weight: 500;" target="_blank">{p["title"]}</a>'
            
            # Add missing indicator if needed
            missing_indicator = ""
            if p['director_id'] is None or p['sr_director_id'] is None:
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

# Generate sample emails
def main():
    print("\n" + "="*80)
    print("GENERATING SAMPLE EMAILS WITH MISSING CONTACT CALLOUT")
    print("="*80)
    
    # MONDAY EMAIL
    print("\n📧 MONDAY EMAIL FOR KENDALL RUSH")
    print("-"*80)
    monday_projects = query_owner_projects('Kendall Rush', not_updated_only=False)
    print(f"Projects: {len(monday_projects)}")
    monday_html = generate_owner_email_html('monday', 'Kendall Rush', monday_projects)
    
    # Save to file
    with open('sample_monday_email.html', 'w', encoding='utf-8') as f:
        f.write(monday_html)
    print("✓ Saved to: sample_monday_email.html")
    
    # WEDNESDAY EMAIL
    print("\n📧 WEDNESDAY EMAIL FOR KENDALL RUSH")
    print("-"*80)
    wednesday_projects = query_owner_projects('Kendall Rush', not_updated_only=True)
    if wednesday_projects:
        print(f"Projects needing update: {len(wednesday_projects)}")
        wednesday_html = generate_owner_email_html('wednesday', 'Kendall Rush', wednesday_projects)
        with open('sample_wednesday_email.html', 'w', encoding='utf-8') as f:
            f.write(wednesday_html)
        print("✓ Saved to: sample_wednesday_email.html")
    else:
        print("No projects needing update - no email would be sent")
    
    # THURSDAY/LEADERSHIP EMAIL - Kristine Torres
    print("\n📧 THURSDAY LEADERSHIP EMAIL FOR KRISTINE TORRES")
    print("-"*80)
    kristine_query = f"""
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
        ap.sr_director_id
    FROM `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE}` ap
    WHERE ap.sr_director_id = 'Kristine Torres' OR ap.director_id = 'Kristine Torres'
    ORDER BY ap.title ASC
    LIMIT 40
    """
    kristine_projects = list(client.query(kristine_query).result())
    print(f"Projects under Kristine: {len(kristine_projects)}")
    
    kristine_html = f"""<!DOCTYPE html>
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
        <p style="margin: 0 0 8px 0; font-size: 16px; font-weight: 500; color: #333;">Hi Kristine,</p>
        <p style="margin: 0 0 24px 0; font-size: 14px; color: #666; line-height: 1.6;">Below is a summary of all projects for your team, including your direct reports. This will help you stay informed on team project status and identify any areas needing attention.</p>
        
        <!-- Projects Count Badge -->
        <div style="background-color: #f0f7ff; border-left: 4px solid #0071CE; padding: 16px 20px; margin-bottom: 24px; border-radius: 4px;">
            <div style="font-size: 11px; font-weight: 700; color: #0071CE; text-transform: uppercase; letter-spacing: 0.5px;">Team Project Summary</div>
            <div style="font-size: 24px; font-weight: 700; color: #0071CE; margin-top: 8px;">{len(kristine_projects)} Total Projects</div>
        </div>
        
        <!-- Projects Table -->
        <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse: collapse; margin-bottom: 24px; border: 1px solid #e0e0e0;">
            <thead>
            <tr style="background-color: #f5f5f5;">
                <th style="padding: 12px; text-align: left; font-weight: 700; font-size: 12px; color: #333; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #0071CE; border-right: 1px solid #e0e0e0; width: 30%;">Project Title</th>
                <th style="padding: 12px; text-align: left; font-weight: 700; font-size: 12px; color: #333; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #0071CE; border-right: 1px solid #e0e0e0; width: 12%;">Owner</th>
                <th style="padding: 12px; text-align: left; font-weight: 700; font-size: 12px; color: #333; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #0071CE; border-right: 1px solid #e0e0e0; width: 10%;">Health</th>
                <th style="padding: 12px; text-align: left; font-weight: 700; font-size: 12px; color: #333; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #0071CE; border-right: 1px solid #e0e0e0; width: 15%;">Business Area</th>
                <th style="padding: 12px; text-align: left; font-weight: 700; font-size: 12px; color: #333; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #0071CE; border-right: 1px solid #e0e0e0; width: 12%;">Update Date</th>
                <th style="padding: 12px; text-align: left; font-weight: 700; font-size: 12px; color: #333; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #0071CE; width: 21%;">Latest Update</th>
            </tr>
            </thead>
            <tbody>
"""
    
    for p in kristine_projects:
        health_value = p.health.lower() if p.health else 'unknown'
        if 'on track' in health_value:
            health_color = '#107C10'  # Green
        elif 'at risk' in health_value:
            health_color = '#F7630C'  # Orange
        elif 'off track' in health_value or 'paused' in health_value:
            health_color = '#DC3545'  # Red
        else:
            health_color = '#666666'  # Gray
        
        project_update = p.project_update if p.project_update and p.project_update.strip() else 'No update provided'
        update_date_str = p.project_update_date.strftime('%b %d, %Y') if p.project_update_date else 'Not updated'
        
        if 'Intake' in (p.project_source or 'Projects'):
            project_url = f"https://hoops.wal-mart.com/intake-hub/projects/{p.project_id}"
        else:
            project_url = f"http://weus42608431466:8088/activity-hub/projects?id={p.project_id}"
        
        project_title_html = f'<a href="{project_url}" style="color: #0071CE; text-decoration: none; font-weight: 500;" target="_blank">{p.title}</a>'
        
        kristine_html += f"""
            <tr style="border-bottom: 1px solid #e0e0e0;">
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; font-weight: 500;">{project_title_html}</td>
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; font-size: 13px; color: #666;">{p.owner}</td>
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; font-weight: 600; color: {health_color};">{p.health}</td>
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; color: #666; font-size: 13px;">{p.business_organization}</td>
                <td style="padding: 12px; border-right: 1px solid #e0e0e0; color: #666; font-size: 13px;">{update_date_str}</td>
                <td style="padding: 12px; font-size: 13px; line-height: 1.4; max-width: 200px; word-wrap: break-word;">{project_update}</td>
            </tr>
"""
    
    kristine_html += """
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
            Generated: """ + datetime.now().strftime('%B %d, %Y') + """
        </p>
    </td>
    </tr>
    </table>

</body>
</html>
"""
    
    with open('sample_leadership_email_kristine.html', 'w', encoding='utf-8') as f:
        f.write(kristine_html)
    print("✓ Saved to: sample_leadership_email_kristine.html")
    
    print("\n" + "="*80)
    print("✓ SAMPLE EMAILS GENERATED")
    print("="*80)
    print("\nFiles created:")
    print("  1. sample_monday_email.html       - Monday owner email with callout")
    print("  2. sample_wednesday_email.html    - Wednesday owner email with callout")
    print("  3. sample_leadership_email_kristine.html - Leadership email (Kristine Torres)")
    print("\nThese are sample/example emails. They have NOT been sent.")
    print("To see them: Open the HTML files in your web browser or email client preview.")

if __name__ == '__main__':
    main()
