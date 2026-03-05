#!/usr/bin/env python3
"""Create the ABSOLUTE MINIMAL working PPTX to debug the blank issue"""

import zipfile
import io

pptx_buffer = io.BytesIO()

with zipfile.ZipFile(pptx_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
    # Minimal [Content_Types].xml
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
<Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
</Types>'''
    zf.writestr('[Content_Types].xml', content_types)
    
    # _rels/.rels
    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>'''
    zf.writestr('_rels/.rels', rels)
    
    # ppt/presentation.xml
    presentation = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<p:sldSz cx="9144000" cy="6858000"/>
<p:notesSz cx="12700000" cy="9525000"/>
<p:sldIdLst>
<p:sldId id="256" r:id="rId1"/>
</p:sldIdLst>
</p:presentation>'''
    zf.writestr('ppt/presentation.xml', presentation)
    
    # ppt/_rels/presentation.xml.rels
    ppt_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/>
</Relationships>'''
    zf.writestr('ppt/_rels/presentation.xml.rels', ppt_rels)
    
    # ppt/slides/_rels/slide1.xml.rels (empty for now)
    slide_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
</Relationships>'''
    zf.writestr('ppt/slides/_rels/slide1.xml.rels', slide_rels)
    
    # ppt/slides/slide1.xml - SIMPLE TITLE SLIDE WITH TEXT ONLY
    slide1 = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
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
<a:off x="457200" y="2743200"/>
<a:ext cx="8229600" cy="1828800"/>
</a:xfrm>
</p:spPr>
<p:txBody>
<a:bodyPr/>
<a:lstStyle/>
<a:p>
<a:pPr algn="ctr"/>
<a:r>
<a:rPr lang="en-US" sz="5400" bold="1"/>
<a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
<a:t>TDA Initiatives Insights</a:t>
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
<a:off x="457200" y="4572000"/>
<a:ext cx="8229600" cy="1143000"/>
</a:xfrm>
</p:spPr>
<p:txBody>
<a:bodyPr/>
<a:lstStyle/>
<a:p>
<a:pPr algn="ctr"/>
<a:r>
<a:rPr lang="en-US" sz="3200"/>
<a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
<a:t>Walmart Inc. Store Support</a:t>
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
    zf.writestr('ppt/slides/slide1.xml', slide1)

pptx_buffer.seek(0)
data = pptx_buffer.getvalue()

# Save test file
with open('test_minimal.pptx', 'wb') as f:
    f.write(data)

print(f"Created test_minimal.pptx: {len(data)} bytes")
print("\nOpen this file in PowerPoint to verify:")
print("- Should have Walmart blue background")
print("- Should show 'TDA Initiatives Insights' in white text")
print("- Should show 'Walmart Inc. Store Support' subtitle")
print("\nIf this works: The basic structure is good!")
print("If this is BLANK: The problem is in our XML structure")
