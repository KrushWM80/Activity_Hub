import os

file_path = r'c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Interface\Admin\admin-dashboard.html'

with open(file_path, 'rb') as f:
    data = f.read()

print(f"File size: {len(data)} bytes")

# Check BOM
has_bom = data[:3] == b'\xef\xbb\xbf'
print(f"UTF-8 BOM present: {has_bom}")
print(f"First 10 bytes: {data[:10].hex(' ')}")

# Check if nav "Admin" area has double-encoded bytes
idx = data.find(b'Admin</a>')
if idx > 0:
    area = data[idx-30:idx+10]
    print(f"\nNav Admin area bytes: {area.hex(' ')}")

# Check title
idx = data.find(b'Admin Dashboard</h2>')
if idx > 0:
    area = data[idx-15:idx]
    print(f"Title prefix bytes: {area.hex(' ')}")

# Check bell
idx = data.find(b'notification-bell')
if idx > 0:
    area = data[idx+19:idx+50]
    print(f"Bell area bytes: {area.hex(' ')}")

# Check CSS checkmark
idx = data.find(b'card-features li::before')
if idx > 0:
    area = data[idx+40:idx+65]
    print(f"CSS checkmark bytes: {area.hex(' ')}")

# Check for double-encoded patterns
# Double-encoded ð (U+00F0 in UTF-8 is c3 b0)
de_count = data.count(b'\xc3\xb0\xc2\x9f')
print(f"\nDouble-encoded emoji prefix (c3 b0 c2 9f) count: {de_count}")

# Check for correct UTF-8 4-byte emoji prefix
correct_count = data.count(b'\xf0\x9f')  
print(f"Correct UTF-8 4-byte emoji prefix (f0 9f) count: {correct_count}")

# Also check for the specific double-encoded patterns
de_patterns = [
    (b'\xc3\xb0\xc2\x9f', 'double-encoded f0 9f prefix'),
    (b'\xc3\xa2\xc2\x9a\xc2\x99', 'double-encoded e2 9a 99 (gear)'),
    (b'\xc3\xa2\xc2\x86\xc2\x92', 'double-encoded e2 86 92 (arrow)'),
    (b'\xc3\xa2\xc2\x9c', 'double-encoded e2 9c (checkmark)'),
    (b'\xc3\xa2\xc2\x80\xc2\xa2', 'double-encoded e2 80 a2 (bullet)'),
]
print("\nDouble-encoded pattern scan:")
for pat, desc in de_patterns:
    c = data.count(pat)
    if c > 0:
        print(f"  FOUND {c}x: {desc}")
    else:
        print(f"  Not found: {desc}")
