"""
Fix ALL corrupted UTF-8 emoji (mojibake) in admin-dashboard.html
Uses binary mode with absolute paths to ensure persistence.
"""
import os
import sys

# Absolute path - no ambiguity
file_path = r'c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Interface\Admin\admin-dashboard.html'

if not os.path.exists(file_path):
    print(f"ERROR: File not found: {file_path}")
    sys.exit(1)

# Step 1: Read as binary
with open(file_path, 'rb') as f:
    original = f.read()

print(f"File size: {len(original)} bytes")
content = original  # work on a copy

# Step 2: Build replacement map
# Mojibake happens when UTF-8 bytes are misread as Latin-1/CP1252 then re-encoded as UTF-8
# To find the broken bytes: take the correct emoji, encode to UTF-8, decode as latin-1, encode as UTF-8
# That gives us exactly what double-encoding produces.

def double_encode(char):
    """Simulate double-encoding: correct UTF-8 -> misread as CP1252 -> re-encoded as UTF-8.
    Handles undefined CP1252 bytes (0x81, 0x8D, 0x8F, 0x90, 0x9D) by mapping to code point."""
    utf8_bytes = char.encode('utf-8')
    chars = []
    for b in utf8_bytes:
        try:
            chars.append(bytes([b]).decode('cp1252'))
        except (UnicodeDecodeError, UnicodeEncodeError):
            chars.append(chr(b))
    return ''.join(chars).encode('utf-8')

# All emoji/symbols we need to fix, mapped to their correct UTF-8 bytes
fix_map = {
    '🔑': double_encode('🔑'),   # key
    '📋': double_encode('📋'),   # clipboard (bell/notification)  
    '🔐': double_encode('🔐'),   # lock
    '⚙️': double_encode('⚙️'),   # gear
    '🔗': double_encode('🔗'),   # link
    '📄': double_encode('📄'),   # document
    '🎯': double_encode('🎯'),   # target
    '→':  double_encode('→'),    # arrow right
    '🗑️': double_encode('🗑️'),   # trash
    '🎨': double_encode('🎨'),   # palette
    '💡': double_encode('💡'),   # lightbulb
    '😞': double_encode('😞'),   # sad
    '😐': double_encode('😐'),   # neutral
    '😊': double_encode('😊'),   # happy
    '😄': double_encode('😄'),   # big smile
    '🤩': double_encode('🤩'),   # star eyes
    '📷': double_encode('📷'),   # camera
    '•':  double_encode('•'),    # bullet
    '✓': double_encode('✓'),    # checkmark  
    '✔': double_encode('✔'),    # heavy checkmark
    '✗': double_encode('✗'),    # x mark
    '✅': double_encode('✅'),   # green checkmark
    '✏️': double_encode('✏️'),   # pencil/edit
    '👤': double_encode('👤'),   # person silhouette
    '🏷️': double_encode('🏷️'),   # label/tag
    '📊': double_encode('📊'),   # chart
    '🔒': double_encode('🔒'),   # padlock
    '🔔': double_encode('🔔'),   # bell
    '🔄': double_encode('🔄'),   # refresh
    '💬': double_encode('💬'),   # speech bubble
    '💾': double_encode('💾'),   # floppy disk
    '🚀': double_encode('🚀'),   # rocket
    '📥': double_encode('📥'),   # inbox
    '📈': double_encode('📈'),   # chart up
    '⏰': double_encode('⏰'),   # clock
    '📍': double_encode('📍'),   # pin
}

# Step 3: Apply replacements (longest broken sequences first to avoid partial matches)
total = 0
for correct_char, broken_bytes in sorted(fix_map.items(), key=lambda x: len(x[1]), reverse=True):
    correct_bytes = correct_char.encode('utf-8')
    count = content.count(broken_bytes)
    if count > 0:
        content = content.replace(broken_bytes, correct_bytes)
        print(f"  Fixed {count:3d}x  {correct_char}  ({broken_bytes.hex(' ')} -> {correct_bytes.hex(' ')})")
        total += count

print(f"\nTotal replacements: {total}")

# Step 4: Only write if changes were made
if content != original:
    with open(file_path, 'wb') as f:
        f.write(content)
    print(f"\nFile saved! New size: {len(content)} bytes (was {len(original)})")
    
    # Verify by re-reading
    with open(file_path, 'rb') as f:
        verify = f.read()
    if verify == content:
        print("VERIFIED: File written and re-read successfully!")
    else:
        print("WARNING: Re-read doesn't match what was written!")
else:
    print("\nNo changes needed - patterns not found in file.")
    print("The file may use a different encoding or the mojibake pattern is different.")
    
    # Diagnostic: dump bytes around known problem areas
    print("\n=== DIAGNOSTIC: Searching for context near known corrupted areas ===")
    markers = [b'landing-card-icon logic">', b'landing-card-icon access">', b'landing-card-arrow">',
               b'clearActivityLog()" style="color: var(--error);">', b'Intake Hub Data',
               b"editField('${key}')\">", b'Delete Field</h3>',
               b'rating-emoji">', b"categorization: '", b'landing-card-icon links">']
    for marker in markers:
        idx = content.find(marker)
        if idx >= 0:
            start = idx + len(marker)
            snippet = content[start:start+30]
            print(f"After '{marker.decode('utf-8', errors='replace')}': {snippet.hex(' ')}")
        else:
            # search backwards for some
            pass
