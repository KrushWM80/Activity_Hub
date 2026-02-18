import requests

response = requests.get('http://127.0.0.1:8001/api/filters', timeout=120)

print(f"Status: {response.status_code}")
print(f"Content-Type: {response.headers.get('content-type')}")
print(f"Content-Length header: {response.headers.get('content-length')}")
print(f"Actual body length: {len(response.content)} bytes")
print(f"\nRaw JSON (first 500 chars):\n{response.text[:500]}")
print(f"\nLast 200 chars:\n{response.text[-200:]}")

# Parse and check fields
data = response.json()
fields = list(data.keys())
print(f"\nParsed fields ({len(fields)}):")
for f in sorted(fields):
    count = len(data.get(f, []))
    print(f"  {f}: {count} items")
