"""
Activity Hub Email Scheduler
Sends Monday and Wednesday emails to project owners and managers
Monday: All projects
Wednesday: Only Not Updated projects
"""

import os
import json
import smtplib
from datetime import datetime, time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from google.cloud import bigquery
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

class ActivityHubEmailer:
    def __init__(self):
        self.bq_client = bigquery.Client(project='wmt-assetprotection-prod')
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        
    def get_current_wm_week(self):
        """Calculate current Walmart week"""
        today = datetime.now()
        fy_start = datetime(today.year if today.month >= 2 else today.year - 1, 2, 1)
        days_since = (today - fy_start).days
        return (days_since // 7) + 1
    
    def get_owner_projects(self, owner_name: str, include_only_not_updated: bool = False) -> list:
        """Get projects for a specific owner"""
        current_week = self.get_current_wm_week()
        
        sql = f"""
        SELECT 
            project_id,
            title,
            owner,
            health,
            status,
            project_update_date,
            business_organization
        FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
        WHERE owner = @owner_name
        ORDER BY title ASC
        """
        
        job_config = bigquery.QueryJobConfig(query_parameters=[
            bigquery.ScalarQueryParameter("owner_name", "STRING", owner_name),
        ])
        
        results = list(self.bq_client.query(sql, job_config=job_config).result())
        
        projects = []
        for row in results:
            # Check if updated this week
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
            
            projects.append({
                'project_id': row.project_id,
                'title': row.title,
                'owner': row.owner,
                'health': row.health or 'Unknown',
                'status': row.status or 'Unknown',
                'updated': is_updated,
                'update_date': row.project_update_date.strftime('%m/%d/%Y') if row.project_update_date else 'Never',
                'business_area': row.business_organization or 'N/A'
            })
        
        return projects
    
    def get_all_owners(self) -> list:
        """Get all unique project owners"""
        sql = "SELECT DISTINCT owner FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects` WHERE owner IS NOT NULL ORDER BY owner ASC"
        results = list(self.bq_client.query(sql).result())
        return [row.owner for row in results]
    
    def generate_owner_email_html(self, owner_name: str, projects: list, email_type: str = 'monday') -> str:
        """Generate HTML email for owner"""
        day_text = "This Week's Projects" if email_type == 'monday' else "Projects Needing Updates"
        
        if not projects:
            project_rows = '<tr><td colspan="5" style="text-align: center; padding: 20px; color: #999;">No projects to display</td></tr>'
        else:
            project_rows = ''.join([f"""
            <tr>
                <td style="border: 1px solid #ddd; padding: 12px; font-weight: 500;">{p['title']}</td>
                <td style="border: 1px solid #ddd; padding: 12px;">{p['health']}</td>
                <td style="border: 1px solid #ddd; padding: 12px;">{p['status']}</td>
                <td style="border: 1px solid #ddd; padding: 12px; color: #999; font-size: 13px;">{p['update_date']}</td>
                <td style="border: 1px solid #ddd; padding: 12px;">
                    <span style="display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; 
                    background-color: {'#d4edda' if p['updated'] else '#f8d7da'}; color: {'#155724' if p['updated'] else '#721c24'};">
                        {'Updated' if p['updated'] else 'Pending'}
                    </span>
                </td>
            </tr>
            """ for p in projects])
        
        html_content = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; color: #333; line-height: 1.6; }}
                    .container {{ max-width: 900px; margin: 0 auto; }}
                    .header {{ background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%); color: white; padding: 30px; border-radius: 8px 8px 0 0; text-align: center; }}
                    .header h1 {{ margin: 0; font-size: 28px; }}
                    .header p {{ margin: 5px 0 0 0; font-size: 16px; opacity: 0.95; }}
                    .content {{ background: white; padding: 30px; border: 1px solid #e0e0e0; border-top: none; }}
                    .greeting {{ margin-bottom: 20px; }}
                    .greeting p {{ margin: 0 0 10px 0; font-size: 16px; }}
                    table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                    th {{ background-color: #f5f5f5; padding: 12px; text-align: left; font-weight: 600; border-bottom: 2px solid #0066cc; font-size: 14px; color: #333; }}
                    td {{ border: 1px solid #ddd; padding: 12px; font-size: 14px; }}
                    tr:nth-child(even) {{ background-color: #f9f9f9; }}
                    .cta-button {{ display: inline-block; background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%); color: white; padding: 14px 32px; text-decoration: none; border-radius: 6px; font-weight: 600; margin: 20px 0; }}
                    .cta-button:hover {{ opacity: 0.9; }}
                    .footer {{ background-color: #f5f5f5; padding: 20px; border-radius: 0 0 8px 8px; font-size: 12px; color: #666; text-align: center; border: 1px solid #e0e0e0; border-top: none; }}
                    .project-count {{ font-size: 18px; font-weight: 600; color: #0066cc; margin: 10px 0; }}
                    .action-text {{ font-style: italic; color: #666; margin: 15px 0; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>📊 Activity Hub Project Update</h1>
                        <p>{day_text}</p>
                    </div>
                    
                    <div class="content">
                        <div class="greeting">
                            <p>Hi {owner_name},</p>
                            <p>{'Below are all your projects for this week.' if email_type == 'monday' else "Below are your projects that still need updates. Please review and provide status updates when possible."}</p>
                        </div>
                        
                        <div class="project-count">📋 {len(projects)} Project{'s' if len(projects) != 1 else ''}</div>
                        
                        <table>
                            <thead>
                                <tr>
                                    <th>Project Title</th>
                                    <th>Health</th>
                                    <th>Status</th>
                                    <th>Last Updated</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {project_rows}
                            </tbody>
                        </table>
                        
                        <div class="action-text">
                            💡 <strong>Action Required:</strong> Please log in to Activity Hub to provide project updates and notes.
                        </div>
                        
                        <center>
                            <a href="http://localhost:8088/activity-hub/projects" class="cta-button">
                                🔗 Open Activity Hub Projects
                            </a>
                        </center>
                    </div>
                    
                    <div class="footer">
                        <p>This is an automated email from Activity Hub. Please do not reply to this email.</p>
                        <p>Generated: {datetime.now().strftime('%b %d, %Y at %I:%M %p')}</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        return html_content
    
    def send_test_email(self, recipient_email: str, owner_name: str = "Kendall Rush", email_type: str = 'monday'):
        """Send a test email for format review"""
        # Get sample projects for this owner
        projects = self.get_owner_projects(owner_name, include_only_not_updated=(email_type == 'wednesday'))
        
        # If no real projects, create sample data
        if not projects:
            projects = [
                {
                    'title': 'Project Management System Implementation',
                    'health': 'On Track',
                    'status': 'In Progress',
                    'updated': True,
                    'update_date': '04/23/2026',
                    'business_area': 'Technology'
                },
                {
                    'title': 'Store Layout Optimization - Region 5',
                    'health': 'At Risk',
                    'status': 'Pending Review',
                    'updated': False,
                    'update_date': '04/09/2026',
                    'business_area': 'Operations'
                },
                {
                    'title': 'Q2 Budget Forecasting Initiative',
                    'health': 'On Track',
                    'status': 'In Progress',
                    'updated': True,
                    'update_date': '04/22/2026',
                    'business_area': 'Finance'
                }
            ]
        
        # Generate HTML
        html_body = self.generate_owner_email_html(owner_name, projects, email_type)
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"{'[DEMO] ' if email_type == 'wednesday' else '[DEMO] '}Activity Hub - {owner_name}'s Projects ({datetime.now().strftime('%A, %b %d')})"
        msg['From'] = 'activity_hub_notifications@walmart.com'
        msg['To'] = recipient_email
        
        # Attach HTML
        msg.attach(MIMEText(html_body, 'html'))
        
        print(f"\n📧 EMAIL PREVIEW - {email_type.upper()}")
        print("=" * 80)
        print(f"To: {recipient_email}")
        print(f"Subject: {msg['Subject']}")
        print("=" * 80)
        print("\nHTML Content Generated Successfully")
        print(f"Owner: {owner_name}")
        print(f"Projects: {len(projects)}")
        print("\nFull HTML will be sent to email client")
        print("=" * 80)
        
        return {
            'success': True,
            'recipient': recipient_email,
            'owner': owner_name,
            'email_type': email_type,
            'projects_count': len(projects),
            'timestamp': datetime.now().isoformat()
        }


def main():
    """Main function for testing"""
    emailer = ActivityHubEmailer()
    
    # Get all owners
    owners = emailer.get_all_owners()
    print(f"\n✓ Found {len(owners)} project owners")
    print(f"Sample owners: {owners[:5]}")
    
    # Send test email
    result = emailer.send_test_email(
        recipient_email='kendall.rush@walmart.com',
        owner_name='Kendall Rush',
        email_type='monday'
    )
    
    print(f"\n✓ Test email prepared: {result}")


if __name__ == '__main__':
    main()
