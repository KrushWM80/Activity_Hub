import json

with open('active_users.json', 'r') as f:
    data = json.load(f)

users = data.get('users', {})
print(f'Total raw sessions: {len(users)}')
print()

# Search for kristii.buttery entries
kristii_sessions = [s for s in users.values() if 'kristii' in s.get('user_email', '').lower()]
print(f'Sessions for kristii.buttery: {len(kristii_sessions)}')

if kristii_sessions:
    print('Found kristii.buttery sessions:')
    for s in kristii_sessions:
        print(f'  Email: {s.get("user_email")}')
        print(f'  Device: {s.get("device_info")}')
        print(f'  Page: {s.get("page")}')
        print(f'  Last Seen: {s.get("last_seen")}')
        print()
else:
    print('NO kristii.buttery sessions found in active_users.json')
    print()
    print('All unique emails in the system:')
    emails = set(s.get('user_email') for s in users.values())
    for email in sorted(emails):
        count = len([s for s in users.values() if s.get('user_email') == email])
        print(f'  - {email} ({count} sessions)')
