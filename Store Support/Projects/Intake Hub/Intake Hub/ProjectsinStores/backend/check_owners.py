"""Check if Jorden Huff is in the API response."""
import requests

# Fetch all projects
resp = requests.get('http://localhost:8001/api/projects')
projects = resp.json()
print(f"Total projects: {len(projects)}")

# Find all unique owners
owners = set()
for p in projects:
    owner = p.get('owner', '')
    if owner:
        owners.add(owner)

print(f"Unique owners: {len(owners)}")

# Look for Jorden
print("\nLooking for 'Jorden' in owners...")
jordan_owners = [o for o in sorted(owners) if 'jorden' in o.lower()]
print(f"Found: {jordan_owners}")

# Look for 'Huff'
print("\nLooking for 'Huff' in owners...")
huff_owners = [o for o in sorted(owners) if 'huff' in o.lower()]
print(f"Found: {huff_owners}")

# Show all owners for debugging
print("\nAll unique owners (first 30):")
for i, o in enumerate(sorted(owners)[:30]):
    print(f"  {i+1}. {o}")
