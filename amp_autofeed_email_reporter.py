"""
AMP AutoFeed Validation - Email Report Generator
Sends daily validation results via email
"""

import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional


class ValidationReportEmail:
    """Generate and send validation report emails"""
    
    def __init__(self, 
                 smtp_server: str = "smtp.gmail.com",
                 smtp_port: int = 587,
                 sender_email: str = None,
                 sender_password: str = None,
                 recipient_email: str = None):
        """
        Initialize email reporter
        
        For Gmail: Use app-specific password (not regular password)
        For Outlook/Office365: Use office365 connector or your email password
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipient_email = recipient_email or sender_email
    
    def generate_html_report(self, validation_result: Dict) -> str:
        """Generate HTML email report from validation results"""
        
        status = validation_result.get('status', 'UNKNOWN')
        status_color = {
            'PASS': '#28a745',
            'FAIL': '#dc3545', 
            'ERROR': '#fd7e14',
        }.get(status, '#6c757d')
        
        date = validation_result.get('date', 'Unknown')
        timestamp = validation_result.get('timestamp', '')
        
        comparison = validation_result.get('comparison', {})
        differences = comparison.get('differences', [])
        
        qb_found = validation_result.get('qb_email_found', False)
        amp_found = validation_result.get('amp_email_found', False)
        
        html = f"""
        <html>
            <head>
                <style>
                    body {{ 
                        font-family: Arial, sans-serif; 
                        margin: 0; 
                        padding: 20px;
                        background-color: #f5f5f5;
                    }}
                    .container {{
                        max-width: 800px;
                        background-color: white;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }}
                    .header {{
                        border-bottom: 3px solid {status_color};
                        margin-bottom: 20px;
                        padding-bottom: 10px;
                    }}
                    .status-badge {{
                        display: inline-block;
                        background-color: {status_color};
                        color: white;
                        padding: 8px 16px;
                        border-radius: 4px;
                        font-weight: bold;
                        font-size: 18px;
                    }}
                    .section {{
                        margin: 15px 0;
                        padding: 15px;
                        background-color: #f9f9f9;
                        border-left: 4px solid {status_color};
                    }}
                    .check-icon {{ color: green; font-weight: bold; }}
                    .cross-icon {{ color: red; font-weight: bold; }}
                    .warning-icon {{ color: orange; font-weight: bold; }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin: 10px 0;
                    }}
                    th, td {{
                        padding: 10px;
                        text-align: left;
                        border-bottom: 1px solid #ddd;
                    }}
                    th {{
                        background-color: {status_color};
                        color: white;
                    }}
                    tr:hover {{
                        background-color: #f5f5f5;
                    }}
                    .difference-item {{
                        background-color: #ffe6e6;
                        border-left: 4px solid #dc3545;
                        padding: 10px;
                        margin: 8px 0;
                        border-radius: 4px;
                    }}
                    .footer {{
                        margin-top: 30px;
                        text-align: center;
                        color: #666;
                        font-size: 12px;
                        border-top: 1px solid #ddd;
                        padding-top: 15px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>AMP AutoFeed Validation Report</h1>
                        <p style="margin: 10px 0; color: #666;">
                            <strong>Date:</strong> {date}<br>
                            <strong>Time:</strong> {timestamp}
                        </p>
                        <div class="status-badge">{status}</div>
                    </div>
                    
                    <div class="section">
                        <h2>Email Status</h2>
                        <table>
                            <tr>
                                <th>Email Type</th>
                                <th>Status</th>
                            </tr>
                            <tr>
                                <td>QuickBase API Response</td>
                                <td>{"<span class='check-icon'>✓</span> Found" if qb_found else "<span class='cross-icon'>✗</span> Not Found"}</td>
                            </tr>
                            <tr>
                                <td>AMP AutoFeed Details</td>
                                <td>{"<span class='check-icon'>✓</span> Found" if amp_found else "<span class='cross-icon'>✗</span> Not Found"}</td>
                            </tr>
                        </table>
                    </div>
        """
        
        if status == 'PASS':
            html += """
                    <div class="section" style="background-color: #e8f5e9; border-left-color: #28a745;">
                        <h2 style="color: #28a745;">✓ Validation Passed</h2>
                        <p>The QuickBase API response data matches the AMP processed AutoFeed details.</p>
                        <p><strong>No discrepancies detected.</strong></p>
                    </div>
            """
        
        elif status == 'FAIL':
            html += f"""
                    <div class="section" style="background-color: #ffebee; border-left-color: #dc3545;">
                        <h2 style="color: #dc3545;">✗ Validation Failed</h2>
                        <p>Discrepancies found between QuickBase and AMP data:</p>
                        <div>
            """
            
            for diff in differences:
                html += f'<div class="difference-item">{diff}</div>'
            
            html += """
                        </div>
                    </div>
            """
        
        elif status == 'ERROR':
            error_msg = validation_result.get('error', 'Unknown error')
            html += f"""
                    <div class="section" style="background-color: #fff3e0; border-left-color: #fd7e14;">
                        <h2 style="color: #fd7e14;">⚠ Validation Error</h2>
                        <p>An error occurred during validation:</p>
                        <div class="difference-item" style="border-left-color: #fd7e14; background-color: #fff3e0;">
                            {error_msg}
                        </div>
                    </div>
            """
        
        # Add data details if available
        if validation_result.get('qb_data') or validation_result.get('amp_data'):
            html += """
                    <div class="section">
                        <h2>Data Summary</h2>
                        <table>
                            <tr>
                                <th>Metric</th>
                                <th>QuickBase</th>
                                <th>AMP</th>
                            </tr>
            """
            
            qb_data = validation_result.get('qb_data', {})
            amp_data = validation_result.get('amp_data', {})
            
            qb_tables = len(qb_data.get('tables', []))
            amp_tables = len(amp_data.get('tables', []))
            
            qb_lists = len(qb_data.get('lists', []))
            amp_lists = len(amp_data.get('lists', []))
            
            html += f"""
                            <tr>
                                <td>Tables Found</td>
                                <td>{qb_tables}</td>
                                <td>{amp_tables}</td>
                            </tr>
                            <tr>
                                <td>Lists Found</td>
                                <td>{qb_lists}</td>
                                <td>{amp_lists}</td>
                            </tr>
            """
            
            html += """
                        </table>
                    </div>
            """
        
        html += """
                    <div class="footer">
                        <p>This is an automated report from the AMP AutoFeed Validation System.</p>
                        <p>For issues or questions, contact your system administrator.</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        return html
    
    def send_report(self, validation_result: Dict) -> bool:
        """Send validation report via email"""
        
        if not all([self.smtp_server, self.sender_email, self.sender_password]):
            print("ERROR: Email configuration incomplete")
            return False
        
        try:
            # Create email
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"AMP AutoFeed Validation Report - {validation_result.get('date')} [{validation_result.get('status')}]"
            msg["From"] = self.sender_email
            msg["To"] = self.recipient_email
            
            # Generate HTML report
            html_content = self.generate_html_report(validation_result)
            
            # Create plain text version
            text_content = f"""
AMP AutoFeed Validation Report
{validation_result.get('date')} - {validation_result.get('status')}

Status: {validation_result.get('status')}

Email Status:
- QuickBase API Response: {"Found" if validation_result.get('qb_email_found') else "Not Found"}
- AMP AutoFeed Details: {"Found" if validation_result.get('amp_email_found') else "Not Found"}

Differences Found:
"""
            
            differences = validation_result.get('comparison', {}).get('differences', [])
            if differences:
                for diff in differences:
                    text_content += f"  - {diff}\n"
            else:
                text_content += "  None\n"
            
            text_content += f"\nFor details, see the HTML version of this report."
            
            # Attach both versions
            msg.attach(MIMEText(text_content, "plain"))
            msg.attach(MIMEText(html_content, "html"))
            
            # Send email
            print(f"Connecting to {self.smtp_server}:{self.smtp_port}...")
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print(f"✓ Report sent to {self.recipient_email}")
            return True
            
        except Exception as e:
            print(f"ERROR sending email: {e}")
            return False


def send_validation_report(log_dir: str = "amp_validation_logs",
                          recipient_email: str = None,
                          date: Optional[str] = None):
    """
    Convenience function to send validation report from log files
    
    Example:
        send_validation_report(
            recipient_email="your.email@walmart.com",
            date="2025-04-14"
        )
    """
    
    log_path = Path(log_dir)
    
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    report_file = log_path / "daily_reports" / f"validation_{date}.json"
    
    if not report_file.exists():
        print(f"ERROR: Report not found: {report_file}")
        return False
    
    with open(report_file, 'r') as f:
        validation_result = json.load(f)
    
    # Get credentials from environment or config
    # For production, store these securely
    import os
    
    smtp_server = os.getenv("VALIDATION_SMTP_SERVER", "smtp.gmail.com")
    sender_email = os.getenv("VALIDATION_SENDER_EMAIL")
    sender_password = os.getenv("VALIDATION_SENDER_PASSWORD")
    
    if not sender_email or not sender_password:
        print("ERROR: Email credentials not configured")
        print("Set environment variables:")
        print("  - VALIDATION_SENDER_EMAIL")
        print("  - VALIDATION_SENDER_PASSWORD")
        print("  - VALIDATION_SMTP_SERVER (optional, defaults to smtp.gmail.com)")
        return False
    
    reporter = ValidationReportEmail(
        smtp_server=smtp_server,
        sender_email=sender_email,
        sender_password=sender_password,
        recipient_email=recipient_email or sender_email
    )
    
    return reporter.send_report(validation_result)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Send AMP AutoFeed validation report email")
    parser.add_argument('--log-dir', default='amp_validation_logs', help='Log directory')
    parser.add_argument('--date', help='Report date (YYYY-MM-DD), defaults to today')
    parser.add_argument('--recipient', help='Recipient email address')
    
    args = parser.parse_args()
    
    send_validation_report(
        log_dir=args.log_dir,
        recipient_email=args.recipient,
        date=args.date
    )
