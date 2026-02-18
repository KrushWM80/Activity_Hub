import requests

# Simulate what the frontend will do
print("Simulating frontend filter for Crystal Souders...\n")

# Build params like the frontend does
params = {
    'owner': 'Crystal Souders',
    'limit': '2000'
}

r = requests.get('http://127.0.0.1:8001/api/projects', params=params, timeout=15)
projects = r.json()

print(f"✓ Backend returned {len(projects)} projects")
print(f"✓ All have correct owner: {all(p.get('owner') == 'Crystal Souders' for p in projects)}")

# Group by project title to see unique projects
titles = {}
for p in projects:
    title = p['title']
    if title not in titles:
        titles[title] = []
    titles[title].append(p)

print(f"✓ {len(titles)} unique project titles")
print(f"\nTop 5 projects:")
for title in list(titles.keys())[:5]:
    count = len(titles[title])
    print(f"  - {title[:60]} ({count} stores)")
