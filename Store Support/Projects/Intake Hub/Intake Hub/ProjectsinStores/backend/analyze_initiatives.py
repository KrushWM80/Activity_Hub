import requests

print("Investigating Store 1 Realty Project Structure")
print("=" * 70)

# Get all Store 1 Realty projects
r = requests.get('http://127.0.0.1:8001/api/projects?store=1&project_source=Realty&limit=1000', timeout=15)
projects = r.json()

print(f"Total rows returned: {len(projects)}")
print()

# Analyze the structure
project_ids = set()
titles = set()
project_title_combos = {}

for p in projects:
    pid = p['project_id']
    title = p['title']
    project_ids.add(pid)
    titles.add(title)
    
    if pid not in project_title_combos:
        project_title_combos[pid] = set()
    project_title_combos[pid].add(title)

print(f"Unique Project IDs: {len(project_ids)}")
print(f"Unique Titles (Initiatives): {len(titles)}")
print()

print("How initiatives map to projects:")
for pid, initiative_titles in sorted(project_title_combos.items()):
    print(f"\nProject ID: {pid}")
    print(f"  Initiatives: {len(initiative_titles)}")
    for title in sorted(initiative_titles):
        count = sum(1 for p in projects if p['project_id'] == pid and p['title'] == title)
        print(f"    - {title} ({count} rows)")

# Show sample data
print("\n" + "=" * 70)
print("Sample rows for analysis:")
for p in projects[:5]:
    print(f"  ID: {p['project_id']} | Title: {p['title'][:50]} | Phase: {p['phase']} | Week: {p['wm_week']}")
