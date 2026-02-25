import json

with open('active_users.json', 'r') as f:
    data = json.load(f)

print('\n' + '='*120)
print('USER-AGENT DETECTION DEBUG')
print('='*120)
print()
print(f'Total Sessions: {len(data.get("users", {}))}')
print()

# Show all sessions with their User-Agent
for idx, (session_id, info) in enumerate(list(data.get('users', {}).items())[-10:], 1):
    email = info.get('user_email', 'Unknown')
    device = info.get('device_info', 'Unknown')
    page = info.get('page', 'Unknown')
    user_agent = info.get('user_agent', 'NOT CAPTURED')
    last_seen = info.get('last_seen', 'Unknown')
    
    print(f'{idx}. Session: {session_id}')
    print(f'   Email: {email}')
    print(f'   Device Detected: {device}')
    print(f'   Page: {page}')
    print(f'   Last Seen: {last_seen}')
    print(f'   User-Agent:')
    print(f'   >>> {user_agent[:100]}...' if len(user_agent) > 100 else f'   >>> {user_agent}')
    print()

print('='*120)
