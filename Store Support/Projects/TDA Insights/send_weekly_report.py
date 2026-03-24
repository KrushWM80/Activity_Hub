#!/usr/bin/env python3
"""
TDA Insights Weekly Email Report
Generates a PPT of all projects and sends via Outlook.
Scheduled for Thursdays at 11:00 AM Central Time.

Usage:
  python send_weekly_report.py              # Send email
  python send_weekly_report.py --preview    # Preview only (save PPT + HTML, no send)
"""

import os
import sys
import json
import io
import re
import zipfile
import time
import base64
import struct
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape
from PIL import Image, ImageChops

# Configuration
RECIPIENTS = ["Kendall.rush@walmart.com", "Matthew.Farnworth@walmart.com", "Justin.Barrick@walmart.com"]
SUBJECT = "TDA Initiative Insights - Weekly Report"
DASHBOARD_URL = "http://WEUS42608431466:5000/tda-initiatives-insights"
SCRIPT_DIR = Path(__file__).parent
# Walmart fiscal week: FY starts Saturday closest to Feb 1
def _walmart_week():
    from datetime import date
    today = date.today()
    # FY start dates (Saturday closest to Feb 1)
    jan31 = date(today.year, 1, 31)
    # Find Saturday closest to Feb 1 (weekday 5=Saturday)
    feb1 = date(today.year, 2, 1)
    days_to_sat = (5 - feb1.weekday()) % 7
    nearest_sat = feb1 + __import__('datetime').timedelta(days=days_to_sat - 7 if days_to_sat > 3 else days_to_sat)
    if today < nearest_sat:
        # Use previous year's FY start
        feb1_prev = date(today.year - 1, 2, 1)
        days_to_sat = (5 - feb1_prev.weekday()) % 7
        nearest_sat = feb1_prev + __import__('datetime').timedelta(days=days_to_sat - 7 if days_to_sat > 3 else days_to_sat)
    return (today - nearest_sat).days // 7 + 1

WEEK_NUM = _walmart_week()
PPT_OUTPUT = SCRIPT_DIR / f"TDA_WK{WEEK_NUM}_Report.pptx"
PDF_OUTPUT = SCRIPT_DIR / f"TDA_WK{WEEK_NUM}_Report.pdf"
HTML_PREVIEW = SCRIPT_DIR / "email_preview.html"

# BQ Configuration
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
    os.environ.get('APPDATA', ''), 'gcloud', 'application_default_credentials.json'
)
BQ_PROJECT = 'wmt-assetprotection-prod'
BQ_DATASET = 'Store_Support_Dev'
BQ_TABLE = 'Output- TDA Report'

EXCLUDED_PHASES = {'Complete'}
PHASE_ORDER = ['Pending', 'POC/POT', 'Test', 'Mkt Scale', 'Roll/Deploy']

SPARK_LOGO = Path(__file__).parent.parent.parent / "General Setup" / "Design" / "Spark Blank.png"
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# Colors
COLORS = {
    'walmart_blue': '#0071CE',
    'walmart_blue_dark': '#004C91',
    'walmart_yellow': '#FFC220',
    'on_track': '#107C10',
    'at_risk': '#F7630C',
    'off_track': '#DC3545',
    'continuous': '#6F42C1',
}


def fetch_data():
    """Fetch latest data from BigQuery"""
    from google.cloud import bigquery
    client = bigquery.Client(project=BQ_PROJECT)
    query = f"""
    SELECT
        Topic as `Initiative - Project Title`,
        Health_Update as `Health Status`,
        Phase,
        SUM(CASE WHEN Phase = Facility_Phase THEN Facility ELSE 0 END) as `# of Stores`,
        Dallas_POC as `Dallas POC`,
        Intake_n_Testing as `Intake & Testing`,
        Deployment,
        MAX(Intake_Card_Nbr) as `Project ID`,
        COALESCE(TDA_Ownership, 'No Selection Provided') as `TDA Ownership`
    FROM `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE}`
    WHERE Topic IS NOT NULL
    GROUP BY Topic, Health_Update, Phase, Intake_n_Testing, Dallas_POC, Deployment, TDA_Ownership
    ORDER BY Topic
    """
    results = client.query(query).result()
    data = []
    for row in results:
        phase = row['Phase'] or 'Unknown'
        if phase in EXCLUDED_PHASES:
            continue
        data.append({
            'Initiative - Project Title': row['Initiative - Project Title'] or 'Unknown',
            'Health Status': row['Health Status'] or 'Unknown',
            'Phase': phase,
            '# of Stores': row['# of Stores'] or 0,
            'Dallas POC': row['Dallas POC'] or 'N/A',
            'Intake & Testing': row['Intake & Testing'] or 'N/A',
            'Deployment': row['Deployment'] or 'N/A',
            'Project ID': row['Project ID'] or 0,
            'TDA Ownership': row['TDA Ownership'] or 'No Selection Provided',
        })
    return data


