#!/usr/bin/env python3
"""Fix UTF-8 corrupted emojis in admin-dashboard.html using binary operations"""

file_path = r'Interface/Admin/admin-dashboard.html'

try:
    # Read as binary to preserve exact bytes
    with open(file_path, 'rb') as f:
        content = f.read()
    
    print(f'✓ Loaded: {len(content)} bytes')
    
    # Map corrupted UTF-8 mojibake to correct Unicode emojis
    # Format: (broken_bytes, correct_bytes)
    fixes = [
        # Admin/Lock emoji
        (b'\xc3\xb0\xc5\xb8\xe2\x80\x9c\xc5\xa1', b'\xf0\x9f\x94\x92'),  # ðŸ"' → 🔒
        (b'\xc3\xb0\xc5\xb8\xe2\x80\x9c', b'\xf0\x9f\x94\x90'),  # ðŸ" → 🔐
        
        # Clipboard emoji  
        (b'\xc3\xb0\xc5\xb8\xe2\x80\x9c\xe2\x80\xb9', b'\xf0\x9f\x93\x8b'),  # ðŸ"‹ → 📋
        
        # Chart/Graph emojis
        (b'\xc3\xb0\xc5\xb8\xe2\x80\x9c\xe2\x80\x9e', b'\xf0\x9f\x93\x8a'),  # ðŸ"„ → 📊
        (b'\xc3\xb0\xc5\xb8\xe2\x80\x9c\xc2\x88', b'\xf0\x9f\x93\x88'),  # ðŸ"ˆ → 📈
        
        # Link emoji
        (b'\xc3\xb0\xc5\xb8\xe2\x80\x9c\xe2\x80\x94', b'\xf0\x9f\x94\x97'),  # ðŸ"— → 🔗
        
        # Target emoji
        (b'\xc3\xb0\xc5\xb8\xc2\x8f\xc2\xaf', b'\xf0\x9f\x8e\xaf'),  # ðŸŽ¯ → 🎯
        
        # Rocket emoji
        (b'\xc3\xb0\xc5\xb8\xc2\xa0\xe2\x82\xac', b'\xf0\x9f\x9a\x80'),  # ðŸš€ → 🚀
        
        # Download/Export emoji
        (b'\xc3\xb0\xc5\xb8\xe2\x80\x9c\xc2\xa5', b'\xf0\x9f\x93\xa5'),  # ðŸ"¥ → 📥
        
        # Save emoji (floppy disk)
        (b'\xc3\xb0\xc5\xb8\xe2\x80\x99\xc2\xbe', b'\xf0\x9f\x92\xbe'),  # ðŸ'¾ → 💾
        
        # Speech bubble emoji
        (b'\xc3\xb0\xc5\xb8\xe2\x80\x99\xc2\xac', b'\xf0\x9f\x92\xac'),  # ðŸ'¬ → 💬
        
        # Bell emoji
        (b'\xc3\xb0\xc5\xb8\xe2\x80\x9c\xe2\x80\x9d', b'\xf0\x9f\x94\x94'),  # ðŸ"" → 🔔
        
        # Delete/Trash emoji
        (b'\xc3\xb0\xc5\xb8\xe2\x80\x94\xe2\x80\x99\xc3\xaf\xc2\xb8', b'\xf0\x9f\x97\x91\xef\xb8\x8f'),  # ðŸ—'ï¸ → 🗑️
        
        # Arrow right
        (b'\xc3\xa2\xe2\x80\x94\xe2\x80\x99', b'\xe2\x86\x92'),  # â†' → →
        
        # Reset/refresh emoji
        (b'\xc3\xb0\xc5\xb8\xe2\x80\x9c\xe2\x80\x9e', b'\xf0\x9f\x94\x84'),  # ðŸ"„ → 🔄
        
        # Tag/label emoji
        (b'\xc3\xb0\xc5\xb8\xe2\x80\x9c\xc2\xb7', b'\xf0\x9f\x93\xad'),  # ðŸ"· → 📭
        
        # Multiply sign
        (b'\xc3\x83\xe2\x80\x94', b'\xc3\x97'),  # Ã— → ×
    ]
    
    fixed_count = 0
    for broken, fixed in fixes:
        count = content.count(broken)
        if count > 0:
            print(f'  ✓ Fixed {count}x {broken!r} → {fixed!r}')
            content = content.replace(broken, fixed)
            fixed_count += count
    
    # Write back as binary
    with open(file_path, 'wb') as f:
        f.write(content)
    
    print(f'\n✅ Complete! Fixed {fixed_count} emoji sequences')
    print(f'   New size: {len(content)} bytes')

except Exception as e:
    print(f'❌ ERROR: {e}')
    exit(1)
