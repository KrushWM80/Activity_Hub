#!/usr/bin/env python3
"""
PayCycle 3 Test Email Generator
Generates and sends PayCycle 3 email using sample data
For use when VPN is unavailable but testing is needed
"""

import json
from pathlib import Path
from datetime import datetime
from email_helper import EmailHelper
import dc_email_config as email_config

def main():
    print("\n" + "="*60)
    print("PayCycle 3 Manual Email Send")
    print("="*60 + "\n")
    
    # Create sample PayCycle 3 email
    paycycle_data = {
        "paycycle_number": 3,
        "paycycle_end_date": "2026-03-06",
        "sent_datetime": datetime.now().isoformat(),
        "mode": "TEST",
        "recipients_count": 3,
        "sample_changes": [
            {
                "location": "Store #1234",
                "manager_name": "John Smith",
                "change_type": "New Hire",
                "role": "Store Manager"
            },
            {
                "location": "Store #5678",
                "manager_name": "Jane Doe",
                "change_type": "Promotion",
                "role": "Market Manager"
            },
            {
                "location": "DC #42",
                "manager_name": "Bob Johnson",
                "change_type": "Transfer",
                "role": "DC GM"
            }
        ]
    }
    
    # Create HTML email
    email_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        .header {{
            background: linear-gradient(135deg, #0071ce 0%, #1e3a8a 100%);
            color: white;
            padding: 30px;
            border-radius: 8px 8px 0 0;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
        .content {{
            padding: 30px;
            background: white;
            border: 1px solid #e0e0e0;
        }}
        .section {{
            margin-bottom: 30px;
        }}
        .section-title {{
            font-size: 14px;
            font-weight: bold;
            color: #0071ce;
            margin-bottom: 15px;
            border-bottom: 2px solid #ffcc00;
            padding-bottom: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        table th {{
            background: #f5f5f5;
            padding: 12px;
            text-align: left;
            font-weight: bold;
            border-bottom: 2px solid #0071ce;
        }}
        table td {{
            padding: 12px;
            border-bottom: 1px solid #e0e0e0;
        }}
        table tr:hover {{
            background: #f9f9f9;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: bold;
        }}
        .badge-new {{
            background: #d4edda;
            color: #155724;
        }}
        .badge-promo {{
            background: #cfe2ff;
            color: #084298;
        }}
        .badge-transfer {{
            background: #fff3cd;
            color: #856404;
        }}
        .footer {{
            background: #f5f5f5;
            padding: 20px;
            border-top: 1px solid #e0e0e0;
            font-size: 12px;
            color: #666;
            text-align: center;
        }}
        .footer a {{
            color: #0071ce;
            text-decoration: none;
        }}
        .test-notice {{
            background: #fff3cd;
            border: 1px solid #ffcc00;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 20px;
            color: #856404;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Manager Change Detection Report</h1>
        <p>PayCycle 3 • {paycycle_data['paycycle_end_date']}</p>
    </div>
    
    <div class="content">
        <div class="test-notice">
            <strong>⚠️ TEST MODE EMAIL</strong> - This is a test email sent during PayCycle 3 manual execution (VPN unavailable). Sample data shown for demonstration.
        </div>
        
        <div class="section">
            <div class="section-title">📍 PayCycle Information</div>
            <table>
                <tr>
                    <td width="200"><strong>PayCycle</strong></td>
                    <td>PC #{paycycle_data['paycycle_number']}</td>
                </tr>
                <tr>
                    <td><strong>End Date</strong></td>
                    <td>{paycycle_data['paycycle_end_date']}</td>
                </tr>
                <tr>
                    <td><strong>Sent</strong></td>
                    <td>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td>
                </tr>
                <tr>
                    <td><strong>Mode</strong></td>
                    <td><span class="badge badge-promo">{paycycle_data['mode']}</span></td>
                </tr>
            </table>
        </div>
        
        <div class="section">
            <div class="section-title">👤 Sample Manager Changes (Test Data)</div>
            <table>
                <thead>
                    <tr>
                        <th>Location</th>
                        <th>Manager</th>
                        <th>Change Type</th>
                        <th>Role</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    # Add sample changes
    for change in paycycle_data["sample_changes"]:
        badge_class = "badge-new" if change["change_type"] == "New Hire" else ("badge-promo" if change["change_type"] == "Promotion" else "badge-transfer")
        email_html += f"""
                    <tr>
                        <td>{change['location']}</td>
                        <td>{change['manager_name']}</td>
                        <td><span class="badge {badge_class}">{change['change_type']}</span></td>
                        <td>{change['role']}</td>
                    </tr>
        """
    
    email_html += """
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <div class="section-title">ℹ️ Additional Information</div>
            <p>This is a test email demonstrating the PayCycle 3 format. When VPN connectivity is restored, the system will automatically generate emails with actual manager change data from SDL.</p>
            <ul>
                <li>Total Recipients: 3 (Kristine Torres, Matthew Farnworth, Kendall Rush)</li>
                <li>System Status: TEST MODE</li>
                <li>Next PayCycle: PC #4 on March 20, 2026</li>
            </ul>
        </div>
    </div>
    
    <div class="footer">
        <p>
            <strong>DC to Store Manager Change Detection System</strong><br>
            Questions? Contact: <a href="mailto:ATCTEAMSUPPORT@walmart.com">ATCTEAMSUPPORT@walmart.com</a>
        </p>
        <p>This email was sent in TEST MODE. For production deployment, VPN connectivity is required.</p>
    </div>
</body>
</html>
    """
    
    # Save HTML to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_file = f"emails_sent/DC-EMAIL-PC-03-MANUAL-{timestamp}.html"
    Path("emails_sent").mkdir(exist_ok=True)
    
    with open(html_file, 'w') as f:
        f.write(email_html)
    
    print(f"[OK] Email HTML generated: {html_file}\n")
    
    # Send email via Outlook
    print(f"[EMAIL] Sending PayCycle 3 email via Outlook...")
    
    try:
        email_helper = EmailHelper(test_mode=True)
        
        success = email_helper.send_email_via_outlook(
            to=[
                "Kristine.Torres@walmart.com",
                "Matthew.Farnworth@walmart.com", 
                "Kendall.Rush@walmart.com"
            ],
            subject=f"Manager Changes - PayCycle 3 ({paycycle_data['paycycle_end_date']})",
            body_html=email_html,
            from_email="supplychainops@email.wal-mart.com"
        )
        
        if success:
            print(f"[OK] ✅ Email sent successfully!")
            print(f"[OK] Recipients: Kristine Torres, Matthew Farnworth, Kendall Rush")
            print(f"[OK] File saved: {html_file}")
            return 0
        else:
            print(f"[ERROR] Failed to send email via Outlook")
            return 1
            
    except Exception as e:
        print(f"[ERROR] Exception while sending: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
