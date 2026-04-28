#!/usr/bin/env python3
"""
Pricing Operations Callouts - Weekly Email Sender
Runs every Friday at 4:00 PM CT
Sends email with callouts + Tableau dashboard screenshot to all recipients

Usage:
  python send_pricing_callouts_email.py              # Send email
  python send_pricing_callouts_email.py --preview    # Preview only (no send)
  python send_pricing_callouts_email.py --test       # Test mode (send to single test email)
"""

import os
import sys
import json
import logging
import argparse
import subprocess
import tempfile
import smtplib
import base64
import re
from datetime import datetime, date, timedelta
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from xml.sax.saxutils import escape
from google.cloud import bigquery
from PIL import Image, ImageChops
import pytz

# ============================================================================
# CONFIGURATION
# ============================================================================

SCRIPT_DIR = Path(__file__).parent
LOG_DIR = SCRIPT_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / 'pricing_callouts_email.log'

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# BigQuery
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
    os.environ.get('APPDATA', ''), 'gcloud', 'application_default_credentials.json'
)
BQ_PROJECT = 'wmt-pricingops-analytics'
BQ_DATASET = 'Pricing_Ops'
BQ_TABLE_CALLOUTS = 'Weekly_Callouts'
BQ_TABLE_RECIPIENTS = 'Callout_Email_Recipients'

# SMTP
SMTP_SERVER = 'smtp-gw1.homeoffice.wal-mart.com'
SMTP_PORT = 25
FROM_EMAIL = 'kendall.rush@walmart.com'

# Tableau Dashboard URL
TABLEAU_URL = 'https://tableau-prep-prod.homeoffice.wal-mart.com/#/views/PricingForecast/PricingForecast?:iid=1'

# Callouts Dashboard URL
CALLOUTS_DASHBOARD_URL = 'http://weus42608431466:8091/'

# Edge browser path
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# Timezone
CT = pytz.timezone('America/Chicago')

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_walmart_week(target_date=None):
    """Calculate Walmart week number"""
    if target_date is None:
        target_date = datetime.now()
    
    if target_date.month >= 2:
        fy_start = date(target_date.year, 2, 1)
    else:
        fy_start = date(target_date.year - 1, 2, 1)
    
    days_since = (target_date.date() - fy_start).days
    wm_week = (days_since // 7) + 1
    return wm_week

def get_next_walmart_week():
    """Get next WM week (for coming Friday's email)"""
    return get_walmart_week() + 1

def get_bq_client():
    """Get BigQuery client"""
    return bigquery.Client(project=BQ_PROJECT)

# ============================================================================
# TABLEAU SCREENSHOT CAPTURE
# ============================================================================

def capture_tableau_screenshot(output_png):
    """
    Capture Tableau dashboard screenshot using Edge headless
    Follows TDA Insights pattern
    """
    logger.info('Capturing Tableau dashboard screenshot via Edge headless...')
    
    try:
        # Build HTML page that loads Tableau (Edge can capture direct URL)
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Tableau Dashboard</title>
            <style>
                body {{ margin: 0; padding: 0; }}
                iframe {{ width: 100%; height: 100vh; border: none; }}
            </style>
        </head>
        <body>
            <iframe src="{TABLEAU_URL}" allow="*"></iframe>
        </body>
        </html>
        """
        
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8') as f:
            f.write(html_content)
            html_path = f.name
        
        try:
            # Capture screenshot via Edge headless
            cmd = [
                EDGE_PATH,
                '--headless',
                '--disable-gpu',
                '--no-sandbox',
                '--hide-scrollbars',
                '--force-device-scale-factor=1.5',
                f'--screenshot={output_png}',
                f'--window-size=1280,2000',
                f'file:///{html_path.replace(os.sep, "/")}'
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=60)
            
            if not Path(output_png).exists():
                logger.warning('Edge screenshot failed, creating placeholder')
                # Create placeholder image
                from PIL import Image, ImageDraw
                img = Image.new('RGB', (1280, 720), color='white')
                draw = ImageDraw.Draw(img)
                draw.text((100, 350), 'Tableau Dashboard Preview', fill='gray')
                img.save(output_png, 'PNG')
            else:
                # Auto-crop whitespace and convert to JPEG
                logger.info('Auto-cropping screenshot...')
                img = Image.open(output_png)
                bg = Image.new(img.mode, img.size, (255, 255, 255))
                diff = ImageChops.difference(img, bg)
                bbox = diff.getbbox()
                
                if bbox:
                    cropped = img.crop((0, 0, bbox[2], bbox[3] + 4))
                    jpg_path = output_png.replace('.png', '.jpg')
                    cropped.convert('RGB').save(jpg_path, 'JPEG', quality=78, optimize=True)
                    
                    # Replace PNG with JPEG
                    import shutil
                    shutil.move(jpg_path, output_png)
                    logger.info(f'✓ Screenshot captured and compressed: {Path(output_png).stat().st_size:,} bytes')
                else:
                    logger.info(f'✓ Screenshot captured: {Path(output_png).stat().st_size:,} bytes')
        
        finally:
            if Path(html_path).exists():
                os.unlink(html_path)
        
        return True
    
    except Exception as e:
        logger.error(f'Error capturing Tableau screenshot: {e}')
        return False

# ============================================================================
# BIGQUERY QUERIES
# ============================================================================

def fetch_callouts_for_week(wm_week):
    """Fetch callouts for specific WM week"""
    try:
        client = get_bq_client()
        query = f"""
        SELECT id, wm_week, title, content, created_date, created_by, last_modified_date
        FROM `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE_CALLOUTS}`
        WHERE wm_week = @wm_week AND (status IS NULL OR status = 'active')
        ORDER BY created_date ASC
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter('wm_week', 'INTEGER', wm_week)
            ]
        )
        results = client.query(query, job_config=job_config).result()
        callouts = [dict(row) for row in results]
        logger.info(f'✓ Fetched {len(callouts)} callouts for WK{wm_week}')
        return callouts
    except Exception as e:
        logger.error(f'Error fetching callouts: {e}')
        return []

