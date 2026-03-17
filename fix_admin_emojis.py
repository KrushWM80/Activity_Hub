#!/usr/bin/env python3
import os

file_path = r"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Interface\Admin\admin-dashboard.html"

# Read the file with proper encoding
with open(file_path, 'rb') as f:
    content = f.read()

# Fix corrupted emoji sequences (mojibake)
fixes = {
    b'\xc3\xb0\xc2\x9f\xc2\x93\xc2\x92': '🔒'.encode('utf-8'),  # ðŸ"'  -> 🔒
    b'\xc3\xb0\xc2\x9f\xc2\x93\xc2\x93': '📓'.encode('utf-8'),  # ðŸ""  -> 📓
    b'\xc3\xb0\xc2\x9f\xc2\x93\xc2\x97': '🔗'.encode('utf-8'),  # ðŸ"—  -> 🔗
    b'\xc3\xb0\xc2\x9f\xc2\x93\xc2\x84': '📊'.encode('utf-8'),  # ðŸ"„  -> 📊
    b'\xc3\xb0\xc2\x9f\xc2\x93\xc2\x90': '📐'.encode('utf-8'),  # ðŸ""  -> 📐
    b'\xc3\xb0\xc2\x9f\xc2\x8e\xc2\xaf': '🎯'.encode('utf-8'),  # ðŸŽ¯  -> 🎯
    b'\xc3\xb0\xc2\x9f\xc2\x94\xc2\xa4': '🔢'.encode('utf-8'),  # ðŸ"¤  -> 🔢
    b'\xc3\xa2\xc2\x80\xc2\xa2': '•'.encode('utf-8'),            # â€¢  -> •
    b'\xc3\xa2\xc2\x86\xc2\x92': '→'.encode('utf-8'),            # â†'  -> →
}

for old, new in fixes.items():
    content = content.replace(old, new)

# Write it back
with open(file_path, 'wb') as f:
    f.write(content)

print("✅ Fixed admin dashboard emoji corruption")
