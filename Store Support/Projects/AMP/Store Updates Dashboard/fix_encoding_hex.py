# Fix garbled text using Unicode code points
import re

# Read as UTF-8
with open('amp_analysis_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Garbled sequences - using exact codepoints found in the file
garbled_patterns = [
    # 4-char emojis (F0 9F xx xx) - straight quote version (U+0022)
    '\u00f0\u0178\u0022\u2039 ',       # clipboard (F0 9F 93 8B)
    '\u00f0\u0178\u0022\u008d ',       # magnifying glass (F0 9F 94 8D)
    '\u00f0\u0178\u0022\u00a5 ',       # fire (F0 9F 94 A5) 
    '\u00f0\u0178\u0022\u201e ',       # refresh (F0 9F 94 84)
    '\u00f0\u0178\u0022\u009d ',       # memo/writing (F0 9F 93 9D)
    # 4-char emojis - apostrophe version (U+0027)
    '\u00f0\u0178\u0027\u00ac ',       # speech balloon (F0 9F 92 AC)
    '\u00f0\u0178\u0027\u00a4 ',       # user bust (F0 9F 91 A4)
    '\u00f0\u0178\u0027\u00a1 ',       # lightbulb (F0 9F 92 A1)
    # 4-char emojis - curly quote version (U+201C)
    '\u00f0\u0178\u201c\u00a5 ',       # fire alternate
    '\u00f0\u0178\u201c\u201e ',       # refresh alternate
    '\u00f0\u0178\u201d ',             # partial 3-char
    # 3-char emojis (E2 xx xx)
    '\u00e2\u0161\u2122 ',             # gear (E2 9A 99)
    '\u00e2\u0161\u00a0 ',             # warning (E2 9A A0) with NBSP
    '\u00e2\u0161\u00a1 ',             # lightning (E2 9A A1)
    '\u00e2\u0020\u201c ',             # partial warning
    '\u00e2\u2020\u2019',              # arrow right (E2 86 92) - curly quote version
    '\u00e2\u2020\u0027',              # arrow right (E2 86 92) - apostrophe version
    '\u00e2\u2020\u0090',              # arrow left (E2 86 90)
    '\u00e2\u0153 ',                   # checkmark partial
    '\u00e2\u0153\u201c',              # checkmark (E2 9C 93)
    # X mark (red cross) - E2 9D 8C -> U+00E2 U+009D U+0152
    '\u00e2\u009d\u0152 ',             # X mark with space
    '\u00e2\u009d\u0152',              # X mark without space
    # Hourglass - E2 8F B3 -> U+00E2 U+008F U+00B3
    '\u00e2\u008f\u00b3',              # hourglass
    # Variation selector
    '\u00ef\u00b8\u008f',              # EF B8 8F
    # Random chars
    '\u00c3\u00a1',                    # garbled a
    '\u00c3&mdash;',                   # garbled X with HTML entity
]

for pattern in garbled_patterns:
    content = content.replace(pattern, '')

# Without trailing space
for pattern in [p.rstrip() for p in garbled_patterns if p.endswith(' ')]:
    content = content.replace(pattern, '')

# Arrow replacements - all variants
content = content.replace('\u00e2\u2020\u2019', '>')
content = content.replace('\u00e2\u2020\u0027', '>')
content = content.replace('\u00e2\u2020\u0090', '<')
content = content.replace('\u00e2\u0020\u201c', '')

# X mark replacements
content = content.replace('\u00e2\u009d\u0152', 'X')

# Hourglass - replace with loading indicator
content = content.replace('\u00e2\u008f\u00b3', '...')

# Fix HTML entity issues
content = content.replace('\u00e2\u2020&mdash;', '>')
content = content.replace('\u00c3&mdash;', 'X')

# Non-breaking space to regular space
content = content.replace('\u00a0', ' ')

# Clean up spaces
content = re.sub(r' +', ' ', content)

with open('amp_analysis_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed garbled characters")