def build_email_html(data):
    """Build professional HTML email body with summary + phase tables"""
    today = datetime.now().strftime('%B %d, %Y')

    # Summary counts
    total = len(data)
    total_stores = sum(int(r.get('# of Stores', 0) or 0) for r in data)
    health_counts = {}
    phase_counts = {}
    for r in data:
        h = r['Health Status']
        p = r['Phase']
        health_counts[h] = health_counts.get(h, 0) + 1
        phase_counts[p] = phase_counts.get(p, 0) + 1

    on_track = health_counts.get('On Track', 0)
    at_risk = health_counts.get('At Risk', 0)
    off_track = health_counts.get('Off Track', 0)
    continuous = health_counts.get('Continuous', 0)

    def badge_style(status):
        s = status.lower()
        if 'on track' in s:
            return f"background-color:rgba(16,124,16,0.15);color:{COLORS['on_track']};padding:3px 10px;border-radius:12px;font-weight:600;font-size:12px;display:inline-block;"
        elif 'at risk' in s:
            return f"background-color:rgba(247,99,12,0.15);color:{COLORS['at_risk']};padding:3px 10px;border-radius:12px;font-weight:600;font-size:12px;display:inline-block;"
        elif 'off track' in s:
            return f"background-color:rgba(220,53,69,0.15);color:{COLORS['off_track']};padding:3px 10px;border-radius:12px;font-weight:600;font-size:12px;display:inline-block;"
        elif 'continuous' in s:
            return f"background-color:rgba(111,66,193,0.15);color:{COLORS['continuous']};padding:3px 10px;border-radius:12px;font-weight:600;font-size:12px;display:inline-block;"
        return "padding:3px 10px;border-radius:12px;font-weight:600;font-size:12px;display:inline-block;"

    total_stores_display = f'{total_stores:,}'

    # Spark logo as base64 for email embedding
    spark_b64 = ''
    if SPARK_LOGO.exists():
        spark_b64 = base64.b64encode(SPARK_LOGO.read_bytes()).decode('ascii')

    spark_img = f'<img src="data:image/png;base64,{spark_b64}" width="44" height="44" alt="Spark" style="display:block;"/>' if spark_b64 else '&#10058;'

    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: 'Segoe UI', Arial, sans-serif; color: #333; max-width: 1000px; margin: 0 auto; padding: 20px;">

<!-- Header -->
<table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 24px;">
<tr>
<td bgcolor="{COLORS['walmart_blue_dark']}" style="background-color:{COLORS['walmart_blue_dark']}; padding: 24px 30px;">
    <table><tr>
    <td style="padding-right: 15px; vertical-align: middle;">
        {spark_img}
    </td>
    <td>
        <div style="color: white; font-size: 26px; font-weight: 700;">TDA Initiative Insights</div>
        <div style="color: #cccccc; font-size: 13px; margin-top: 2px;">Weekly Report &mdash; {today}</div>
    </td>
    </tr></table>
</td>
</tr>
</table>

<!-- Dashboard Button -->
<table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 24px;">
<tr>
<td align="center" style="padding: 16px 0;">
    <table cellpadding="0" cellspacing="0" style="border-collapse: separate;">
    <tr>
    <td align="center" bgcolor="#0052CC" style="background-color: #0052CC; border-radius: 30px; mso-padding-alt: 14px 40px;">
        <a href="{DASHBOARD_URL}" target="_blank" style="background-color: #0052CC; color: #FFFFFF; font-family: 'Segoe UI', Arial, sans-serif; font-size: 16px; font-weight: 700; text-decoration: none; padding: 14px 40px; border-radius: 30px; display: inline-block; letter-spacing: 0.5px; mso-padding-alt: 0; border: 2px solid #0052CC;">Go to Dashboard</a>
    </td>
    </tr>
    </table>
</td>
</tr>
</table>

<!-- Context -->
<table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 24px;"><tr>
<td bgcolor="#f8f9fa" style="background-color:#f8f9fa; border: 1px solid #e5e5e5; padding: 16px 20px; font-size: 13px; line-height: 1.6; color: #444;">
    <strong style="color: {COLORS['walmart_blue_dark']};">About This Report</strong><br>
    This is your weekly TDA (Technology Deployment Acceleration) Initiative Insights report. It provides a snapshot of all active projects currently tracked through the Intake Hub, filtered to Implement, Validation, and Intake &amp; Test branches. Projects are grouped by their current phase in the deployment pipeline. Each project title links directly to its Intake Hub card for full details. A PowerPoint version is attached for offline review and sharing.
