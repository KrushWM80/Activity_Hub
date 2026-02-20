"""
Simplified Email Service for Intake Hub Reporting
Uses only built-in Python modules - no external packages required
Sends HTML emails via SMTP
"""

import os
import json
import smtplib
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / '.env')

from database import DatabaseService
from models import FilterCriteria


class SimpleEmailReportService:
    """Service for generating and sending simple HTML email reports"""
    
    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp-gw1.homeoffice.wal-mart.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "25"))
        self.from_email = os.getenv("FROM_EMAIL", "ATCTEAMSUPPORT@Walmart.com")
        self.mock_mode = os.getenv("MOCK_EMAIL_MODE", "false").lower() == "true"
        
    async def generate_and_send_report(
        self, 
        config: Dict,
        current_user_email: Optional[str] = None,
        override_email: Optional[str] = None
    ) -> Dict:
        """Generate and send a report based on configuration
        
        Args:
            config: Report configuration
            current_user_email: Email of the logged-in user (for dynamic recipient)
            override_email: Override recipient for testing
        """
        
        try:
            # Get data from database based on filters and timeframe
            projects = await self._get_report_data(config)
            
            # Convert Project objects to dictionaries
            projects_dicts = []
            for p in projects:
                if hasattr(p, '__dict__'):
                    # Convert object to dict
                    projects_dicts.append({
                        'project_id': getattr(p, 'project_id', ''),
                        'title': getattr(p, 'title', ''),
                        'project_title': getattr(p, 'title', ''),
                        'partner': getattr(p, 'partner', ''),
                        'store_id': getattr(p, 'store', ''),
                        'store_name': getattr(p, 'store_address', ''),
                        'status': getattr(p, 'status', ''),
                        'priority': getattr(p, 'phase', ''),
                        'due_date': getattr(p, 'last_updated', ''),
                        'owner': getattr(p, 'owner', ''),
                        'division': getattr(p, 'division', ''),
                        'region': getattr(p, 'region', ''),
                        'market': getattr(p, 'market', ''),
                        'intake_card_number': getattr(p, 'project_id', ''),
                    })
                else:
                    projects_dicts.append(p)
            
            # Generate HTML email body
            html_body = self._generate_html_report(config, projects_dicts)
            
            # Determine recipients - use current user email if provided, otherwise use config email
            primary_recipient = override_email or current_user_email or config['primary_email']
            to_emails = [primary_recipient]
            cc_emails = [] if override_email else config.get('cc_emails', [])
            
            # Send email
            self._send_email(
                to_emails=to_emails,
                cc_emails=cc_emails,
                subject=f"Intake Hub Report: {config['report_name']}",
                html_body=html_body
            )
            
            return {
                "success": True,
                "message": f"Report sent successfully to {', '.join(to_emails)}",
                "timestamp": datetime.now().isoformat(),
                "sent_to": to_emails
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error generating report: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "sent_to": []
            }
    
    async def _get_report_data(self, config: Dict) -> List[Dict]:
        """Fetch data from database based on report configuration"""
        
        # Build filters from config
        filters = FilterCriteria()
        
        if 'filters' in config:
            filter_config = config['filters']
            if 'partner' in filter_config:
                filters.partners = filter_config['partner']
            if 'store_area' in filter_config:
                filters.store_areas = filter_config['store_area']
            if 'business_organization' in filter_config:
                filters.business_orgs = filter_config['business_organization']
        
        # Apply timeframe filter
        if config.get('timeframes'):
            timeframe = config['timeframes'][0]  # Use first timeframe
            filters.date_from = self._calculate_date_from_timeframe(timeframe)
        
        # Get projects from database
        projects = await self.db_service.get_projects(filters)
        
        return projects
    
    def _calculate_date_from_timeframe(self, timeframe: str) -> Optional[datetime]:
        """Calculate start date based on timeframe"""
        now = datetime.now()
        
        if timeframe == "Last 24 Hours":
            return now - timedelta(days=1)
        elif timeframe == "Last 7 Days":
            return now - timedelta(days=7)
        elif timeframe == "Last 30 Days":
            return now - timedelta(days=30)
        elif timeframe == "Last Quarter":
            return now - timedelta(days=90)
        elif timeframe == "Last Year":
            return now - timedelta(days=365)
        else:  # "All Time"
            return None
    
    def _generate_html_report(self, config: Dict, projects: List[Dict]) -> str:
        """Generate SUMMARIZED HTML email body with compact table layout"""
        
        report_name = config['report_name']
        content_types = config.get('content_types', [])
        
        # Build header - MORE COMPACT
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: 'Segoe UI', Arial, sans-serif;
                    background: #f5f7fa;
                    color: #333;
                }}
                .container {{
                    max-width: 900px;
                    margin: 0 auto;
                    background: white;
                }}
                .header {{
                    background: linear-gradient(135deg, #0071ce 0%, #004f9a 100%);
                    color: white;
                    padding: 18px 25px;
                }}
                .header h1 {{ font-size: 20px; margin-bottom: 3px; }}
                .header p {{ font-size: 11px; opacity: 0.85; }}
                .content {{ padding: 18px 25px; }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 15px;
                    font-size: 12px;
                }}
                th {{
                    background: #2d3748;
                    color: white;
                    padding: 8px 10px;
                    text-align: left;
                    font-weight: 600;
                    border: 1px solid #1a202c;
                }}
                td {{
                    padding: 7px 10px;
                    border: 1px solid #e2e8f0;
                    word-break: break-word;
                }}
                tr:nth-child(even) {{ background: #f7fafc; }}
                tr:hover {{ background: #edf2f7; }}
                a {{ color: #0071ce; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
                .section-title {{
                    font-size: 12px;
                    font-weight: 700;
                    color: #0071ce;
                    margin-top: 16px;
                    margin-bottom: 8px;
                    padding-bottom: 4px;
                    border-bottom: 2px solid #0071ce;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }}
                .footer {{
                    padding: 12px 25px;
                    border-top: 1px solid #e2e8f0;
                    font-size: 10px;
                    color: #718096;
                    text-align: center;
                }}
                
                /* Dark Mode Support */
                @media (prefers-color-scheme: dark) {{
                    body {{ background: #1a1a1a; color: #e0e0e0; }}
                    .container {{ background: #2a2a2a; }}
                    td {{ border: 1px solid #444; color: #e0e0e0; }}
                    tr:nth-child(even) {{ background: #333; }}
                    tr:hover {{ background: #404040; }}
                    th {{ background: #1f1f1f; border: 1px solid #444; }}
                    .footer {{ border-top: 1px solid #444; color: #999; }}
                    .content {{ color: #e0e0e0; }}
                    a {{ color: #66c2ff; }}
                    .section-title {{ color: #66c2ff; border-bottom: 2px solid #66c2ff; }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 {report_name}</h1>
                    <p>{datetime.now().strftime('%B %d, %Y at %I:%M %p')} | {len(projects)} Projects</p>
                </div>
                
                <div class="content">
        """
        
        # Generate tables for each content type - WITH LIMITS
        if 'New' in content_types or 'Overview' in content_types:
            html += self._generate_new_projects_table(projects)
        
        if 'Upcoming' in content_types:
            html += self._generate_upcoming_table(projects)
        
        if 'Notes' in content_types:
            html += self._generate_notes_table(projects)
        
        if not projects:
            html += '<p style="text-align:center; color:#718096; padding:20px;">No projects found matching your criteria.</p>'
        
        # Footer
        html += f"""
                </div>
                
                <div class="footer">
                    <p>Automated report from Intake Hub Dashboard | Questions? Email <a href="mailto:ATCTEAMSUPPORT@Walmart.com">ATCTEAMSUPPORT@Walmart.com</a></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _generate_new_projects_table(self, projects: List[Dict]) -> str:
        """Generate table for new projects - SUMMARIZED (TOP 5 ONLY)"""
        if not projects:
            return ""
        
        html = '<div class="section-title">🆕 New Projects</div>'
        html += '<table>'
        html += '<thead><tr><th>Project</th><th>Owner</th><th>Created</th><th>Start Date</th></tr></thead><tbody>'
        
        for project in projects[:5]:  # Limit to 5 projects ONLY
            title = project.get('title', '') or project.get('project_title', '')
            owner = project.get('owner', '-')
            created = project.get('created_date', '-')
            start_date = project.get('last_updated', '-')
            
            # Format dates if they're datetime objects
            if created and created != '-':
                try:
                    if hasattr(created, 'strftime'):
                        created = created.strftime('%m/%d/%y')
                    else:
                        created = str(created)[:10]
                except:
                    pass
            
            if start_date and start_date != '-':
                try:
                    if hasattr(start_date, 'strftime'):
                        start_date = start_date.strftime('%m/%d/%y')
                    else:
                        start_date = str(start_date)[:10]
                except:
                    pass
            
            html += f'<tr><td><a href="#">{title[:60]}</a></td><td>{owner}</td><td>{created}</td><td>{start_date}</td></tr>'
        
        html += '</tbody></table>'
        
        if len(projects) > 5:
            html += f'<p style="font-size: 11px; color: #718096; text-align: center; margin-top: 8px;">Showing 5 of {len(projects)} new projects</p>'
        
        return html
    
    def _generate_upcoming_table(self, projects: List[Dict]) -> str:
        """Generate table for upcoming projects - SUMMARIZED (TOP 3 ONLY)"""
        if not projects:
            return ""
        
        html = '<div class="section-title">📅 Upcoming</div>'
        html += '<table>'
        html += '<thead><tr><th>Project</th><th>Phase</th><th>Target Date</th><th>Owner</th></tr></thead><tbody>'
        
        for project in projects[:3]:
            title = project.get('title', '') or project.get('project_title', '')
            phase = project.get('priority', project.get('phase', '-'))
            target_date = project.get('due_date', '-')
            owner = project.get('owner', '-')
            
            if target_date and target_date != '-':
                try:
                    if hasattr(target_date, 'strftime'):
                        target_date = target_date.strftime('%m/%d/%y')
                    else:
                        target_date = str(target_date)[:10]
                except:
                    pass
            
            html += f'<tr><td><a href="#">{title[:50]}</a></td><td>{phase}</td><td>{target_date}</td><td>{owner}</td></tr>'
        
        html += '</tbody></table>'
        return html
    
    def _generate_notes_table(self, projects: List[Dict]) -> str:
        """Generate table for notes - SUMMARIZED (TOP 3 ONLY)"""
        if not projects:
            return ""
        
        html = '<div class="section-title">📝 Notes</div>'
        html += '<table>'
        html += '<thead><tr><th>Project</th><th>User</th><th>Note</th><th>Date</th></tr></thead><tbody>'
        
        for project in projects[:3]:
            title = project.get('title', '') or project.get('project_title', '')
            user = project.get('owner', '-')
            note = project.get('description', '')[:80] if project.get('description') else 'No notes'
            date = project.get('last_updated', '-')
            
            if date and date != '-':
                try:
                    if hasattr(date, 'strftime'):
                        date = date.strftime('%m/%d %I:%M %p')
                    else:
                        date = str(date)[:16]
                except:
                    pass
            
            html += f'<tr><td><a href="#">{title[:40]}</a></td><td>{user}</td><td>{note}...</td><td>{date}</td></tr>'
        
        html += '</tbody></table>'
        return html
    
    def _send_email(
        self,
        to_emails: List[str],
        subject: str,
        html_body: str,
        cc_emails: List[str] = None
    ):
        """Send email via SMTP using built-in libraries, or save to file in mock mode"""
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.from_email
        msg['To'] = ', '.join(to_emails)
        
        if cc_emails:
            msg['Cc'] = ', '.join(cc_emails)
        
        # Attach HTML body
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)
        
        # Handle mock mode - save to file instead of sending
        if self.mock_mode:
            mock_dir = os.path.join(os.path.dirname(__file__), "mock_emails")
            os.makedirs(mock_dir, exist_ok=True)
            
            # Create filename with timestamp
            from datetime import datetime
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            filepath = os.path.join(mock_dir, filename)
            
            # Save the HTML content and metadata
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"<!-- EMAIL METADATA -->\n")
                f.write(f"<!-- From: {self.from_email} -->\n")
                f.write(f"<!-- To: {', '.join(to_emails)} -->\n")
                if cc_emails:
                    f.write(f"<!-- CC: {', '.join(cc_emails)} -->\n")
                f.write(f"<!-- Subject: {subject} -->\n")
                f.write(f"<!-- Timestamp: {datetime.now().isoformat()} -->\n")
                f.write(f"<!-- Mode: MOCK EMAIL (Not Actually Sent) -->\n")
                f.write(f"\n{html_body}\n")
            
            print(f"✅ [MOCK MODE] Email report saved to: {filepath}")
            return
        
        # Send via SMTP (production mode)
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                recipients = to_emails + (cc_emails if cc_emails else [])
                server.sendmail(self.from_email, recipients, msg.as_string())
                print(f"✅ Email sent successfully to {', '.join(to_emails)}")
        except Exception as e:
            print(f"❌ Error sending email: {str(e)}")
            raise
