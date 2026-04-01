#!/usr/bin/env python3
import requests
import json
import time

time.sleep(3)  # Give server time to start

try:
    print("\n" + "="*70)
    print("TESTING JOB CODES LOOKUP ENDPOINT")
    print("="*70)
    
    # Login
    print("\n[1] Logging in...")
    login_resp = requests.post(
        "http://10.97.114.181:8080/api/login",
        json={"username": "admin", "password": "admin123"},
        timeout=5
    )
    print(f"    Status: {login_resp.status_code}")
    
    if login_resp.status_code != 200:
        print(f"    Error: {login_resp.text[:200]}")
        exit(1)
    
    # Test lookup
    print("\n[2] Querying for job code 30-49-855 (pay types H, S)...")
    lookup_resp = requests.post(
        "http://10.97.114.181:8080/api/job-codes/lookup",
        json={"job_code": "30-49-855", "pay_types": ["H", "S"]},
        timeout=10,
        cookies=login_resp.cookies
    )
    
    print(f"    Status: {lookup_resp.status_code}")
    
    if lookup_resp.status_code == 200:
        data = lookup_resp.json()
        emp_count = data.get('employee_count', 0)
        print(f"\n✅ SUCCESS!")
        print(f"    Job Code: {data.get('job_code')}")
        print(f"    Employees Found: {emp_count}")
        
        if data.get('workers'):
            print(f"\n    First 5 Employees:")
            for worker in data.get('workers', [])[:5]:
                print(f"      - ID {worker.get('worker_id')}: {worker.get('first_name')} {worker.get('last_name')} ({worker.get('worker_payment_type')})")
        
        print("\n✅ JOB CODES DASHBOARD IS FULLY OPERATIONAL!")
        print("="*70)
        print(f"Access the dashboard at: http://10.97.114.181:8080/static/index.html#")
        print("="*70 + "\n")
        
    else:
        print(f"\n❌ Lookup failed:")
        print(f"    Response: {lookup_resp.text[:500]}")
        
except requests.exceptions.ConnectionError as e:
    print(f"\n❌ Server not responding: {e}")
except requests.exceptions.Timeout:
    print(f"\n❌ Request timeout")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

