"""Diagnose the actual byte sequences for corrupted emoji in admin-dashboard.html"""
import os

file_path = os.path.join(os.path.dirname(__file__), 'Interface', 'Admin', 'admin-dashboard.html')

with open(file_path, 'rb') as f:
    content = f.read()

print(f"File size: {len(content)} bytes")
print()

# Search for known mojibake patterns by looking for surrounding context
targets = [
    (b'landing-card-icon logic">', 'Logic icon (gear)'),
    (b'landing-card-arrow">', 'Card arrow'),
    (b'value="Admin Features"><span>', 'Feedback gear'),
    (b'Email ', 'Email bullet (table header)'),
    (b"' \xc3\xa2", 'Bullet pattern check'),
]

# Let's find all occurrences of common mojibake starter bytes
# Double-encoded UTF-8 typically starts with C3 followed by another high byte
print("=== Searching for mojibake byte patterns ===")
print()

# Find the gear emoji mojibake: âš™ï¸
# â = C3 A2, š = C5 A1 or C2 9A, ™ = E2 84 A2 or C2 99, ï = C3 AF, ¸ = C2 B8, Â = C2 8F
# But double-encoded: â(U+00E2) š(U+0161) ™(U+2122) ... 
# Actually the mojibake "âš™ï¸" when stored as UTF-8 bytes is just the UTF-8 encoding of those display chars

# Let's just search for the UTF-8 encoding of the display string "âš™ï¸"
gear_display = 'âš™ï¸'.encode('utf-8')
bullet_display = 'â€¢'.encode('utf-8')
arrow_display = 'â†''.encode('utf-8')

print(f"Looking for gear mojibake bytes: {gear_display.hex(' ')}")
print(f"Looking for bullet mojibake bytes: {bullet_display.hex(' ')}")
print(f"Looking for arrow mojibake bytes: {arrow_display.hex(' ')}")
print()

gear_count = content.count(gear_display)
bullet_count = content.count(bullet_display)
arrow_count = content.count(arrow_display)

print(f"Gear mojibake occurrences: {gear_count}")
print(f"Bullet mojibake occurrences: {bullet_count}")
print(f"Arrow mojibake occurrences: {arrow_count}")
print()

# Show context around first occurrence of each
for pattern, name in [(gear_display, 'Gear'), (bullet_display, 'Bullet'), (arrow_display, 'Arrow')]:
    idx = content.find(pattern)
    if idx >= 0:
        start = max(0, idx - 40)
        end = min(len(content), idx + len(pattern) + 40)
        snippet = content[start:end]
        print(f"--- {name} at offset {idx} ---")
        print(f"Context: {snippet}")
        print(f"Hex: {snippet.hex(' ')}")
        print()

# Also check what the correct emoji bytes look like
correct_gear = '⚙️'.encode('utf-8')
correct_bullet = '•'.encode('utf-8')
correct_arrow = '→'.encode('utf-8')

print(f"Correct gear bytes: {correct_gear.hex(' ')}")
print(f"Correct bullet bytes: {correct_bullet.hex(' ')}")
print(f"Correct arrow bytes: {correct_arrow.hex(' ')}")
