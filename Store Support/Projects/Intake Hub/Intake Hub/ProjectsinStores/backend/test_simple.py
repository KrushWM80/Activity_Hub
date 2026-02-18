import requests
import sys

response = requests.get('http://127.0.0.1:8001/api/filters', timeout=120)
data = response.json()
print(f'Status: {response.status_code}')
print(f'Fields: {sorted(list(data.keys()))}')
print(f'Count: {len(data.keys())}')
if 'owners' in data:
    print(f'Owners: {len(data.get("owners", []))}')
