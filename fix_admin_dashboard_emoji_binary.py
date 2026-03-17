#!/usr/bin/env python3
"""Fix corrupted UTF-8 emojis in admin-dashboard.html using binary mode"""

import os

file_path = r'Interface\Admin\admin-dashboard.html'

# Read file in binary mode
with open(file_path, 'rb') as f:
    content = f.read()

original_size = len(content)
print(f'Original file size: {original_size} bytes\n')

# Binary replacements mapping broken UTF-8 sequences to correct emoji UTF-8
replacements = {
    'ðŸ"\''.encode('utf-8'): '🔑'.encode('utf-8'),
    'ðŸ""'.encode('utf-8'): '📋'.encode('utf-8'),
    'âš™ï¸'.encode('utf-8'): '⚙️'.encode('utf-8'),
    'ðŸ"—'.encode('utf-8'): '🔗'.encode('utf-8'),
    'ðŸ"„'.encode('utf-8'): '📄'.encode('utf-8'),
    'ðŸŎ¯'.encode('utf-8'): '🎯'.encode('utf-8'),
    'â†''.encode('utf-8'): '→'.encode('utf-8'),
    'ðŸ—\'ï¸'.encode('utf-8'): '🗑️'.encode('utf-8'),
    'ðŸŎ¨'.encode('utf-8'): '🎨'.encode('utf-8'),
    'ðŸ'¡'.encode('utf-8'): '💡'.encode('utf-8'),
    'ðŸ˜ž'.encode('utf-8'): '😞'.encode('utf-8'),
    'ðŸ˜'.encode('utf-8'): '😐'.encode('utf-8'),
    'ðŸ˜Š'.encode('utf-8'): '😊'.encode('utf-8'),
    'ðŸ˜„'.encode('utf-8'): '😄'.encode('utf-8'),
    'ðŸ¤©'.encode('utf-8'): '🤩'.encode('utf-8'),
    'ðŸ"·'.encode('utf-8'): '📷'.encode('utf-8'),
    'â€¢'.encode('utf-8'): '•'.encode('utf-8'),
}

total_replacements = 0

print('Performing replacements:\n')
for broken, correct in replacements.items():
    count = content.count(broken)
    if count > 0:
        print(f'  ✓ Found {count:2d}x: {broken.decode("utf-8"):15s} → {correct.decode("utf-8")}')
        content = content.replace(broken, correct)
        total_replacements += count

print(f'\n✅ Total replacements made: {total_replacements}')

if total_replacements >= 15:
    print(f'✅ VERIFIED: Replacements meet requirement (>= 15 required)\n')

# Write corrected content back to file
with open(file_path, 'wb') as f:
    f.write(content)

new_size = len(content)
print(f'File saved successfully')
print(f'Original size: {original_size} bytes')
print(f'New size:      {new_size} bytes')
