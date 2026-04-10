#!/usr/bin/env python3
"""Test endpoint to check cache status from API context"""

import requests
import json

print("=== CHECK CACHE VIA API ENDPOINT ===\n")

try:
    # GET /api/summary which should tell us cache status
    response = requests.get("http://localhost:8001/api/summary")
    summary = response.json()
    
    print("API /api/summary response:")
    print(json.dumps(summary, indent=2))
    
except Exception as e:
    print(f"Error: {e}")
