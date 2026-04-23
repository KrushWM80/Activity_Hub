"""
Dallas Team Report Email Service
Sends Dallas Team Report via Walmart internal SMTP (no Outlook dependency)
"""

import logging
import smtplib
import base64
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import json

SMTP_SERVER = "smtp-gw1.homeoffice.wal-mart.com"
SMTP_PORT = 25
FROM_EMAIL = "kendall.rush@walmart.com"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VETEmailService:
    """Service to send Dallas Team Report emails"""
    
    def __init__(self):
        """Initialize email service"""
        self.from_email = FROM_EMAIL
    
    def generate_html_body(self, report_data: Dict[str, Any], ppt_filename: str) -> str:
        """
        Generate HTML email body for Dallas Team Report - Dashboard format
        
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
        dashboard_html = report_data.get('dashboard_html', None)
        
        # Don't embed exec summary HTML — build Outlook-compatible version instead
        dashboard_html_section = ''
        
        # Load Spark logo as base64 for email header
        spark_b64 = ''
        for logo_path in [
            os.path.join(os.path.dirname(__file__), 'Spark_Blank.png'),
            os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Interface', 'Spark_Blank.png'),
        ]:
            if os.path.exists(logo_path):
                with open(logo_path, 'rb') as _f:
                    spark_b64 = base64.b64encode(_f.read()).decode('ascii')
                break
        spark_img_html = f'<img src="data:image/png;base64,{spark_b64}" width="36" height="36" alt="Spark" style="vertical-align:middle;margin-right:12px;">' if spark_b64 else ''
        
        # Calculate percentages
        pct_on_track = (on_track / total_projects * 100) if total_projects > 0 else 0
        pct_at_risk = (at_risk / total_projects * 100) if total_projects > 0 else 0
        pct_off_track = (off_track / total_projects * 100) if total_projects > 0 else 0
        avg_stores = (total_stores / total_projects) if total_projects > 0 else 0
        
        html = f"""
<html>
<head>
    <meta charset="UTF-8">
    <title>Dallas Team Report</title>
</head>
<body style="font-family: Arial, sans-serif; color: #333; margin: 0; padding: 0; background-color: white;">

