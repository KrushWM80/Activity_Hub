#!/usr/bin/env python3
"""Test custom trigger Logic Request creation"""

import requests
import json
import time

# Wait for service
time.sleep(2)

payload = {
    'name': 'Test: Projects With No Activity 30+ Days',
    'trigger_type': 'custom',
    'description': 'Alert when a project has no activity',
    'custom_trigger_text': 'Project has not had a note in more than 30 days',
    'has_notification_component': True,
    'notification_rule': {
        'category': 'PROJECT_LIFECYCLE',
        'schedule': 'immediate',
        'title': 'Inactive Project Alert: {project_name}',
        'message': 'This project has had no updates for more than 30 days. Please review.'
    }
}

try:
    print("Testing POST /api/v1/logic-requests")
    print("-" * 60)
    response = requests.post('http://localhost:5011/api/v1/logic-requests', json=payload, timeout=5)
    print(f'HTTP Status: {response.status_code}')
    result = response.json()
    
    if response.status_code == 200:
        print('\n✓ SUCCESS - Logic Request Created')
        print('-' * 60)
        print(f'Request ID: {result.get("request_id")}')
        print(f'Name: {result.get("name")}')
        print(f'Approval Status: {result.get("approval_status")}')
        print(f'Trigger Type: {result.get("trigger_type")}')
        if result.get("custom_trigger_text"):
            print(f'Custom Trigger Text: {result.get("custom_trigger_text")}')
        if result.get("note"):
            print(f'Note: {result.get("note")}')
        print('-' * 60)
    else:
        print('\n✗ ERROR')
        print('-' * 60)
        print(json.dumps(result, indent=2))
        print('-' * 60)
except Exception as e:
    print(f'\n✗ Connection Error: {e}')
    print('-' * 60)
