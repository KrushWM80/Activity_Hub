#!/usr/bin/env python
import requests
import json

# Try to delete the callout
response = requests.delete('http://localhost:8091/api/callouts/callout_13_1777665106')
print("Delete response:")
print(json.dumps(response.json(), indent=2))
print(f'Status: {response.status_code}')
