#!/usr/bin/env python3
"""Test the /api/job-codes endpoint with real requests"""

import requests
import json
import time

def test_job_codes_endpoint():
    base_url = "http://localhost:8080"
    
    print("=" * 60)
    print("Testing /api/job-codes Endpoint")
    print("=" * 60)
    
    # Step 1: Login
    print("\n[STEP 1] Logging in...")
    login_data = {"username": "krush", "password": "test"}
    response = requests.post(f"{base_url}/api/login", json=login_data)
    print(f"Login status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        return
    
    cookies = response.cookies
    print(f"Login successful. Got session cookie.")
    
    # Step 2: Call /api/job-codes
    print("\n[STEP 2] Calling /api/job-codes...")
    response = requests.get(f"{base_url}/api/job-codes", cookies=cookies)
    print(f"Status: {response.status_code}")
    print(f"Content-Type: {response.headers.get('content-type')}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"SUCCESS! Response is valid JSON")
            print(f"Job codes count: {len(data.get('job_codes', []))}")
            if data.get('job_codes'):
                print(f"First job code keys: {list(data['job_codes'][0].keys())}")
        except json.JSONDecodeError as e:
            print(f"ERROR: Response is not valid JSON: {e}")
            print(f"Response text: {response.text[:500]}")
    else:
        print(f"ERROR: Got status {response.status_code}")
        print(f"Response text: {response.text[:1000]}")
        print("\nFull response:")
        print(response.text[:2000])
    
    # Step 3: Also test /api/teams for comparison
    print("\n" + "=" * 60)
    print("[STEP 3] Testing /api/teams for comparison...")
    response = requests.get(f"{base_url}/api/teams", cookies=cookies)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"SUCCESS! Got {len(data.get('teams', []))} teams")
    else:
        print(f"ERROR: {response.status_code} - {response.text[:200]}")

if __name__ == "__main__":
    try:
        test_job_codes_endpoint()
    except Exception as e:
        print(f"Exception: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
