#!/usr/bin/env python3
import requests, time, json

print("Testing /api/filters endpoint...")
start = time.time()

try:
    r = requests.get('http://127.0.0.1:8001/api/filters', timeout=120)
    elapsed = time.time() - start
    
    data = r.json()
    
    print(f"\nResponse time: {elapsed:.1f}s")
    print(f"HTTP Status: {r.status_code}")
    print(f"Filter count: {len(data)}")
    print("\nFilters returned:")
    
    for key in sorted(data.keys()):
        count = len(data[key])
        print(f"  {key}: {count} values")
    
    print("\n" + "="*50)
    if len(data) == 16:
        print("SUCCESS: All 16 fields returned!")
        if 'owners' in data and len(data['owners']) > 0:
            print(f"✓ Owners field has {len(data['owners'])} values")
    else:
        print(f"FAILURE: Expected 16 fields, got {len(data)}")
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
