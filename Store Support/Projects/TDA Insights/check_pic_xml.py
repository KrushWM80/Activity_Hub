#!/usr/bin/env python3
"""Extract and show raw picture XML"""

import zipfile
import xml.etree.ElementTree as ET

with zipfile.ZipFile('test_output.pptx', 'r') as zf:
    slide2_xml = zf.read('ppt/slides/slide2.xml').decode('utf-8')
    
    print("SLIDE 2 PICTURE XML SECTION:")
    print("=" * 70)
    
    # Find and extract picture section
    start = slide2_xml.find('<p:pic>')
    end = slide2_xml.find('</p:pic>') + len('</p:pic>')
    
    if start != -1 and end > start:
        pic_xml = slide2_xml[start:end]
        # Pretty print with indentation
        print(pic_xml)
    else:
        print("Picture element not found - checking for alternate syntax...")
        root = ET.fromstring(slide2_xml)
        ns = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
        pic = root.find('.//p:pic', ns)
        if pic is not None:
            print(ET.tostring(pic, encoding='unicode'))
        else:
            print("NO PICTURE FOUND")