</td></tr></table>

<!-- Summary Cards -->
<table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 24px;">
<tr>
    <td width="16%" style="padding: 0 4px;">
        <div style="background:white; border:1px solid #e5e5e5; border-left:4px solid {COLORS['walmart_yellow']}; border-radius:6px; padding:12px; text-align:center;">
            <div style="font-size:11px; color:#666; text-transform:uppercase; letter-spacing:0.5px;">Total Projects</div>
            <div style="font-size:24px; font-weight:700; color:{COLORS['walmart_blue_dark']};">{total}</div>
        </div>
    </td>
    <td width="16%" style="padding: 0 4px;">
        <div style="background:white; border:1px solid #e5e5e5; border-left:4px solid {COLORS['walmart_yellow']}; border-radius:6px; padding:12px; text-align:center;">
            <div style="font-size:11px; color:#666; text-transform:uppercase; letter-spacing:0.5px;">Total Stores</div>
            <div style="font-size:24px; font-weight:700; color:{COLORS['walmart_blue_dark']};">{total_stores_display}</div>
        </div>
    </td>
    <td width="16%" style="padding: 0 4px;">
        <div style="background:white; border:1px solid #e5e5e5; border-left:4px solid {COLORS['on_track']}; border-radius:6px; padding:12px; text-align:center;">
            <div style="font-size:11px; color:#666; text-transform:uppercase; letter-spacing:0.5px;">On Track</div>
            <div style="font-size:24px; font-weight:700; color:{COLORS['on_track']};">{on_track}</div>
        </div>
    </td>
    <td width="16%" style="padding: 0 4px;">
        <div style="background:white; border:1px solid #e5e5e5; border-left:4px solid {COLORS['at_risk']}; border-radius:6px; padding:12px; text-align:center;">
            <div style="font-size:11px; color:#666; text-transform:uppercase; letter-spacing:0.5px;">At Risk</div>
            <div style="font-size:24px; font-weight:700; color:{COLORS['at_risk']};">{at_risk}</div>
        </div>
    </td>
    <td width="16%" style="padding: 0 4px;">
        <div style="background:white; border:1px solid #e5e5e5; border-left:4px solid {COLORS['off_track']}; border-radius:6px; padding:12px; text-align:center;">
            <div style="font-size:11px; color:#666; text-transform:uppercase; letter-spacing:0.5px;">Off Track</div>
            <div style="font-size:24px; font-weight:700; color:{COLORS['off_track']};">{off_track}</div>
        </div>
    </td>
    <td width="16%" style="padding: 0 4px;">
        <div style="background:white; border:1px solid #e5e5e5; border-left:4px solid {COLORS['continuous']}; border-radius:6px; padding:12px; text-align:center;">
            <div style="font-size:11px; color:#666; text-transform:uppercase; letter-spacing:0.5px;">Continuous</div>
            <div style="font-size:24px; font-weight:700; color:{COLORS['continuous']};">{continuous}</div>
        </div>
    </td>
</tr>
</table>
"""

    # Phase tables — grouped by TDA Ownership → Phase
    UNASSIGNED = 'No Selection Provided'

    # Build ordered sections: Pending+unassigned first, then custom ownership order
    OWNERSHIP_ORDER = ['Dallas POC', 'Intake & Test', 'Deployment', UNASSIGNED]
    sections = []
    pending_unassigned = [r for r in data if r['Phase'] == 'Pending' and r.get('TDA Ownership', UNASSIGNED) == UNASSIGNED]
    if pending_unassigned:
        sections.append(('TDA Ownership - Currently No TDA Ownership', 'Pending', pending_unassigned, False))

    # Ordered ownership list: defined order first, then any new values alphabetically
    all_ownerships = set(r.get('TDA Ownership', UNASSIGNED) or UNASSIGNED for r in data)
    known_set = set(OWNERSHIP_ORDER)
    unknown_ownerships = sorted(o for o in all_ownerships if o not in known_set)
    ownership_list = [o for o in OWNERSHIP_ORDER if o in all_ownerships] + unknown_ownerships
    for ownership in ownership_list:
        for phase in PHASE_ORDER:
            if phase == 'Pending' and ownership == UNASSIGNED:
                continue  # already handled above
            phase_data = [r for r in data if (r.get('TDA Ownership', UNASSIGNED) or UNASSIGNED) == ownership and r['Phase'] == phase]
            if not phase_data:
                continue
            label = 'TDA Ownership - Currently No TDA Ownership' if ownership == UNASSIGNED else ownership
            sections.append((label, phase, phase_data, False))

    for ownership_label, phase, phase_data, _unused in sections:
        count = len(phase_data)
        # Ownership banner (navy)
        html += f"""
