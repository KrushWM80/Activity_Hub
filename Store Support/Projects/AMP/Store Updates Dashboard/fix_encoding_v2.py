# Fix garbled text by reading as Windows-1252 and replacing visible garbled sequences
import re

# Read as UTF-8 since that's how VS Code sees it
with open('amp_analysis_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# These are the exact garbled strings as they appear when viewed
garbled_replacements = [
    # Pattern: garbled emoji -> replacement
    ('\u00f0\u0178\u201c\u2039 ', ''),      # clipboard
    ('\u00f0\u0178\u2019\u00ac ', ''),      # speech balloon
    ('\u00f0\u0178\u2019\u00a4 ', ''),      # user/admin
    ('\u00e2\u0160\u00a1 ', ''),            # lightning
    ('\u00f0\u0178\u201d ', ''),            # magnifying glass
    ('\u00e2\u0160\u0099\u00ef\u00b8 ', ''), # gear
    ('\u00e2\u0020\u201c ', ''),            # warning partial
    ('\u00ef\u00b8\u008f', ''),             # variation selector
    ('\u00e2\u2020\u2019', '>'),            # arrow
    ('\u00c3\u00a1', ''),                   # random a
]

for bad, good in garbled_replacements:
    content = content.replace(bad, good)

# Also try different variations - the exact string from the browser
variations = [
    'ðŸ"‹ ',  # clipboard from screenshot
    'ðŸ'¬ ',  # speech
    'ðŸ'¤ ',  # user
    'âš¡ ',   # lightning  
    'ðŸ" ',   # magnifying glass
    'âš™ï¸ ',  # gear
    'ðŸ"¥ ',  # fire
    'ðŸ"„ ',  # refresh
    'ï¸',     # variation selector
    'á',      # latin small a with acute (random char)
]

for v in variations:
    content = content.replace(v, '')

# Clean up
content = re.sub(r' +', ' ', content)

with open('amp_analysis_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed garbled text")
