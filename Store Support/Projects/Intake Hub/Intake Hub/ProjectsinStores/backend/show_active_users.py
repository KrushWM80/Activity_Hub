import json

with open('active_users.json', 'r') as f:
    data = json.load(f)

# Group by email + device to get consolidated view
consolidated = {}
for session_id, session_data in data.get('users', {}).items():
    email = session_data.get('user_email', 'Unknown')
    device = session_data.get('device_info', 'Unknown')
    page = session_data.get('page', 'Unknown')
    key = f'{email}|{device}'
    
    if key not in consolidated or session_data.get('timestamp', 0) > consolidated[key].get('timestamp', 0):
        consolidated[key] = {
            'session_id': session_id,
            'email': email,
            'device': device,
            'page': page,
            'last_seen': session_data.get('last_seen', 'Unknown')
        }

print('\n' + '='*140)
print('ACTIVE SESSIONS ON: http://weus42608431466.homeoffice.wal-mart.com:8001/admin.html')
print('='*140)
print()
print('{:<35} {:<15} {:<37} {:<25} {:<20}'.format('EMAIL', 'BROWSER', 'SESSION ID', 'PAGE', 'LAST SEEN'))
print('-'*140)

if not consolidated:
    print('No active sessions')
else:
    for key, info in sorted(consolidated.items()):
        email = info['email'][:34]
        device = info['device'][:14]
        session = info['session_id'][:36]
        page = info['page'][:24]
        last_seen = info['last_seen'][:19]
        print('{:<35} {:<15} {:<37} {:<25} {:<20}'.format(email, device, session, page, last_seen))

print()
print('='*140)
print('Total Consolidated Sessions: {}'.format(len(consolidated)))
print('='*140)
print()
