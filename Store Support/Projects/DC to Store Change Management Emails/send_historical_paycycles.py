#!/usr/bin/env python3
"""
Send Historical PayCycle Emails - Production Style
Sends emails that simulate what would have been sent on 2/6/26 and 2/20/26
"""

import sys
import win32com.client
from datetime import datetime

import config
import dc_email_config as email_config

test_recipients = config.TEST_EMAILS if hasattr(config, 'TEST_EMAILS') else [config.TEST_EMAIL]

print("\n" + "="*70)
print("HISTORICAL PAYCYCLE EMAILS - Production Style")
print("="*70 + "\n")

print(f"Sending to: {', '.join(test_recipients)}\n")

# ============================================================================
# EMAIL 1: PayCycle 01 - 2/6/2026
# ============================================================================

email1_subject = "Manager Changes - PayCycle 01 (Week Ending 2/6/2026)"

email1_body = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 0;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            margin: 20px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .header {
            background: linear-gradient(135deg, #0071ce 0%, #00a4e4 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0 0 10px 0;
            font-size: 28px;
            font-weight: 600;
        }
        .header p {
            margin: 5px 0;
            font-size: 14px;
            opacity: 0.95;
        }
        .content {
            padding: 30px;
        }
        .summary-box {
            background-color: #ecf0f7;
            border-left: 4px solid #0071ce;
            padding: 15px;
            margin-bottom: 25px;
            border-radius: 4px;
        }
        .summary-box h3 {
            margin: 0 0 10px 0;
            color: #0071ce;
        }
        .change-section {
            margin-bottom: 20px;
        }
        .change-section h4 {
            background-color: #f0f0f0;
            padding: 10px 15px;
            margin: 0 0 10px 0;
            border-radius: 4px;
            color: #0071ce;
            font-size: 14px;
            font-weight: 600;
        }
        .change-item {
            background-color: #fafafa;
            border: 1px solid #e0e0e0;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 4px;
        }
        .change-item p {
            margin: 8px 0;
            font-size: 13px;
        }
        .change-item strong {
            color: #0071ce;
        }
        .old-value {
            color: #d32f2f;
            text-decoration: line-through;
        }
        .new-value {
            color: #388e3c;
            font-weight: bold;
        }
        .footer {
            background-color: #f9f9f9;
            padding: 20px 30px;
            border-top: 1px solid #e0e0e0;
            font-size: 12px;
            color: #666;
            text-align: center;
        }
        .dc-section {
            background-color: #f5f5f5;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 4px;
            border-left: 3px solid #0071ce;
        }
        .dc-section h3 {
            margin: 0 0 15px 0;
            color: #0071ce;
            font-size: 16px;
        }
        .info-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }
        .info-table td {
            padding: 8px;
            border-bottom: 1px solid #e0e0e0;
        }
        .info-table td:first-child {
            font-weight: 600;
            color: #333;
            width: 150px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔔 Manager Changes Detected</h1>
            <p>PayCycle 01 - Week Ending February 6, 2026</p>
        </div>
        
        <div class="content">
            <div class="summary-box">
                <h3>Summary</h3>
                <p>Changes detected in manager assignments across your distribution center territory.</p>
                <p><strong>Total Changes: 4 Store Managers | 2 Market Managers</strong></p>
            </div>
            
            <div class="dc-section">
                <h3>DC 6020 - Dallas Region (Ambient)</h3>
                
                <div class="change-section">
                    <h4>Store Manager Changes (3)</h4>
                    
                    <div class="change-item">
                        <p><strong>Location:</strong> Store #1234 - Dallas, TX</p>
                        <p><strong>Position:</strong> Store Manager</p>
                        <p><strong>Previous:</strong> <span class="old-value">John Martinez</span></p>
                        <p><strong>New:</strong> <span class="new-value">Sarah Johnson</span></p>
                        <p><strong>Effective Date:</strong> 2/3/2026</p>
                    </div>
                    
                    <div class="change-item">
                        <p><strong>Location:</strong> Store #1456 - Fort Worth, TX</p>
                        <p><strong>Position:</strong> Store Manager</p>
                        <p><strong>Previous:</strong> <span class="old-value">Michael Chen</span></p>
                        <p><strong>New:</strong> <span class="new-value">Christopher Lee</span></p>
                        <p><strong>Effective Date:</strong> 2/2/2026</p>
                    </div>
                    
                    <div class="change-item">
                        <p><strong>Location:</strong> Store #1678 - Arlington, TX</p>
                        <p><strong>Position:</strong> Store Manager</p>
                        <p><strong>Previous:</strong> <span class="old-value">Patricia Williams</span></p>
                        <p><strong>New:</strong> <span class="new-value">Amanda Rodriguez</span></p>
                        <p><strong>Effective Date:</strong> 2/4/2026</p>
                    </div>
                </div>
                
                <div class="change-section">
                    <h4>Market Manager Changes (1)</h4>
                    
                    <div class="change-item">
                        <p><strong>Market:</strong> Dallas Metro - Stores #1200-#1500</p>
                        <p><strong>Position:</strong> Market Manager</p>
                        <p><strong>Previous:</strong> <span class="old-value">David Thompson</span></p>
                        <p><strong>New:</strong> <span class="new-value">Jennifer Adams</span></p>
                        <p><strong>Effective Date:</strong> 2/1/2026</p>
                    </div>
                </div>
            </div>
            
            <div class="dc-section">
                <h3>DC 6040 - Dallas Region (Perishable)</h3>
                
                <div class="change-section">
                    <h4>Market Manager Changes (1)</h4>
                    
                    <div class="change-item">
                        <p><strong>Market:</strong> North Texas Perishable - Stores #1300-#1400</p>
                        <p><strong>Position:</strong> Market Manager</p>
                        <p><strong>Previous:</strong> <span class="old-value">Robert Martinez</span></p>
                        <p><strong>New:</strong> <span class="new-value">Kevin Peterson</span></p>
                        <p><strong>Effective Date:</strong> 2/5/2026</p>
                    </div>
                </div>
            </div>
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #e0e0e0;">
                <h3 style="color: #0071ce; margin-top: 0;">Next Steps</h3>
                <ul style="line-height: 1.8; font-size: 14px;">
                    <li>Review the manager changes listed above</li>
                    <li>Update your internal systems and communications</li>
                    <li>Reach out to new managers to establish working relationships</li>
                    <li>Notify affected stores of any supply chain coordination changes</li>
                </ul>
            </div>
        </div>
        
        <div class="footer">
            <p style="margin: 0;">DC to Store Manager Change Notification System</p>
            <p style="margin: 5px 0 0 0; font-size: 11px; color: #999;">Automated notification generated on February 6, 2026 | PayCycle 01</p>
        </div>
    </div>
</body>
</html>"""

print("[EMAIL 1/2] Sending PayCycle 01 email (2/6/2026)...")
try:
    outlook = win32com.client.Dispatch('Outlook.Application')
    mail = outlook.CreateItem(0)
    mail.To = '; '.join(test_recipients)
    mail.Subject = email1_subject
    mail.HTMLBody = email1_body
    mail.Send()
    print("  ✅ PayCycle 01 email sent successfully!\n")
except Exception as e:
    print(f"  ❌ Failed: {e}\n")
    sys.exit(1)

# ============================================================================
# EMAIL 2: PayCycle 02 - 2/20/2026
# ============================================================================

email2_subject = "Manager Changes - PayCycle 02 (Week Ending 2/20/2026)"

email2_body = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 0;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            margin: 20px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .header {
            background: linear-gradient(135deg, #0071ce 0%, #00a4e4 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0 0 10px 0;
            font-size: 28px;
            font-weight: 600;
        }
        .header p {
            margin: 5px 0;
            font-size: 14px;
            opacity: 0.95;
        }
        .content {
            padding: 30px;
        }
        .summary-box {
            background-color: #ecf0f7;
            border-left: 4px solid #0071ce;
            padding: 15px;
            margin-bottom: 25px;
            border-radius: 4px;
        }
        .summary-box h3 {
            margin: 0 0 10px 0;
            color: #0071ce;
        }
        .change-section {
            margin-bottom: 20px;
        }
        .change-section h4 {
            background-color: #f0f0f0;
            padding: 10px 15px;
            margin: 0 0 10px 0;
            border-radius: 4px;
            color: #0071ce;
            font-size: 14px;
            font-weight: 600;
        }
        .change-item {
            background-color: #fafafa;
            border: 1px solid #e0e0e0;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 4px;
        }
        .change-item p {
            margin: 8px 0;
            font-size: 13px;
        }
        .change-item strong {
            color: #0071ce;
        }
        .old-value {
            color: #d32f2f;
            text-decoration: line-through;
        }
        .new-value {
            color: #388e3c;
            font-weight: bold;
        }
        .footer {
            background-color: #f9f9f9;
            padding: 20px 30px;
            border-top: 1px solid #e0e0e0;
            font-size: 12px;
            color: #666;
            text-align: center;
        }
        .dc-section {
            background-color: #f5f5f5;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 4px;
            border-left: 3px solid #0071ce;
        }
        .dc-section h3 {
            margin: 0 0 15px 0;
            color: #0071ce;
            font-size: 16px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔔 Manager Changes Detected</h1>
            <p>PayCycle 02 - Week Ending February 20, 2026</p>
        </div>
        
        <div class="content">
            <div class="summary-box">
                <h3>Summary</h3>
                <p>Changes detected in manager assignments across your distribution center territory.</p>
                <p><strong>Total Changes: 2 Store Managers | 1 Market Manager</strong></p>
            </div>
            
            <div class="dc-section">
                <h3>DC 6080 - Houston Region (Ambient)</h3>
                
                <div class="change-section">
                    <h4>Store Manager Changes (2)</h4>
                    
                    <div class="change-item">
                        <p><strong>Location:</strong> Store #2234 - Houston, TX</p>
                        <p><strong>Position:</strong> Store Manager</p>
                        <p><strong>Previous:</strong> <span class="old-value">Thomas Anderson</span></p>
                        <p><strong>New:</strong> <span class="new-value">Maria Garcia</span></p>
                        <p><strong>Effective Date:</strong> 2/17/2026</p>
                    </div>
                    
                    <div class="change-item">
                        <p><strong>Location:</strong> Store #2556 - Galveston, TX</p>
                        <p><strong>Position:</strong> Store Manager</p>
                        <p><strong>Previous:</strong> <span class="old-value">Jennifer White</span></p>
                        <p><strong>New:</strong> <span class="new-value">James Wilson</span></p>
                        <p><strong>Effective Date:</strong> 2/19/2026</p>
                    </div>
                </div>
                
                <div class="change-section">
                    <h4>Market Manager Changes (1)</h4>
                    
                    <div class="change-item">
                        <p><strong>Market:</strong> Houston Metro - Stores #2200-#2600</p>
                        <p><strong>Position:</strong> Market Manager</p>
                        <p><strong>Previous:</strong> <span class="old-value">Michelle Brown</span></p>
                        <p><strong>New:</strong> <span class="new-value">William Davis</span></p>
                        <p><strong>Effective Date:</strong> 2/18/2026</p>
                    </div>
                </div>
            </div>
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #e0e0e0;">
                <h3 style="color: #0071ce; margin-top: 0;">Next Steps</h3>
                <ul style="line-height: 1.8; font-size: 14px;">
                    <li>Review the manager changes listed above</li>
                    <li>Update your internal systems and communications</li>
                    <li>Reach out to new managers to establish working relationships</li>
                    <li>Notify affected stores of any supply chain coordination changes</li>
                </ul>
            </div>
        </div>
        
        <div class="footer">
            <p style="margin: 0;">DC to Store Manager Change Notification System</p>
            <p style="margin: 5px 0 0 0; font-size: 11px; color: #999;">Automated notification generated on February 20, 2026 | PayCycle 02</p>
        </div>
    </div>
</body>
</html>"""

print("[EMAIL 2/2] Sending PayCycle 02 email (2/20/2026)...")
try:
    outlook = win32com.client.Dispatch('Outlook.Application')
    mail = outlook.CreateItem(0)
    mail.To = '; '.join(test_recipients)
    mail.Subject = email2_subject
    mail.HTMLBody = email2_body
    mail.Send()
    print("  ✅ PayCycle 02 email sent successfully!\n")
except Exception as e:
    print(f"  ❌ Failed: {e}\n")
    sys.exit(1)

# ============================================================================
# SUMMARY
# ============================================================================

print("="*70)
print("✅ HISTORICAL EMAILS SENT SUCCESSFULLY")
print("="*70 + "\n")

print("Email 1:")
print(f"  Subject: {email1_subject}")
print(f"  PayCycle: 01 (2/6/2026)")
print(f"  Recipients: 3 people")
print(f"  Status: ✅ Sent\n")

print("Email 2:")
print(f"  Subject: {email2_subject}")
print(f"  PayCycle: 02 (2/20/2026)")
print(f"  Recipients: 3 people")
print(f"  Status: ✅ Sent\n")

print(f"Sent to: {', '.join(test_recipients)}\n")

print("These emails simulate what would have been sent on those PayCycle")
print("dates in a production environment. All emails use professional")
print("production formatting without test labels.\n")
