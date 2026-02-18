#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DC Email Generator - HTML Version
Generates DC-specific manager change notification emails in beautiful HTML format.
"""

from datetime import datetime
from typing import List, Dict, Any
import json
from collections import defaultdict

import dc_leadership_config as dc_config
import dc_email_config as email_config

def generate_dc_email_html(dc_number: int, dc_type: str, changes: List[Any], date_str: str, intended_recipients: List[str]) -> str:
    """
    Generate beautiful HTML email for DC-specific notification.
    
    Args:
        dc_number: DC number
        dc_type: 'Ambient' or 'Perishable'
        changes: List of ManagerChange objects
        date_str: Date string (YYYY-MM-DD)
        intended_recipients: List of email addresses that would receive this
    
    Returns:
        HTML email body
    """
    dc_display = dc_config.get_dc_display_name(dc_number, dc_type)
    formatted_date = datetime.strptime(date_str, '%Y-%m-%d').strftime('%B %d, %Y')
    
    # Group changes by role
    by_role = defaultdict(list)
    for change in changes:
        by_role[change.role].append(change)
    
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
            background-color: #f5f5f5;
        }}
        .header {{
            background: #008a00;
            color: white;
            padding: 30px;
            border-radius: 8px 8px 0 0;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            margin: 0;
            font-size: 28px;
            font-weight: 600;
        }}
        .header p {{
            margin: 10px 0 0 0;
            font-size: 16px;
            opacity: 0.9;
        }}
        .test-banner {{
            background: #ff6b6b;
            color: white;
            padding: 15px;
            text-align: center;
            font-weight: bold;
            font-size: 14px;
            border-bottom: 3px solid #c92a2a;
        }}
        .recipients-box {{
            background: #fff3cd;
            border: 2px solid #ffc107;
            border-radius: 6px;
            padding: 15px;
            margin: 20px 0;
        }}
        .recipients-box h3 {{
            margin: 0 0 10px 0;
            color: #856404;
            font-size: 16px;
        }}
        .recipients-box ul {{
            margin: 5px 0;
            padding-left: 20px;
        }}
        .recipients-box li {{
            color: #856404;
            font-size: 13px;
        }}
        .content {{
            background: white;
            padding: 30px;
            border: 1px solid #e0e0e0;
            border-radius: 0 0 8px 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .intro {{
            background: #e3f2fd;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 25px;
            border-left: 4px solid #0071ce;
        }}
        .role-section {{
            margin: 30px 0;
        }}
        .role-header {{
            background: #f5f5f5;
            padding: 12px 15px;
            border-radius: 6px;
            margin-bottom: 15px;
            font-weight: bold;
            color: #0071ce;
            font-size: 18px;
            border-left: 4px solid #0071ce;
        }}
        .change-card {{
            background: white;
            padding: 20px;
            margin: 15px 0;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: box-shadow 0.2s;
        }}
        .change-card:hover {{
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        .location-link {{
            color: #0071ce;
            text-decoration: none;
            font-weight: bold;
            font-size: 16px;
        }}
        .location-link:hover {{
            text-decoration: underline;
        }}
        .field {{
            margin: 8px 0;
            display: flex;
            align-items: baseline;
        }}
        .label {{
            font-weight: 600;
            color: #666;
            min-width: 140px;
            flex-shrink: 0;
        }}
        .value {{
            color: #333;
        }}
        .manager-change {{
            background: #f9f9f9;
            padding: 12px;
            border-radius: 4px;
            margin: 10px 0;
        }}
        .old-manager {{
            color: #d32f2f;
            text-decoration: line-through;
            opacity: 0.8;
        }}
        .arrow {{
            color: #666;
            margin: 0 10px;
            font-weight: bold;
        }}
        .new-manager {{
            color: #2e7d32;
            font-weight: bold;
            font-size: 16px;
        }}
        .summary {{
            background: #e8f5e9;
            padding: 15px;
            border-radius: 6px;
            margin-top: 30px;
            text-align: center;
        }}
        .summary-stat {{
            display: inline-block;
            margin: 0 20px;
        }}
        .summary-number {{
            font-size: 24px;
            font-weight: bold;
            color: #2e7d32;
        }}
        .summary-label {{
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid #e0e0e0;
            font-size: 13px;
            color: #666;
            text-align: center;
        }}
        {email_config.DISCLAIMER_CSS}
    </style>
</head>
<body>
    <div class="test-banner">
        ⚠️ THIS IS A TEST EMAIL - In production, this would be sent to DC leadership teams
    </div>
    
    <div class="header">
        <h1>🏢 Recent Field Leadership Updates</h1>
        <p>{formatted_date}</p>
    </div>
    
    <div class="content">
        <div class="recipients-box">
            <h3>📧 Production Distribution List</h3>
            <p>In production, this email would be sent to:</p>
            <ul>
"""
    
    for email in intended_recipients:
        if 'jhendr6' in email:
            html += f"                <li><strong>{email}</strong> (TEST RECIPIENT - YOU)</li>\n"
        else:
            html += f"                <li>{email}</li>\n"
    
    html += """
            </ul>
        </div>
        
        <div class="intro">
            <p><strong>The following manager changes were detected in stores/markets served by your DC.</strong></p>
            <p>These changes may impact your supply chain coordination and store relationships.</p>
        </div>
"""
    
    # Generate each role section
    for role in ['Store Manager', 'Market Manager', 'Region Manager']:
        if role not in by_role:
            continue
        
        role_changes = by_role[role]
        plural = 's' if len(role_changes) != 1 else ''
        
        html += f"""
        <div class="role-section">
            <div class="role-header">
                {role.upper()} ({len(role_changes)} change{plural})
            </div>
"""
        
        for change in role_changes:
            html += "            <div class='change-card'>\n"
            
            if role == 'Store Manager':
                # Make store number and name a clickable link to SDL
                store_url = f"https://sdl.prod.walmart.com/detail/US/{change.location_id}"
                html += f"""
                <div class="field">
                    <span class="label">Store:</span>
                    <a href="{store_url}" class="location-link" target="_blank">Store {change.location_id} - {change.location_name}</a>
                </div>
"""
            elif role == 'Market Manager':
                html += f"""
                <div class="field">
                    <span class="label">Market:</span>
                    <span class="value"><strong>{change.location_id}</strong> - {change.location_name}</span>
                </div>
"""
            elif role == 'Region Manager':
                html += f"""
                <div class="field">
                    <span class="label">Region:</span>
                    <span class="value"><strong>{change.location_id}</strong> - {change.location_name}</span>
                </div>
"""
            
            # Manager change info
            html += f"""
                <div class="manager-change">
                    <span class="old-manager">{change.previous_manager}</span>
                    <span class="arrow">→</span>
                    <span class="new-manager">{change.new_manager}</span>
                </div>
"""
            
            # Additional context
            if hasattr(change, 'market') and change.market and role == 'Store Manager':
                html += f"""
                <div class="field">
                    <span class="label">Market:</span>
                    <span class="value">{change.market}</span>
                </div>
"""
            
            if hasattr(change, 'region') and change.region:
                html += f"""
                <div class="field">
                    <span class="label">Region:</span>
                    <span class="value">{change.region}</span>
                </div>
"""
            
            if hasattr(change, 'new_email') and change.new_email:
                html += f"""
                <div class="field">
                    <span class="label">Email:</span>
                    <span class="value"><a href="mailto:{change.new_email}">{change.new_email}</a></span>
                </div>
"""
            
            html += "            </div>\n"
        
        html += "        </div>\n"
    
    # Summary
    html += f"""
        <div class="summary">
            <div class="summary-stat">
                <div class="summary-number">{len(changes)}</div>
                <div class="summary-label">Total Changes</div>
            </div>
            <div class="summary-stat">
                <div class="summary-number">{len(intended_recipients) - 1}</div>
                <div class="summary-label">DC Recipients</div>
            </div>
        </div>
        
{email_config.get_email_footer_html()}
    </div>
</body>
</html>
"""
    
    return html

