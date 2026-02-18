# Test the API endpoints
# Run this script to verify the backend is working correctly

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health check endpoint"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_summary():
    """Test summary endpoint"""
    print("Testing summary endpoint...")
    response = requests.get(f"{BASE_URL}/api/summary")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total Projects: {data['total_active_projects']}")
    print(f"Total Stores: {data['total_stores']}")
    print(f"Intake Hub: {data['intake_hub_projects']} projects, {data['intake_hub_stores']} stores")
    print(f"Realty: {data['realty_projects']} projects, {data['realty_stores']} stores")
    print()

def test_projects():
    """Test projects endpoint"""
    print("Testing projects endpoint...")
    response = requests.get(f"{BASE_URL}/api/projects", params={"status": "Active"})
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Number of projects: {len(data)}")
    if data:
        print(f"First project: {data[0]['project_id']} - {data[0]['title']}")
    print()

def test_filters():
    """Test filters endpoint"""
    print("Testing filters endpoint...")
    response = requests.get(f"{BASE_URL}/api/filters")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Divisions: {data['divisions']}")
    print(f"Phases: {data['phases']}")
    print(f"Number of tribes: {len(data['tribes'])}")
    print()

def test_store_counts():
    """Test store counts endpoint"""
    print("Testing store counts endpoint...")
    response = requests.get(f"{BASE_URL}/api/store-counts", params={"group_by": "division"})
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Group by: {data['group_by']}")
    print(f"Number of groups: {len(data['counts'])}")
    print()

def test_ai_query():
    """Test AI query endpoint"""
    print("Testing AI query endpoint...")
    response = requests.post(
        f"{BASE_URL}/api/ai/query",
        json={
            "query": "How many projects are there in total?",
            "context": {"summary": {}}
        }
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Query: {data['query']}")
    print(f"Answer: {data['answer']}")
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("Projects in Stores Dashboard - API Test Script")
    print("=" * 60)
    print()
    
    try:
        test_health()
        test_summary()
        test_projects()
        test_filters()
        test_store_counts()
        test_ai_query()
        
        print("=" * 60)
        print("✅ All tests completed successfully!")
        print("=" * 60)
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API server.")
        print("Make sure the backend is running at http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")
