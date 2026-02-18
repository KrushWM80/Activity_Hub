#!/usr/bin/env python3
"""
Update the dashboard HTML with correct table rows from table_rows.html
"""

import re

# Read table_rows.html
with open('table_rows.html', 'r', encoding='utf-8') as f:
    table_rows_content = f.read()

# Read the main dashboard HTML
with open('amp_analysis_dashboard.html', 'r', encoding='utf-8-sig') as f:
    dashboard_content = f.read()

# Find the tbody section and replace all rows between <tbody id="tableBody">  and </tbody>
# We need to preserve the opening and closing tags

# Extract just the rows from table_rows.html (remove any wrapping content)
rows_to_insert = table_rows_content.strip()

# Find the tbody tag
tbody_start = dashboard_content.find('<tbody id="tableBody">')
tbody_end = dashboard_content.find('</tbody>')

if tbody_start == -1 or tbody_end == -1:
    print("ERROR: Could not find tbody tags!")
    exit(1)

# Get the part before tbody, the tbody tags, and the part after tbody
before_tbody = dashboard_content[:tbody_start]
after_tbody = dashboard_content[tbody_end:]

# Construct the new content
new_content = before_tbody + '<tbody id="tableBody">\n' + rows_to_insert + '\n ' + after_tbody

# Write the updated content back to the dashboard
with open('amp_analysis_dashboard.html', 'w', encoding='utf-8-sig') as f:
    f.write(new_content)

print("✓ Successfully updated amp_analysis_dashboard.html with correct table rows")
print(f"✓ Replaced all hardcoded rows with {'rows from table_rows.html'}")
