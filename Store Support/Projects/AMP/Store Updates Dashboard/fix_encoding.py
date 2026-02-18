import re

# Read file
with open('amp_analysis_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix em dash characters - this is UTF-8 em dash bytes read as Latin-1
# The sequence 'â€"' is the em dash (—) encoded as UTF-8 but displayed as Latin-1
content = content.replace('â€"', '&mdash;')

# Also check for the raw UTF-8 byte patterns
content = content.replace('\xe2\x80\x94', '&mdash;')  # Raw UTF-8 bytes for em dash
content = content.replace('—', '&mdash;')  # Actual em dash

# Write file
with open('amp_analysis_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed em dash encoding issues")
print(f"File size: {len(content)} bytes")
