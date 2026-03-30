"""
V.E.T. Executive Report Email Service
Sends V.E.T. Dashboard reports via Outlook with HTML formatting
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VETEmailService:
    """Service to send V.E.T. Executive Report emails"""
    
    def __init__(self):
        """Initialize email service"""
        self.from_email = None
        self.outlook = None
        self.namespace = None
        self._initialize_outlook()
    
    def _initialize_outlook(self):
        """Initialize Outlook COM automation"""
        try:
            import win32com.client
            self.outlook = win32com.client.Dispatch('Outlook.Application')
            self.namespace = self.outlook.GetNamespace("MAPI")
            logger.info("✅ Outlook initialized successfully")
            return True
        except ImportError:
            logger.error("❌ pywin32 not installed. Cannot send emails.")
            return False
        except Exception as e:
            logger.error(f"❌ Error initializing Outlook: {e}")
            return False
    
    def generate_html_body(self, report_data: Dict[str, Any], ppt_filename: str) -> str:
        """
        Generate HTML email body for V.E.T. Executive Report - Dashboard format
        
        Args:
            report_data: Dictionary with report statistics and details
            ppt_filename: Name of the generated PowerPoint file
        
        Returns:
            HTML string for email body
        """
        
        total_projects = report_data.get('total_projects', 0)
        total_stores = report_data.get('total_stores', 0)
        on_track = report_data.get('on_track', 0)
        at_risk = report_data.get('at_risk', 0)
        off_track = report_data.get('off_track', 0)
        wm_week = report_data.get('wm_week', '')
        
        # Calculate percentages
        pct_on_track = (on_track / total_projects * 100) if total_projects > 0 else 0
        pct_at_risk = (at_risk / total_projects * 100) if total_projects > 0 else 0
        pct_off_track = (off_track / total_projects * 100) if total_projects > 0 else 0
        avg_stores = (total_stores / total_projects) if total_projects > 0 else 0
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>V.E.T. Executive Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
            background-color: #fafafa;
        }}
        .wrapper {{
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 4px;
            overflow: hidden;
            max-width: 800px;
            margin: 20px auto;
        }}
        .header {{
            background: linear-gradient(135deg, #1e3a8a 0%, #0071ce 100%);
            color: white;
            padding: 24px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0 0 8px 0;
            font-size: 32px;
            font-weight: bold;
            color: white;
        }}
        .header p {{
            margin: 0;
            font-size: 16px;
            opacity: 0.9;
        }}
        .content {{
            padding: 24px;
        }}
        h2 {{
            font-size: 18px;
            color: #1e3a8a;
            margin: 0 0 16px 0;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: bold;
            border-bottom: 2px solid #0071ce;
            padding-bottom: 8px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 12px;
            margin-bottom: 24px;
        }}
        .stat-item {{
            background-color: #f8f9fa;
            border-left: 4px solid #0071ce;
            padding: 14px 10px;
            text-align: center;
            border-radius: 4px;
        }}
        .stat-number {{
            font-size: 28px;
            font-weight: bold;
            color: #1e3a8a;
            margin: 0;
        }}
        .stat-label {{
            font-size: 11px;
            color: #666;
            text-transform: uppercase;
            margin-top: 6px;
            font-weight: 600;
            letter-spacing: 0.5px;
        }}
        .stat-item.on-track {{
            border-left-color: #107c10;
        }}
        .stat-item.on-track .stat-number {{
            color: #107c10;
        }}
        .stat-item.at-risk {{
            border-left-color: #f7630c;
        }}
        .stat-item.at-risk .stat-number {{
            color: #f7630c;
        }}
        .stat-item.off-track {{
            border-left-color: #dc3545;
        }}
        .stat-item.off-track .stat-number {{
            color: #dc3545;
        }}
        .insights-box {{
            background-color: #f0f4ff;
            border-left: 4px solid #0071ce;
            padding: 16px;
            border-radius: 4px;
            margin-bottom: 20px;
        }}
        .insights-box h3 {{
            margin: 0 0 12px 0;
            font-size: 13px;
            color: #1e3a8a;
            text-transform: uppercase;
            font-weight: bold;
            letter-spacing: 0.5px;
        }}
        .insights-box ul {{
            margin: 0;
            padding-left: 20px;
            list-style-type: none;
        }}
        .insights-box li {{
            margin: 8px 0;
            color: #333;
            font-size: 13px;
            line-height: 1.5;
        }}
        .insights-box li:before {{
            content: '•';
            color: #0071ce;
            font-weight: bold;
            margin-right: 8px;
        }}
        .footer {{
            background-color: #f8f9fa;
            padding: 16px;
            text-align: center;
            font-size: 11px;
            color: #666;
            border-top: 1px solid #e0e0e0;
        }}
        @media (max-width: 600px) {{
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="header">
            <h1>V.E.T. Executive Report</h1>
            <p>Walmart Enterprise Transformation Dashboard</p>
        </div>
        
        <div class="content">
            <h2>Executive Summary</h2>
            
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-number">{total_projects}</div>
                    <div class="stat-label">Total Projects</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{total_stores:,}</div>
                    <div class="stat-label">Stores Impacted</div>
                </div>
                <div class="stat-item on-track">
                    <div class="stat-number">{on_track}</div>
                    <div class="stat-label">On Track</div>
                </div>
                <div class="stat-item at-risk">
                    <div class="stat-number">{at_risk}</div>
                    <div class="stat-label">At Risk</div>
                </div>
                <div class="stat-item off-track">
                    <div class="stat-number">{off_track}</div>
                    <div class="stat-label">Off Track</div>
                </div>
            </div>
            
            <div class="insights-box">
                <h3>Key Insights</h3>
                <ul>
                    <li><strong>{pct_on_track:.1f}%</strong> of initiatives are on track</li>
                    <li><strong>{pct_at_risk:.1f}%</strong> of initiatives are at risk</li>
                    <li><strong>{pct_off_track:.1f}%</strong> of initiatives are off track</li>
                    <li>Average stores per initiative: <strong>{avg_stores:.0f}</strong></li>
                </ul>
            </div>
            
            <p style="font-size: 12px; color: #666; margin: 16px 0; line-height: 1.5;">
                <strong>Report Contents:</strong> PowerPoint attachment includes detailed phase summaries, health status metrics, store counts, and strategic initiatives for each project.
            </p>
        </div>
        
        <div class="footer">
            <p style="margin: 0;">Data Source: Walmart Enterprise Transformation Dashboard | {datetime.now().strftime('%B %d, %Y')}</p>
        </div>
    </div>
</body>
</html>
        """
        
        return html
    
    def send_report_email(
        self,
        to_recipients: List[str],
        report_data: Dict[str, Any],
        attachment_paths: List[str] = None,
        ppt_file_path: str = None,
        subject: str = None,
        test_mode: bool = False
    ) -> bool:
        """
        Send V.E.T. Executive Report email with attachments
        
        Args:
            to_recipients: List of email addresses to send to
            report_data: Dictionary with report statistics
            attachment_paths: List of file paths to attach (PPTX, PDF, etc.)
            ppt_file_path: (Deprecated) Full path to PowerPoint file - use attachment_paths instead
            subject: Custom email subject (optional)
            test_mode: If True, just generate email without sending
        
        Returns:
            True if successful, False otherwise
        """
        
        if not self.outlook:
            logger.error("❌ Outlook not initialized. Cannot send email.")
            return False
        
        try:
            # Support both old single ppt_file_path and new attachment_paths list
            if attachment_paths is None:
                attachment_paths = []
            if ppt_file_path:
                attachment_paths.insert(0, ppt_file_path)
            
            # Validate all attachment files exist
            valid_attachments = []
            for file_path in attachment_paths:
                path = Path(file_path)
                if path.exists():
                    valid_attachments.append(str(path.absolute()))
                else:
                    logger.warning(f"⚠️  Attachment file not found, skipping: {file_path}")
            
            if not valid_attachments:
                logger.error("❌ No valid attachment files found")
                return False
            
            # Generate email body
            html_body = self.generate_html_body(report_data, "VET_Executive_Report.pptx")
            
            # Use default subject if not provided (include WM Week)
            if not subject:
                wm_week = report_data.get('wm_week', 'Current')
                subject = f"V.E.T. Executive Report - {wm_week}"
            
            # Format attachment info for logging
            attachment_info = ", ".join([Path(p).name for p in valid_attachments])
            
            logger.info(f"📧 Creating email:")
            logger.info(f"  To: {', '.join(to_recipients)}")
            logger.info(f"  Subject: {subject}")
            logger.info(f"  Attachments: {attachment_info}")
            
            # Create email
            mail = self.outlook.CreateItem(0)  # 0 = olMailItem
            mail.To = '; '.join(to_recipients)
            mail.Subject = subject
            mail.HTMLBody = html_body
            
            # Attach all files
            for attachment_file in valid_attachments:
                mail.Attachments.Add(attachment_file)
                logger.info(f"✓ Attached: {Path(attachment_file).name}")
            
            # In test mode, just save as draft without sending
            if test_mode:
                mail.Save()
                logger.info("📝 [TEST MODE] Email saved as draft (not sent)")
                return True
            
            # Send email
            mail.Send()
            logger.info(f"✅ Email sent successfully to {len(to_recipients)} recipient(s)")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error sending email: {e}")
            import traceback
            traceback.print_exc()
            return False


