#!/usr/bin/env python
import requests
import json

response = requests.post('http://localhost:8091/api/callouts', 
    json={
        'wm_week': 13,
        'title': 'Call out Test Title',
        'content': 'Call Out Message Body',
        'created_by': 'Test User'
    })

print(json.dumps(response.json(), indent=2))
print(f'Status: {response.status_code}')
