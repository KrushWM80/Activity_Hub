#!/usr/bin/env python
"""Test script for session-based login"""

import requests
import json

BASE_URL = "http://localhost:8001"

print("Testing Session-Based Login System")
print("=" * 50)

# 1. Test initial /api/auth/user (no session, local Windows user)
print("\n1. Testing /api/auth/user (local Windows user)")
try:
    response = requests.get(f"{BASE_URL}/api/auth/user")
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   User: {data.get('email')}")
    print(f"   Is Admin: {data.get('is_admin')}")
    print(f"   Auth Method: {data.get('auth_method')}")
except Exception as e:
    print(f"   ERROR: {e}")

# 2. Test login endpoint
print("\n2. Testing /api/auth/login (remote user login)")
print("   Attempting login with test credentials...")
try:
    login_data = {
        "username": "testuser",
        "password": "Admin2026"  # fallback password
    }
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json=login_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   User: {data.get('email')}")
        print(f"   Is Admin: {data.get('is_admin')}")
        print(f"   Auth Method: {data.get('auth_method')}")
        print(f"   Session Cookie Set: {'session_id' in response.cookies}")
        if 'session_id' in response.cookies:
            session_id = response.cookies['session_id']
            print(f"   Session ID: {session_id[:20]}...")
            
            # 3. Use session cookie in subsequent request
            print("\n3. Testing /api/auth/user with session cookie")
            response2 = requests.get(
                f"{BASE_URL}/api/auth/user",
                cookies={"session_id": session_id}
            )
            print(f"   Status: {response2.status_code}")
            data2 = response2.json()
            print(f"   User: {data2.get('email')}")
            print(f"   Auth Method: {data2.get('auth_method')}")
    else:
        print(f"   ERROR: {response.text}")
except Exception as e:
    print(f"   ERROR: {e}")

# 4. Test logout
print("\n4. Testing /api/auth/logout")
try:
    response = requests.post(
        f"{BASE_URL}/api/auth/logout",
        cookies={"session_id": session_id} if 'session_id' in locals() else {}
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   ERROR: {e}")

print("\n" + "=" * 50)
print("Login system tests complete!")
