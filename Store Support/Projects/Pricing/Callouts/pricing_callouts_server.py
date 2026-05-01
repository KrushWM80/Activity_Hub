#!/usr/bin/env python3
"""
Pricing Operations Callouts Dashboard Server
Standalone Flask app (port 8091) for Home Office users to manage pricing callouts by Walmart week.

Features:
  - Intake callouts for specific WM weeks
  - Manage email recipient list via UI
  - Email preview generation
  - Callout history with audit trail
  - Auto-send Friday 4 PM email with Tableau screenshot

Usage:
  python pricing_callouts_server.py              # Run server
  python pricing_callouts_server.py --init-tables  # Initialize BigQuery tables (one-time)
"""

import os
import sys
import json
import logging
import argparse
import smtplib
import subprocess
import base64
import tempfile
from datetime import datetime, timedelta, date
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from xml.sax.saxutils import escape
from flask import Flask, render_template, request, jsonify
from google.cloud import bigquery

# ─── Configuration ───────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
LOG_DIR = SCRIPT_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "callouts_server.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Flask setup
app = Flask(__name__, template_folder=str(SCRIPT_DIR))
app.config['JSON_SORT_KEYS'] = False

# BigQuery configuration
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
    os.environ.get('APPDATA', ''), 'gcloud', 'application_default_credentials.json'
)
BQ_PROJECT = 'wmt-assetprotection-prod'
BQ_DATASET = 'Store_Support_Dev'
BQ_TABLE_CALLOUTS = 'Pricing_Weekly_Callouts'
BQ_TABLE_RECIPIENTS = 'Pricing_Callout_Email_Recipients'
BQ_TABLE_CAL_DIM = 'Cal_Dim_Data'

# Email configuration
SMTP_SERVER = 'smtp-gw1.homeoffice.wal-mart.com'
SMTP_PORT = 25
FROM_EMAIL = 'kendall.rush@walmart.com'
DASHBOARD_URL = 'https://tableau-entprod.walmart.com/views/PendingPriceChanges_16788014706880/FuturePriceChanges?%3Aembed=yes&%3Aiid=10&%3Atoolbar=yes#1'
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# ─── Utility Functions ───────────────────────────────────────────────────────

def get_bq_client():
    """Get BigQuery client."""
    return bigquery.Client(project=BQ_PROJECT)

