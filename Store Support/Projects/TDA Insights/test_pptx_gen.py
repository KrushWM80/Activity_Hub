#!/usr/bin/env python3
"""Test PPT generation directly"""

import base64
import io
import json
import zipfile
from xml.etree import ElementTree as ET

def generate_pptx_from_screenshots(screenshots_data, title="TDA Report"):
    """Generate PPTX from base64 encoded screenshots with proper structure and headers"""
    try:
        pptx_buffer = io.BytesIO()
        slide_num = 1
        
        with zipfile.ZipFile(pptx_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Count total slides (title + screenshots)
            total_slides = len(screenshots_data) + 1
            
            # [Content_Types].xml - Complete with all required types
            content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Default Extension="png" ContentType="image/png"/>
<Default Extension="jpeg" ContentType="image/jpeg"/>
<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
<Override PartName="/ppt/presProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presProps+xml"/>
<Override PartName="/ppt/viewProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.viewProps+xml"/>
<Override PartName="/ppt/tableStyles.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml"/>'''
            
            # Add slide overrides
            for i in range(1, total_slides + 1):
                content_types += f'\n<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
            
            content_types += '\n</Types>'
            zf.writestr('[Content_Types].xml', content_types)
            
            # _rels/.rels
            rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>'''
            zf.writestr('_rels/.rels', rels)
            
            # ppt/_rels/presentation.xml.rels
            ppt_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/presProps" Target="presProps.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/viewProps" Target="viewProps.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/tableStyles" Target="tableStyles.xml"/>'''
            for i in range(1, total_slides + 1):
                ppt_rels += f'\n<Relationship Id="rId{i+3}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>'
            ppt_rels += '\n</Relationships>'
            zf.writestr('ppt/_rels/presentation.xml.rels', ppt_rels)
            
            # ppt/presentation.xml - with proper slide size for 960x720 (converted to EMUs)
            # 960px = 914400 EMUs, 720px = 685800 EMUs at 96 DPI
            presentation = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<p:sldSz cx="9144000" cy="6858000"/>
<p:notesSz cx="12700000" cy="9525000"/>
<p:sldIdLst>'''
            for i in range(1, total_slides + 1):
                presentation += f'\n<p:sldId id="{255+i}" r:id="rId{i+3}"/>'
            presentation += '''
</p:sldIdLst>
</p:presentation>'''
            zf.writestr('ppt/presentation.xml', presentation)
            
            # ppt/presProps.xml
            pres_props = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presProps xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>'''
            zf.writestr('ppt/presProps.xml', pres_props)
            
            # ppt/viewProps.xml
            view_props = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:viewPr xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<p:normalViewPr><p:restoredLeft sz="15000"/><p:restoredTop sz="94611"/></p:normalViewPr>
<p:slideViewPr/><p:outlineViewPr/><p:notesViewPr/><p:handoutViewPr/></p:viewPr>'''
            zf.writestr('ppt/viewProps.xml', view_props)
            
            # ppt/tableStyles.xml
            table_styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:tblStyleLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" def="0"/>'''
            zf.writestr('ppt/tableStyles.xml', table_styles)
            
            # Create title slide (Walmart blue background)
            slide_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
</Relationships>'''
            zf.writestr(f'ppt/slides/_rels/slide{slide_num}.xml.rels', slide_rels)
            
            title_slide = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<p:cSld>
<p:bg>
<p:bgPr>
<a:solidFill><a:srgbClr val="0063B1"/></a:solidFill>
<a:effectLst/>
</p:bgPr>
</p:bg>
<p:spTree>
<p:nvGrpSpPr>
<p:cNvPr id="1" name="Title"/>
<p:cNvGrpSpPr/>
<p:nvPr/>
</p:nvGrpSpPr>
<p:grpSpPr>
<a:xfrm>
<a:off x="0" y="0"/>
<a:ext cx="9144000" cy="6858000"/>
</a:xfrm>
</p:grpSpPr>
<p:sp>
<p:nvSpPr>
<p:cNvPr id="2" name="Title"/>
<p:cNvSpPr/>
<p:nvPr/>
</p:nvSpPr>
<p:spPr>
<a:xfrm>
<a:off x="457200" y="2400000"/>
<a:ext cx="8230200" cy="1500000"/>
</a:xfrm>
</p:spPr>
<p:txBody>
<a:bodyPr/>
<a:lstStyle/>
<a:p>
<a:pPr algn="ctr"/>
<a:r>
<a:rPr lang="en-US" sz="6000" bold="1" latin="1"/>
<a:t>Initiative Status Insights</a:t>
</a:r>
</a:p>
</p:txBody>
</p:sp>
<p:sp>
<p:nvSpPr>
<p:cNvPr id="3" name="Subtitle"/>
<p:cNvSpPr/>
<p:nvPr/>
</p:nvSpPr>
<p:spPr>
<a:xfrm>
<a:off x="457200" y="4200000"/>
<a:ext cx="8230200" cy="800000"/>
</a:xfrm>
</p:spPr>
<p:txBody>
<a:bodyPr/>
<a:lstStyle/>
<a:p>
<a:pPr algn="ctr"/>
<a:r>
<a:rPr lang="en-US" sz="3600" latin="1"/>
<a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
<a:t>Walmart Inc.</a:t>
</a:r>
</a:p>
</p:txBody>
</p:sp>
</p:spTree>
</p:cSld>
<p:clrMapOvr>
<a:masterClrMapping/>
</p:clrMapOvr>
</p:sld>'''
            zf.writestr(f'ppt/slides/slide{slide_num}.xml', title_slide)
            slide_num += 1
            
            # Add screenshot slides with headers
            for idx, screenshot_info in enumerate(screenshots_data, 1):
                try:
                    image_data = screenshot_info.get('imageData', '')
                    header_text = screenshot_info.get('header', f'Page {idx}')
                    
                    if ',' in image_data:
                        image_data = image_data.split(',')[1]
                    
                    # Decode and store image
                    image_bytes = base64.b64decode(image_data)
                    image_filename = f'image{idx}.png'
                    zf.writestr(f'ppt/media/{image_filename}', image_bytes)
                    
                    # Create slide with image and header
                    slide_rels = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/{image_filename}"/>
</Relationships>'''
                    zf.writestr(f'ppt/slides/_rels/slide{slide_num}.xml.rels', slide_rels)
                    
                    # Image slide XML with header bar
                    image_slide = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<p:cSld>
<p:bg>
<p:bgPr>
<a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
<a:effectLst/>
</p:bgPr>
</p:bg>
<p:spTree>
<p:nvGrpSpPr>
<p:cNvPr id="1" name=""/>
<p:cNvGrpSpPr/>
<p:nvPr/>
</p:nvGrpSpPr>
<p:grpSpPr>
<a:xfrm>
<a:off x="0" y="0"/>
<a:ext cx="9144000" cy="6858000"/>
</a:xfrm>
</p:grpSpPr>
<p:sp>
<p:nvSpPr>
<p:cNvPr id="2" name="Header"/>
<p:cNvSpPr/>
<p:nvPr/>
</p:nvSpPr>
<p:spPr>
<a:xfrm>
<a:off x="0" y="0"/>
<a:ext cx="9144000" cy="457200"/>
</a:xfrm>
</p:spPr>
<p:txBody>
<a:bodyPr/>
<a:lstStyle/>
<a:p>
<a:pPr algn="l"/>
<a:r>
<a:rPr lang="en-US" sz="2800" bold="1" latin="1"/>
<a:solidFill><a:srgbClr val="0063B1"/></a:solidFill>
<a:t>{header_text}</a:t>
</a:r>
</a:p>
</p:txBody>
</p:sp>
<p:pic>
<p:nvPicPr>
<p:cNvPr id="3" name="{image_filename}"/>
<p:cNvPicPr>
<a:picLocks noChangeAspect="1"/>
</p:cNvPicPr>
<p:nvPr/>
</p:nvPicPr>
<p:blipFill>
<a:blip r:embed="rId1"/>
<a:stretch>
<a:fillRect/>
</a:stretch>
</p:blipFill>
<p:spPr>
<a:xfrm>
<a:off x="0" y="457200"/>
<a:ext cx="9144000" cy="6400800"/>
</a:xfrm>
<a:prstGeom prst="rect">
<a:avLst/>
</a:prstGeom>
</p:spPr>
</p:pic>
</p:spTree>
</p:cSld>
<p:clrMapOvr>
<a:masterClrMapping/>
</p:clrMapOvr>
</p:sld>'''
                    zf.writestr(f'ppt/slides/slide{slide_num}.xml', image_slide)
                    slide_num += 1
                    
                except Exception as e:
                    print(f"[WARN] Failed to process screenshot {idx}: {e}")
                    continue
        
        pptx_buffer.seek(0)
        return pptx_buffer.getvalue()
        
    except Exception as e:
        print(f"[ERROR] Failed to generate PPTX from screenshots: {e}")
        raise

# Test it
if __name__ == '__main__':
    try:
        screenshots_data = [{'page': 1, 'header': 'Test Header', 'imageData': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='}]
        pptx_bytes = generate_pptx_from_screenshots(screenshots_data, 'Test Title')
        print(f'[OK] PPTX generated successfully: {len(pptx_bytes)} bytes')
        
        with open('test_output.pptx', 'wb') as f:
            f.write(pptx_bytes)
        print('[OK] Test file saved to test_output.pptx')
    except Exception as e:
        print(f'[ERROR] {e}')
        import traceback
        traceback.print_exc()
