import json

with open('active_users.json', 'r') as f:
    data = json.load(f)

users = data.get('users', {})

# Show each unique email|device combo with details
consolidated = {}
for session_id, session_data in users.items():
    email = session_data.get('user_email', 'Unknown')
    device = session_data.get('device_info', 'Unknown')
    key = f'{email}|{device}'
    
    if key not in consolidated or session_data.get('timestamp', 0) > consolidated[key].get('timestamp', 0):
        consolidated[key] = session_data.copy()

print('=' * 80)
print('CONSOLIDATED ACTIVE USERS (What /api/admin/active-users Returns)')
print('=' * 80)
for idx, (key, info) in enumerate(consolidated.items(), 1):
    parts = key.split('|')
    email = parts[0] if len(parts) > 0 else 'Unknown'
    device = parts[1] if len(parts) > 1 else 'Unknown'
    page = info.get('page', 'Unknown')
    last_seen = info.get('last_seen', 'Unknown')
    
    print(f'{idx}. {email} - {device}')
    print(f'   Page: {page}')
    print(f'   Last Seen: {last_seen}')
    print()

print(f'Total distinct consolidated sessions: {len(consolidated)}')