def calculate_walmart_week():
    """Get current Walmart week from Cal_Dim_Data (WK1-WK53)."""
    try:
        client = get_bq_client()
        query = f"""
        SELECT WM_WEEK_NBR
        FROM `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE_CAL_DIM}`
        WHERE CALENDAR_DATE = CURRENT_DATE()
        LIMIT 1
        """
        result = list(client.query(query).result())
        if result:
            return int(result[0]['WM_WEEK_NBR'])
    except Exception as e:
        logger.warning(f"Could not get week from Cal_Dim_Data: {e}")
    
    # Fallback: calculate from date
    today = date.today()
    fy_start = date(today.year if today.month >= 2 else today.year - 1, 2, 1)
    days_since = (today - fy_start).days
    wm_week = (days_since // 7) + 1
    return wm_week

def calculate_next_walmart_week():
    """Calculate next Walmart week."""
    return calculate_walmart_week() + 1

def format_wm_week_string(week_num):
    """Format WM week as 'WK##' string."""
    return f"WK{week_num:02d}"

# ─── BigQuery Initialization ────────────────────────────────────────────────

def init_tables():
    """Create BigQuery tables if they don't exist."""
    client = get_bq_client()
    
    # Weekly_Callouts table
    callouts_schema = [
        bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("wm_week", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("title", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("content", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("created_date", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("created_by", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("last_modified_date", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("status", "STRING", mode="NULLABLE"),  # "active", "archived"
    ]
    
    table_ref_callouts = f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE_CALLOUTS}"
    try:
        client.get_table(table_ref_callouts)
        logger.info(f"✓ Table {table_ref_callouts} already exists")
    except Exception as e:
        if "Not found" in str(e):
            table = bigquery.Table(table_ref_callouts, schema=callouts_schema)
            client.create_table(table)
            logger.info(f"✓ Created table {table_ref_callouts}")
        else:
            raise
    
    # Callout_Email_Recipients table
    recipients_schema = [
        bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("email", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("added_date", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("is_active", "BOOLEAN", mode="REQUIRED"),
    ]
    
    table_ref_recipients = f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE_RECIPIENTS}"
    try:
        client.get_table(table_ref_recipients)
        logger.info(f"✓ Table {table_ref_recipients} already exists")
    except Exception as e:
        if "Not found" in str(e):
            table = bigquery.Table(table_ref_recipients, schema=recipients_schema)
            client.create_table(table)
            logger.info(f"✓ Created table {table_ref_recipients}")
        else:
            raise

# ─── Email Functions ────────────────────────────────────────────────────────

def capture_dashboard_screenshot(wm_week):
    """
    Load latest Tableau dashboard screenshot from local images folder.
    
    Checks ../Images for the most recent PNG/JPG file,
    converts it to base64, and returns for email embedding.
    """
    try:
        # Path to images folder (../Images from Callouts folder)
        images_folder = Path(SCRIPT_DIR).parent / 'Images'
        
        logger.info(f'Looking for dashboard image in: {images_folder}')
        
        if not images_folder.exists():
            logger.warning(f'Images folder does not exist: {images_folder}')
            return None
        
        # Find all image files (png, jpg, jpeg)
        image_files = list(images_folder.glob('*.png')) + \
                      list(images_folder.glob('*.jpg')) + \
                      list(images_folder.glob('*.jpeg'))
        
        if not image_files:
            logger.warning('No image files found in images folder')
            return None
        
        # Get the most recently modified image
        latest_image = max(image_files, key=lambda p: p.stat().st_mtime)
        file_size = latest_image.stat().st_size
        
        logger.info(f'Using latest image: {latest_image.name} ({file_size:,} bytes)')
        
        # Read and encode to base64
        with open(latest_image, 'rb') as f:
            image_data = f.read()
            screenshot_base64 = base64.b64encode(image_data).decode('ascii')
        
        logger.info(f'Image encoded to base64 for email embedding')
        return screenshot_base64
    
    except Exception as e:
        logger.error(f'Error loading dashboard image: {e}')
        return None

def build_callout_email_html(callouts, wm_week, screenshot_base64=None):
    """Build HTML email with callouts for the week - matches official template."""
    
    # Build callouts section
    if callouts:
        callouts_html = '<div style="margin: 15px 0;">'
        
        for callout in callouts:
            content = escape(callout.get('content') or '')
            callouts_html += f'''<p style="margin:10px 0; padding:10px; background:#f9f9f9; border-left:4px solid #FFCC00; border-radius:2px;">{content}</p>'''
        
        callouts_html += '</div>'
    else:
        callouts_html = '<p style="color:#666; margin:15px 0;">There are no Callouts this week.</p>'
    
    # Build dashboard section with screenshot and link
    dashboard_html = ''
    if screenshot_base64:
        dashboard_html = f'<p><img src="data:image/png;base64,{screenshot_base64}" alt="Dashboard Screenshot" style="max-width:100%; border:1px solid #ddd; border-radius:4px; margin: 15px 0;"></p>'
    
    dashboard_html += f'''<p><strong>View the dashboard:</strong></p>
<p><a href="{DASHBOARD_URL}" style="color: #0071CE; text-decoration: none; font-weight: bold;">Future Price Changes →</a></p>'''
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Weekly Pricing Forecast Callouts</title>
    <style>
        body {{ font-family: Arial, sans-serif; color: #333; line-height: 1.5; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; }}
        .content {{ padding: 20px; }}
        .section {{ margin: 20px 0; }}
        .signature {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 13px; }}
        h2 {{ color: #0071CE; font-size: 16px; margin: 20px 0 10px 0; }}
        p {{ margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="content">
            <p>Hello, team!</p>
            
            <p>Please see below for next week's forecast.</p>
            
            <h2>Callouts:</h2>
            <div class="section">
                {callouts_html}
            </div>
            
            <h2>Dashboard:</h2>
            <div class="section">
                {dashboard_html}
            </div>
            
            <p>Please let me know if you have any questions.</p>
            
            <p>Thank you,</p>
            
            <div class="signature">
                Emily Varner<br>
                Senior Manager - Pricing<br>
                Walmart US - Operations Support<br>
                479-387-8916
            </div>
        </div>
    </div>
</body>
</html>
'''
    return html

def send_test_email(recipient_email, subject, html_body):
    """Send test email via Walmart SMTP server."""
    try:
        logger.info(f'Connecting to {SMTP_SERVER}:{SMTP_PORT}...')
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30)
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = FROM_EMAIL
        msg['To'] = recipient_email
        msg.attach(MIMEText(html_body, 'html'))
        
        server.send_message(msg)
        server.quit()
        
        logger.info(f'[SUCCESS] Test email sent to {recipient_email}')
        return True
    
    except Exception as e:
        logger.error(f'Error sending email: {e}')
        return False

# ─── Routes: HTML Pages ──────────────────────────────────────────────────────

@app.route('/')
def dashboard():
    """Serve main dashboard page."""
    current_wm_week = calculate_walmart_week()
    next_wm_week = calculate_next_walmart_week()
    return render_template('dashboard.html', 
                          current_wm_week=current_wm_week,
                          next_wm_week=next_wm_week)

@app.route('/PricingOperationsCallouts')
def dashboard_pricing_callouts():
    """Serve main dashboard page (alternate URL)."""
    current_wm_week = calculate_walmart_week()
    next_wm_week = calculate_next_walmart_week()
    return render_template('dashboard.html', 
                          current_wm_week=current_wm_week,
                          next_wm_week=next_wm_week)

# ─── API Routes: Callouts ────────────────────────────────────────────────────

@app.route('/api/callouts/<int:wm_week>', methods=['GET'])
def get_callouts(wm_week):
    """Fetch callouts for a specific WM week with current fiscal year."""
    try:
        client = get_bq_client()
        
        # Get current fiscal year from today's date
        current_fy_query = f"""
        SELECT FISCAL_YEAR_NBR
        FROM `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE_CAL_DIM}`
        WHERE CALENDAR_DATE = CURRENT_DATE()
        LIMIT 1
        """
        current_fy_results = list(client.query(current_fy_query).result())
        fiscal_year = int(current_fy_results[0]['FISCAL_YEAR_NBR']) if current_fy_results else 2027
        
        # Get callouts
        query = f"""
        SELECT 
            id, wm_week, title, content, created_date, created_by, 
            last_modified_date, status
        FROM `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE_CALLOUTS}`
        WHERE wm_week = @wm_week AND (status IS NULL OR status = 'active')
        ORDER BY created_date DESC
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("wm_week", "INTEGER", wm_week)]
        )
        results = client.query(query, job_config=job_config).result()
        callouts = [dict(row) for row in results]
        
        # Add fiscal year and convert timestamps to ISO format strings
        for c in callouts:
            c['fiscal_year'] = fiscal_year
            c['created_date'] = c['created_date'].isoformat() if c['created_date'] else None
            c['last_modified_date'] = c['last_modified_date'].isoformat() if c['last_modified_date'] else None
        
        logger.info(f"✓ Fetched {len(callouts)} callouts for WK{wm_week} (FY {fiscal_year})")
        return jsonify({"success": True, "data": callouts, "fiscal_year": fiscal_year})
    except Exception as e:
        logger.error(f"Error fetching callouts for WK{wm_week}: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/callouts', methods=['POST'])
def create_callout():
    """Create a new callout."""
    try:
        data = request.get_json()
        wm_week = data.get('wm_week')
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        created_by = data.get('created_by', 'Unknown User').strip()
        
        if not wm_week or not title or not content:
            return jsonify({"success": False, "error": "Missing required fields"}), 400
        
        # Generate ID
        callout_id = f"callout_{wm_week}_{int(datetime.now().timestamp())}"
        now = datetime.utcnow().isoformat()
        
        client = get_bq_client()
        table = client.get_table(f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE_CALLOUTS}")
        rows = [
            {
                "id": callout_id,
                "wm_week": wm_week,
                "title": title,
                "content": content,
                "created_date": now,
                "created_by": created_by,
                "last_modified_date": now,
                "status": "active",
            }
        ]
        client.insert_rows_json(table, rows)
        
        logger.info(f"✓ Created callout {callout_id} for WK{wm_week}")
        return jsonify({"success": True, "id": callout_id})
    except Exception as e:
        logger.error(f"Error creating callout: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/callouts/<callout_id>', methods=['PUT'])
def update_callout(callout_id):
    """Update an existing callout."""
    try:
        data = request.get_json()
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        
        # Title is required; content is optional
        if not title:
            return jsonify({"success": False, "error": "Title is required"}), 400
        
        now = datetime.utcnow()
        client = get_bq_client()
        
        # Build dynamic UPDATE query - only update content if provided
        if content:
            set_clause = "SET title = @title, content = @content, last_modified_date = @now"
            params = [
                bigquery.ScalarQueryParameter("title", "STRING", title),
                bigquery.ScalarQueryParameter("content", "STRING", content),
                bigquery.ScalarQueryParameter("now", "TIMESTAMP", now),
                bigquery.ScalarQueryParameter("id", "STRING", callout_id),
            ]
        else:
            set_clause = "SET title = @title, last_modified_date = @now"
            params = [
                bigquery.ScalarQueryParameter("title", "STRING", title),
                bigquery.ScalarQueryParameter("now", "TIMESTAMP", now),
                bigquery.ScalarQueryParameter("id", "STRING", callout_id),
            ]
        
        query = f"""
        UPDATE `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE_CALLOUTS}`
        {set_clause}
        WHERE id = @id
        """
        job_config = bigquery.QueryJobConfig(query_parameters=params)
        client.query(query, job_config=job_config).result()
        
        logger.info(f"✓ Updated callout {callout_id}")
        return jsonify({"success": True})
    except Exception as e:
        logger.error(f"Error updating callout {callout_id}: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/callouts/<callout_id>', methods=['DELETE'])
def delete_callout(callout_id):
    """Delete (soft) a callout by setting status to archived."""
    try:
        client = get_bq_client()
        query = f"""
        UPDATE `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE_CALLOUTS}`
        SET status = 'archived'
        WHERE id = @id
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("id", "STRING", callout_id)]
        )
        client.query(query, job_config=job_config).result()
        
        logger.info(f"✓ Archived callout {callout_id}")
        return jsonify({"success": True})
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error deleting callout {callout_id}: {error_msg}")
        
        # Handle streaming buffer error - data was recently inserted
        if "streaming buffer" in error_msg.lower():
            return jsonify({
                "success": False, 
                "error": "Callout is too new. Please wait a few seconds before deleting."
            }), 409  # 409 Conflict
        
        return jsonify({"success": False, "error": error_msg}), 500

# ─── API Routes: Email Recipients ────────────────────────────────────────────

@app.route('/api/email-recipients', methods=['GET'])
def get_email_recipients():
    """Get all active email recipients."""
    try:
        client = get_bq_client()
        query = f"""
        SELECT id, email, added_date, is_active
        FROM `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE_RECIPIENTS}`
        WHERE is_active = TRUE
        ORDER BY added_date DESC
        """
        results = client.query(query).result()
        recipients = [dict(row) for row in results]
        logger.info(f"[DEBUG] Raw recipients from BigQuery: {recipients}")
        
        # Convert timestamps to ISO format (handle both string and datetime)
        for r in recipients:
            if r['added_date']:
                if isinstance(r['added_date'], str):
                    # Already a string, keep as is
                    r['added_date'] = r['added_date']
                else:
                    # DateTime object, convert to ISO string
                    r['added_date'] = r['added_date'].isoformat()
            else:
                r['added_date'] = None
        
        logger.info(f"[DEBUG] Processed recipients: {recipients}")
        logger.info(f"[DEBUG] Total recipients to return: {len(recipients)}")
        return jsonify({"success": True, "data": recipients})
    except Exception as e:
        logger.error(f"Error fetching email recipients: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/email-recipients', methods=['POST'])
def add_email_recipient():
    """Add a new email recipient."""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        
        if not email or '@' not in email:
            return jsonify({"success": False, "error": "Invalid email address"}), 400
        
        # Check if already exists
        client = get_bq_client()
        check_query = f"""
        SELECT COUNT(*) as cnt FROM `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE_RECIPIENTS}`
        WHERE email = @email AND is_active = TRUE
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("email", "STRING", email)]
        )
        result = list(client.query(check_query, job_config=job_config).result())
        if result[0]['cnt'] > 0:
            return jsonify({"success": False, "error": "Email already exists"}), 400
        
        recipient_id = f"recipient_{int(datetime.now().timestamp())}"
        now = datetime.utcnow().isoformat()
        
        table = client.get_table(f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE_RECIPIENTS}")
        rows = [
            {
                "id": recipient_id,
                "email": email,
                "added_date": now,
                "is_active": True,
            }
        ]
        client.insert_rows_json(table, rows)
        
        logger.info(f"✓ Added email recipient: {email}")
        return jsonify({"success": True, "id": recipient_id})
    except Exception as e:
        logger.error(f"Error adding email recipient: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/email-recipients/<recipient_id>', methods=['DELETE'])
def remove_email_recipient(recipient_id):
    """Remove (soft delete) an email recipient."""
    try:
        client = get_bq_client()
        query = f"""
        UPDATE `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE_RECIPIENTS}`
        SET is_active = FALSE
        WHERE id = @id
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("id", "STRING", recipient_id)]
        )
        client.query(query, job_config=job_config).result()
        
        logger.info(f"✓ Removed email recipient {recipient_id}")
        return jsonify({"success": True})
    except Exception as e:
        logger.error(f"Error removing email recipient {recipient_id}: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/send-test-email', methods=['POST'])
def send_test_email_endpoint():
    """Send a test email with Friday callouts preview and dashboard screenshot."""
    try:
        data = request.get_json()
        recipient_email = data.get('recipient_email', '').strip().lower()
        wm_week = data.get('wm_week', calculate_next_walmart_week())
        
        if not recipient_email or '@' not in recipient_email:
            return jsonify({"success": False, "error": "Invalid email address"}), 400
        
        # Fetch callouts for the week
        client = get_bq_client()
        query = f"""
        SELECT id, wm_week, title, content, created_date, created_by, last_modified_date, status
        FROM `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE_CALLOUTS}`
        WHERE wm_week = @wm_week AND (status IS NULL OR status = 'active')
        ORDER BY created_date DESC
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("wm_week", "INTEGER", wm_week)]
        )
        results = client.query(query, job_config=job_config).result()
        callouts = [dict(row) for row in results]
        
        # Capture dashboard screenshot
        logger.info(f'Capturing dashboard screenshot for WK{wm_week}...')
        screenshot_base64 = capture_dashboard_screenshot(wm_week)
        
        # Build email HTML with screenshot
        html_body = build_callout_email_html(callouts, wm_week, screenshot_base64)
        subject = f"Weekly Pricing Forecast Callouts - WK{wm_week}"
        
        # Send email
        if send_test_email(recipient_email, subject, html_body):
            return jsonify({
                "success": True,
                "message": f"Test email sent to {recipient_email}",
                "callout_count": len(callouts),
                "week": wm_week,
                "screenshot": "included" if screenshot_base64 else "failed"
            })
        else:
            return jsonify({"success": False, "error": "Failed to send email"}), 500
    
    except Exception as e:
        logger.error(f"Error sending test email: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

# ─── API Routes: Utilities ───────────────────────────────────────────────────

@app.route('/api/current-time', methods=['GET'])
def get_current_time():
    """Get current server time (for countdown timer)."""
    return jsonify({
        "current_time": datetime.now().isoformat(),
        "current_wm_week": calculate_walmart_week(),
        "next_wm_week": calculate_next_walmart_week(),
    })

@app.route('/api/weeks', methods=['GET'])
def get_weeks():
    """Fetch available weeks from Cal Dim data."""
    try:
        fy = request.args.get('fy', None)
        
        client = get_bq_client()
        query = f"""
        SELECT DISTINCT WM_WEEK_NBR as week_number, FISCAL_YEAR_NBR as fy_year
        FROM `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE_CAL_DIM}`
        WHERE FISCAL_YEAR_NBR IS NOT NULL
        """
        if fy:
            query += f" AND FISCAL_YEAR_NBR = {int(fy)}"
        
        query += " ORDER BY FISCAL_YEAR_NBR DESC, WM_WEEK_NBR ASC"
        
        result = list(client.query(query).result())
        weeks = [{"week": int(row['week_number']), "fy": int(row['fy_year'])} for row in result]
        
        logger.info(f"✓ Fetched {len(weeks)} weeks from Cal Dim")
        return jsonify({"success": True, "weeks": weeks})
    except Exception as e:
        logger.warning(f"Could not fetch weeks from Cal Dim: {e}. Using default weeks.")
        # Fallback: generate 52 weeks for current FY
        current_week = calculate_walmart_week()
        current_fy = date.today().year if date.today().month >= 2 else date.today().year - 1
        weeks = [{"week": i, "fy": current_fy} for i in range(1, 53)]
        return jsonify({"success": True, "weeks": weeks, "fallback": True})

@app.route('/api/fy', methods=['GET'])
def get_fiscal_years():
    """Fetch available fiscal years from Cal_Dim_Data."""
    try:
        client = get_bq_client()
        
        # Get today's fiscal year from Cal_Dim_Data
        current_fy_query = f"""
        SELECT FISCAL_YEAR_NBR as fy_year
        FROM `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE_CAL_DIM}`
        WHERE CALENDAR_DATE = CURRENT_DATE()
        LIMIT 1
        """
        current_fy_result = list(client.query(current_fy_query).result())
        current_fy = int(current_fy_result[0]['fy_year']) if current_fy_result else 2026
        
        # Return current FY and 2 prior years
        fiscal_years = [current_fy, current_fy - 1, current_fy - 2]
        
        logger.info(f"✓ Fiscal years: {fiscal_years}. Current FY: {current_fy}")
        return jsonify({"success": True, "fiscal_years": fiscal_years, "current_fy": current_fy})
    except Exception as e:
        logger.warning(f"Could not fetch fiscal years: {e}. Using default.")
        fiscal_years = [2027, 2026, 2025]
        current_fy = 2027
        return jsonify({"success": True, "fiscal_years": fiscal_years, "current_fy": current_fy, "fallback": True})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/walmart-spark-logo.png')
def serve_logo():
    """Serve the Walmart Spark logo."""
    logo_path = SCRIPT_DIR / 'walmart-spark-logo.png'
    if not logo_path.exists():
        return jsonify({"error": "Logo not found"}), 404
    
    with open(logo_path, 'rb') as f:
        logo_data = f.read()
    
    from flask import Response
    return Response(logo_data, mimetype='image/png')

# ─── Error Handlers ──────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({"success": False, "error": "Internal server error"}), 500

# ─── Main ───────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pricing Callouts Server')
    parser.add_argument('--init-tables', action='store_true', help='Initialize BigQuery tables')
    args = parser.parse_args()
    
    if args.init_tables:
        logger.info("Initializing BigQuery tables...")
        init_tables()
        logger.info("✓ Initialization complete")
        sys.exit(0)
    
    logger.info("Starting Pricing Callouts Server on port 8091...")
    app.run(host='0.0.0.0', port=8091, debug=False, use_reloader=False)