<table style="width: 100%; max-width: 800px; margin: 0; background-color: white;" cellpadding="0" cellspacing="0" border="0">
    
    <!-- HEADER -->
    <tr>
        <td style="background-color: #1e3a8a; color: #ffffff; padding: 32px 24px; text-align: center; font-weight: bold;">
            <h1 style="margin: 0 0 8px 0; font-size: 32px; font-weight: 700; color: #ffffff; letter-spacing: -0.5px;">{spark_img_html}Dallas Team Report</h1>
            <p style="margin: 0; font-size: 14px; font-weight: 500; color: #ffffff; letter-spacing: 0.5px;">Walmart Enterprise Transformation Dashboard</p>
        </td>
    </tr>
    
    <!-- GO TO DASHBOARD BUTTON -->
    <tr>
        <td style="background-color: #f0f4ff; padding: 12px 24px; text-align: center;">
            <table cellpadding="0" cellspacing="0" border="0" style="margin: 0 auto;">
                <tr>
                    <td style="background-color: #0071ce; border-radius: 6px; padding: 10px 24px; text-align: center;">
                        <a href="http://localhost:5001/Dallas_Team_Report" style="color: #ffffff; font-size: 14px; font-weight: 700; text-decoration: none; display: inline-block;">Go to Dashboard</a>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
    
    <!-- CONTENT -->
    <tr>
        <td style="padding: 24px;">
            
            <!-- Section Title -->
            <h2 style="font-size: 16px; font-weight: 700; color: #1e3a8a; margin: 0 0 14px 0; text-transform: uppercase; border-bottom: 2px solid #0071ce; padding-bottom: 6px;">Executive Summary</h2>
            
            <!-- Stats - Table Layout for Outlook Compatibility -->
            <table style="width: 100%; margin-bottom: 20px; border-collapse: collapse;" cellpadding="0" cellspacing="0" border="0">
                <tr>
                    <td style="width: 25%; background-color: #f8f9fa; border-left: 4px solid #0071ce; padding: 12px 8px; text-align: center; font-size: 22px; font-weight: 700; color: #1e3a8a; line-height: 1.3;">{total_projects}</td>
                    <td style="width: 25%; background-color: #f8f9fa; border-left: 4px solid #107c10; padding: 12px 8px; text-align: center; font-size: 22px; font-weight: 700; color: #107c10; line-height: 1.3;">{on_track}</td>
                    <td style="width: 25%; background-color: #f8f9fa; border-left: 4px solid #f7630c; padding: 12px 8px; text-align: center; font-size: 22px; font-weight: 700; color: #f7630c; line-height: 1.3;">{at_risk}</td>
                    <td style="width: 25%; background-color: #f8f9fa; border-left: 4px solid #dc3545; padding: 12px 8px; text-align: center; font-size: 22px; font-weight: 700; color: #dc3545; line-height: 1.3;">{off_track}</td>
                </tr>
                <tr>
                    <td style="text-align: center; font-size: 10px; color: #666; text-transform: uppercase; font-weight: 600; letter-spacing: 0.3px; padding: 6px 4px;">Total Projects</td>
                    <td style="text-align: center; font-size: 10px; color: #666; text-transform: uppercase; font-weight: 600; letter-spacing: 0.3px; padding: 6px 4px;">On Track</td>
                    <td style="text-align: center; font-size: 10px; color: #666; text-transform: uppercase; font-weight: 600; letter-spacing: 0.3px; padding: 6px 4px;">At Risk</td>
                    <td style="text-align: center; font-size: 10px; color: #666; text-transform: uppercase; font-weight: 600; letter-spacing: 0.3px; padding: 6px 4px;">Off Track</td>
                </tr>
            </table>
            
            <!-- Key Insights -->
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 18px; background-color: #f0f4ff; border-left: 4px solid #0071ce;" cellpadding="0" cellspacing="0" border="0">
                <tr>
                    <td style="padding: 14px;">
                        <h3 style="margin: 0 0 10px 0; font-size: 12px; color: #1e3a8a; text-transform: uppercase; font-weight: 700; letter-spacing: 0.3px;">Key Insights</h3>
                        <ul style="margin: 0; padding-left: 18px; list-style: none;">
                            <li style="margin: 6px 0; color: #333; font-size: 12px; line-height: 1.4;"><span style="color: #0071ce; font-weight: 700;">•</span> <strong>{pct_on_track:.1f}%</strong> of initiatives are on track</li>
                            <li style="margin: 6px 0; color: #333; font-size: 12px; line-height: 1.4;"><span style="color: #0071ce; font-weight: 700;">•</span> <strong>{pct_at_risk:.1f}%</strong> of initiatives are at risk</li>
                            <li style="margin: 6px 0; color: #333; font-size: 12px; line-height: 1.4;"><span style="color: #0071ce; font-weight: 700;">•</span> <strong>{pct_off_track:.1f}%</strong> of initiatives are off track</li>
                        </ul>
                    </td>
                </tr>
            </table>
            
            <!-- Dashboard Content Section -->
            {dashboard_html_section}
            
            <p style="font-size: 11px; color: #666; margin: 14px 0; line-height: 1.5;">
                <strong>Report Contents:</strong> PowerPoint and PDF attachments include detailed phase summaries, health status metrics, store counts, and strategic initiatives for each project phase.
            </p>
            
        </td>
    </tr>
    
    <!-- FOOTER -->
    <tr>
        <td style="background-color: #f8f9fa; padding: 14px; text-align: center; font-size: 10px; color: #999; border-top: 1px solid #e0e0e0;">
            <p style="margin: 0;">Data Source: Walmart Enterprise Transformation Dashboard | {datetime.now().strftime('%B %d, %Y')}</p>
        </td>
    </tr>
    
</table>

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
        Send Dallas Team Report email with attachments
        
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
            html_body = self.generate_html_body(report_data, "Dallas_Team_Report.pptx")
            
            # Use default subject if not provided (include WM Week)
            if not subject:
                wm_week = report_data.get('wm_week', 'Current')
                subject = f"Dallas Team Report - {wm_week}"
            
            # Format attachment info for logging
            attachment_info = ", ".join([Path(p).name for p in valid_attachments])
            
            logger.info(f"📧 Creating email:")
            logger.info(f"  To: {', '.join(to_recipients)}")
            logger.info(f"  Subject: {subject}")
            logger.info(f"  Attachments: {attachment_info}")
            
            # Build MIME message
            msg = MIMEMultipart('mixed')
            msg['From'] = FROM_EMAIL
            msg['To'] = '; '.join(to_recipients)
            msg['Subject'] = subject
            msg.attach(MIMEText(html_body, 'html', 'utf-8'))
            
            # Attach all files
            for attachment_file in valid_attachments:
                with open(attachment_file, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{Path(attachment_file).name}"')
                msg.attach(part)
                logger.info(f"✓ Attached: {Path(attachment_file).name}")
            
            if test_mode:
                logger.info("📝 [TEST MODE] Email built but not sent")
                return True
            
            # Send via Walmart internal SMTP (no auth required)
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
                server.sendmail(FROM_EMAIL, to_recipients, msg.as_string())
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
    Convenience function to send Dallas Team Report
    
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
