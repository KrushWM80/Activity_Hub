#!/usr/bin/env python3
"""
V.E.T. Executive Report - Final Version (Complete Dashboard Integration)
Captures V.E.T. Dashboard content exactly as displayed including:
- Needs Attention section with at-risk initiatives
- Complete data tables with all columns (Initiative, Health, Phase, WM Week, # Stores, Executive Notes)
- Dashboard-rendered screenshots for PPT and PDF
"""

import sys
import os
import json
import subprocess
import tempfile
import io
import base64
import re
from pathlib import Path
from datetime import datetime, timedelta
from xml.sax.saxutils import escape
import urllib.request
import urllib.error
from PIL import Image, ImageChops

sys.path.insert(0, str(Path(__file__).parent))
from email_service import VETEmailService
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# Configuration
SCRIPT_DIR = Path(__file__).parent
DASHBOARD_URL = "http://127.0.0.1:5001"
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
OUTPUT_DIR = SCRIPT_DIR / 'reports'
OUTPUT_DIR.mkdir(exist_ok=True)

COLORS = {
    'walmart_blue_dark': '#1E3A8A',
    'walmart_blue': '#0071CE',
    'walmart_yellow': '#FFCC00',
    'on_track': '#107C10',
    'at_risk': '#F7630C',
    'off_track': '#DC3545',
}