def fetch_email_recipients():
    """Fetch all active email recipients"""
    try:
        client = get_bq_client()
        query = f"""
        SELECT email FROM `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE_RECIPIENTS}`
        WHERE is_active = TRUE
        ORDER BY added_date ASC
        """
        results = client.query(query).result()
        recipients = [row['email'] for row in results]
        logger.info(f'✓ Fetched {len(recipients)} email recipients')
        return recipients
    except Exception as e:
        logger.error(f'Error fetching email recipients: {e}')
        return []

# ============================================================================
# EMAIL GENERATION
# ============================================================================

def build_email_html(callouts, screenshot_base64=None, wm_week=None):
    """Build HTML email with callouts + Tableau screenshot"""
    
    if wm_week is None:
        wm_week = get_next_walmart_week()
    
    today = datetime.now(CT).strftime('%B %d, %Y')
    
    # Build callouts section
    if callouts:
        callouts_html = '<table style="width:100%; border-collapse:collapse; margin: 15px 0;">'
        callouts_html += '<thead style="background:#f0f0f0;"><tr>'
        callouts_html += '<th style="padding:10px; text-align:left; border:1px solid #ddd; font-weight:600;">Title</th>'
        callouts_html += '<th style="padding:10px; text-align:left; border:1px solid #ddd; font-weight:600;">Details</th>'
        callouts_html += '</tr></thead><tbody>'
        
        for i, callout in enumerate(callouts):
            bg = '#ffffff' if i % 2 == 0 else '#fafafa'
            title = escape(callout.get('title') or '(No title)')
            content = escape(callout.get('content') or '')
            callouts_html += f'''<tr style="background:{bg};">
                <td style="padding:10px; border:1px solid #ddd; font-weight:600;">{title}</td>
                <td style="padding:10px; border:1px solid #ddd;">{content}</td>
            </tr>'''
        
        callouts_html += '</tbody></table>'
    else:
        callouts_html = '<p style="color:#999; font-style:italic; margin:15px 0;">There are no Callouts this week.</p>'
    
    # Build screenshot section
    screenshot_html = ''
    if screenshot_base64:
        screenshot_html = f'''
        <div style="margin: 20px 0; text-align: center;">
            <h3 style="color:#0071CE; margin-bottom:15px;">Dashboard</h3>
            <a href="{TABLEAU_URL}" target="_blank" style="display:inline-block;">
                <img src="data:image/jpeg;base64,{screenshot_base64}" alt="Tableau Dashboard" style="max-width:100%; border:1px solid #ddd; border-radius:4px; max-height:600px;">
            </a>
            <p style="margin-top:10px; font-size:12px; color:#666;">
                <a href="{TABLEAU_URL}" target="_blank" style="color:#0071CE; text-decoration:none;">View full Tableau dashboard →</a>
            </p>
        </div>
        '''
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Weekly Pricing Forecast Callouts</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #333; line-height: 1.6; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
        .content {{ padding: 30px; }}
        .cta {{ background: #0071CE; color: white; padding: 15px 30px; border-radius: 6px; text-align: center; margin: 20px 0; }}
        .cta a {{ color: white; text-decoration: none; font-weight: 600; }}
        .footer {{ background: #f8f9fa; padding: 20px; text-align: center; font-size: 12px; color: #999; border-top: 1px solid #ddd; }}
        .signature {{ margin-top: 30px; padding-top: 20px; border-top: 2px solid #ddd; font-size: 13px; }}
    </style>
</head>
<body>
    <div class="container">
        <!-- HEADER -->
        <div class="header">
            <h1 style="margin: 0; font-size: 28px;">Weekly Pricing Forecast</h1>
            <p style="margin: 5px 0 0 0; opacity: 0.9;">{today}</p>
        </div>

        <!-- MAIN CONTENT -->
        <div class="content">
            <p style="font-size: 16px; margin-bottom: 20px;">
                Hello, team!<br><br>
                Please see below for next week's forecast.
            </p>

            <!-- CALLOUTS SECTION -->
            <h2 style="color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 10px;">Callouts</h2>
            {callouts_html}

            <!-- DASHBOARD SECTION -->
            <h2 style="color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 10px; margin-top: 30px;">Dashboard</h2>
            {screenshot_html}

            <!-- LINKS -->
            <div style="margin: 30px 0; padding: 20px; background: #f8f9fa; border-left: 4px solid #667eea; border-radius: 4px;">
                <h3 style="color: #667eea; margin-top: 0;">📊 Quick Links</h3>
                <ul style="list-style: none; padding: 0;">
                    <li><a href="{CALLOUTS_DASHBOARD_URL}?wm_week={wm_week}" style="color: #0071CE; text-decoration: none;">→ View Pricing Callouts Dashboard</a></li>
                    <li style="margin-top: 8px;"><a href="{TABLEAU_URL}" target="_blank" style="color: #0071CE; text-decoration: none;">→ View Full Tableau Dashboard</a></li>
                </ul>
            </div>

            <!-- CLOSING -->
            <p style="margin-top: 30px; margin-bottom: 0;">
                Please let me know if you have any questions.
            </p>

            <!-- SIGNATURE -->
            <div class="signature">
                Thank you,<br><br>
                <strong>Emily Varner</strong><br>
                Senior Manager - Pricing<br>
                Walmart US - Operations Support<br>
                479-387-8916
            </div>
        </div>

        <!-- FOOTER -->
        <div class="footer">
            <p>This email was automatically generated from the Pricing Operations Callouts Dashboard.<br>
            If you believe this was sent in error, please contact the Pricing Operations team.</p>
            <p style="margin: 10px 0 0 0;">Sent: {today} {datetime.now(CT).strftime('%I:%M %p %Z')}</p>
        </div>
    </div>
</body>
</html>
'''
    return html

# ============================================================================
# EMAIL SENDING
# ============================================================================

def send_email(recipients, subject, html_body):
    """Send email via SMTP"""
    try:
        logger.info(f'Sending email to {len(recipients)} recipients via SMTP...')
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30)
        
        for recipient in recipients:
            try:
                # Create message
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = FROM_EMAIL
                msg['To'] = recipient
                
                # Attach HTML
                msg.attach(MIMEText(html_body, 'html'))
                
                # Send
                server.send_message(msg)
                logger.info(f'✓ Email sent to {recipient}')
            
            except Exception as e:
                logger.error(f'✗ Failed to send to {recipient}: {e}')
        
        server.quit()
        logger.info(f'✓ Email sending complete')
        return True
    
    except Exception as e:
        logger.error(f'Error sending emails: {e}')
        return False

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main(preview=False, test=False):
    """Main execution"""
    logger.info('=' * 80)
    logger.info('Pricing Operations Callouts - Weekly Email')
    logger.info('=' * 80)
    
    try:
        # Determine target week
        target_week = get_next_walmart_week()
        logger.info(f'Target week: WK{target_week}')
        
        # Step 1: Capture Tableau screenshot
        screenshot_png = SCRIPT_DIR / f'tableau_screenshot_wk{target_week}.png'
        screenshot_base64 = None
        
        if capture_tableau_screenshot(str(screenshot_png)):
            try:
                with open(screenshot_png, 'rb') as f:
                    screenshot_base64 = base64.b64encode(f.read()).decode('ascii')
                logger.info(f'✓ Screenshot encoded (base64): {len(screenshot_base64)} chars')
            except Exception as e:
                logger.warning(f'Could not encode screenshot: {e}')
        
        # Step 2: Fetch callouts for next week
        callouts = fetch_callouts_for_week(target_week)
        
        # Step 3: Build HTML email
        html_body = build_email_html(callouts, screenshot_base64, target_week)
        
        # Step 4: Save preview if requested
        if preview:
            preview_path = SCRIPT_DIR / f'email_preview_wk{target_week}.html'
            with open(preview_path, 'w', encoding='utf-8') as f:
                f.write(html_body)
            logger.info(f'✓ Email preview saved: {preview_path}')
            return
        
        # Step 5: Fetch recipients
        recipients = fetch_email_recipients()
        
        if not recipients:
            logger.warning('No email recipients configured, skipping send')
            return
        
        # Step 6: Determine send recipients
        if test:
            send_recipients = ['kendall.rush@walmart.com']
            logger.info('TEST MODE: sending to test recipient only')
        else:
            send_recipients = recipients
        
        # Step 7: Send email
        subject = f'Weekly Pricing Forecast Callouts - WK{target_week}'
        success = send_email(send_recipients, subject, html_body)
        
        if success:
            logger.info('✓ Email sending completed successfully')
        else:
            logger.error('✗ Email sending failed')
        
        # Cleanup
        if screenshot_png.exists():
            try:
                screenshot_png.unlink()
                logger.info('✓ Cleaned up screenshot file')
            except:
                pass
    
    except Exception as e:
        logger.error(f'Fatal error: {e}', exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pricing Callouts Weekly Email Sender')
    parser.add_argument('--preview', action='store_true', help='Generate preview only (no send)')
    parser.add_argument('--test', action='store_true', help='Test mode (send to test email)')
    args = parser.parse_args()
    
    main(preview=args.preview, test=args.test)
