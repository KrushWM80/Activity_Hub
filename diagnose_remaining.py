#!/usr/bin/env python3
"""Diagnose exact hex bytes of remaining corrupted emoji in admin-dashboard.html"""

filepath = r'c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Interface\Admin\admin-dashboard.html'

with open(filepath, 'rb') as f:
    data = f.read()

print(f'File size: {len(data)} bytes')

# Search for all known corruption byte patterns
patterns = {
    'c3 a2': b'\xc3\xa2',
    'ef bf bd (FFFD)': b'\xef\xbf\xbd',
    'f0 9f 94 90 (lock)': b'\xf0\x9f\x94\x90',
}

for name, pat in patterns.items():
    positions = []
    idx = 0
    while True:
        idx = data.find(pat, idx)
        if idx < 0:
            break
        positions.append(idx)
        idx += 1
    print(f'\n{name}: {len(positions)} occurrences')
    for pos in positions[:20]:
        context = data[max(0, pos-30):pos+len(pat)+30]
        print(f'  @ {pos}: ...{context}...')

# Specific checks
print('\n--- Specific locations ---')

idx = data.find(b'Condition</strong>')
if idx > 0:
    chunk = data[idx-20:idx+5]
    print(f'Before "Condition": hex={chunk.hex(" ")}')

idx = data.find(b'Action</strong>')
if idx > 0:
    chunk = data[idx-20:idx+5]
    print(f'Before "Action": hex={chunk.hex(" ")}')

idx = data.find(b'Auth</div>')
if idx > 0:
    chunk = data[idx-40:idx]
    print(f'Before "Auth": hex={chunk.hex(" ")}')

idx = data.find(b'Back</button>')
if idx > 0:
    chunk = data[idx-10:idx]
    print(f'Before "Back": hex={chunk.hex(" ")}')

for key in [b"status: '", b"location: '", b"time: '", b"impact: '", b"description: '", b"amp_meeting: '"]:
    idx = data.find(key)
    if idx > 0:
        val_start = idx + len(key)
        val_end = data.find(b"'", val_start)
        if val_end > 0:
            val = data[val_start:val_end]
            print(f'{key.decode()} value hex={val.hex(" ")} len={len(val)}')

# Export buttons
for marker in [b'Export Schema</button>', b'exportActivityLog']:
    idx = data.find(marker)
    if idx > 0:
        chunk = data[max(0,idx-20):idx+5]
        print(f'Near "{marker[:20].decode()}": hex={chunk.hex(" ")}')
