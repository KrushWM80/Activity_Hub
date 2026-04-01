"""Compare reference PDF (Dallas VET Weekly Report) vs our generated output"""
import sys
sys.path.insert(0, '.')

# Try to extract text content from both PDFs
try:
    import fitz  # PyMuPDF
    HAS_FITZ = True
except ImportError:
    HAS_FITZ = False

from PIL import Image
import io
from pathlib import Path

ref_pdf = Path('reports/Dallas VET Weekly Report 3.30.pdf')
our_pdf = Path('reports/VET_Executive_Report_WK09.pdf')

print(f"Reference: {ref_pdf.name} ({ref_pdf.stat().st_size / 1024:.1f} KB)")
print(f"Ours:      {our_pdf.name} ({our_pdf.stat().st_size / 1024:.1f} KB)")
print()

if HAS_FITZ:
    # Extract text and page info from both PDFs
    ref_doc = fitz.open(str(ref_pdf))
    our_doc = fitz.open(str(our_pdf))
    
    print(f"=== REFERENCE PDF: {ref_pdf.name} ===")
    print(f"Pages: {len(ref_doc)}")
    for i, page in enumerate(ref_doc):
        rect = page.rect
        print(f"  Page {i+1}: {rect.width:.0f}x{rect.height:.0f}pt ({rect.width/72:.1f}\"x{rect.height/72:.1f}\")")
        text = page.get_text().strip()
        if text:
            lines = text.split('\n')
            print(f"    Text lines: {len(lines)}")
            for line in lines[:15]:
                line = line.strip()
                if line:
                    print(f"      {line[:100]}")
            if len(lines) > 15:
                print(f"      ... ({len(lines) - 15} more lines)")
        else:
            print(f"    [Image-only page - no extractable text]")
        # Count images
        images = page.get_images()
        if images:
            print(f"    Images: {len(images)}")
    
    print()
    print(f"=== OUR PDF: {our_pdf.name} ===")
    print(f"Pages: {len(our_doc)}")
    for i, page in enumerate(our_doc):
        rect = page.rect
        print(f"  Page {i+1}: {rect.width:.0f}x{rect.height:.0f}pt ({rect.width/72:.1f}\"x{rect.height/72:.1f}\")")
        text = page.get_text().strip()
        if text:
            lines = text.split('\n')
            print(f"    Text lines: {len(lines)}")
            for line in lines[:15]:
                line = line.strip()
                if line:
                    print(f"      {line[:100]}")
            if len(lines) > 15:
                print(f"      ... ({len(lines) - 15} more lines)")
        else:
            print(f"    [Image-only page - no extractable text]")
        images = page.get_images()
        if images:
            print(f"    Images: {len(images)}")
    
    # Summary comparison
    print()
    print("=== COMPARISON SUMMARY ===")
    
    # Extract all project names from reference
    ref_projects = set()
    for page in ref_doc:
        text = page.get_text()
        for line in text.split('\n'):
            line = line.strip()
            if line and len(line) > 10 and not line.startswith(('Phase', 'Initiative', 'Health', '#', 'WM', 'Executive', 'V.E.T', 'Dallas', 'Needs', 'At Risk', 'On Track', 'Off Track', 'Pending', 'Vet', 'Test', 'Roll')):
                # Likely a project title
                pass
    
    ref_doc.close()
    our_doc.close()
    
else:
    print("PyMuPDF not installed. Installing...")
    import subprocess
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'PyMuPDF'], capture_output=True)
    print("Installed. Please re-run this script.")
