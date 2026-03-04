import json

with open('activity_log.json', 'r') as f:
    data = json.load(f)

print('='*80)
print('ACTIVITY LOG - SEARCH FOR 77bebcdf')
print('='*80)
print()

found = False
for activity in data.get('activities', []):
    if '77bebcdf' in str(activity):
        found = True
        print(f"Timestamp: {activity.get('timestamp')}")
        print(f"Action: {activity.get('action')}")
        print(f"User: {activity.get('user')}")
        print(f"Details: {activity.get('details')}")
        print()

if not found:
    print('❌ No activity log entries found for 77bebcdf')
    print()
    print('Last 10 activities:')
    print('-'*80)
    for activity in data.get('activities', [])[-10:]:
        ts = activity.get('timestamp', 'N/A')
        user = activity.get('user', 'N/A')
        action = activity.get('action', 'N/A')
        details = activity.get('details', '')[:70]
        print(f'{ts} | {user}')
        print(f'  Action: {action}')
        print(f'  {details}')
        print()
