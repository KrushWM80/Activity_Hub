#!/usr/bin/env python3
"""Fix final remaining corrupted emoji in admin-dashboard.html"""

filepath = r'c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Interface\Admin\admin-dashboard.html'

with open(filepath, 'rb') as f:
    data = f.read()

original_size = len(data)
print(f'Original file size: {original_size} bytes')

fixes = []

# Fix 1: info icon - double-encoded via CP1252
# Original: e2 84 b9 ef b8 8f (U+2139 U+FE0F = info source with variation selector)
# Corrupted: c3 a2 e2 80 9e c2 b9 c3 af c2 b8 c2 8f
old = b'\xc3\xa2\xe2\x80\x9e\xc2\xb9\xc3\xaf\xc2\xb8\xc2\x8f'
new = b'\xe2\x84\xb9\xef\xb8\x8f'  # info source with VS16
count = data.count(old)
if count > 0:
    data = data.replace(old, new)
    fixes.append(f'Info icon: {count}x')

# Fix 2: warning icon - double-encoded via CP1252
# Original: e2 9a a0 ef b8 8f (U+26A0 U+FE0F = warning sign with variation selector)
# Corrupted: c3 a2 c5 a1 c2 a0 c3 af c2 b8 c2 8f
old = b'\xc3\xa2\xc5\xa1\xc2\xa0\xc3\xaf\xc2\xb8\xc2\x8f'
new = b'\xe2\x9a\xa0\xef\xb8\x8f'  # warning with VS16
count = data.count(old)
if count > 0:
    data = data.replace(old, new)
    fixes.append(f'Warning icon: {count}x')

# Fix 3: Feedback category "Workflows & Logic" icon
# f0 9f 94 90 e2 80 b9 (🔐‹) near "Workflows"
# Use context to target specifically
old = b'value="Workflows"><span>\xf0\x9f\x94\x90\xe2\x80\xb9</span> Workflows'
new = b'value="Workflows"><span>\xf0\x9f\x94\x84</span> Workflows'  # 🔄
count = data.count(old)
if count > 0:
    data = data.replace(old, new)
    fixes.append(f'Feedback Workflows icon: {count}x')

# Fix 4: Empty activity log state icon
# f0 9f 94 90 e2 80 b9 (🔐‹) near "No activity logs"
old = b'var(--space-4);">\xf0\x9f\x94\x90\xe2\x80\xb9</div><p>No activity logs'
new = b'var(--space-4);">\xf0\x9f\x93\x8b</div><p>No activity logs'  # 📋
count = data.count(old)
if count > 0:
    data = data.replace(old, new)
    fixes.append(f'Empty activity log icon: {count}x')

# Fix 5: categoryIcons fallback
# f0 9f 94 90 c2 81 -> f0 9f 93 81 (📁)
old = b"categoryIcons[category] || '\xf0\x9f\x94\x90\xc2\x81'}"
new = b"categoryIcons[category] || '\xf0\x9f\x93\x81'}"  # 📁
count = data.count(old)
if count > 0:
    data = data.replace(old, new)
    fixes.append(f'categoryIcons fallback: {count}x')

with open(filepath, 'wb') as f:
    f.write(data)

new_size = len(data)
print(f'\nApplied {len(fixes)} fixes:')
for fix in fixes:
    print(f'  + {fix}')
print(f'\nNew file size: {new_size} bytes (delta: {new_size - original_size})')

# Verify no remaining corruption
remaining_c3a2 = data.count(b'\xc3\xa2')
remaining_fffd = data.count(b'\xef\xbf\xbd')
lock_count = data.count(b'\xf0\x9f\x94\x90')
print(f'\nVerification:')
print(f'  c3 a2 (double-encoded lead): {remaining_c3a2}')
print(f'  ef bf bd (FFFD): {remaining_fffd}')
print(f'  f0 9f 94 90 (lock emoji): {lock_count} (1 expected for Access card)')