<!-- {ownership_label} / {phase} Section -->
<div style="background:#1E3A8A; color:white; padding:10px 16px; font-size:15px; font-weight:700; border-radius:6px 6px 0 0; margin-top:16px;">
    {escape(ownership_label)} &mdash; {count} Project{'s' if count != 1 else ''}
</div>
"""
        # Phase sub-banner (blue, half height)
        html += f"""<div style="background:{COLORS['walmart_blue']}; color:white; padding:5px 16px; font-size:13px; font-weight:600;">
    {escape(phase)}
</div>
"""
        html += f"""<table width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #e5e5e5; border-top:none; border-collapse:collapse; margin-bottom:8px; font-size:14px;">
<thead>
<tr style="background:#f5f5f5;">
    <th style="padding:10px 12px; text-align:left; border-bottom:2px solid #ddd; font-weight:700; color:#333; font-size:14px;">Initiative - Project Title</th>
    <th style="padding:10px 12px; text-align:left; border-bottom:2px solid #ddd; font-weight:700; color:#333; font-size:14px; width:100px;">Health</th>
    <th style="padding:10px 12px; text-align:center; border-bottom:2px solid #ddd; font-weight:700; color:#333; font-size:14px; width:80px;"># of Stores</th>
</tr>
</thead>
<tbody>
"""
        for i, row in enumerate(phase_data):
            bg = '#ffffff' if i % 2 == 0 else '#fafafa'
            title = escape(row['Initiative - Project Title'])
            pid = row.get('Project ID', 0)
            link = f'https://hoops.wal-mart.com/intake-hub/projects/{pid}' if pid else '#'
            health = escape(row['Health Status'])
            stores = int(row.get('# of Stores', 0) or 0)
            stores_display = f'{stores:,}'
            bs = badge_style(row['Health Status'])

            html += f"""<tr style="background:{bg};">
    <td style="padding:10px 12px; border-bottom:1px solid #eee;"><a href="{link}" style="color:{COLORS['walmart_blue']}; text-decoration:none; font-weight:500; font-size:14px;">{title}</a></td>
    <td style="padding:10px 12px; border-bottom:1px solid #eee;"><span style="{bs}">{health}</span></td>
    <td style="padding:10px 12px; border-bottom:1px solid #eee; text-align:center; font-weight:600; color:{COLORS['walmart_blue']}; font-size:14px;">{stores_display}</td>
</tr>
"""
        html += "</tbody></table>\n"

    # Footer
    html += f"""
<div style="margin-top:24px; padding:16px; border-top:2px solid #e5e5e5; text-align:center; color:#999; font-size:11px;">
    <p>This report was automatically generated from the TDA Initiative Insights Dashboard.<br>
    PPT report is attached for offline review.</p>
    <p style="margin-top:8px;">Generated on {today} at {datetime.now().strftime('%I:%M %p')} CT</p>
</div>

