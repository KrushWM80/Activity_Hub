#!/usr/bin/env python3
"""Test the API endpoints directly"""
import requests
import json

base_url = "http://localhost:8080"

# Test 1: Login
print("=" * 60)
print("TEST 1: Login")
print("=" * 60)
try:
    login_resp = requests.post(
        f"{base_url}/api/login",
        json={"username": "admin", "password": "admin123"}
    )
    print(f"Status: {login_resp.status_code}")
    print(f"Response: {login_resp.json()}")
    
    # Get session cookie
    cookies = requests.utils.dict_from_cookiejar(login_resp.cookies)
    print(f"Cookies: {cookies}")
    session = requests.Session()
    session.cookies.update(cookies)
    
except Exception as e:
    print(f"Error: {e}")
    exit(1)

# Test 2: Get Job Codes
print("\n" + "=" * 60)
print("TEST 2: Get Job Codes")
print("=" * 60)
try:
    job_codes_resp = session.get(f"{base_url}/api/job-codes")
    print(f"Status: {job_codes_resp.status_code}")
    
    data = job_codes_resp.json()
    print(f"Total: {data.get('total', 0)}")
    print(f"Job codes count: {len(data.get('job_codes', []))}")
    
    if data.get('job_codes'):
        print(f"\nFirst 3 job codes:")
        for jc in data['job_codes'][:3]:
            print(f"  - {jc['job_code']}: {jc['job_title']} (users: {jc['user_count']})")
    else:
        print("No job codes in response!")
        print(f"Full response: {json.dumps(data, indent=2)}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Cache Status
print("\n" + "=" * 60)
print("TEST 3: Cache Status")
print("=" * 60)
try:
    cache_resp = session.get(f"{base_url}/api/cache-status")
    print(f"Status: {cache_resp.status_code}")
    print(f"Response: {json.dumps(cache_resp.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
