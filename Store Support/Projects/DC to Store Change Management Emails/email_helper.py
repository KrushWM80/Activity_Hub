#!/usr/bin/env python3
"""
Email Helper Module
Handles email notifications via Microsoft Graph.
"""

import json
import subprocess
from typing import List, Dict, Any
from datetime import datetime

import config


class EmailHelper:
    """
    Helper class to send emails via Microsoft Graph (msgraph Code Puppy agent).
    """
    
    def __init__(self, test_mode: bool = config.TEST_MODE):
        self.test_mode = test_mode
        # Support both single email and list of test emails
        if hasattr(config, 'TEST_EMAILS'):
            self.test_emails = config.TEST_EMAILS
            self.test_email = config.TEST_EMAILS[0]  # For backward compatibility
        else:
            self.test_email = config.TEST_EMAIL
            self.test_emails = [config.TEST_EMAIL]
    
    def _invoke_msgraph(self, prompt: str) -> str:
        """
        Invoke the msgraph agent via subprocess.
        
        For now, this is a placeholder that prints what would be sent.
        In production, this would actually invoke the Code Puppy msgraph agent.
        """
        print(f"\n[EMAIL] Would invoke msgraph agent:")
        print(f"  Prompt: {prompt[:200]}...\n")
        return "Email sent successfully (simulated)"
    
    def get_recipients(self, role: str) -> List[str]:
        """
        Get the email recipients for a given role.
        
        Args:
            role: The manager role (Store Manager, DC GM, etc.)
        
        Returns:
            List of email addresses
        """
        if self.test_mode:
            # Return all test recipients (supports 1 or more)
            return self.test_emails
        
        # Get role-specific distribution list
        recipients = config.EMAIL_DISTRIBUTION.get(role)
        
        # Fall back to default if role not found
        if not recipients:
            recipients = config.EMAIL_DISTRIBUTION.get('_default', [])
        
        return recipients
    
    def format_change_email_html(self, change: Dict[str, Any]) -> str:
        """
        Format a manager change as HTML email.
        
        Args:
            change: ManagerChange dictionary
        
        Returns:
            HTML email body
        """
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: #0071ce;
            color: white;
            padding: 20px;
            border-radius: 5px 5px 0 0;
            text-align: center;
        }}
        .content {{
            background: #f9f9f9;
            padding: 30px;
            border: 1px solid #ddd;
            border-radius: 0 0 5px 5px;
        }}
        .change-box {{
            background: white;
            padding: 20px;
            margin: 20px 0;
            border-left: 4px solid #0071ce;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .field {{
            margin: 10px 0;
        }}
        .label {{
            font-weight: bold;
            color: #666;
            display: inline-block;
            width: 150px;
        }}
        .value {{
            color: #333;
        }}
        .old-value {{
            color: #d32f2f;
            text-decoration: line-through;
        }}
        .new-value {{
            color: #388e3c;
            font-weight: bold;
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            font-size: 12px;
            color: #666;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔔 Manager Change Alert</h1>
    </div>
    
    <div class="content">
        <p>A manager change has been detected in your area:</p>
        
        <div class="change-box">
            <div class="field">
                <span class="label">Location:</span>
                <span class="value">{change['location_name']} (#{change['location_id']})</span>
            </div>
            
            <div class="field">
                <span class="label">Location Type:</span>
                <span class="value">{change['location_type']}</span>
            </div>
            
            <div class="field">
                <span class="label">Role:</span>
                <span class="value">{change['role']}</span>
            </div>
            
            <div class="field">
                <span class="label">Previous Manager:</span>
                <span class="value old-value">{change['previous_manager']}</span>
            </div>
            
            <div class="field">
                <span class="label">New Manager:</span>
                <span class="value new-value">{change['new_manager']}</span>
            </div>
"""
        
        # Add optional fields if available
        if change.get('new_email'):
            html += f"""
            <div class="field">
                <span class="label">Email:</span>
                <span class="value">{change['new_email']}</span>
            </div>
"""
        
        if change.get('market'):
            html += f"""
            <div class="field">
                <span class="label">Market:</span>
                <span class="value">{change['market']}</span>
            </div>
"""
        
        if change.get('region'):
            html += f"""
            <div class="field">
                <span class="label">Region:</span>
                <span class="value">{change['region']}</span>
            </div>
"""
        
        html += f"""
            <div class="field">
                <span class="label">Detected:</span>
                <span class="value">{change['change_detected']}</span>
            </div>
        </div>
        
        <p><strong>Action Required:</strong> Please update your records and reach out to the new manager to ensure a smooth transition.</p>
        
        <div class="footer">
            <p>This is an automated notification from the Manager Change Detection System.</p>
            <p>If you have questions, please contact the sender of this email.</p>
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def format_summary_email_html(self, changes: List[Dict[str, Any]], date: str) -> str:
        """
        Format a summary of multiple changes as HTML email.
        
        Args:
            changes: List of ManagerChange dictionaries
            date: Date string
        
        Returns:
            HTML email body
        """
        changes_by_role = {}
        for change in changes:
            role = change['role']
            if role not in changes_by_role:
                changes_by_role[role] = []
            changes_by_role[role].append(change)
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: #0071ce;
            color: white;
            padding: 20px;
            border-radius: 5px 5px 0 0;
            text-align: center;
        }}
        .content {{
            background: #f9f9f9;
            padding: 30px;
            border: 1px solid #ddd;
            border-radius: 0 0 5px 5px;
        }}
        .summary {{
            background: #fff3cd;
            border: 1px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        .role-section {{
            margin: 30px 0;
        }}
        .role-title {{
            background: #0071ce;
            color: white;
            padding: 10px 15px;
            border-radius: 3px;
            font-weight: bold;
        }}
        .change-item {{
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #0071ce;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .change-item strong {{
            color: #0071ce;
        }}
        .old {{ color: #d32f2f; text-decoration: line-through; }}
        .new {{ color: #388e3c; font-weight: bold; }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            font-size: 12px;
            color: #666;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Daily Manager Change Summary</h1>
        <p>Date: {date}</p>
    </div>
    
    <div class="content">
        <div class="summary">
            <strong>Total Changes Detected: {len(changes)}</strong>
        </div>
        
        <p>The following manager changes were detected in today's scan:</p>
"""
        
        for role, role_changes in changes_by_role.items():
            html += f"""
        <div class="role-section">
            <div class="role-title">{role} ({len(role_changes)} change(s))</div>
"""
            
            for change in role_changes:
                html += f"""
            <div class="change-item">
                <strong>{change['location_name']}</strong> (#{change['location_id']})<br>
                <span class="old">{change['previous_manager']}</span> &rarr; <span class="new">{change['new_manager']}</span>
            </div>
"""
            
            html += """</div>"""
        
        html += f"""
        <div class="footer">
            <p>This is an automated notification from the Manager Change Detection System.</p>
            <p>Review the full change report in your snapshots folder for complete details.</p>
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def send_email_via_outlook(self, to: List[str], subject: str, body_html: str, from_email: str = None, bcc: List[str] = None) -> bool:
        """
        Send email via Walmart internal SMTP gateway (reliable, no Outlook dependency).
        
        Args:
            to: List of recipient email addresses
            subject: Email subject
            body_html: HTML body content
            from_email: Optional - override FROM address (default: kendall.rush@walmart.com)
            bcc: Optional - List of BCC recipient email addresses
        
        Returns:
            True if sent successfully
        """
        try:
            import smtplib
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            
            # Walmart internal SMTP gateway
            SMTP_SERVER = "smtp-gw1.homeoffice.wal-mart.com"
            SMTP_PORT = 25
            SENDER = from_email or "kendall.rush@walmart.com"
            
            # Build message
            msg = MIMEMultipart('alternative')
            msg['From'] = SENDER
            msg['To'] = '; '.join(to)
            if bcc:
                msg['Bcc'] = '; '.join(bcc)
            msg['Subject'] = subject
            msg.attach(MIMEText(body_html, 'html', 'utf-8'))
            
            # Send via SMTP
            print(f"\n[EMAIL] Sending via Walmart SMTP gateway:")
            print(f"  To: {', '.join(to)}")
            if bcc:
                print(f"  BCC: {', '.join(bcc)}")
            print(f"  Subject: {subject}")
            print(f"  From: {SENDER}")
            
            recipients = to + (bcc if bcc else [])
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
                server.sendmail(SENDER, recipients, msg.as_string())
            
            print(f"  [OK] Email sent successfully!\n")
            return True
            
        except Exception as e:
            print(f"  [ERROR] Failed to send email: {e}\n")
            import traceback
            traceback.print_exc()
            return False
    
    def send_email_via_msgraph(self, to: List[str], subject: str, body_html: str) -> bool:
        """
        Actually send email via Microsoft Graph msgraph agent.
        
        This will invoke the Code Puppy msgraph agent to send the email.
        
        Args:
            to: List of recipient email addresses
            subject: Email subject
            body_html: HTML email body
        
        Returns:
            True if email sent successfully
        """
        print(f"\n[EMAIL] Sending via Microsoft Graph:")
        print(f"  To: {', '.join(to)}")
        print(f"  Subject: {subject}")
        
        # Save a backup copy for records
        from pathlib import Path
        emails_dir = Path("emails_sent")
        emails_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        email_file = emails_dir / f"email_{timestamp}.html"
        
        with open(email_file, 'w', encoding='utf-8') as f:
            f.write(f"<!-- To: {', '.join(to)} -->\n")
            f.write(f"<!-- Subject: {subject} -->\n\n")
            f.write(body_html)
        
        print(f"  [SAVED] Backup: {email_file}")
        
        # Create a trigger file that tells Code Puppy to send the email
        trigger_file = Path("email_send_queue.txt")
        with open(trigger_file, 'a', encoding='utf-8') as f:
            f.write(f"{email_file}|{', '.join(to)}|{subject}\n")
        
        print(f"  [INFO] Email queued for sending")
        print(f"  [NOTE] Email content saved to: {email_file}")
        print(f"  [NOTE] To actually send, Code Puppy must invoke msgraph agent\n")
        
        # Return True since we successfully queued it
        return True
    
    def send_change_notification(self, change: Dict[str, Any]) -> bool:
        """
        Send email notification for a single manager change.
        
        Args:
            change: ManagerChange dictionary
        
        Returns:
            True if email sent successfully
        """
        recipients = self.get_recipients(change['role'])
        
        if not recipients:
            print(f"[WARNING] No recipients configured for role: {change['role']}")
            return False
        
        subject = f"Manager Change Alert - {change['role']} at {change['location_name']}"
        body_html = self.format_change_email_html(change)
        
        print(f"\n[EMAIL] Sending change notification:")
        print(f"  Change: {change['previous_manager']} -> {change['new_manager']} at {change['location_name']}")
        
        # Send via Outlook COM automation (same as seasonal dashboard)
        return self.send_email_via_outlook(recipients, subject, body_html)
        
        return False
    
    def send_no_changes_notification(self, date: str) -> bool:
        """
        Send email notification when NO changes are detected.
        Confirms that the daily job ran successfully.
        
        Args:
            date: Date string
        
        Returns:
            True if email sent successfully
        """
        recipients = [config.TEST_EMAIL] if config.TEST_MODE else [config.TEST_EMAIL]  # Always send to primary recipient
        
        subject = f"Manager Change Detection - No Changes ({date})"
        
        body_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: #28a745;
            color: white;
            padding: 20px;
            border-radius: 5px 5px 0 0;
            text-align: center;
        }}
        .content {{
            background: #f9f9f9;
            padding: 30px;
            border: 1px solid #ddd;
            border-radius: 0 0 5px 5px;
        }}
        .success-box {{
            background: #d4edda;
            border: 1px solid #28a745;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
            text-align: center;
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            font-size: 12px;
            color: #666;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>✅ Daily Job Completed Successfully</h1>
        <p>Date: {date}</p>
    </div>
    
    <div class="content">
        <div class="success-box">
            <h2 style="color: #28a745; margin: 0;">No Manager Changes Detected</h2>
            <p style="margin: 10px 0 0 0;">All managers remain in their current positions.</p>
        </div>
        
        <p><strong>Job Status:</strong> Completed successfully</p>
        <p><strong>Locations Scanned:</strong> ~9,000</p>
        <p><strong>Next Run:</strong> Tomorrow at 2:00 AM</p>
        
        <div class="footer">
            <p>This is an automated notification from the Manager Change Detection System.</p>
            <p>You receive this email to confirm the daily job is running correctly.</p>
        </div>
    </div>
</body>
</html>
"""
        
        print(f"\n[EMAIL] Sending 'no changes' confirmation:")
        print(f"  To: {', '.join(recipients)}")
        
        # Use Outlook COM automation from shared mailbox
        return self.send_email_via_outlook(
            to=recipients,
            subject=subject,
            body_html=body_html,
            from_email="supplychainops@email.wal-mart.com"
        )
    
    def send_error_notification(self, error_message: str, date: str) -> bool:
        """
        Send email notification when job encounters an error.
        
        Args:
            error_message: Description of the error
            date: Date string
        
        Returns:
            True if email sent successfully
        """
        recipients = [config.TEST_EMAIL]  # Always send errors to primary recipient
        
        subject = f"ERROR: Manager Change Detection Failed - {date}"
        
        body_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: #dc3545;
            color: white;
            padding: 20px;
            border-radius: 5px 5px 0 0;
            text-align: center;
        }}
        .content {{
            background: #f9f9f9;
            padding: 30px;
            border: 1px solid #ddd;
            border-radius: 0 0 5px 5px;
        }}
        .error-box {{
            background: #f8d7da;
            border: 1px solid #dc3545;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        .code {{
            background: #f4f4f4;
            border: 1px solid #ddd;
            padding: 10px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            overflow-x: auto;
        }}
        .restart-button {{
            background: #0071ce;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 5px;
            display: inline-block;
            margin: 20px 0;
            font-weight: bold;
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            font-size: 12px;
            color: #666;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚨 Daily Job Failed</h1>
        <p>Date: {date}</p>
    </div>
    
    <div class="content">
        <div class="error-box">
            <h2 style="color: #dc3545; margin: 0;">Error Encountered</h2>
            <p style="margin: 10px 0 0 0;">The manager change detection job failed to complete.</p>
        </div>
        
        <h3>Error Details:</h3>
        <div class="code">
{error_message}
        </div>
        
        <h3>Manual Restart Instructions:</h3>
        <p>To manually restart the process:</p>
        <ol>
            <li>Open Command Prompt or PowerShell</li>
            <li>Navigate to: <code>C:\\Users\\jhendr6\\puppy\\elm</code></li>
            <li>Run: <code>python daily_check.py</code></li>
        </ol>
        
        <p><strong>Or use this one-liner:</strong></p>
        <div class="code">
cd C:\\Users\\jhendr6\\puppy\\elm && python daily_check.py
        </div>
        
        <h3>Troubleshooting:</h3>
        <ul>
            <li>Check if SDL is accessible</li>
            <li>Verify network connectivity</li>
            <li>Review logs in: <code>C:\\Users\\jhendr6\\puppy\\elm\\logs</code></li>
            <li>Check screenshots in project directory for visual debugging</li>
        </ul>
        
        <div class="footer">
            <p>This is an automated error notification from the Manager Change Detection System.</p>
            <p>The job will attempt to run again tomorrow at 2:00 AM.</p>
        </div>
    </div>
</body>
</html>
"""
        
        print(f"\n[EMAIL] Sending error notification:")
        print(f"  To: {', '.join(recipients)}")
        
        # Use Outlook COM automation from shared mailbox
        return self.send_email_via_outlook(
            to=recipients,
            subject=subject,
            body_html=body_html,
            from_email="supplychainops@email.wal-mart.com"
        )
    
    def send_incomplete_alignment_notification(self, incomplete_assignments: List[Dict], date: str) -> bool:
        """
        Send email notification for stores with incomplete DC assignments.
        Alerts admin that some stores are missing Ambient or Perishable DC assignments.
        
        Args:
            incomplete_assignments: List of dicts with 'change', 'dcs_found', 'missing'
            date: Date string
        
        Returns:
            True if email sent successfully
        """
        recipients = [config.TEST_EMAIL]  # Always send to admin
        
        subject = f"WARNING: Incomplete DC Alignment - {len(incomplete_assignments)} Store(s) - {date}"
        
        # Build store rows HTML
        store_rows = ""
        for item in incomplete_assignments:
            change = item['change']
            dcs_found = item['dcs_found']
            missing = item['missing']
            
            # Format DCs found
            if not dcs_found:
                dcs_html = '<span style="color: #dc3545;"><strong>NO DCs ASSIGNED</strong></span>'
            else:
                dcs_list = [f"DC {dc['dc']} ({dc['type']})" for dc in dcs_found]
                dcs_html = '<br>'.join(dcs_list)
            
            # Format missing DCs
            missing_html = '<br>'.join([f'<span style="color: #dc3545;">X {m}</span>' for m in missing])
            
            store_rows += f"""
            <tr>
                <td style="padding: 12px; border: 1px solid #ddd;">{change.location_id}</td>
                <td style="padding: 12px; border: 1px solid #ddd;">{change.location_name}</td>
                <td style="padding: 12px; border: 1px solid #ddd;">{change.role}</td>
                <td style="padding: 12px; border: 1px solid #ddd;">
                    <strong>Previous:</strong> {change.previous_manager}<br>
                    <strong>New:</strong> {change.new_manager}
                </td>
                <td style="padding: 12px; border: 1px solid #ddd;">{dcs_html}</td>
                <td style="padding: 12px; border: 1px solid #ddd;">{missing_html}</td>
            </tr>
"""
        
        body_html = f"""
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
        }}
        .header {{
            background: #ff9800;
            color: white;
            padding: 20px;
            border-radius: 5px 5px 0 0;
            text-align: center;
        }}
        .content {{
            background: #f9f9f9;
            padding: 30px;
            border: 1px solid #ddd;
            border-radius: 0 0 5px 5px;
        }}
        .warning-box {{
            background: #fff3cd;
            border: 2px solid #ff9800;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
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
            border: 1px solid #ddd;
        }}
        td {{
            padding: 12px;
            border: 1px solid #ddd;
        }}
        tr:nth-child(even) {{
            background: #f8f9fa;
        }}
        .info-box {{
            background: #e7f3ff;
            border-left: 4px solid #0071ce;
            padding: 15px;
            margin: 20px 0;
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            font-size: 12px;
            color: #666;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>[WARNING] Incomplete DC Alignment Detected</h1>
        <p>Date: {date}</p>
    </div>
    
    <div class="content">
        <div class="warning-box">
            <h2 style="color: #ff9800; margin: 0;">Action Required</h2>
            <p style="margin: 10px 0 0 0;">
                <strong>{len(incomplete_assignments)} store(s)</strong> with manager changes are missing DC assignments.
                These stores may not receive proper notifications until alignment is corrected.
            </p>
        </div>
        
        <div class="info-box">
            <strong>Expected Behavior:</strong> Each store should be assigned to 2 DCs:
            <ul style="margin: 10px 0;">
                <li><strong>Ambient/Regional DC</strong> - General Merchandise warehouse</li>
                <li><strong>Perishable/Grocery DC</strong> - Food/Fresh distribution center</li>
            </ul>
            Each DC should have a GM and AGM, resulting in <strong>4 email recipients per store change</strong>.
        </div>
        
        <h3>Stores with Incomplete Alignment:</h3>
        
        <table>
            <thead>
                <tr>
                    <th>Store #</th>
                    <th>Location</th>
                    <th>Role</th>
                    <th>Manager Change</th>
                    <th>DCs Found</th>
                    <th>Missing DC Type</th>
                </tr>
            </thead>
            <tbody>
{store_rows}
            </tbody>
        </table>
        
        <div class="info-box">
            <h3 style="margin-top: 0;">Recommended Actions:</h3>
            <ol>
                <li>Verify DC assignments in LAS system for flagged stores</li>
                <li>Check if stores are new or recently changed format</li>
                <li>Confirm with DC Ops if alignment is intentionally incomplete</li>
                <li>Update LAS alignment data if corrections are needed</li>
                <li>Re-run alignment refresh: <code>python dc_alignment_refresh.py</code></li>
            </ol>
        </div>
        
        <div class="footer">
            <p>This is an automated notification from the Manager Change Detection System.</p>
            <p>DC alignment data was refreshed from LAS API on {date}.</p>
        </div>
    </div>
</body>
</html>
"""
        
        print(f"\n[EMAIL] Sending incomplete alignment notification:")
        print(f"  To: {', '.join(recipients)}")
        print(f"  Stores flagged: {len(incomplete_assignments)}")
        
        # Use Outlook COM automation from shared mailbox
        return self.send_email_via_outlook(
            to=recipients,
            subject=subject,
            body_html=body_html,
            from_email="supplychainops@email.wal-mart.com"
        )
    
    def send_summary_notification(self, changes: List[Dict[str, Any]], date: str) -> bool:
        """
        Send summary email with all changes for the day.
        
        Args:
            changes: List of ManagerChange dictionaries
            date: Date string
        
        Returns:
            True if email sent successfully
        """
        if not changes:
            print("[INFO] No changes to report, skipping summary email\n")
            return False
        
        recipients = [self.test_email] if self.test_mode else [config.TEST_EMAIL]
        
        subject = f"Manager Change Summary - {len(changes)} change(s) detected on {date}"
        body_html = self.format_summary_email_html(changes, date)
        
        print(f"\n[EMAIL] Sending summary notification:")
        print(f"  Changes: {len(changes)}")
        
        # Send via Outlook COM automation (same as seasonal dashboard)
        return self.send_email_via_outlook(recipients, subject, body_html)


if __name__ == "__main__":
    # Test email helper
    print("Testing Email Helper...\n")
    
    helper = EmailHelper(test_mode=True)
    
    # Test data
    test_change = {
        "location_id": "05403",
        "location_name": "Store 05403",
        "location_type": "Retail",
        "role": "Store Manager",
        "previous_manager": "Jane Smith",
        "new_manager": "John Doe",
        "new_email": "john.doe@walmart.com",
        "market": "Market 123",
        "region": "Region 5",
        "change_detected": datetime.now().isoformat()
    }
    
    # Test single change notification
    print("Testing single change notification:")
    helper.send_change_notification(test_change)
    
    # Test summary notification
    print("\nTesting summary notification:")
    helper.send_summary_notification([test_change], "2026-01-06")
    
    print("\nEmail Helper test complete!")
