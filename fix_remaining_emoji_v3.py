#!/usr/bin/env python3
"""Fix all remaining corrupted emoji in admin-dashboard.html using binary replacement"""

filepath = r'c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Interface\Admin\admin-dashboard.html'

with open(filepath, 'rb') as f:
    data = f.read()

original_size = len(data)
print(f'Original file size: {original_size} bytes')

fixes = []

# === Fix 1: Workflow Condition -> ❓ ===
# Bytes: c3 a2 c2 9d e2 80 9c -> e2 9d 93
old = b'\xc3\xa2\xc2\x9d\xe2\x80\x9c'
new = b'\xe2\x9d\x93'
count = data.count(old)
if count > 0:
    data = data.replace(old, new)
    fixes.append(f'Condition icon: {count}x')

# === Fix 2: Workflow Action -> ⚡ ===
# Bytes: c3 a2 c5 a1 c2 a1 -> e2 9a a1
old = b'\xc3\xa2\xc5\xa1\xc2\xa1'
new = b'\xe2\x9a\xa1'
count = data.count(old)
if count > 0:
    data = data.replace(old, new)
    fixes.append(f'Action icon: {count}x')

# === Fix 3: Analytics health dots -> ● ===
# Bytes: c3 a2 e2 80 94 c2 8f -> e2 97 8f
old = b'\xc3\xa2\xe2\x80\x94\xc2\x8f'
new = b'\xe2\x97\x8f'
count = data.count(old)
if count > 0:
    data = data.replace(old, new)
    fixes.append(f'Health dots: {count}x')

# === Fix 4: Feedback back arrow -> ← ===
# Bytes: c3 a2 e2 80 a0 c2 90 -> e2 86 90
old = b'\xc3\xa2\xe2\x80\xa0\xc2\x90'
new = b'\xe2\x86\x90'
count = data.count(old)
if count > 0:
    data = data.replace(old, new)
    fixes.append(f'Back arrow: {count}x')

# === Fix 5: Export Schema - FFFD replacement char ===
old = b'exportSchema()">\xef\xbf\xbd Export Schema'
new = b'exportSchema()">\xf0\x9f\x93\xa4 Export Schema'
count = data.count(old)
if count > 0:
    data = data.replace(old, new)
    fixes.append(f'Export Schema icon: {count}x')

# === Fix 6: Export Activity Log - FFFD replacement char ===
old = b'exportActivityLog()">\xef\xbf\xbd Export'
new = b'exportActivityLog()">\xf0\x9f\x93\xa4 Export'
count = data.count(old)
if count > 0:
    data = data.replace(old, new)
    fixes.append(f'Export Activity icon: {count}x')

# === Fix 7-12: categoryIcons values ===
icon_fixes = [
    (b"status: '\xf0\x9f\x94\x90\xc5\xa0'", b"status: '\xf0\x9f\x93\x8a'", 'status'),
    (b"location: '\xf0\x9f\x94\x90\xc2\x8d'", b"location: '\xf0\x9f\x93\x8d'", 'location'),
    (b"time: '\xf0\x9f\x94\x90\xe2\x80\xa6'", b"time: '\xe2\x8f\xb0'", 'time'),
    (b"impact: '\xf0\x9f\x94\x90\xcb\x86'", b"impact: '\xf0\x9f\x92\xa5'", 'impact'),
    (b"description: '\xf0\x9f\x94\x90\xc2\x9d'", b"description: '\xf0\x9f\x93\x9d'", 'description'),
    (b"amp_meeting: '\xf0\x9f\x94\x90\xe2\x80\xb9'", b"amp_meeting: '\xf0\x9f\x93\x85'", 'amp_meeting'),
]

for old, new, label in icon_fixes:
    count = data.count(old)
    if count > 0:
        data = data.replace(old, new)
        fixes.append(f'categoryIcons {label}: {count}x')

# === Fix 13: categoryIcons fallback ===
old = b"categoryIcons[category] || '\xf0\x9f\x94\x90'}"
new = b"categoryIcons[category] || '\xf0\x9f\x93\x81'}"
count = data.count(old)
if count > 0:
    data = data.replace(old, new)
    fixes.append(f'categoryIcons fallback: {count}x')

# Write result
with open(filepath, 'wb') as f:
    f.write(data)

new_size = len(data)
print(f'\nApplied {len(fixes)} fixes:')
for fix in fixes:
    print(f'  + {fix}')
print(f'\nNew file size: {new_size} bytes (delta: {new_size - original_size})')
print('Done!')
