#!/usr/bin/env python3
"""Fix corrupted UTF-8 emojis in admin-dashboard.html"""

file_path = r'Interface/Admin/admin-dashboard.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f'Loaded: {len(content)} bytes')

# String replacements for corrupted emoji (mojibake sequences)
fixes = [
    ('ðŸ"\'', '🔒'),
    ('ðŸ""', '🔔'),
    ('ðŸ"', '🔐'),
    ('ðŸ"—', '🔗'),
    ('ðŸ"‹', '📋'),
    ('ðŸ"„', '📊'),
    ('ðŸŽ¯', '🎯'),
    ('ðŸš€', '🚀'),
    ('ðŸ"¥', '📥'),
    ('ðŸ'¾', '💾'),
    ('ðŸ'¬', '💬'),
    ('ðŸ—\'ï¸', '🗑️'),
    ('â†'', '→'),
    ('Ã—', '×'),
]

for broken, fixed in fixes:
    count = content.count(broken)
    if count > 0:
        print(f'Replacing {count}x: {repr(broken)} → {repr(fixed)}')
        content = content.replace(broken, fixed)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'✅ Fixed! New size: {len(content)} bytes')
