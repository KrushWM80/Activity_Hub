import os
import sys

file_path = os.path.join(os.path.dirname(__file__), 'business-overview-dashboard.html')

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f'Loaded file: {len(content)} bytes')
    
    # Replace broken emoji
    fixes = [
        ('ðŸ"‹', '📋'),
        ('ðŸ"ˆ', '📈'),
        ('ðŸ"Š', '📊'),
        ('â–¼', '▼'),
    ]
    
    for broken, fixed in fixes:
        if broken in content:
            count = content.count(broken)
            print(f'Replacing {count}x {broken} with {fixed}')
            content = content.replace(broken, fixed)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'✅ Saved! New size: {len(content)} bytes')
    
except Exception as e:
    print(f'ERROR: {e}', file=sys.stderr)
    sys.exit(1)
