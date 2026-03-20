"""Diagnose and fix ALL corrupted UTF-8 emoji in admin-dashboard.html"""
import sys

file_path = r'c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Interface\Admin\admin-dashboard.html'

with open(file_path, 'rb') as f:
    original = f.read()

print(f"File size: {len(original)} bytes")

def double_encode(char):
    return char.encode('utf-8').decode('latin-1').encode('utf-8')

def double_encode_cp1252(char):
    try:
        return char.encode('utf-8').decode('cp1252').encode('utf-8')
    except:
        return None

emoji_list = [
    '\U0001f511', '\U0001f4cb', '\U0001f510', '\u2699\ufe0f',
    '\U0001f517', '\U0001f4c4', '\U0001f3af', '\u2192',
    '\U0001f5d1\ufe0f', '\U0001f3a8', '\U0001f4a1', '\U0001f61e',
    '\U0001f610', '\U0001f60a', '\U0001f604', '\U0001f929',
    '\U0001f4f7', '\u2022', '\u2713', '\u2714', '\u2717',
    '\u2705', '\u270f\ufe0f', '\U0001f464', '\U0001f3f7\ufe0f',
    '\U0001f4ca', '\U0001f512', '\U0001f514', '\U0001f504',
    '\U0001f4ac', '\U0001f4be', '\U0001f680', '\U0001f4e5',
    '\U0001f4c8', '\u23f0', '\U0001f4cd', '\u26a0\ufe0f',
]

# Diagnostic
print("\n=== DIAGNOSTIC: latin-1 double-encode ===")
found_latin1 = False
for char in emoji_list:
    broken = double_encode(char)
    count = original.count(broken)
    if count > 0:
        found_latin1 = True
        print(f"  Found {count:3d}x {char} ({broken.hex(' ')})")

print("\n=== DIAGNOSTIC: cp1252 double-encode ===")
found_cp1252 = False
for char in emoji_list:
    broken = double_encode_cp1252(char)
    if broken:
        count = original.count(broken)
        if count > 0:
            found_cp1252 = True
            print(f"  Found {count:3d}x {char} ({broken.hex(' ')})")

content = original
total = 0

if found_latin1:
    print("\n=== FIXING (latin-1) ===")
    for char in sorted(emoji_list, key=lambda c: len(double_encode(c)), reverse=True):
        broken = double_encode(char)
        correct = char.encode('utf-8')
        count = content.count(broken)
        if count > 0:
            content = content.replace(broken, correct)
            total += count
            print(f"  Fixed {count:3d}x {char}")
elif found_cp1252:
    print("\n=== FIXING (cp1252) ===")
    for char in sorted(emoji_list, key=lambda c: len(double_encode_cp1252(c) or b''), reverse=True):
        broken = double_encode_cp1252(char)
        if broken:
            correct = char.encode('utf-8')
            count = content.count(broken)
            if count > 0:
                content = content.replace(broken, correct)
                total += count
                print(f"  Fixed {count:3d}x {char}")
else:
    print("\nNo double-encoded patterns found. Dumping raw bytes at problem areas:")
    for marker, name in [(b'landing-card-icon logic">', 'Logic'), (b'landing-card-icon access">', 'Access'), (b'landing-card-arrow">', 'Arrow'), (b'card-features li::before', 'CSS')]:
        idx = original.find(marker)
        if idx >= 0:
            s = idx + len(marker)
            print(f"  {name}: {original[s:s+30].hex(' ')}")
    sys.exit(1)

print(f"\nTotal: {total}")

if content != original:
    with open(file_path, 'wb') as f:
        f.write(content)
    with open(file_path, 'rb') as f:
        verify = f.read()
    if verify == content:
        print(f"SUCCESS! Verified. Size: {len(original)} -> {len(content)}")
    else:
        print("ERROR: verify failed"); sys.exit(1)
else:
    print("No changes."); sys.exit(1)
