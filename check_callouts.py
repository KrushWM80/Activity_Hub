#!/usr/bin/env python
import requests
import json

# Get callouts for WK 13
response = requests.get('http://localhost:8091/api/callouts/13')
print("Callouts for WK 13:")
print(json.dumps(response.json(), indent=2))
print(f'Status: {response.status_code}')