</body>
</html>"""
    return html


def _build_phase_html(phase, rows, ownership=None, is_special=False):
    """Build the EXACT same HTML the dashboard builds for PPT screenshots."""
    columns = ['Initiative - Project Title', 'Health Status', 'Phase',
                '# of Stores', 'Dallas POC', 'Intake & Testing', 'Deployment']

    # Ownership banner (navy) + phase sub-banner (blue, half height)
    ownership_label = ownership or phase
    banner = f'<div style="background:#1E3A8A;color:white;padding:15px 20px;font-size:18px;font-weight:700;text-align:center;border-radius:4px 4px 0 0;">{escape(ownership_label)}</div>'
    banner += f'<div style="background:#3B82F6;color:white;padding:7px 20px;font-size:14px;font-weight:600;text-align:center;">{escape(phase)}</div>'

    table = '<table style="width:100%;border-collapse:collapse;font-size:14px;font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',\'Helvetica Neue\',Arial,sans-serif;">'
    table += '<thead style="background-color:#F5F5F5;border-bottom:2px solid #E5E5E5;"><tr>'
    for col in columns:
        table += f'<th style="padding:16px 24px;text-align:left;font-weight:600;color:#212121;white-space:nowrap;">{escape(col)}</th>'
    table += '</tr></thead><tbody>'

    for row in rows:
        table += '<tr>'
        for col in columns:
            value = str(row.get(col, '') or '')
            if col == '# of Stores':
                value = str(int(row.get(col, 0) or 0))
            cell_style = 'padding:16px 24px;border-bottom:1px solid #E5E5E5;text-align:left;'

            if col == 'Health Status':
                status = value.lower()
                bg, clr = '#f0f0f0', '#333'
                if 'on track' in status:
                    bg, clr = 'rgba(16,124,16,0.2)', '#107C10'
                elif 'at risk' in status:
                    bg, clr = 'rgba(247,99,12,0.2)', '#F7630C'
                elif 'off track' in status:
                    bg, clr = 'rgba(220,53,69,0.2)', '#DC3545'
                elif 'continuous' in status:
                    bg, clr = 'rgba(111,66,193,0.2)', '#6F42C1'
                table += f'<td style="{cell_style}"><span style="display:inline-block;padding:4px 10px;background-color:{bg};color:{clr};border-radius:12px;font-weight:600;font-size:12px;white-space:nowrap;">{escape(value)}</span></td>'
            elif col == 'Phase':
                table += f'<td style="{cell_style}"><span style="display:inline-block;padding:4px 10px;background-color:#DBEAFE;color:#1E3A8A;border-radius:4px;font-weight:500;font-size:12px;">{escape(value)}</span></td>'
            elif col == '# of Stores':
                table += f'<td style="{cell_style}font-weight:600;color:#0071CE;">{escape(value)}</td>'
            elif col == 'Initiative - Project Title':
                pid = row.get('Project ID', 0)
                if pid:
                    table += f'<td style="{cell_style}"><a href="https://hoops.wal-mart.com/intake-hub/projects/{pid}" style="color:#0071CE;text-decoration:none;font-weight:500;">{escape(value)}</a></td>'
                else:
                    table += f'<td style="{cell_style}">{escape(value)}</td>'
            else:
                table += f'<td style="{cell_style}">{escape(value)}</td>'
        table += '</tr>'
    table += '</tbody></table>'

    full_html = f'''<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{{margin:0;padding:0;box-sizing:border-box;}} body{{background:white;}}</style>
</head><body>{banner}{table}</body></html>'''
    return full_html


def _measure_row_heights(phase, rows):
    """Use Edge --dump-dom to measure row heights with same styling as dashboard's packRowsIntoPages."""
    columns = ['Initiative - Project Title', 'Health Status', 'Phase',
                '# of Stores', 'Dallas POC', 'Intake & Testing', 'Deployment']

    # Build measurement HTML that matches dashboard's measurement container
    # Dashboard uses padding:8px, border:1px solid #ddd, word-wrap:break-word — NOT the render padding
    table = '<table style="width:100%;border-collapse:collapse;font-size:14px;font-family:Segoe UI,Arial,sans-serif;line-height:1.5;">'
    table += '<thead><tr style="background-color:#f0f0f0;border-bottom:2px solid #999;height:50px;">'
    for col in columns:
        table += f'<th style="padding:8px;text-align:left;border:1px solid #ddd;">{escape(col)}</th>'
    table += '</tr></thead><tbody>'
    for row in rows:
        table += '<tr style="border:1px solid #ddd;">'
        for col in columns:
            value = str(row.get(col, '') or '')
            if col == '# of Stores':
                value = str(int(row.get(col, 0) or 0))
            style = 'padding:8px;border:1px solid #ddd;word-wrap:break-word;white-space:normal;'
            if col in ('Health Status', 'Phase', '# of Stores'):
                style += 'font-weight:600;'
            table += f'<td style="{style}">{escape(value)}</td>'
        table += '</tr>'
    table += '</tbody></table>'

    meas_html = f'''<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{{margin:0;padding:0;box-sizing:border-box;}}</style>
</head><body style="width:1280px;">
{table}
<script>
window.onload=function(){{
  var rs=document.querySelectorAll("tbody tr");
  var h=[];rs.forEach(function(r){{h.push(r.offsetHeight);}});
  document.getElementById("_rh").textContent="ROW_HEIGHTS:"+JSON.stringify(h);
}};
</script><pre id="_rh"></pre>
</body></html>'''

    with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8') as f:
        f.write(meas_html)
        html_path = f.name
    try:
        cmd = [
            EDGE_PATH, '--headless', '--disable-gpu', '--no-sandbox',
            '--dump-dom', '--virtual-time-budget=5000',
            f'--window-size=1280,4000',
            f'file:///{html_path.replace(os.sep, "/")}'
        ]
        result = subprocess.run(cmd, capture_output=True, timeout=30)
        stdout = result.stdout.decode('utf-8', errors='replace')
        match = re.search(r'ROW_HEIGHTS:\[([\d,]+)\]', stdout)
        if match:
            return [int(x) for x in match.group(1).split(',')]
    finally:
        os.unlink(html_path)
    # Fallback: assume 55px per row
    return [55] * len(rows)


