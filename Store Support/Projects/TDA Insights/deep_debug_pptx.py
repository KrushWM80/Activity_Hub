#!/usr/bin/env python3
"""Deep diagnostic to check PPTX XML validity and content"""

import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

def check_slide_details(pptx_path):
    """Check actual slide XML content and dimensions"""
    
    print("\n" + "=" * 70)
    print("DETAILED SLIDE ANALYSIS")
    print("=" * 70 + "\n")
    
    try:
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            # Check slide1
            print("[SLIDE 1 - Title Slide]")
            try:
                slide1_xml = zf.read('ppt/slides/slide1.xml').decode('utf-8')
                
                # Pretty print first 500 chars
                print("First 800 chars of XML:")
                print(slide1_xml[:800])
                print("\n...")
                
                # Parse and check structure
                root = ET.fromstring(slide1_xml)
                ns = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
                      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
                
                shapes = root.findall('.//p:sp', ns)
                print(f"\nShapes found: {len(shapes)}")
                for i, shape in enumerate(shapes):
                    # Get text
                    texts = shape.findall('.//a:t', ns)
                    text_content = ''.join([t.text or '' for t in texts])
                    print(f"  Shape {i+1}: {text_content[:100]}")
                    
                    # Get position
                    nvSpPr = shape.find('.//p:nvSpPr', ns)
                    if nvSpPr is not None:
                        cNvPr = nvSpPr.find('p:cNvPr', ns)
                        if cNvPr is not None:
                            print(f"    Name: {cNvPr.get('name')}")
                
                # Check background
                bg = root.find('.//p:bg', ns)
                if bg is not None:
                    print("Background fill found ✓")
                else:
                    print("Background fill: NOT FOUND ⚠️")
                    
            except Exception as e:
                print(f"ERROR analyzing slide1: {e}")
            
            print("\n" + "-" * 70)
            print("\n[SLIDE 2 - Content Slide]")
            try:
                slide2_xml = zf.read('ppt/slides/slide2.xml').decode('utf-8')
                
                # Pretty print first 500 chars
                print("First 800 chars of XML:")
                print(slide2_xml[:800])
                print("\n...")
                
                # Parse and check structure
                root = ET.fromstring(slide2_xml)
                ns = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
                      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
                      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
                
                shapes = root.findall('.//p:sp', ns)
                pics = root.findall('.//p:pic', ns)
                
                print(f"\nShapes found: {len(shapes)}")
                print(f"Pictures found: {len(pics)}")
                
                # Check shape (header)
                for i, shape in enumerate(shapes):
                    texts = shape.findall('.//a:t', ns)
                    text_content = ''.join([t.text or '' for t in texts])
                    print(f"  Shape {i+1} (header): {text_content[:100]}")
                
                # Check image positioning
                for i, pic in enumerate(pics):
                    print(f"\n  Picture {i+1}:")
                    
                    # Get rId
                    blipFill = pic.find('.//p:blipFill', ns)
                    if blipFill is not None:
                        blip = blipFill.find('.//a:blip', ns)
                        if blip is not None:
                            embed = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                            print(f"    Image rId: {embed}")
                    
                    # Get position and size
                    xfrm = pic.find('.//p:xfrm', ns)
                    if xfrm is not None:
                        off = xfrm.find('a:off', ns)
                        ext = xfrm.find('a:ext', ns)
                        
                        if off is not None:
                            x = off.get('x')
                            y = off.get('y')
                            print(f"    Position: x={x}, y={y}")
                        
                        if ext is not None:
                            cx = ext.get('cx')
                            cy = ext.get('cy')
                            print(f"    Size: cx={cx}, cy={cy}")
                            # Convert to inches for reference (914400 EMU = 1 inch)
                            if cx and cy:
                                cx_in = int(cx) / 914400
                                cy_in = int(cy) / 914400
                                print(f"    Size in inches: {cx_in:.2f}\" x {cy_in:.2f}\"")
                
            except Exception as e:
                print(f"ERROR analyzing slide2: {e}")
                import traceback
                traceback.print_exc()
            
            # Check slide relationships
            print("\n" + "-" * 70)
            print("\n[SLIDE RELATIONSHIPS]")
            
            for slide_num in [1, 2]:
                rels_path = f'ppt/slides/_rels/slide{slide_num}.xml.rels'
                if rels_path in zf.namelist():
                    try:
                        rels_xml = zf.read(rels_path).decode('utf-8')
                        root = ET.fromstring(rels_xml)
                        ns = {'r': 'http://schemas.openxmlformats.org/package/2006/relationships'}
                        
                        rels = root.findall('.//r:Relationship', ns)
                        print(f"\nSlide {slide_num} relationships: {len(rels)}")
                        for rel in rels:
                            print(f"  {rel.get('Id')} → {rel.get('Target')}")
                    except Exception as e:
                        print(f"  ERROR: {e}")
    
    except FileNotFoundError:
        print("test_output.pptx not found")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_file = Path('test_output.pptx')
    if test_file.exists():
        check_slide_details(test_file)
        
        print("\n" + "=" * 70)
        print("DIAGNOSTIC COMPLETE")
        print("=" * 70)
    else:
        print(f"test_output.pptx not found in {Path.cwd()}")