def create_dc_email_package_html(dc_number: int, dc_type: str, changes: List[Any], date_str: str, intended_recipients: List[str]) -> Dict[str, Any]:
    """
    Create complete email package for a DC with HTML formatting.
    
    Args:
        dc_number: DC number
        dc_type: 'Ambient' or 'Perishable'
        changes: List of ManagerChange objects
        date_str: Date string (YYYY-MM-DD)
        intended_recipients: List of emails that would receive this
        test_mode: If True, sends to test recipient only
    
    Returns:
        Dict with 'from', 'to', 'bcc', 'subject', 'body_html', 'headers'
    """
    dc_display = dc_config.get_dc_display_name(dc_number, dc_type)
    sender_info = email_config.get_sender_info()
    test_mode = email_config.is_test_mode()
    
    # Subject line - generic field leadership updates
    subject_prefix = "TEST: " if test_mode else ""
    subject = f"{subject_prefix}Recent Field Leadership Updates - {date_str}"
    
    # Determine TO, BCC based on mode
    if test_mode:
        # Test mode: send TO test recipient, show others in email body
        to_emails = [email_config.get_test_recipient()]
        bcc_emails = []
    else:
        # Production mode: use BCC for all recipients
        if email_config.should_use_bcc():
            to_emails = []  # Empty TO field
            bcc_emails = intended_recipients
        else:
            to_emails = intended_recipients
            bcc_emails = []
    
    return {
        'dc_number': dc_number,
        'dc_type': dc_type,
        'from_email': sender_info['email'],
        'from_name': sender_info['name'],
        'to': to_emails,
        'bcc': bcc_emails,
        'reply_to': email_config.get_reply_to(),
        'subject': subject,
        'body_html': generate_dc_email_html(dc_number, dc_type, changes, date_str, intended_recipients),
        'headers': email_config.EMAIL_HEADERS,
        'change_count': len(changes),
        'test_mode': test_mode
    }