"""Test AI owner search by simulating what the frontend does."""
import requests

# Step 1: Fetch projects (like the frontend does)
print("Step 1: Fetching projects from API...")
projects_resp = requests.get('http://localhost:8001/api/projects')
projects = projects_resp.json()
print(f"  Got {len(projects)} projects")

# Step 2: Show owner values
print("\nStep 2: Sample owner values from fetched projects:")
owners_seen = set()
for p in projects[:50]:
    owner = p.get('owner', '')
    if owner and owner not in owners_seen:
        owners_seen.add(owner)
        print(f"  - {owner}")
        if len(owners_seen) >= 5:
            break

# Check if Jorden Huff is in the data
print("\nStep 3: Looking for 'Jorden' in owner field...")
jorden_projects = [p for p in projects if 'jorden' in (p.get('owner') or '').lower()]
print(f"  Found {len(jorden_projects)} projects owned by Jorden")
for p in jorden_projects[:5]:
    print(f"    - {p.get('title')[:60]} | Owner: {p.get('owner')}")

# Step 4: Test AI query WITH projects
print("\nStep 4: Sending AI query with project context...")
# Prepare context like frontend does
project_list = []
for p in projects:
    project_list.append({
        'project_id': p.get('project_id'),
        'title': p.get('title'),
        'project_source': p.get('project_source'),
        'division': p.get('division'),
        'phase': p.get('phase'),
        'wm_week': p.get('wm_week'),
        'region': p.get('region'),
        'market': p.get('market'),
        'Owner': p.get('owner', ''),  # Uppercase
        'owner': p.get('owner', '')   # Lowercase
    })

payload = {
    "query": "projects owned by Jorden Huff",
    "context": {
        "total_projects": len(projects),
        "all_projects": project_list
    }
}

ai_resp = requests.post('http://localhost:8001/api/ai/query', json=payload)
ai_result = ai_resp.json()
print(f"  AI Response:\n{ai_result['answer']}")
