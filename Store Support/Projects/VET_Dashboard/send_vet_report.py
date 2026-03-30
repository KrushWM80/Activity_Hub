"""
V.E.T. Executive Report - Email Reporter
Fetches live dashboard data via API, generates PPTX/PDF, and sends via Outlook
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime, timedelta
import urllib.request
import urllib.error
from io import BytesIO

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from email_service import VETEmailService
from generate_ppt import TDAPowerPointGenerator


def get_current_walmart_week():
    """
    Determine current Walmart Week (WK format)
    
    Returns:
        String in format "WK##" (e.g., "WK09")
    """
    today = datetime.now().date()
    
    # Walmart fiscal year starts in February
    if today.month >= 2:
        year_start = datetime(today.year, 2, 1).date()
    else:
        year_start = datetime(today.year - 1, 2, 1).date()
    
    # Find first Saturday
    days_until_saturday = (5 - year_start.weekday()) % 7
    first_saturday = year_start + timedelta(days=days_until_saturday)
    
    # Calculate week number
    days_diff = (today - first_saturday).days
    weeks = max(1, (days_diff // 7) + 1)
    
    return f"WK{weeks:02d}"


def fetch_dashboard_stats(api_url: str = "http://127.0.0.1:5001") -> dict:
    """
    Fetch current dashboard statistics from the running backend API
    
    Args:
        api_url: Base URL of the V.E.T. Dashboard backend
    
    Returns:
        Dictionary with report stats or None if fetch fails
    """
    try:
        # Fetch summary data endpoint
        summary_url = f"{api_url}/api/summary"
        with urllib.request.urlopen(summary_url, timeout=5) as response:
            response_data = json.loads(response.read().decode())
        
        # Extract summary from response
        summary = response_data.get('summary', {})
        health_status = summary.get('by_health_status', {})
        
        current_wm_week = get_current_walmart_week()
        
        return {
            'total_projects': summary.get('total_projects', 0),
            'total_stores': summary.get('total_stores', 0),
            'on_track': health_status.get('On Track', 0),
            'at_risk': health_status.get('At Risk', 0),
            'off_track': health_status.get('Off Track', 0),
            'continuous': 0,  # Not available in current API
            'wm_week': current_wm_week
        }
    
    except urllib.error.URLError as e:
        print(f"     ❌ API not reachable at {api_url}: {e}")
        return None
    except Exception as e:
        print(f"     ❌ Error fetching API data: {e}")
        return None


def generate_pdf_from_pptx(pptx_path: str, pdf_path: str) -> bool:
    """
    Convert PPTX to PDF using LibreOffice (if available)
    Falls back to creating a simple PDF if LibreOffice not available
    
    Args:
        pptx_path: Path to input PPTX file
        pdf_path: Path to output PDF file
    
    Returns:
        True if successful, False otherwise
    """
    try:
        import subprocess
        
        # Try using LibreOffice to convert PPTX to PDF
        try:
            result = subprocess.run([
                'libreoffice', '--headless', '--convert-to', 'pdf',
                '--outdir', str(Path(pdf_path).parent),
                pptx_path
            ], capture_output=True, timeout=30)
            
            if result.returncode == 0:
                print(f"     ✓ PDF generated via LibreOffice: {Path(pdf_path).name}")
                return True
        except FileNotFoundError:
            # LibreOffice not installed, try reportlab instead
            pass
    except Exception as e:
        pass
    
    # Fallback: Create a simple PDF using reportlab if available
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        pdf_file = pdf_path
        c = canvas.Canvas(str(pdf_file), pagesize=letter)
        c.drawString(100, 750, "V.E.T. Executive Report")
        c.drawString(100, 730, f"Generated: {datetime.now().strftime('%B %d, %Y')}")
        c.save()
        
        print(f"     ✓ PDF created: {Path(pdf_path).name}")
        return True
    except ImportError:
        print(f"     [!] PDF generation not available:")
        print(f"        - LibreOffice: Not installed")
        print(f"        - reportlab: Not installed")
        print(f"        Install reportlab with: pip install reportlab")
        return False
    except Exception as e:
        print(f"     [!] PDF generation failed: {e}")
        return False


def generate_ppt_using_backend(output_path: str) -> bool:
    """
    Generate PPT by calling the ppt_service backend API directly.
    
    The backend should capture the dashboard via browser automation internally
    and generate a styled PPTX that matches the dashboard's rendered output.
    
    Args:
        output_path: Path to save the generated PPTX
    
    Returns:
        True if successful, False otherwise
    """
    try:
        api_url = "http://127.0.0.1:5001"
        generate_url = f"{api_url}/api/ppt/generate"
        
        print("     [*] Generating PPT from dashboard...")
        
        # Call the backend endpoint to generate styled PPT
        ppt_data = {
            'phases': [],
            'force_regenerate': True
        }
        
        req = urllib.request.Request(
            generate_url,
            data=json.dumps(ppt_data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            # Read the binary PPT data directly from response
            ppt_content = response.read()
            
            # Save to file
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(ppt_content)
            
            print(f"     [OK] PPT generated: {Path(output_path).name}")
            return True
        
    except urllib.error.HTTPError as e:
        print(f"     [!] Backend API error (HTTP {e.code}): {e.reason}")
        print(f"        Make sure /api/ppt/generate endpoint is working correctly")
        return False
    except urllib.error.URLError as e:
        print(f"     [!] Could not reach backend: {e}")
        return False
    except Exception as e:
        print(f"     [!] Error generating PPT: {e}")
        return False


def send_vet_report_email(recipient_email: str = "kendall.rush@walmart.com", test_mode: bool = False):
    """
    Fetch dashboard data, generate reports, and send email
    
    Args:
        recipient_email: Email address to send to
        test_mode: If True, save as draft instead of sending
    
    Returns:
        True if successful
    """
    
    print("=" * 90)
    print("V.E.T. EXECUTIVE REPORT - EMAIL GENERATOR")
    print("=" * 90)
    print()
    
    try:
        # Step 1: Fetch dashboard data
        print("[1/4] Fetching live dashboard data from backend...")
        print()
        
        stats = fetch_dashboard_stats()
        if not stats:
            print("     [!] Failed to fetch dashboard data")
            print()
            print("     Make sure the V.E.T. Dashboard backend is running:")
            print("     $ cd 'Store Support/Projects/VET_Dashboard'")
            print("     $ python backend.py")
            return False
        
        print("     [OK] Data fetched successfully")
        print(f"       * Total Projects: {stats['total_projects']}")
        print(f"       * Stores Impacted: {stats['total_stores']:,}")
        print(f"       * On Track: {stats['on_track']}")
        print(f"       * At Risk: {stats['at_risk']}")
        print(f"       * Off Track: {stats['off_track']}")
        print(f"       * WM Week: {stats['wm_week']}")
        print()
        
        # Step 2: Generate PowerPoint report
        print("[2/4] Generating PowerPoint report...")
        reports_dir = Path(__file__).parent / 'reports'
        reports_dir.mkdir(exist_ok=True)
        
        # Generate PPTX with WK format in filename
        wk = stats['wm_week']
        pptx_filename = f"VET_Executive_Report_{wk}.pptx"
        pdf_filename = f"VET_Executive_Report_{wk}.pdf"
        
        pptx_path = reports_dir / pptx_filename
        pdf_path = reports_dir / pdf_filename
        
        # Generate PPT from dashboard using backend API
        ppt_result = generate_ppt_using_backend(output_path=str(pptx_path))
        
        if ppt_result:
            pass  # PPT successfully generated
        else:
            print(f"     [!] Could not generate PPT from backend")
            pptx_path = None
        
        # Step 3: Generate PDF
        print()
        print("[3/4] Generating PDF report...")
        
        if pptx_path and pptx_path.exists():
            pdf_success = generate_pdf_from_pptx(str(pptx_path), str(pdf_path))
        else:
            pdf_success = False
        
        if not pdf_success:
            print(f"     [*] PDF generation skipped - will attach PPTX only")
        
        print()
        
        # Step 4: Send email
        print("[4/4] Sending email...")
        email_service = VETEmailService()
        
        mode_text = "DRAFT" if test_mode else "SEND"
        print(f"     Email Configuration:")
        print(f"       * Mode: {mode_text}")
        print(f"       * Recipient: {recipient_email}")
        print(f"       * Subject: V.E.T. Executive Report - {wk}")
        print(f"       * Attachments: {pptx_filename}" + (f", {pdf_filename}" if pdf_success else ""))
        print()
        
        # Prepare attachments list
        attachments = []
        if pptx_path and pptx_path.exists():
            attachments.append(str(pptx_path))
        if pdf_path and pdf_path.exists():
            attachments.append(str(pdf_path))
        
        # Send email with PPTX and PDF (if available)
        success = email_service.send_report_email(
            to_recipients=[recipient_email],
            report_data=stats,
            attachment_paths=attachments,
            test_mode=test_mode
        )
        
        print()
        print("=" * 90)
        
        if success:
            if test_mode:
                print(f"[OK] EMAIL PREPARED (DRAFT)")
                print()
                print(f"   Check Outlook Drafts to review")
            else:
                print(f"[OK] EMAIL SENT SUCCESSFULLY")
                print()
                print(f"   Recipient: {recipient_email}")
                print(f"   Subject: V.E.T. Executive Report - {wk}")
                print(f"   Data: {stats['total_projects']} projects, {stats['total_stores']:,} stores")
        else:
            print(f"[ERROR] FAILED TO SEND EMAIL")
        
        print("=" * 90)
        
        return success
    
    except Exception as e:
        print()
        print("=" * 90)
        print(f"[ERROR] {e}")
        print("=" * 90)
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate V.E.T. Executive Report and send via email',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Send report to kendall.rush@walmart.com (default)
  python send_vet_report.py
  
  # Save as draft instead of sending
  python send_vet_report.py --draft
  
  # Send to different recipient
  python send_vet_report.py --email someone.else@walmart.com
        """
    )
    
    parser.add_argument(
        '--email',
        default='kendall.rush@walmart.com',
        help='Email recipient (default: kendall.rush@walmart.com)'
    )
    parser.add_argument(
        '--draft',
        action='store_true',
        help='Save as draft instead of sending'
    )
    
    args = parser.parse_args()
    
    send_vet_report_email(args.email, test_mode=args.draft)