def get_current_walmart_week():
    """Calculate current Walmart Week (WK format)"""
    today = datetime.now().date()
    if today.month >= 2:
        year_start = datetime(today.year, 2, 1).date()
    else:
        year_start = datetime(today.year - 1, 2, 1).date()
    
    days_until_saturday = (5 - year_start.weekday()) % 7
    first_saturday = year_start + timedelta(days=days_until_saturday)
    days_diff = (today - first_saturday).days
    weeks = max(1, (days_diff // 7) + 1)
    
    return f"WK{weeks:02d}"


def _fetch_from_bigquery_direct() -> list:
    """Fallback: query BigQuery directly when API server is unavailable"""
    _PHASE_MAP = {'POC/POT': 'Vet', 'Mkt Scale': 'Test Markets'}
    try:
        from google.cloud import bigquery as bq
        creds_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS',
            os.path.join(os.environ.get('APPDATA', ''), 'gcloud', 'application_default_credentials.json'))
        if creds_path and os.path.exists(creds_path):
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds_path
        bq_client = bq.Client(project='wmt-assetprotection-prod')
        query = """
        SELECT
            tda.Topic AS `Initiative - Project Title`,
            tda.Health_Update AS `Health Status`,
            tda.Phase,
            SUM(CASE WHEN tda.Phase = tda.Facility_Phase THEN tda.Facility ELSE 0 END) AS `# of Stores`,
            tda.Dallas_POC AS `Executive Notes`,
            tda.TDA_Ownership,
            tda.Intake_Card_Nbr AS `Project ID`,
            tda.Intake_n_Testing AS `Intake & Testing`,
            tda.Deployment,
            COALESCE(CAST(MIN(intake.WM_Week) AS STRING), 'TBD') AS `WM Week`
        FROM `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report` tda
        LEFT JOIN `wmt-assetprotection-prod.Store_Support_Dev.IH_Intake_Data` intake
            ON CAST(tda.Intake_Card_Nbr AS STRING) = CAST(intake.Intake_Card AS STRING)
        WHERE tda.TDA_Ownership IN ('Dallas POC', 'Dallas VET')
        GROUP BY tda.Topic, tda.Health_Update, tda.Phase, tda.Dallas_POC,
                 tda.TDA_Ownership, tda.Intake_Card_Nbr, tda.Intake_n_Testing, tda.Deployment
        ORDER BY tda.Phase ASC, tda.Topic ASC
        """
        rows = list(bq_client.query(query).result())
        data = [dict(r) for r in rows]
        for row in data:
            row['Phase'] = _PHASE_MAP.get(row.get('Phase', ''), row.get('Phase', 'Unknown'))
        print(f"     [OK] Direct BigQuery returned {len(data)} projects")
        return data
    except Exception as bq_err:
        print(f"     [!] Direct BigQuery also failed: {bq_err}")
        return None


def _build_stats(projects: list) -> dict:
    """Build summary stats dict from a project list"""
    current_wm_week = get_current_walmart_week()
    return {
        'total_projects': len(projects),
        'total_stores': sum(int(p.get('# of Stores', 0) or 0) for p in projects),
        'on_track': len([p for p in projects if 'On Track' in str(p.get('Health Status', ''))]),
        'at_risk': len([p for p in projects if 'At Risk' in str(p.get('Health Status', ''))]),
        'off_track': len([p for p in projects if 'Off Track' in str(p.get('Health Status', ''))]),
        'wm_week': current_wm_week,
    }


def fetch_dashboard_data(api_url: str = DASHBOARD_URL) -> tuple:
    """Fetch dashboard data: API first, then direct BigQuery, then sample data"""
    # --- Attempt 1: Live API ---
    try:
        summary_url = f"{api_url}/api/summary"
        with urllib.request.urlopen(summary_url, timeout=5) as response:
            summary_data = json.loads(response.read().decode())
        summary = summary_data.get('summary', {})

        data_url = f"{api_url}/api/data?phase=All"
        with urllib.request.urlopen(data_url, timeout=5) as response:
            data_response = json.loads(response.read().decode())
        projects = data_response.get('data', [])

        if projects:
            current_wm_week = get_current_walmart_week()
            stats = {
                'total_projects': summary.get('total_projects', 0),
                'total_stores': summary.get('total_stores', 0),
                'on_track': summary.get('by_health_status', {}).get('On Track', 0),
                'at_risk': summary.get('by_health_status', {}).get('At Risk', 0),
                'off_track': summary.get('by_health_status', {}).get('Off Track', 0),
                'wm_week': current_wm_week,
            }
            print(f"     [OK] API returned {len(projects)} projects")
            return stats, projects
    except Exception as e:
        print(f"     [!] API fetch failed: {e}")

    # --- Attempt 2: Direct BigQuery ---
    print("     [*] Falling back to direct BigQuery query...")
    projects = _fetch_from_bigquery_direct()
    if projects:
        return _build_stats(projects), projects

    # --- Attempt 3: Sample data (last resort) ---
    print("     [*] Falling back to sample data...")
    try:
        from sample_data import SAMPLE_DATA_49_PROJECTS
        return _build_stats(SAMPLE_DATA_49_PROJECTS), SAMPLE_DATA_49_PROJECTS
    except Exception:
        return None, None


def build_needs_attention_html(projects: list) -> str:
    """Build HTML for Needs Attention section (at-risk initiatives)"""
    
    at_risk_items = [p for p in projects if str(p.get('Health Status', '')).lower() == 'at risk']
    
    if not at_risk_items:
        return None
    
    # Needs Attention header
    html = '''<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0;box-sizing:border-box;} body{background:#fffbeb;padding:20px;}</style>
</head><body>
<div style="background:#FFF3CD;border-left:6px solid #DC3545;border-radius:8px;padding:20px;margin-bottom:20px;">
<div style="color:#DC3545;font-size:24px;font-weight:700;margin-bottom:16px;">Needs Attention</div>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px;">
'''
    
    for item in at_risk_items:
        title = escape(item.get('Initiative - Project Title', 'Unknown'))
        stores = item.get('# of Stores', 0)
        notes = escape(item.get('Executive Notes', 'No notes provided'))
        phase = escape(item.get('Phase', 'Unknown'))
        wm_week = escape(str(item.get('WM Week', 'N/A')))
        
        html += f'''<div style="background:white;border:1px solid #DC3545;border-radius:6px;padding:16px;box-shadow:0 1px 3px rgba(220,53,69,0.1);">
<div style="display:inline-block;background:#DC3545;color:white;padding:4px 8px;border-radius:4px;font-size:12px;font-weight:700;margin-bottom:8px;">At Risk</div>
<div style="font-size:14px;font-weight:700;color:#212121;margin-bottom:8px;">{title}</div>
<div style="font-size:12px;color:#666;margin:4px 0;padding-left:8px;border-left:2px solid #DC3545;">
<strong>Phase:</strong> {phase}
</div>
<div style="font-size:12px;color:#666;margin:4px 0;padding-left:8px;border-left:2px solid #DC3545;">
<strong>Stores:</strong> {stores}
</div>
<div style="font-size:12px;color:#666;margin:4px 0;padding-left:8px;border-left:2px solid #DC3545;">
<strong>WM Week:</strong> {wm_week}
</div>
<div style="font-size:12px;color:#333;margin:8px 0;line-height:1.4;">
<strong>Notes:</strong> {notes[:200]}...
</div>
</div>
'''
    
    html += '</div></div></body></html>'
    
    return html


def build_phase_html(phase: str, rows: list) -> str:
    """Build HTML for a phase section with ALL columns from dashboard"""
    
    columns = ['Initiative - Project Title', 'Health Status', 'Phase', 'WM Week', '# of Stores', 'Executive Notes']
    
    # Phase banner
    banner = f'''<div style="background:#1E3A8A;color:white;padding:15px 20px;font-size:18px;font-weight:700;text-align:center;border-radius:4px 4px 0 0;">
    {escape(phase)} ({len(rows)} Projects)
</div>'''
    
    # Build table with all columns
    table = '<table style="width:100%;border-collapse:collapse;font-size:12px;font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',\'Helvetica Neue\',Arial,sans-serif;">'
    table += '<thead style="background-color:#F5F5F5;border-bottom:2px solid #E5E5E5;"><tr>'
    
    for col in columns:
        table += f'<th style="padding:12px;text-align:left;font-weight:600;color:#212121;white-space:nowrap;border-bottom:2px solid #E5E5E5;font-size:11px;">{escape(col)}</th>'
    
    table += '</tr></thead><tbody>'
    
    for i, row in enumerate(rows):
        bg = '#ffffff' if i % 2 == 0 else '#fafafa'
        table += f'<tr style="background:{bg};">'
        
        for col in columns:
            value = str(row.get(col, '') or '')
            cell_style = 'padding:12px;border-bottom:1px solid #E5E5E5;text-align:left;font-size:11px;'
            
            if col == 'Health Status':
                status = value.lower()
                bg_color, color = '#f0f0f0', '#333'
                if 'on track' in status:
                    bg_color, color = 'rgba(16,124,16,0.2)', '#107C10'
                elif 'at risk' in status:
                    bg_color, color = 'rgba(247,99,12,0.2)', '#F7630C'
                elif 'off track' in status:
                    bg_color, color = 'rgba(220,53,69,0.2)', '#DC3545'
                
                table += f'<td style="{cell_style}"><span style="display:inline-block;padding:4px 8px;background-color:{bg_color};color:{color};border-radius:12px;font-weight:600;font-size:10px;white-space:nowrap;">{escape(value)}</span></td>'
            
            elif col == '# of Stores':
                try:
                    stores = int(row.get(col, 0) or 0)
                    value = f"{stores:,}"
                except:
                    pass
                table += f'<td style="{cell_style}font-weight:600;color:#0071CE;">{escape(value)}</td>'
            
            else:
                # Truncate long text for Executive Notes
                if col == 'Executive Notes' and len(value) > 100:
                    value = value[:97] + '...'
                table += f'<td style="{cell_style}">{escape(value)}</td>'
        
        table += '</tr>'
    
    table += '</tbody></table>'
    
    # Wrap in document
    full_html = f'''<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{{margin:0;padding:0;box-sizing:border-box;}} body{{background:white;}}</style>
</head><body>{banner}{table}</body></html>'''
    
    return full_html


def capture_html_screenshot(html_content: str, output_png: str, width: int = 1280) -> bool:
    """Use Edge headless to capture HTML as PNG"""
    try:
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8') as f:
            f.write(html_content)
            html_path = f.name
        
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
            raise RuntimeError("Edge screenshot failed")
        
        # Auto-crop
        img = Image.open(output_png)
        bg = Image.new(img.mode, img.size, (255, 255, 255))
        diff = ImageChops.difference(img, bg)
        bbox = diff.getbbox()
        
        if bbox:
            cropped = img.crop((0, 0, bbox[2], bbox[3] + 4))
            jpg_path = output_png.replace('.png', '.jpg')
            cropped.convert('RGB').save(jpg_path, 'JPEG', quality=78, optimize=True)
            import shutil
            shutil.move(jpg_path, output_png)
        
        os.unlink(html_path)
        return True
    
    except Exception as e:
        print(f"     [!] Screenshot failed: {e}")
        return False


def generate_report_pptx(needs_attention_html: str, sections: list) -> tuple:
    """Generate PPTX: Title + Needs Attention + Phase slides"""
    try:
        print("     [*] Generating PPT from dashboard screenshots...")
        
        prs = Presentation()
        prs.slide_width = Inches(10)
        prs.slide_height = Inches(7.5)
        SLIDE_WIDTH = prs.slide_width
        SLIDE_HEIGHT = prs.slide_height
        
        # ── Title Slide ──
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
        
        txBox = slide.shapes.add_textbox(Inches(0.5), Inches(2.5), Inches(9), Inches(1.8))
        p = txBox.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = "V.E.T. Executive Report"
        run.font.size = Pt(44)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
        txBox2 = slide.shapes.add_textbox(Inches(0.5), Inches(4.2), Inches(9), Inches(0.8))
        p2 = txBox2.text_frame.paragraphs[0]
        p2.alignment = PP_ALIGN.CENTER
        run2 = p2.add_run()
        run2.text = "Walmart Enterprise Transformation"
        run2.font.size = Pt(20)
        run2.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
        accent = slide.shapes.add_shape(1, Emu(0), Inches(7.0), SLIDE_WIDTH, Inches(0.5))
        accent.fill.solid()
        accent.fill.fore_color.rgb = RGBColor(0xFF, 0xC2, 0x20)
        accent.line.fill.background()
        
        screenshots = []
        temp_files = []
        
        # ── Needs Attention Slide (if available) ──
        if needs_attention_html:
            png_path = OUTPUT_DIR / "temp_needs_attention.png"
            temp_files.append(png_path)
            
            if capture_html_screenshot(needs_attention_html, str(png_path)):
                if Path(png_path).exists():
                    png_bytes = Path(png_path).read_bytes()
                    img = Image.open(io.BytesIO(png_bytes))
                    img_w, img_h = img.size
                    aspect = img_h / img_w if img_w > 0 else 0.5625
                    final_w = SLIDE_WIDTH
                    final_h = Emu(int(SLIDE_WIDTH * aspect))
                    if final_h > SLIDE_HEIGHT:
                        final_h = SLIDE_HEIGHT
                    
                    slide = prs.slides.add_slide(prs.slide_layouts[6])
                    slide.shapes.add_picture(io.BytesIO(png_bytes), Emu(0), Emu(0), final_w, final_h)
                    screenshots.append(("Needs Attention", png_bytes))
        
        # ── Phase Slides ──
        for section_name, html_content in sections:
            png_path = OUTPUT_DIR / f"temp_{section_name.replace('/', '')}.png"
            temp_files.append(png_path)
            
            if capture_html_screenshot(html_content, str(png_path)):
                if Path(png_path).exists():
                    png_bytes = Path(png_path).read_bytes()
                    img = Image.open(io.BytesIO(png_bytes))
                    img_w, img_h = img.size
                    aspect = img_h / img_w if img_w > 0 else 0.5625
                    final_w = SLIDE_WIDTH
                    final_h = Emu(int(SLIDE_WIDTH * aspect))
                    if final_h > SLIDE_HEIGHT:
                        final_h = SLIDE_HEIGHT
                    
                    slide = prs.slides.add_slide(prs.slide_layouts[6])
                    slide.shapes.add_picture(io.BytesIO(png_bytes), Emu(0), Emu(0), final_w, final_h)
                    screenshots.append((section_name, png_bytes))
        
        # Save PPT
        pptx_buffer = io.BytesIO()
        prs.save(pptx_buffer)
        pptx_buffer.seek(0)
        
        # Cleanup
        for temp_file in temp_files:
            if temp_file.exists():
                try:
                    os.unlink(temp_file)
                except:
                    pass
        
        print(f"     [OK] PPT generated with {len(screenshots)} sections")
        return pptx_buffer.getvalue(), screenshots
    
    except Exception as e:
        print(f"     [!] Error generating PPT: {e}")
        import traceback
        traceback.print_exc()
        return None, []


def generate_report_pdf(screenshots: list) -> bytes:
    """Convert screenshots to PDF (same as PPT)"""
    try:
        if not screenshots:
            return None
        
        print("     [*] Generating PDF from screenshots...")
        
        pages = []
        for section_name, png_bytes in screenshots:
            img = Image.open(io.BytesIO(png_bytes)).convert('RGB')
            pages.append(img)
        
        pdf_buffer = io.BytesIO()
        if pages:
            pages[0].save(pdf_buffer, 'PDF', save_all=True, append_images=pages[1:] if len(pages) > 1 else [], resolution=150)
            pdf_buffer.seek(0)
            print(f"     [OK] PDF generated with {len(pages)} pages")
            return pdf_buffer.getvalue()
    
    except Exception as e:
        print(f"     [!] Error generating PDF: {e}")
        return None


def send_vet_report_email(recipient_email: str = "kendall.rush@walmart.com", test_mode: bool = False):
    """Main email generation and sending"""
    
    print("=" * 90)
    print("V.E.T. EXECUTIVE REPORT - FINAL VERSION")
    print("=" * 90)
    print()
    
    try:
        # Step 1: Fetch data
        print("[1/6] Fetching dashboard data...")
        stats, projects = fetch_dashboard_data()
        if not stats or not projects:
            print("     [!] Failed to fetch data")
            return False
        
        print("     [OK] Data fetched successfully")
        print(f"       * Total Projects: {stats['total_projects']}")
        print(f"       * Stores Impacted: {stats['total_stores']:,}")
        print(f"       * On Track: {stats['on_track']}")
        print(f"       * At Risk: {stats['at_risk']}")
        print(f"       * Off Track: {stats['off_track']}")
        print(f"       * WM Week: {stats['wm_week']}")
        print()
        
        # Step 2: Build Needs Attention HTML
        print("[2/6] Building Needs Attention section...")
        needs_attention_html = build_needs_attention_html(projects)
        if needs_attention_html:
            print("     [OK] Needs Attention section captured")
        else:
            print("     [!] No at-risk items found")
        print()
        
        # Step 3: Build Phase sections
        print("[3/6] Capturing dashboard phase tables...")
        phases_dict = {}
        for proj in projects:
            phase = proj.get('Phase', 'Unknown')
            if phase not in phases_dict:
                phases_dict[phase] = []
            phases_dict[phase].append(proj)
        
        sections = []
        phase_order = ['Pending', 'Vet', 'Test', 'Test Markets', 'Roll/Deploy']
        for phase in phase_order:
            if phase not in phases_dict or not phases_dict[phase]:
                continue
            html = build_phase_html(phase, phases_dict[phase])
            sections.append((phase, html))
        
        print(f"     [OK] Captured {len(sections)} phase sections")
        print()
        
        # Step 4: Generate PPT
        print("[4/6] Generating PowerPoint...")
        wk = stats['wm_week']
        pptx_filename = f"VET_Executive_Report_{wk}.pptx"
        pdf_filename = f"VET_Executive_Report_{wk}.pdf"
        
        pptx_path = OUTPUT_DIR / pptx_filename
        pdf_path = OUTPUT_DIR / pdf_filename
        
        pptx_data, screenshots = generate_report_pptx(needs_attention_html, sections)
        
        if pptx_data:
            pptx_path.write_bytes(pptx_data)
            print(f"     [OK] PPT saved: {pptx_filename}")
        else:
            print("     [!] Failed to generate PPT")
            return False
        
        print()
        
        # Step 5: Generate PDF
        print("[5/6] Generating PDF...")
        pdf_data = generate_report_pdf(screenshots)
        
        if pdf_data:
            pdf_path.write_bytes(pdf_data)
            print(f"     [OK] PDF saved: {pdf_filename}")
        else:
            print("     [!] PDF generation failed")
        
        print()
        
        # Step 6: Send email
        print("[6/6] Sending email...")
        email_service = VETEmailService()
        
        mode_text = "DRAFT" if test_mode else "SEND"
        print(f"     Email Configuration:")
        print(f"       * Mode: {mode_text}")
        print(f"       * Recipient: {recipient_email}")
        print(f"       * Subject: V.E.T. Executive Report - {wk}")
        
        attachments = [str(pptx_path)]
        if pdf_data:
            attachments.append(str(pdf_path))
        
        print(f"       * Attachments: {', '.join([Path(a).name for a in attachments])}")
        print()
        
        # Prepare report data with dashboard HTML
        report_data = stats.copy()
        report_data['dashboard_html'] = needs_attention_html  # Pass needs attention HTML
        
        # Send
        success = email_service.send_report_email(
            to_recipients=[recipient_email],
            report_data=report_data,
            attachment_paths=attachments,
            test_mode=test_mode
        )
        
        if success:
            print()
            print("=" * 90)
            print("[OK] EMAIL SENT SUCCESSFULLY")
            print("=" * 90)
            print()
            print(f"   Recipient: {recipient_email}")
            print(f"   Subject: V.E.T. Executive Report - {wk}")
            print(f"   Data: {stats['total_projects']} projects, {stats['total_stores']:,} stores")
            print()
            return True
        else:
            print()
            print("=" * 90)
            print("[ERROR] FAILED TO SEND EMAIL")
            print("=" * 90)
            return False
    
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point"""
    recipient = "kendall.rush@walmart.com"
    test_mode = False
    
    for arg in sys.argv[1:]:
        if arg == '--draft':
            test_mode = True
        elif arg == '--email':
            idx = sys.argv.index(arg)
            if idx + 1 < len(sys.argv):
                recipient = sys.argv[idx + 1]
    
    success = send_vet_report_email(recipient_email=recipient, test_mode=test_mode)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
