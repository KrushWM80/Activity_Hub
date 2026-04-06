#!/usr/bin/env python3
"""Test Logic Metrics endpoint"""

import requests
import json

print("Testing GET /api/v1/logic-metrics")
print("=" * 60)

try:
    response = requests.get('http://localhost:5011/api/v1/logic-metrics', timeout=5)
    print(f'HTTP Status: {response.status_code}')
    
    if response.status_code == 200:
        data = response.json()
        print('\n✓ SUCCESS - Metrics Retrieved')
        print('-' * 60)
        print(f'Active Rules: {data.get("activeRules")}')
        print(f'Notifications Today: {data.get("notificationsToday")}')
        print(f'Pending Approvals: {data.get("pendingApprovals")}')
        print(f'Total Logic Requests: {data.get("totalLogicRequests")}')
        print(f'Timestamp: {data.get("timestamp")}')
        print('-' * 60)
    else:
        print(f'\n✗ Error: {response.status_code}')
        print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f'✗ Connection Error: {e}')
