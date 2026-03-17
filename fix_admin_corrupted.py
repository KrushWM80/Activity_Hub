#!/usr/bin/env python3
"""Fix corrupted emoji in admin-dashboard.html using binary operations"""

file_path = r"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Interface\Admin\admin-dashboard.html"

with open(file_path, 'rb') as f:
    content = f.read()

# Binary replacements for corrupted UTF-8 sequences
fixes = [
    (b'\xc3\xb0\xc2\x9f\xc2\x93\xc2\x92', '\u1f512'.encode('utf-8')),  # lock
    (b'\xc3\xb0\xc2\x9f\xc2\x93\xc2\x93', '\u1f4d3'.encode('utf-8')),  # clipboard
    (b'\xc3\xb0\xc2\x9f\xc2\x93\xc2\x90', '\u1f510'.encode('utf-8')),  # keys
    (b'\xc3\xb0\xc2\x9f\xc2\x93\xc2\x97', '\u1f517'.encode('utf-8')),  # link
    (b'\xc3\xb0\xc2\x9f\xc2\x93\xc2\x84', '\u1f4ca'.encode('utf-8')),  # chart
    (b'\xc3\xb0\xc2\x9f\xc2\x8e\xc2\xaf', '\u1f3af'.encode('utf-8')),  # target
    (b'\xc3\xb0\xc2\x9f\xc2\x93\xc2\xa4', '\u1f522'.encode('utf-8')),  # numbers
    (b'\xc3\xa2\xc2\x80\xc2\xa2', '\u2022'.encode('utf-8')),  # bullet
    (b'\xc3\xa2\xc2\x86\xc2\x92', '\u2192'.encode('utf-8')),  # arrow
    (b'\xc3\xa2\xc2\x9a\xc2\x99\xef\xb8\x8f', '\u2699\ufe0f'.encode('utf-8')),  # gear
]

for old, new in fixes:
    content = content.replace(old, new)

with open(file_path, 'wb') as f:
    f.write(content)

print("OK")