def _paginate_by_height(rows, heights):
    """Replicate dashboard packRowsIntoPages — split rows when cumulative height > AVAILABLE_HEIGHT."""
    AVAILABLE_HEIGHT = 800  # calibrated to match dashboard's packRowsIntoPages via Edge headless
    pages = []
    current_page = []
    current_h = 0
    for row, h in zip(rows, heights):
        if current_h + h > AVAILABLE_HEIGHT and current_page:
            pages.append(current_page)
            current_page = [row]
            current_h = h
        else:
            current_page.append(row)
            current_h += h
    if current_page:
        pages.append(current_page)
    return pages


def _capture_html_screenshot(html_content, output_png, width=1280):
    """Use Edge headless to capture HTML as a PNG screenshot."""
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8') as f:
        f.write(html_content)
        html_path = f.name

    try:
        cmd = [
            EDGE_PATH,
            '--headless',
            '--disable-gpu',
            '--no-sandbox',
            '--hide-scrollbars',
            '--force-device-scale-factor=1.5',
            f'--screenshot={output_png}',
            f'--window-size={width},2000',
            f'file:///{html_path.replace(os.sep, "/")}'
        ]
        result = subprocess.run(cmd, capture_output=True, timeout=30)
        if not Path(output_png).exists():
            raise RuntimeError(f"Edge screenshot failed: {result.stderr.decode(errors='replace')[:200]}")

        # Auto-crop whitespace — match html2canvas element-only capture
        img = Image.open(output_png)
        bg = Image.new(img.mode, img.size, (255, 255, 255))
        diff = ImageChops.difference(img, bg)
        bbox = diff.getbbox()
        if bbox:
            # Crop exactly to content boundary — no padding on right
            cropped = img.crop((0, 0, bbox[2], bbox[3] + 4))
            # Save as JPEG for smaller file size
            jpg_path = output_png.replace('.png', '.jpg')
            cropped.convert('RGB').save(jpg_path, 'JPEG', quality=78, optimize=True)
            import shutil
            shutil.move(jpg_path, output_png)  # keep .png extension for caller
    finally:
        os.unlink(html_path)


