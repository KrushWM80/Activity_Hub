import requests

# Test debug endpoint
try:
    r = requests.get('http://127.0.0.1:8001/api/filters-debug', timeout=30)
    print(f'Debug endpoint status: {r.status_code}')
    if r.status_code == 200:
        d = r.json()
        print(f'Fields: {len(d)}')
        print(f'Keys: {sorted(d.keys())}')
    else:
        print(f'Error response')
except:
    print('Connection failed')

# Test regular endpoint
try:
    r = requests.get('http://127.0.0.1:8001/api/filters', timeout=30)
    d = r.json()
    print(f'\nRegular endpoint: {len(d)} fields')
    print(f'Keys: {sorted(d.keys())}')
except:
    print('Regular endpoint failed')
