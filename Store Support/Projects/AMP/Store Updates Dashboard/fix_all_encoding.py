# Fix all encoding issues in the dashboard
import re

with open('amp_analysis_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix garbled em dashes (various patterns)
# â€" is the garbled UTF-8 for em dash
content = content.replace('â€"', '-')
content = content.replace('â€™', "'")
content = content.replace('â€œ', '"')
content = content.replace('â€', '"')
content = content.replace('\u2014', '-')  # em dash
content = content.replace('\u2013', '-')  # en dash
content = content.replace('\u2019', "'")  # right single quote
content = content.replace('\u201c', '"')  # left double quote
content = content.replace('\u201d', '"')  # right double quote

# Also fix any hex-encoded versions
content = re.sub(r'[\x80-\xff]+--?', '-', content)

with open('amp_analysis_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed all encoding issues")
