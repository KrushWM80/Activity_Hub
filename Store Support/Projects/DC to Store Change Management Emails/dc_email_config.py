#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DC Email Configuration
Email sending configuration for DC-segmented notifications.
"""

# ============================================================================
# SENDER CONFIGURATION
# ============================================================================

# Email address to send FROM
SEND_FROM_EMAIL = "supplychainops@email.wal-mart.com"

# Display name for sender
SEND_FROM_NAME = "ELM Manager Change Tracking System"

# ============================================================================
# RECIPIENT CONFIGURATION
# ============================================================================

# Use BCC for all recipients (privacy and prevents reply-all)
USE_BCC = True

# Test mode - send all emails to these recipients for validation
TEST_MODE = True  # Set to False when ready for production
TEST_RECIPIENTS = [
    "Kristine.Torres@walmart.com",
    "Matthew.Farnworth@walmart.com",
    "Kendall.Rush@walmart.com"
]  # 3-person test group
TEST_RECIPIENT = TEST_RECIPIENTS[0]  # Backward compatibility

# Admin email - ALWAYS receives error and no-change notifications (even in production)
ADMIN_EMAIL = "jhendr6@homeoffice.wal-mart.com"

# ============================================================================
# NOTIFICATION RULES
# ============================================================================

# Send "no changes" emails to DC teams? (Recommended: False)
# Even if True, no-change emails ALWAYS go to admin only
SEND_NO_CHANGE_TO_DCS = False

# Send error notifications to DC teams? (Recommended: False)  
# Even if True, error emails ALWAYS go to admin only
SEND_ERRORS_TO_DCS = False

# ============================================================================
# REPLY CONFIGURATION
# ============================================================================

# Reply-To address (if different from sender)
# Set to None to use the FROM address
# Set to a monitored mailbox if you want people to reply somewhere specific
# Set to "noreply@walmart.com" to discourage replies
REPLY_TO_EMAIL = "ATCTEAMSUPPORT@walmart.com"  # Support team email for questions/replies

# ============================================================================
# DISCLAIMER TEXT
# ============================================================================

DISCLAIMER_TEXT = """
This is an automated email from the ELM Manager Change Tracking System. 
Questions or feedback? Reply to this email or contact ATCTEAMSUPPORT@walmart.com
"""

# ============================================================================
# EMAIL FOOTER (HTML)
# ============================================================================

def get_email_footer_html() -> str:
    """
    Generate HTML footer with disclaimer.
    
    Returns:
        HTML footer string
    """
    return """
        <div class="disclaimer">
            <div class="disclaimer-icon">ℹ️</div>
            <div class="disclaimer-title">Questions? We'd Like To Hear From You</div>
            <p>
                This is an automated email from the <strong>ELM Manager Change Tracking System</strong>. 
                Have feedback or questions? <strong>Reply to this email</strong> or contact <a href="mailto:ATCTEAMSUPPORT@walmart.com">ATCTEAMSUPPORT@walmart.com</a>
            </p>
        </div>
        
        <div class="footer-info">
            <p><strong>ELM Manager Change Tracking System</strong></p>
            <p>Automated daily monitoring of SDL manager assignments</p>
            <p style="font-size: 11px; color: #999; margin-top: 10px;">
                This email was sent to you because manager changes were detected in your DC's service territory. 
                Updates are generated daily based on SDL export data.
            </p>
        </div>
"""

# ============================================================================
# CSS FOR DISCLAIMER
# ============================================================================

DISCLAIMER_CSS = """
        .disclaimer {
            background: #fff3cd;
            border: 2px solid #ffc107;
            border-radius: 6px;
            padding: 20px;
            margin: 30px 0 20px 0;
            text-align: center;
        }
        .disclaimer-icon {
            font-size: 32px;
            margin-bottom: 10px;
        }
        .disclaimer-title {
            font-size: 16px;
            font-weight: bold;
            color: #856404;
            margin-bottom: 10px;
        }
        .disclaimer p {
            font-size: 13px;
            color: #856404;
            margin: 8px 0;
            line-height: 1.5;
        }
        .disclaimer a {
            color: #0071ce;
            text-decoration: none;
            font-weight: bold;
        }
        .disclaimer a:hover {
            text-decoration: underline;
        }
        .footer-info {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 2px solid #e0e0e0;
            font-size: 13px;
            color: #666;
            text-align: center;
        }
        .footer-info p {
            margin: 5px 0;
        }
"""

# ============================================================================
# EMAIL HEADERS TO PREVENT REPLIES
# ============================================================================

# Note: Some of these may not be supported by all email clients
EMAIL_HEADERS = {
    # Prevent reply-all (not widely supported but worth trying)
    'X-Auto-Response-Suppress': 'All',  # Outlook
    
    # Mark as automated
    'Auto-Submitted': 'auto-generated',
    'Precedence': 'bulk',
    
    # Importance
    'Importance': 'normal',
    'Priority': 'normal',
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_sender_info() -> dict:
    """
    Get sender information for email.
    
    Returns:
        Dict with 'email' and 'name'
    """
    return {
        'email': SEND_FROM_EMAIL,
        'name': SEND_FROM_NAME
    }

def get_reply_to() -> str:
    """
    Get reply-to address.
    
    Returns:
        Reply-to email address or None
    """
    return REPLY_TO_EMAIL

def should_use_bcc() -> bool:
    """
    Check if BCC should be used for recipients.
    
    Returns:
        True if BCC should be used
    """
    return USE_BCC

def is_test_mode() -> bool:
    """
    Check if in test mode.
    
    Returns:
        True if test mode enabled
    """
    return TEST_MODE

def get_test_recipient() -> str:
    """
    Get test recipient email.
    
    Returns:
        Test recipient email address
    """
    return TEST_RECIPIENT

def get_admin_email() -> str:
    """
    Get admin email for error and no-change notifications.
    
    Returns:
        Admin email address
    """
    return ADMIN_EMAIL

def should_send_no_change_to_dcs() -> bool:
    """
    Check if no-change emails should go to DCs.
    Note: They ALWAYS go to admin regardless of this setting.
    
    Returns:
        True if DCs should receive no-change emails (not recommended)
    """
    return SEND_NO_CHANGE_TO_DCS

def should_send_errors_to_dcs() -> bool:
    """
    Check if error emails should go to DCs.
    Note: They ALWAYS go to admin regardless of this setting.
    
    Returns:
        True if DCs should receive error emails (not recommended)
    """
    return SEND_ERRORS_TO_DCS
