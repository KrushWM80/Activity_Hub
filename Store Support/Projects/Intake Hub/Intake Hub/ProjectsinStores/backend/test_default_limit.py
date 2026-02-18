import requests

r = requests.get('http://127.0.0.1:8001/api/projects', timeout=10)
data = r.json()
print(f'Status: {r.status_code}')
print(f'Projects returned: {len(data)}')
print(f'First project: {data[0]["title"][:50]}... | BA: {data[0].get("business_area")}')
print(f'Response size: {len(r.text):,} bytes')