def generate_report_pptx(data):
    """Generate PPTX using Edge headless screenshots — identical to dashboard Generate PPT."""
    print("    Using Edge headless for screenshot-based PPT (matches dashboard)...")

    # Build ownership → phase sections (same logic as dashboard & email)
    UNASSIGNED = 'No Selection Provided'
    sections = []

    # 1. Pending + unassigned first
    pending_unassigned = [r for r in data if r['Phase'] == 'Pending' and r.get('TDA Ownership', UNASSIGNED) == UNASSIGNED]
    if pending_unassigned:
        sections.append(('TDA Ownership - Currently No TDA Ownership', 'Pending', pending_unassigned))

    # 2. Custom ownership order: Dallas POC, Intake & Test, Deployment, then unassigned
    OWNERSHIP_ORDER = ['Dallas POC', 'Intake & Test', 'Deployment', UNASSIGNED]
    all_ownerships = set(r.get('TDA Ownership', UNASSIGNED) or UNASSIGNED for r in data)
    known_set = set(OWNERSHIP_ORDER)
    unknown_ownerships = sorted(o for o in all_ownerships if o not in known_set)
    ownership_list = [o for o in OWNERSHIP_ORDER if o in all_ownerships] + unknown_ownerships
    for ownership in ownership_list:
        for phase in PHASE_ORDER:
            if phase == 'Pending' and ownership == UNASSIGNED:
                continue
            rows = [r for r in data if (r.get('TDA Ownership', UNASSIGNED) or UNASSIGNED) == ownership and r['Phase'] == phase]
            if not rows:
                continue
            label = 'TDA Ownership - Currently No TDA Ownership' if ownership == UNASSIGNED else ownership
            sections.append((label, phase, rows))

    screenshots = []  # list of (label, png_bytes)

    with tempfile.TemporaryDirectory() as tmp_dir:
        for ownership_label, phase, rows in sections:
            if not rows:
                continue
            # Measure actual row heights via Edge (matches dashboard packRowsIntoPages)
            heights = _measure_row_heights(phase, rows)
            pages = _paginate_by_height(rows, heights)
            total_pages = len(pages)
            for page, page_rows in enumerate(pages):
                label = f'{ownership_label} — {phase}'
                if total_pages > 1:
                    label += f' ({page + 1}/{total_pages})'

                html = _build_phase_html(phase, page_rows, ownership=ownership_label)
                png_path = os.path.join(tmp_dir, f'slide_{len(screenshots) + 1}.png')
                _capture_html_screenshot(html, png_path)
                png_bytes = Path(png_path).read_bytes()
                screenshots.append((label, png_bytes))
                print(f"    Captured: {ownership_label}/{phase} page {page + 1}/{total_pages} ({len(png_bytes):,} bytes)")

    # Build the PPTX with title slide + screenshot slides
    pptx_buffer = io.BytesIO()
    total_slides = 1 + len(screenshots)

    with zipfile.ZipFile(pptx_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        # [Content_Types].xml
        ct_parts = '\n'.join(
            f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
            for i in range(1, total_slides + 1)
        )
        zf.writestr('[Content_Types].xml', f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Default Extension="jpeg" ContentType="image/jpeg"/>
<Default Extension="png" ContentType="image/png"/>
<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
{ct_parts}
</Types>''')

        zf.writestr('_rels/.rels', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>''')

        ppt_rels = '\n'.join(
            f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>'
            for i in range(1, total_slides + 1)
        )
        zf.writestr('ppt/_rels/presentation.xml.rels', f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
{ppt_rels}
</Relationships>''')

        sld_ids = '\n'.join(
            f'<p:sldId id="{255 + i}" r:id="rId{i}"/>'
            for i in range(1, total_slides + 1)
        )
        zf.writestr('ppt/presentation.xml', f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<p:sldIdLst>
{sld_ids}
</p:sldIdLst>
<p:sldSz cx="9144000" cy="6858000" type="custom"/>
<p:notesSz cx="6858000" cy="9144000"/>
</p:presentation>''')

        # ── Slide 1: Title slide (white bg, blue header, yellow accent — same as dashboard) ──
        zf.writestr('ppt/slides/_rels/slide1.xml.rels', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>''')

        title_slide = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<p:cSld>
<p:bg><p:bgPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>
<p:spTree>
<p:nvGrpSpPr><p:cNvPr id="1" name="Title"/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="9144000" cy="6858000"/></a:xfrm></p:grpSpPr>
<p:sp><p:nvSpPr><p:cNvPr id="2" name="HeaderBar"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
<p:spPr>
<a:xfrm><a:off x="0" y="0"/><a:ext cx="9144000" cy="1143000"/></a:xfrm>
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
<a:solidFill><a:srgbClr val="3B82F6"/></a:solidFill>
<a:ln><a:noFill/></a:ln>
</p:spPr>
<p:txBody><a:bodyPr anchor="ctr" lIns="457200" rIns="91440" tIns="0" bIns="0"/><a:lstStyle/>
<a:p><a:pPr algn="l"/><a:r><a:rPr lang="en-US" sz="2800" b="1" dirty="0"><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill><a:latin typeface="Segoe UI"/></a:rPr><a:t>TDA Initiatives Insights</a:t></a:r></a:p>
</p:txBody></p:sp>
<p:sp><p:nvSpPr><p:cNvPr id="3" name="MainTitle"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
<p:spPr><a:xfrm><a:off x="457200" y="2200000"/><a:ext cx="8230000" cy="1800000"/></a:xfrm></p:spPr>
<p:txBody><a:bodyPr anchor="ctr"/><a:lstStyle/>
<a:p><a:pPr algn="ctr"/><a:r><a:rPr lang="en-US" sz="4000" b="1" dirty="0"><a:solidFill><a:srgbClr val="1E3A5F"/></a:solidFill><a:latin typeface="Segoe UI"/></a:rPr><a:t>Initiative Status Insights</a:t></a:r></a:p>
</p:txBody></p:sp>
<p:sp><p:nvSpPr><p:cNvPr id="4" name="Subtitle"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
<p:spPr><a:xfrm><a:off x="457200" y="3900000"/><a:ext cx="8230000" cy="800000"/></a:xfrm></p:spPr>
<p:txBody><a:bodyPr anchor="t"/><a:lstStyle/>
<a:p><a:pPr algn="ctr"/><a:r><a:rPr lang="en-US" sz="2000" dirty="0"><a:solidFill><a:srgbClr val="666666"/></a:solidFill><a:latin typeface="Segoe UI"/></a:rPr><a:t>Store Support  |  Asset Protection</a:t></a:r></a:p>
</p:txBody></p:sp>
<p:sp><p:nvSpPr><p:cNvPr id="5" name="AccentLine"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
<p:spPr>
<a:xfrm><a:off x="0" y="6658000"/><a:ext cx="9144000" cy="200000"/></a:xfrm>
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
<a:solidFill><a:srgbClr val="FFC220"/></a:solidFill>
<a:ln><a:noFill/></a:ln>
</p:spPr></p:sp>
</p:spTree>
</p:cSld>
</p:sld>'''
        zf.writestr('ppt/slides/slide1.xml', title_slide)

        # ── Screenshot slides (identical to dashboard Generate PPT) ──
        SLIDE_W = 9144000
        SLIDE_H = 6858000

        for idx, (label, png_bytes) in enumerate(screenshots):
            slide_num = idx + 2
            img_filename = f'image{idx + 1}.jpg'

            # Store the image
            zf.writestr(f'ppt/media/{img_filename}', png_bytes)

            # Read JPEG dimensions
            img_w, img_h = 1920, 1080
            try:
                pil_img = Image.open(io.BytesIO(png_bytes))
                img_w, img_h = pil_img.size
            except Exception:
                pass

            # Scale to fill slide width, maintain aspect
            aspect = img_h / img_w if img_w > 0 else 0.5625
            final_w = SLIDE_W
            final_h = int(SLIDE_W * aspect)
            if final_h > SLIDE_H:
                final_h = SLIDE_H

            # Slide relationships (link to image)
            zf.writestr(f'ppt/slides/_rels/slide{slide_num}.xml.rels', f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/{img_filename}"/>
</Relationships>''')

            slide_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<p:cSld>
<p:bg><p:bgPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>
<p:spTree>
<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{SLIDE_W}" cy="{SLIDE_H}"/></a:xfrm></p:grpSpPr>
<p:pic>
<p:nvPicPr><p:cNvPr id="2" name="Screenshot"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>
<p:blipFill><a:blip r:embed="rId1"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>
<p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{final_w}" cy="{final_h}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>
</p:pic>
</p:spTree>
</p:cSld>
</p:sld>'''
            zf.writestr(f'ppt/slides/slide{slide_num}.xml', slide_xml)

    pptx_buffer.seek(0)
    return pptx_buffer.getvalue(), screenshots


def generate_report_pdf(pptx_screenshots):
    """Convert screenshot images to a multi-page PDF using Pillow."""
    if not pptx_screenshots:
        return None
    pages = []
    for label, png_bytes in pptx_screenshots:
        img = Image.open(io.BytesIO(png_bytes)).convert('RGB')
        pages.append(img)
    pdf_buffer = io.BytesIO()
    pages[0].save(pdf_buffer, 'PDF', save_all=True, append_images=pages[1:], resolution=150)
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()


def send_outlook_email(html_body, attachments, recipients):
    """Send email via Outlook with PPT attachment"""
    import win32com.client
    outlook = win32com.client.Dispatch('Outlook.Application')
    mail = outlook.CreateItem(0)  # 0 = olMailItem
    mail.Subject = SUBJECT
    mail.HTMLBody = html_body
    mail.To = '; '.join(recipients)
    for att in attachments:
        mail.Attachments.Add(str(att))
    mail.Send()
    print(f"[OK] Email sent to: {', '.join(recipients)}")


def main():
    preview_only = '--preview' in sys.argv

    print("=" * 60)
    print("TDA Initiative Insights - Weekly Email Report")
    print("=" * 60)

    # 1. Fetch data
    print("\n[1/4] Fetching data from BigQuery...")
    data = fetch_data()
    print(f"  Loaded {len(data)} projects")

    # 2. Generate PPT + PDF
    print("[2/5] Generating PPT report...")
    pptx_data, screenshots = generate_report_pptx(data)
    PPT_OUTPUT.write_bytes(pptx_data)
    print(f"  Saved: {PPT_OUTPUT}")
    print(f"  Size: {len(pptx_data):,} bytes")

    print("[3/5] Generating PDF report...")
    pdf_data = generate_report_pdf(screenshots)
    if pdf_data:
        PDF_OUTPUT.write_bytes(pdf_data)
        print(f"  Saved: {PDF_OUTPUT}")
        print(f"  Size: {len(pdf_data):,} bytes")

    # 4. Build email HTML
    print("[4/5] Building email HTML...")
    html = build_email_html(data)

    if preview_only:
        HTML_PREVIEW.write_text(html, encoding='utf-8')
        print(f"\n  PREVIEW MODE - files saved:")
        print(f"  PPT:   {PPT_OUTPUT}")
        print(f"  PDF:   {PDF_OUTPUT}")
        print(f"  HTML:  {HTML_PREVIEW}")
        print(f"\n  Open {HTML_PREVIEW} in a browser to review the email.")
        print("  Run without --preview to send.")
        return

    # 5. Send email with PPT + PDF attachments
    print(f"[5/5] Sending email to {', '.join(RECIPIENTS)}...")
    attachments = [PPT_OUTPUT]
    if PDF_OUTPUT.exists():
        attachments.append(PDF_OUTPUT)
    send_outlook_email(html, attachments, RECIPIENTS)

    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == '__main__':
    main()
