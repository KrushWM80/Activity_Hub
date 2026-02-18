"""
Email Service for Intake Hub Reporting
Handles report generation, email composition, and PDF generation
"""

import os
import io
import json
import uuid
import smtplib
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# PDF generation
try:
    from reportlab.lib.pagesizes import letter, landscape
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.units import inch
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("⚠️ reportlab not installed. PDF generation will be disabled.")

from email_report_models import (
    EmailReportConfig, ReportContentType, ReportTimeframe,
    ReportFormat, ReportGenerationResponse
)
from database import DatabaseService
from models import FilterCriteria, ProjectStatus


class EmailReportService:
    """Service for generating and sending email reports"""
    
    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service
        self.smtp_server = os.getenv("SMTP_SERVER", "mailhub.wal-mart.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "25"))
        self.from_email = os.getenv("FROM_EMAIL", "ATCTEAMSUPPORT@Walmart.com")
        
    async def generate_and_send_report(
        self, 
        config: EmailReportConfig,
        override_email: Optional[str] = None
    ) -> ReportGenerationResponse:
        """
        Generate and send a report based on configuration
        
        Args:
            config: Email report configuration
            override_email: Optional email to override recipients (for testing)
            
        Returns:
            ReportGenerationResponse with status and details
        """
        try:
            report_id = str(uuid.uuid4())
            
            # Step 1: Gather report data
            report_data = await self._gather_report_data(config)
            
            # Step 2: Generate HTML content
            html_content = self._generate_html_report(config, report_data)
            
            # Step 3: Generate PDF if needed
            pdf_data = None
            if config.report_format in [ReportFormat.PDF, ReportFormat.BOTH]:
                if PDF_AVAILABLE:
                    pdf_data = self._generate_pdf_report(config, report_data)
                else:
                    print("⚠️ PDF generation requested but reportlab not available")
            
            # Step 4: Send email
            recipients = [override_email] if override_email else [config.primary_email] + config.cc_emails
            self._send_email(
                to_emails=recipients,
                subject=f"{config.report_name} - {datetime.now().strftime('%B %d, %Y')}",
                html_body=html_content,
                pdf_attachment=pdf_data,
                attachment_name=f"{config.report_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
            )
            
            return ReportGenerationResponse(
                success=True,
                message="Report generated and sent successfully",
                report_id=report_id,
                sent_to=recipients,
                generated_at=datetime.utcnow()
            )
            
        except Exception as e:
            return ReportGenerationResponse(
                success=False,
                message=f"Failed to generate report: {str(e)}",
                report_id=None,
                sent_to=[],
                generated_at=datetime.utcnow()
            )
    
    async def _gather_report_data(self, config: EmailReportConfig) -> Dict:
        """Gather all data needed for the report"""
        
        # Build filter criteria from config
        filters = FilterCriteria()
        filters.status = ProjectStatus.ACTIVE
        
        if config.filters.partner:
            filters.tribe = config.filters.partner
        if config.filters.store_area:
            filters.store_area = config.filters.store_area
        if config.filters.business_organization:
            filters.business_area = config.filters.business_organization
        if config.filters.phase:
            filters.phase = config.filters.phase
        if config.filters.owner:
            # Owner filtering needs custom handling
            pass
        
        # Get projects based on filters
        projects = await self.db_service.get_projects(filters)
        
        # Get summary statistics
        summary = await self.db_service.get_summary(filters)
        
        # Calculate date ranges based on timeframes
        date_ranges = self._calculate_date_ranges(config.timeframes)
        
        # Organize data by content type
        report_data = {
            "config": config,
            "generated_at": datetime.now(),
            "date_ranges": date_ranges,
            "projects": projects,
            "summary": summary,
            "content_sections": {}
        }
        
        # Generate each requested content type
        for content_type in config.content_types:
            if content_type == ReportContentType.OVERVIEW:
                report_data["content_sections"]["overview"] = self._generate_overview_section(projects, summary)
            
            elif content_type == ReportContentType.COUNTS:
                report_data["content_sections"]["counts"] = self._generate_counts_section(projects)
            
            elif content_type == ReportContentType.NEW:
                report_data["content_sections"]["new"] = self._generate_new_cards_section(projects, date_ranges)
            
            elif content_type == ReportContentType.UPCOMING:
                report_data["content_sections"]["upcoming"] = self._generate_upcoming_section(projects)
            
            elif content_type == ReportContentType.NOTES:
                report_data["content_sections"]["notes"] = self._generate_notes_section(projects)
            
            elif content_type == ReportContentType.MY_ACTIONS:
                report_data["content_sections"]["my_actions"] = self._generate_my_actions_section(config)
            
            elif content_type.value.startswith("Activity Feed"):
                report_data["content_sections"]["activity_feed"] = self._generate_activity_feed_section(
                    projects, content_type
                )
        
        return report_data
    
    def _calculate_date_ranges(self, timeframes: List[ReportTimeframe]) -> Dict[str, Tuple[datetime, datetime]]:
        """Calculate start and end dates for each timeframe"""
        ranges = {}
        now = datetime.now()
        
        for timeframe in timeframes:
            if timeframe == ReportTimeframe.CURRENT_DAY:
                ranges["current_day"] = (now.replace(hour=0, minute=0, second=0), now)
            
            elif timeframe == ReportTimeframe.CURRENT_WEEK:
                start_of_week = now - timedelta(days=now.weekday())
                ranges["current_week"] = (start_of_week.replace(hour=0, minute=0, second=0), now)
            
            elif timeframe == ReportTimeframe.CURRENT_MONTH:
                start_of_month = now.replace(day=1, hour=0, minute=0, second=0)
                ranges["current_month"] = (start_of_month, now)
            
            elif timeframe == ReportTimeframe.CURRENT_YEAR:
                start_of_year = now.replace(month=1, day=1, hour=0, minute=0, second=0)
                ranges["current_year"] = (start_of_year, now)
            
            elif timeframe == ReportTimeframe.LAST_7_DAYS:
                ranges["last_7_days"] = (now - timedelta(days=7), now)
            
            elif timeframe == ReportTimeframe.LAST_30_DAYS:
                ranges["last_30_days"] = (now - timedelta(days=30), now)
        
        return ranges
    
    def _generate_overview_section(self, projects, summary) -> Dict:
        """Generate overview statistics"""
        return {
            "total_projects": summary.total_active_projects,
            "total_stores": summary.total_stores,
            "intake_hub_projects": summary.intake_hub_projects,
            "intake_hub_stores": summary.intake_hub_stores,
            "realty_projects": summary.realty_projects,
            "realty_stores": summary.realty_stores,
            "by_phase": summary.by_phase if hasattr(summary, 'by_phase') else {},
            "by_division": summary.by_division if hasattr(summary, 'by_division') else {}
        }
    
    def _generate_counts_section(self, projects) -> Dict:
        """Generate count breakdowns"""
        counts = {
            "by_business_org": {},
            "by_store_area": {},
            "by_phase": {},
            "by_partner": {}
        }
        
        for project in projects:
            # Count by business area
            if project.business_area:
                counts["by_business_org"][project.business_area] = \
                    counts["by_business_org"].get(project.business_area, 0) + 1
            
            # Count by store area
            if project.store_area:
                counts["by_store_area"][project.store_area] = \
                    counts["by_store_area"].get(project.store_area, 0) + 1
            
            # Count by phase
            if project.phase:
                counts["by_phase"][project.phase] = \
                    counts["by_phase"].get(project.phase, 0) + 1
            
            # Count by partner (tribe)
            if project.tribe:
                counts["by_partner"][project.tribe] = \
                    counts["by_partner"].get(project.tribe, 0) + 1
        
        return counts
    
    def _generate_new_cards_section(self, projects, date_ranges) -> Dict:
        """Generate list of newly created cards"""
        new_cards = []
        
        # Get the most recent date range to determine "new"
        if "current_week" in date_ranges:
            cutoff_date = date_ranges["current_week"][0]
        elif "last_7_days" in date_ranges:
            cutoff_date = date_ranges["last_7_days"][0]
        else:
            cutoff_date = datetime.now() - timedelta(days=7)
        
        for project in projects:
            if project.created_date and project.created_date >= cutoff_date:
                new_cards.append({
                    "project_id": project.project_id,
                    "title": project.title,
                    "created_date": project.created_date,
                    "partner": project.tribe,
                    "phase": project.phase,
                    "store_count": project.store_count
                })
        
        return {
            "cutoff_date": cutoff_date,
            "count": len(new_cards),
            "cards": sorted(new_cards, key=lambda x: x["created_date"], reverse=True)
        }
    
    def _generate_upcoming_section(self, projects) -> Dict:
        """Generate list of cards with upcoming dates"""
        upcoming = []
        now = datetime.now()
        two_weeks_from_now = now + timedelta(days=14)
        
        for project in projects:
            # This would check for upcoming implementation dates
            # You'll need to adjust based on your actual date fields
            if hasattr(project, 'implementation_date') and project.implementation_date:
                if now <= project.implementation_date <= two_weeks_from_now:
                    upcoming.append({
                        "project_id": project.project_id,
                        "title": project.title,
                        "upcoming_date": project.implementation_date,
                        "days_until": (project.implementation_date - now).days,
                        "partner": project.tribe,
                        "phase": project.phase
                    })
        
        return {
            "count": len(upcoming),
            "cards": sorted(upcoming, key=lambda x: x["upcoming_date"])
        }
    
    def _generate_notes_section(self, projects) -> Dict:
        """Generate notes section (placeholder - needs notes table)"""
        # This would query a notes table if available
        return {
            "note": "Notes functionality requires additional database tables",
            "projects_with_notes": []
        }
    
    def _generate_my_actions_section(self, config) -> Dict:
        """Generate my actions section (placeholder - needs actions/tasks table)"""
        # This would query tasks assigned to the user
        return {
            "note": "Actions functionality requires additional database tables",
            "incomplete_actions": []
        }
    
    def _generate_activity_feed_section(self, projects, content_type: ReportContentType) -> Dict:
        """Generate activity feed section (placeholder - needs activity log table)"""
        # This would query activity logs filtered by type
        return {
            "note": f"Activity feed functionality requires additional database tables",
            "activity_type": content_type.value,
            "activities": []
        }
    
    def _generate_html_report(self, config: EmailReportConfig, report_data: Dict) -> str:
        """Generate HTML email content"""
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #0071ce 0%, #004f9a 100%);
            color: white;
            padding: 30px;
            border-radius: 10px 10px 0 0;
            margin-bottom: 0;
        }}
        .header h1 {{
            margin: 0;
            font-size: 28px;
        }}
        .header .subtitle {{
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 14px;
        }}
        .content {{
            background: white;
            padding: 30px;
            border-radius: 0 0 10px 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .section {{
            margin-bottom: 30px;
            border-left: 4px solid #0071ce;
            padding-left: 20px;
        }}
        .section h2 {{
            color: #0071ce;
            font-size: 22px;
            margin-top: 0;
        }}
        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        .stat-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #0071ce;
        }}
        .stat-card .number {{
            font-size: 32px;
            font-weight: bold;
            color: #0071ce;
            margin: 0;
        }}
        .stat-card .label {{
            font-size: 14px;
            color: #666;
            margin: 5px 0 0 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
        }}
        th {{
            background: #0071ce;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #e0e0e0;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        .project-link {{
            color: #0071ce;
            text-decoration: none;
            font-weight: 500;
        }}
        .project-link:hover {{
            text-decoration: underline;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }}
        .badge-success {{
            background: #d4edda;
            color: #155724;
        }}
        .badge-warning {{
            background: #fff3cd;
            color: #856404;
        }}
        .badge-info {{
            background: #d1ecf1;
            color: #0c5460;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 12px;
            margin-top: 30px;
        }}
        .timestamp {{
            color: #999;
            font-size: 12px;
            margin-top: 10px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 {config.report_name}</h1>
        <div class="subtitle">Intake Hub Automated Report</div>
        <div class="timestamp">Generated: {report_data['generated_at'].strftime('%B %d, %Y at %I:%M %p')}</div>
    </div>
    
    <div class="content">
"""
        
        # Add Overview section if requested
        if "overview" in report_data["content_sections"]:
            overview = report_data["content_sections"]["overview"]
            html += f"""
        <div class="section">
            <h2>📈 Overview</h2>
            <div class="stat-grid">
                <div class="stat-card">
                    <div class="number">{overview['total_projects']}</div>
                    <div class="label">Total Active Projects</div>
                </div>
                <div class="stat-card">
                    <div class="number">{overview['total_stores']}</div>
                    <div class="label">Total Facilities</div>
                </div>
                <div class="stat-card">
                    <div class="number">{overview['intake_hub_projects']}</div>
                    <div class="label">Intake Hub Projects</div>
                </div>
                <div class="stat-card">
                    <div class="number">{overview['realty_projects']}</div>
                    <div class="label">Realty Projects</div>
                </div>
            </div>
        </div>
"""
        
        # Add Counts section if requested
        if "counts" in report_data["content_sections"]:
            counts = report_data["content_sections"]["counts"]
            html += f"""
        <div class="section">
            <h2>📊 Card Counts</h2>
"""
            if counts["by_business_org"]:
                html += "<h3>By Business Organization</h3><table><tr><th>Organization</th><th>Count</th></tr>"
                for org, count in sorted(counts["by_business_org"].items(), key=lambda x: x[1], reverse=True):
                    html += f"<tr><td>{org}</td><td><strong>{count}</strong></td></tr>"
                html += "</table>"
            
            if counts["by_store_area"]:
                html += "<h3>By Store Area</h3><table><tr><th>Store Area</th><th>Count</th></tr>"
                for area, count in sorted(counts["by_store_area"].items(), key=lambda x: x[1], reverse=True):
                    html += f"<tr><td>{area}</td><td><strong>{count}</strong></td></tr>"
                html += "</table>"
            
            html += "</div>"
        
        # Add New Cards section if requested
        if "new" in report_data["content_sections"]:
            new_section = report_data["content_sections"]["new"]
            html += f"""
        <div class="section">
            <h2>🆕 New Cards ({new_section['count']})</h2>
            <p>Cards created since {new_section['cutoff_date'].strftime('%B %d, %Y')}</p>
"""
            if new_section["cards"]:
                html += "<table><tr><th>Card #</th><th>Title</th><th>Partner</th><th>Phase</th><th>Facilities</th><th>Created</th></tr>"
                for card in new_section["cards"]:
                    html += f"""
                    <tr>
                        <td>{card['project_id']}</td>
                        <td><a href="#" class="project-link">{card['title']}</a></td>
                        <td>{card['partner'] or 'N/A'}</td>
                        <td><span class="badge badge-info">{card['phase']}</span></td>
                        <td>{card['store_count']}</td>
                        <td>{card['created_date'].strftime('%m/%d/%Y') if card['created_date'] else 'N/A'}</td>
                    </tr>
"""
                html += "</table>"
            else:
                html += "<p><em>No new cards in this period.</em></p>"
            html += "</div>"
        
        # Add Upcoming section if requested
        if "upcoming" in report_data["content_sections"]:
            upcoming = report_data["content_sections"]["upcoming"]
            html += f"""
        <div class="section">
            <h2>📅 Upcoming ({upcoming['count']})</h2>
            <p>Cards with dates in the next 2 weeks</p>
"""
            if upcoming["cards"]:
                html += "<table><tr><th>Card #</th><th>Title</th><th>Partner</th><th>Phase</th><th>Date</th><th>Days Until</th></tr>"
                for card in upcoming["cards"]:
                    html += f"""
                    <tr>
                        <td>{card['project_id']}</td>
                        <td><a href="#" class="project-link">{card['title']}</a></td>
                        <td>{card['partner'] or 'N/A'}</td>
                        <td><span class="badge badge-warning">{card['phase']}</span></td>
                        <td>{card['upcoming_date'].strftime('%m/%d/%Y')}</td>
                        <td><strong>{card['days_until']} days</strong></td>
                    </tr>
"""
                html += "</table>"
            else:
                html += "<p><em>No upcoming items in the next 2 weeks.</em></p>"
            html += "</div>"
        
        # Add main projects table
        if report_data["projects"]:
            html += f"""
        <div class="section">
            <h2>📋 Projects ({len(report_data['projects'])})</h2>
            <table>
                <tr>
                    <th>Card #</th>
                    <th>Title</th>
"""
            
            # Add column headers based on config
            if config.columns.partner:
                html += "<th>Partner</th>"
            if config.columns.business_organization:
                html += "<th>Business Org</th>"
            if config.columns.store_area:
                html += "<th>Store Area</th>"
            if config.columns.owner:
                html += "<th>Owner</th>"
            if config.columns.phase:
                html += "<th>Phase</th>"
            html += "<th>Facilities</th></tr>"
            
            # Add project rows
            for project in report_data["projects"][:50]:  # Limit to first 50 for email
                html += f"""
                <tr>
                    <td>{project.project_id}</td>
                    <td><a href="#" class="project-link">{project.title}</a></td>
"""
                if config.columns.partner:
                    html += f"<td>{project.tribe or 'N/A'}</td>"
                if config.columns.business_organization:
                    html += f"<td>{project.business_area or 'N/A'}</td>"
                if config.columns.store_area:
                    html += f"<td>{project.store_area or 'N/A'}</td>"
                if config.columns.owner:
                    html += f"<td>{project.owner or 'N/A'}</td>"
                if config.columns.phase:
                    html += f"<td><span class='badge badge-info'>{project.phase}</span></td>"
                html += f"<td>{project.store_count}</td></tr>"
            
            if len(report_data["projects"]) > 50:
                html += f"<tr><td colspan='10' style='text-align:center; font-style:italic;'>Showing first 50 of {len(report_data['projects'])} projects. See attached PDF for complete list.</td></tr>"
            
            html += "</table></div>"
        
        html += """
    </div>
    
    <div class="footer">
        <p>This is an automated report from Intake Hub. Do not reply to this email.</p>
        <p>To modify your report settings, log in to Intake Hub and visit the Reports section.</p>
    </div>
</body>
</html>
"""
        
        return html
    
    def _generate_pdf_report(self, config: EmailReportConfig, report_data: Dict) -> bytes:
        """Generate PDF attachment"""
        if not PDF_AVAILABLE:
            return None
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#0071ce'),
            spaceAfter=30
        )
        story.append(Paragraph(config.report_name, title_style))
        story.append(Paragraph(f"Generated: {report_data['generated_at'].strftime('%B %d, %Y at %I:%M %p')}", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Overview section
        if "overview" in report_data["content_sections"]:
            overview = report_data["content_sections"]["overview"]
            story.append(Paragraph("Overview", styles['Heading2']))
            
            overview_data = [
                ['Metric', 'Value'],
                ['Total Active Projects', str(overview['total_projects'])],
                ['Total Facilities', str(overview['total_stores'])],
                ['Intake Hub Projects', str(overview['intake_hub_projects'])],
                ['Realty Projects', str(overview['realty_projects'])]
            ]
            
            t = Table(overview_data, colWidths=[4*inch, 2*inch])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0071ce')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(t)
            story.append(Spacer(1, 0.3*inch))
        
        # Projects table
        if report_data["projects"]:
            story.append(Paragraph(f"Projects ({len(report_data['projects'])})", styles['Heading2']))
            
            # Build table data
            headers = ['Card #', 'Title']
            if config.columns.partner:
                headers.append('Partner')
            if config.columns.phase:
                headers.append('Phase')
            headers.append('Facilities')
            
            table_data = [headers]
            
            for project in report_data["projects"]:
                row = [project.project_id, project.title[:50]]  # Truncate title
                if config.columns.partner:
                    row.append(project.tribe or 'N/A')
                if config.columns.phase:
                    row.append(project.phase)
                row.append(str(project.store_count))
                table_data.append(row)
            
            t = Table(table_data, repeatRows=1)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0071ce')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]))
            story.append(t)
        
        # Build PDF
        doc.build(story)
        pdf_data = buffer.getvalue()
        buffer.close()
        
        return pdf_data
    
    def _send_email(
        self,
        to_emails: List[str],
        subject: str,
        html_body: str,
        pdf_attachment: Optional[bytes] = None,
        attachment_name: str = "report.pdf"
    ):
        """Send email via SMTP"""
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.from_email
        msg['To'] = ', '.join(to_emails)
        
        # Attach HTML body
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)
        
        # Attach PDF if provided
        if pdf_attachment:
            pdf_part = MIMEBase('application', 'pdf')
            pdf_part.set_payload(pdf_attachment)
            encoders.encode_base64(pdf_part)
            pdf_part.add_header('Content-Disposition', f'attachment; filename="{attachment_name}"')
            msg.attach(pdf_part)
        
        # Send email
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.send_message(msg)
                print(f"✅ Report email sent to {', '.join(to_emails)}")
        except Exception as e:
            print(f"⚠️ Failed to send email: {str(e)}")
            raise
