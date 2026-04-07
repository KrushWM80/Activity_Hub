"""Test API response for Realty projects"""
import requests
import json

url = "http://localhost:8001/api/projects"
params = {
    "project_source": "Realty",
    "limit": 100
}

try:
    resp = requests.get(url, params=params, timeout=5)
    print(f"Status: {resp.status_code}")
    
    if resp.status_code == 200:
        data = resp.json()
        if 'result' in data:
            results = data['result']
            print(f"Count: {len(results)}")
            
            if results:
                print(f"\nFirst record:")
                for key in list(results[0].keys())[:5]:
                    print(f"  {key}: {results[0][key]}")
        else:
            print(f"Response keys: {list(data.keys())}")
    else:
        print(f"Error: {resp.text[:200]}")
        
except requests.exceptions.ConnectionError:
    print("❌ Could not connect to http://localhost:8001")
except Exception as e:
    print(f"❌ Error: {e}")
