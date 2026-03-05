#!/usr/bin/env python3
"""Debug script to analyze PPTX structure and find what's broken"""

import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

def analyze_pptx(pptx_path):
    """Extract and analyze PPTX structure"""
    
    print("=" * 70)
    print(f"Analyzing: {pptx_path}")
    print("=" * 70)
    print()
    
    try:
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            # List all files
            print("[FILE LISTING]")
            for name in sorted(zf.namelist()):
                print(f"  {name}")
            print()
            
            # Check [Content_Types].xml
            print("[CONTENT_TYPES.XML]")
            try:
                ct = zf.read('[Content_Types].xml').decode('utf-8')
                root = ET.fromstring(ct)
                print(f"Status: Valid XML ✓")
                print(f"Override entries: {len(root.findall('{http://schemas.openxmlformats.org/package/2006/content-types}Override'))}")
            except Exception as e:
                print(f"Status: ERROR - {e}")
            print()
            
            # Check ppt/presentation.xml
            print("[PPT/PRESENTATION.XML]")
            try:
                pres = zf.read('ppt/presentation.xml').decode('utf-8')
                root = ET.fromstring(pres)
                ns = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
                slides = root.findall('.//p:sldId', ns)
                print(f"Status: Valid XML ✓")
                print(f"Slide references: {len(slides)}")
                # Check for sldSz
                sldSz = root.find('.//p:sldSz', ns)
                if sldSz is not None:
                    print(f"Slide size (cx, cy): ({sldSz.get('cx')}, {sldSz.get('cy')})")
                else:
                    print("Slide size: NOT FOUND ⚠️")
            except Exception as e:
                print(f"Status: ERROR - {e}")
            print()
            
            # Check ppt/_rels/presentation.xml.rels
            print("[PPT/_RELS/PRESENTATION.XML.RELS]")
            try:
                rels = zf.read('ppt/_rels/presentation.xml.rels').decode('utf-8')
                root = ET.fromstring(rels)
                ns = {'r': 'http://schemas.openxmlformats.org/package/2006/relationships'}
                relationships = root.findall('.//r:Relationship', ns)
                print(f"Status: Valid XML ✓")
                print(f"Total relationships: {len(relationships)}")
                for rel in relationships:
                    rid = rel.get('Id')
                    rtype = rel.get('Type').split('/')[-1]
                    target = rel.get('Target')
                    print(f"  {rid:6} → {rtype:20} → {target}")
            except Exception as e:
                print(f"Status: ERROR - {e}")
            print()
            
            # Check for presProps.xml
            print("[PPT/PRESPROPS.XML]")
            try:
                if 'ppt/presProps.xml' in zf.namelist():
                    pp = zf.read('ppt/presProps.xml').decode('utf-8')
                    root = ET.fromstring(pp)
                    print(f"Status: Present ✓")
                    print(f"Content length: {len(pp)} bytes")
                else:
                    print(f"Status: Missing ⚠️")
            except Exception as e:
                print(f"Status: ERROR - {e}")
            print()
            
            # Check slides
            print("[SLIDES]")
            for i in range(1, 5):
                slide_path = f'ppt/slides/slide{i}.xml'
                if slide_path in zf.namelist():
                    try:
                        slide = zf.read(slide_path).decode('utf-8')
                        root = ET.fromstring(slide)
                        ns = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
                        
                        # Count shapes
                        shapes = root.findall('.//p:sp', ns)
                        pics = root.findall('.//p:pic', ns)
                        
                        print(f"slide{i}.xml: {len(shapes)} shapes, {len(pics)} pics", end="")
                        
                        # Check for text
                        texts = root.findall('.//a:t', {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'})
                        if texts:
                            print(f", text: {[t.text for t in texts[:2]]}")
                        else:
                            print()
                    except Exception as e:
                        print(f"slide{i}.xml: ERROR - {e}")
            print()
            
            # Check media
            print("[MEDIA]")
            media_files = [n for n in zf.namelist() if 'ppt/media/' in n]
            print(f"Image files: {len(media_files)}")
            for mf in media_files:
                size = len(zf.read(mf))
                print(f"  {mf}: {size} bytes")
            print()
    
    except FileNotFoundError:
        print(f"ERROR: File not found: {pptx_path}")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    # Check for test_output.pptx
    test_file = Path('test_output.pptx')
    if test_file.exists():
        analyze_pptx(test_file)
        print("\n" + "=" * 70)
        print("NEXT STEPS:")
        print("=" * 70)
        print("1. If slides > 1: Images might not be showing (check pic positioning)")
        print("2. If relationships broken: Check Id mapping between .rels and .xml files")
        print("3. If presProps/viewProps missing: Add them back correctly")
        print("4. If Content-Types incomplete: May need entries for presProps/viewProps")
    else:
        print("test_output.pptx not found. Generate one first:")
        print("  cd TDA Insights")
        print("  python test_pptx_gen.py")
