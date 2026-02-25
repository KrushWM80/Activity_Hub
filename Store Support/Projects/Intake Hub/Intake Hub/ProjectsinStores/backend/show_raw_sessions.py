import json
from collections import Counter

with open('active_users.json', 'r') as f:
    data = json.load(f)

total_sessions = len(data.get('users', {}))

print('\n' + '='*100)
print('RAW SESSION DATA (BEFORE CONSOLIDATION)')
print('='*100)
print(f'\nTotal Raw Sessions: {total_sessions}\n')

# Show last 5 sessions
sessions_list = list(data.get('users', {}).items())
for idx, (session_id, info) in enumerate(sessions_list[-5:], 1):
    print(f'{idx}. Session ID: {session_id}')
    print(f'   Email: {info.get("user_email")}')
    print(f'   Device: {info.get("device_info")}')
    print(f'   Page: {info.get("page")}')
    print(f'   Last Seen: {info.get("last_seen")}')
    print()

# Count by device
devices = Counter([info.get('device_info', 'Unknown') for info in data.get('users', {}).values()])
print('='*100)
print('Device Distribution:')
for device, count in devices.items():
    print(f'  {device}: {count} sessions')
print('='*100 + '\n')
