import json

with open('active_users.json', 'r') as f:
    data = json.load(f)

print('=' * 80)
print('LATEST 5 SESSIONS - CHECKING FOR ACTIVITY LOG AND MOBILE USER-AGENTS')
print('=' * 80)
print()

sessions = list(data.get('users', {}).items())
for session_id, info in sessions[-5:]:
    email = info.get('user_email', 'Unknown')
    device = info.get('device_info', 'Unknown')
    page = info.get('page', 'Unknown')
    last_seen = info.get('last_seen', 'Unknown')
    user_agent = info.get('user_agent', 'NO USER-AGENT')
    
    print(f'Email: {email}')
    print(f'Page: {page}')
    print(f'Device: {device}')
    print(f'Last Seen: {last_seen}')
    print(f'User-Agent (first 120 chars): {user_agent[:120]}...')
    print()

print('=' * 80)
print(f'Total Sessions: {len(data.get("users", {}))}')

# Check if Activity Log page exists
pages = [s.get('page') for s in data.get('users', {}).values()]
print(f'Unique Pages Visited: {set(pages)}')
print('=' * 80)
