#!/usr/bin/env python
import requests
import json

response = requests.post('http://localhost:8091/api/send-test-email', 
    json={'recipient_email': 'kendall.rush@walmart.com', 'wm_week': 13})

print(json.dumps(response.json(), indent=2))
print(f'Status: {response.status_code}')
