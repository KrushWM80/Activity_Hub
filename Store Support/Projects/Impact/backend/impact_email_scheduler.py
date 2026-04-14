#!/usr/bin/env python3
"""
Impact Platform Email Scheduler
Sends weekly email notifications:
- Monday 6 AM: Project owners receive update request with their projects
- Thursday 10 AM: Admin (kendall.rush@walmart.com) receives org-wide report

Usage:
  python impact_email_scheduler.py monday    # Send Monday emails manually
  python impact_email_scheduler.py thursday  # Send Thursday emails manually
  python impact_email_scheduler.py test      # Test mode (preview only)
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
from typing import List

from google.cloud import bigquery
from impact_report_generator import generate_pptx_report

# Configuration
BQ_PROJECT = "wmt-assetprotection-prod"
BQ_DATASET = "Store_Support_Dev"
BQ_TABLE = "AH_Projects"

SMTP_SERVER = "smtp-gw1.homeoffice.wal-mart.com"
SMTP_PORT = 25
SENDER_EMAIL = "kendall.rush@walmart.com"

ADMIN_RECIPIENTS = ["kendall.rush@walmart.com"]
DASHBOARD_URL = "http://weus42608431466:8088/activity-hub/Impact"

class ImpactEmailScheduler:
    def __init__(self):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
            os.environ.get('APPDATA', ''), 'gcloud', 'application_default_credentials.json'
        )
        self.bq_client = bigquery.Client(project=BQ_PROJECT)

    def get_active_projects(self) -> List[dict]:
        """Query all active projects from BigQuery"""
        query = f"""
        SELECT 
            impact_id,
            title,
            description,
            owner_id,
            owner_name,
            business_area,
            health_status,
            latest_update,
            latest_update_timestamp,
            current_wm_week_update,
            current_wm_week_update_timestamp,
            project_status
        FROM `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE}`
        WHERE project_status = 'Active'
        ORDER BY business_area, title
        """
        
        try:
            results = self.bq_client.query(query).result()
            return [dict(row) for row in results]
        except Exception as e:
            print(f"Error querying projects: {e}")
            return []

    def get_owner_projects(self, owner_id: str) -> List[dict]:
        """Get all projects for specific owner"""
        query = f"""
        SELECT * FROM `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE}`
        WHERE owner_id = '{owner_id}' AND project_status = 'Active'
        ORDER BY business_area, title
        """
        
        try:
            results = self.bq_client.query(query).result()
            return [dict(row) for row in results]
        except Exception as e:
            print(f"Error querying owner projects: {e}")
            return []

    def build_owner_email_html(self, owner_name: str, projects: List[dict]) -> str:
        """Build HTML email for project owner with their projects and update request"""
        
        # Build project table rows
        project_rows = ""
        for p in projects:
            status = "✓ Updated" if p.get('current_wm_week_update') else "⚠ Not Updated This Week"
            latest = p.get('latest_update', 'N/A')[:100]
            health_color = "#107C10" if "green" in (p.get('health_status') or "").lower() else "#F7630C" if "yellow" in (p.get('health_status') or "").lower() else "#DC3545"
            
            project_rows += f"""
            <tr style="border-bottom: 1px solid #ddd;">
                <td style="padding: 12px; font-weight: bold;">{p.get('title', '')}</td>
                <td style="padding: 12px;">{p.get('description', '')[:100]}...</td>
                <td style="padding: 12px; color: {health_color}; font-weight: bold;">{p.get('health_status', 'N/A')}</td>
                <td style="padding: 12px; color: #0071CE;">{latest}</td>
                <td style="padding: 12px; text-align: center;"><span style="background: {'#107C10' if p.get('current_wm_week_update') else '#DC3545'}; color: white; padding: 4px 8px; border-radius: 3px; font-size: 12px;">{status}</span></td>
            </tr>
            """
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Segoe UI, Arial, sans-serif; color: #333; background: #f5f5f5; }}
                .container {{ max-width: 900px; margin: 0 auto; background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
                .header {{ background: linear-gradient(135deg, #0071CE 0%, #004C91 100%); color: white; padding: 30px; border-radius: 8px 8px 0 0; text-align: center; }}
                .header h1 {{ margin: 0; font-size: 28px; }}
                .header p {{ margin: 5px 0 0 0; opacity: 0.9; }}
                .content {{ padding: 30px; }}
                .section {{ margin-bottom: 30px; }}
                .section h2 {{ color: #0071CE; border-bottom: 2px solid #FFC220; padding-bottom: 10px; }}
                table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
                th {{ background: #0071CE; color: white; padding: 12px; text-align: left; font-weight: bold; }}
                .metric-box {{ display: inline-block; background: #f0f0f0; padding: 15px 25px; margin-right: 15px; border-radius: 4px; border-left: 4px solid #0071CE; }}
                .metric-box strong {{ color: #0071CE; }}
                .button {{ display: inline-block; background: #0071CE; color: white; padding: 12px 24px; border-radius: 4px; text-decoration: none; font-weight: bold; margin: 10px 0; }}
                .button:hover {{ background: #004C91; }}
                .footer {{ background: #f5f5f5; padding: 20px; text-align: center; border-top: 1px solid #ddd; color: #666; font-size: 12px; }}
                .warning {{ background: #FFF3CD; border: 1px solid #FFE69C; padding: 12px; border-radius: 4px; margin: 15px 0; color: #856404; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Impact Platform - Weekly Update Request</h1>
                    <p>Your projects need updates for the current Walmart week</p>
                </div>
                
                <div class="content">
                    <p>Hi <strong>{owner_name}</strong>,</p>
                    
                    <p>This is your weekly update request for projects in the Impact Platform. Please review your projects below and provide updates for the current Walmart week.</p>
                    
                    <div class="section">
                        <h2>Your Projects</h2>
                        <p>You have <strong>{len(projects)}</strong> active projects. {len([p for p in projects if p.get('current_wm_week_update')])} have been updated this week.</p>
                        
                        <table>
                            <tr>
                                <th>Project Title</th>
                                <th>Description</th>
                                <th>Health</th>
                                <th>Latest Update</th>
                                <th>Status</th>
                            </tr>
                            {project_rows}
                        </table>
                    </div>
                    
                    <div class="warning">
                        <strong>⏰ Action Required:</strong> Please update any projects that haven't been updated this week. Updates are due by <strong>Wednesday EOD</strong>.
                    </div>
                    
                    <div class="section">
                        <h2>Update Your Projects</h2>
                        <p>Click the button below to visit the Impact Platform dashboard where you can view, edit, and update your projects:</p>
                        <a href="{DASHBOARD_URL}" class="button">Go to Impact Dashboard</a>
                    </div>
                    
                    <div class="section">
                        <h2>Need Help?</h2>
                        <p>For questions or technical issues, please contact <strong>kendall.rush@walmart.com</strong></p>
                    </div>
                </div>
                
                <div class="footer">
                    <p>This email was automatically generated by the Impact Platform. Do not reply to this email.</p>
                    <p>Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html

    def build_admin_email_html(self, all_projects: List[dict], metrics: dict) -> str:
        """Build comprehensive admin/leadership report HTML"""
        
        # Build business area summary
        business_areas = {}
        for p in all_projects:
            ba = p.get('business_area', 'Unknown')
            if ba not in business_areas:
                business_areas[ba] = {'total': 0, 'updated': 0, 'projects': []}
            business_areas[ba]['total'] += 1
            if p.get('current_wm_week_update'):
                business_areas[ba]['updated'] += 1
            business_areas[ba]['projects'].append(p)
        
        ba_rows = ""
        for ba, data in sorted(business_areas.items()):
            percent = (data['updated'] / data['total'] * 100) if data['total'] > 0 else 0
            ba_rows += f"""
            <tr style="border-bottom: 1px solid #ddd;">
                <td style="padding: 12px; font-weight: bold;">{ba}</td>
                <td style="padding: 12px; text-align: center;">{data['total']}</td>
                <td style="padding: 12px; text-align: center;">{data['updated']}</td>
                <td style="padding: 12px; text-align: center;"><strong>{percent:.1f}%</strong></td>
            </tr>
            """
        
        # Projects not updated this week
        not_updated = [p for p in all_projects if not p.get('current_wm_week_update')]
        not_updated_rows = ""
        for p in not_updated[:15]:  # Show top 15
            not_updated_rows += f"""
            <tr style="border-bottom: 1px solid #fdd;">
                <td style="padding: 12px;">{p.get('title', '')}</td>
                <td style="padding: 12px;">{p.get('owner_name', '')}</td>
                <td style="padding: 12px;">{p.get('business_area', '')}</td>
                <td style="padding: 12px;"><span style="background: #DC3545; color: white; padding: 4px 8px; border-radius: 3px; font-size: 12px;">No Update</span></td>
            </tr>
            """
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Segoe UI, Arial, sans-serif; color: #333; background: #f5f5f5; }}
                .container {{ max-width: 1000px; margin: 0 auto; background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
                .header {{ background: linear-gradient(135deg, #0071CE 0%, #004C91 100%); color: white; padding: 30px; border-radius: 8px 8px 0 0; text-align: center; }}
                .header h1 {{ margin: 0; font-size: 32px; }}
                .metrics {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 20px 0; }}
                .metric {{ background: linear-gradient(135deg, #0071CE 0%, #004C91 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }}
                .metric .number {{ font-size: 32px; font-weight: bold; }}
                .metric .label {{ font-size: 14px; opacity: 0.9; margin-top: 5px; }}
                .content {{ padding: 30px; }}
                .section {{ margin-bottom: 30px; }}
                .section h2 {{ color: #0071CE; border-bottom: 2px solid #FFC220; padding-bottom: 10px; }}
                table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
                th {{ background: #0071CE; color: white; padding: 12px; text-align: left; font-weight: bold; }}
                .footer {{ background: #f5f5f5; padding: 20px; text-align: center; border-top: 1px solid #ddd; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Impact Platform - Leadership Report</h1>
                    <p>Weekly Project Status Overview</p>
                </div>
                
                <div class="content">
                    <div class="metrics">
                        <div class="metric">
                            <div class="number">{metrics.get('active_projects', 0)}</div>
                            <div class="label">Active Projects</div>
                        </div>
                        <div class="metric">
                            <div class="number">{metrics.get('unique_owners', 0)}</div>
                            <div class="label">Unique Owners</div>
                        </div>
                        <div class="metric">
                            <div class="number">{metrics.get('projects_updated_this_week', 0)}</div>
                            <div class="label">Updated This Week</div>
                        </div>
                        <div class="metric">
                            <div class="number">{metrics.get('percent_updated', 0):.1f}%</div>
                            <div class="label">Percent Updated</div>
                        </div>
                    </div>
                    
                    <div class="section">
                        <h2>Business Area Summary</h2>
                        <table>
                            <tr>
                                <th>Business Area</th>
                                <th>Total Projects</th>
                                <th>Updated This Week</th>
                                <th>% Updated</th>
                            </tr>
                            {ba_rows}
                        </table>
                    </div>
                    
                    <div class="section">
                        <h2>Projects Requiring Updates (Top {min(15, len(not_updated))})</h2>
                        {f'<p><strong>Good news!</strong> All active projects have been updated this week.</p>' if not not_updated else f'<p>The following {len(not_updated)} projects have not been updated for the current Walmart week:</p>'}
                        {f'<table><tr><th>Project Title</th><th>Owner</th><th>Business Area</th><th>Status</th></tr>{not_updated_rows}</table>' if not_updated else ''}
                    </div>
                    
                    <div class="section">
                        <h2>View Full Dashboard</h2>
                        <p>For detailed project information and management, visit the Impact Platform dashboard:</p>
                        <p><a href="{DASHBOARD_URL}" style="display: inline-block; background: #0071CE; color: white; padding: 12px 24px; border-radius: 4px; text-decoration: none; font-weight: bold;">Open Impact Dashboard</a></p>
                    </div>
                </div>
                
                <div class="footer">
                    <p>This email was automatically generated by the Impact Platform.</p>
                    <p>Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html

    def send_email(self, recipients: List[str], subject: str, html_body: str, 
                   attachments: List[Path] = None, preview_only: bool = False) -> bool:
        """Send email via SMTP"""
        
        if preview_only:
            print(f"\n[PREVIEW] Email would be sent to: {', '.join(recipients)}")
            print(f"[PREVIEW] Subject: {subject}")
            print(f"[PREVIEW] Attachments: {[a.name for a in (attachments or [])]}")
            return True
        
        try:
            msg = MIMEMultipart('related')
            msg['From'] = SENDER_EMAIL
            msg['To'] = '; '.join(recipients)
            msg['Subject'] = subject
            
            # Attach HTML body
            msg.attach(MIMEText(html_body, 'html', 'utf-8'))
            
            # Attach files
            if attachments:
                for file_path in attachments:
                    if file_path.exists():
                        with open(file_path, 'rb') as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', f'attachment; filename= {file_path.name}')
                        msg.attach(part)
            
            # Send via SMTP
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
                server.sendmail(SENDER_EMAIL, recipients, msg.as_string())
            
            print(f"✓ Email sent to {len(recipients)} recipient(s)")
            return True
        
        except Exception as e:
            print(f"✗ Error sending email: {e}")
            return False

    def send_monday_emails(self, preview_only: bool = False) -> None:
        """Send Monday 6 AM emails to all project owners with their projects"""
        print("\n=== MONDAY EMAIL: Project Owner Update Requests ===")
        
        projects = self.get_active_projects()
        if not projects:
            print("No active projects found")
            return
        
        # Group by owner
        owners = {}
        for p in projects:
            owner_id = p.get('owner_id')
            if owner_id not in owners:
                owners[owner_id] = {'name': p.get('owner_name'), 'projects': []}
            owners[owner_id]['projects'].append(p)
        
        # Send email to each owner
        for owner_id, data in owners.items():
            owner_name = data['name']
            owner_projects = data['projects']
            
            print(f"\nSending to {owner_name} ({owner_id}): {len(owner_projects)} projects")
            
            # Generate report PPT
            pptx_data, report_id = generate_pptx_report(owner_projects)
            from pathlib import Path
            import tempfile
            temp_dir = Path(tempfile.gettempdir()) / "impact_reports"
            pptx_file = temp_dir / f"{report_id}.pptx"
            
            # Build HTML
            html = self.build_owner_email_html(owner_name, owner_projects)
            
            # Send
            self.send_email(
                recipients=[f"{owner_id}@walmart.com"],
                subject="Impact Platform - Weekly Update Request",
                html_body=html,
                attachments=[pptx_file],
                preview_only=preview_only
            )

    def send_thursday_emails(self, preview_only: bool = False) -> None:
        """Send Thursday 10 AM admin/leadership report"""
        print("\n=== THURSDAY EMAIL: Leadership Report ===")
        
        projects = self.get_active_projects()
        if not projects:
            print("No active projects found")
            return
        
        # Calculate metrics
        updated = [p for p in projects if p.get('current_wm_week_update')]
        unique_owners = set(p.get('owner_id') for p in projects)
        
        metrics = {
            'active_projects': len(projects),
            'projects_updated_this_week': len(updated),
            'percent_updated': round(len(updated) / max(len(projects), 1) * 100, 1),
            'unique_owners': len(unique_owners)
        }
        
        # Generate report PPT
        pptx_data, report_id = generate_pptx_report(projects)
        from pathlib import Path
        import tempfile
        temp_dir = Path(tempfile.gettempdir()) / "impact_reports"
        pptx_file = temp_dir / f"{report_id}.pptx"
        
        # Build HTML
        html = self.build_admin_email_html(projects, metrics)
        
        # Send to admin
        print(f"\nSending to admin: {projects[0]['owner_name']}")
        self.send_email(
            recipients=ADMIN_RECIPIENTS,
            subject="Impact Platform - Weekly Leadership Report",
            html_body=html,
            attachments=[pptx_file],
            preview_only=preview_only
        )

if __name__ == "__main__":
    scheduler = ImpactEmailScheduler()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        preview = "--preview" in sys.argv
        
        if command == "monday":
            scheduler.send_monday_emails(preview_only=preview)
        elif command == "thursday":
            scheduler.send_thursday_emails(preview_only=preview)
        elif command == "test":
            scheduler.send_monday_emails(preview_only=True)
            scheduler.send_thursday_emails(preview_only=True)
        else:
            print(f"Unknown command: {command}")
            print("Usage: monday | thursday | test")
    else:
        print("Usage: python impact_email_scheduler.py [monday|thursday|test] [--preview]")