def send_vet_report_email(
    to_recipients: List[str] = None,
    report_data: Dict[str, Any] = None,
    ppt_file_path: str = None,
    test_mode: bool = False
) -> bool:
    """
    Convenience function to send V.E.T. Executive Report
    
    Args:
        to_recipients: List of email addresses (default: kendall.rush@walmart.com)
        report_data: Report statistics dictionary
        ppt_file_path: Path to PowerPoint file
        test_mode: If True, save as draft instead of sending
    
    Returns:
        True if successful
    """
    if to_recipients is None:
        to_recipients = ['kendall.rush@walmart.com']
    
    service = VETEmailService()
    return service.send_report_email(to_recipients, report_data, ppt_file_path, test_mode=test_mode)


if __name__ == '__main__':
    """Test the email service"""
    
    # Example usage
    test_report_data = {
        'total_projects': 96,
        'total_stores': 1845,
        'on_track': 68,
        'at_risk': 20,
        'off_track': 8,
        'wm_week': 'WK12-WK13'
    }
    
    # Example PPT file (would come from actual generation)
    # ppt_file_path = r"C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\VET_Dashboard\reports\VET_Executive_Report_20260330_120000.pptx"
    
    # Send test email
    # send_vet_report_email(['your.email@walmart.com'], test_report_data, ppt_file_path, test_mode=True)
    
    print("✅ V.E.T. Email Service initialized and ready to use")
