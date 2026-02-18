import re

# Read file with explicit encoding
with open('amp_analysis_dashboard.html', 'rb') as f:
    content = f.read()

# The garbled "â€"" is bytes: C3 A2 E2 82 AC E2 80 9C which is UTF-8 double-encoded
# Let's replace with a simple dash character
# First decode as UTF-8
text = content.decode('utf-8', errors='replace')

# Replace the garbled em dash pattern
text = text.replace('â€"', '-')

# Also replace double-encoded patterns
text = re.sub(r'[^\x00-\x7F]+', lambda m: '-' if m.group() in ['â€"', '—'] else m.group(), text)

# Write file back
with open('amp_analysis_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed em dash encoding")
