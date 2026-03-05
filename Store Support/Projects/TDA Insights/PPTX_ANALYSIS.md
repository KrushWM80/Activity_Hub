#!/usr/bin/env python3
"""Restore PPTX generation to working state with minimal improvements"""

# This is the WORKING structure from before - showing what generates valid PPTX
# Key principle: Keep it SIMPLE, PowerPoint will render it

working_example = """
def generate_pptx_from_screenshots(screenshots_data, title="TDA Report"):
    # MINIMAL structure that PowerPoint accepts:
    # - [Content_Types].xml (SIMPLE version with just file type defaults)
    # - _rels/.rels (point to ppt/presentation.xml)
    # - ppt/presentation.xml (list slides)
    # - ppt/_rels/presentation.xml.rels (map slide IDs)
    # - ppt/slides/slide1.xml ... slideN.xml (actual content)
    # - ppt/slides/_rels/slideX.xml.rels (point to images)
    # - ppt/media/imageX.png (the screenshots)
    
    # DO NOT ADD: presProps, viewProps, tableStyles, slideMasters, slideLayouts, theme
    # These require full relationships and proper linking that we don't need
"""

print("The WORKING approach:")
print("=" * 70)
print("1. Keep [Content_Types].xml SIMPLE - just Default for file extensions")
print("2. Keep relationship files minimal - only what's actually used")
print("3. Keep presentation.xml simple - just slide list")
print("4. Don't add optional files unless they're properly integrated")
print()
print("How to add improvements WITHOUT breaking it:")
print("- Title slide: Just change the first slide's background color to blue")
print("- Headers: Add a text shape at top of content slides (y=0, cx=9144000, cy=457200)")
print("- Pagination: Already working in dashboard with packRowsIntoPages()")
print()
print("What NOT to do:")
print("- Don't add slideMasters/slideLayouts unless you also add the proper theme+relationships")
print("- Don't add presProps/viewProps unless they're minimal and properly referenced")
print("- Don't shift relationship IDs - PowerPoint expects stable IDs")
