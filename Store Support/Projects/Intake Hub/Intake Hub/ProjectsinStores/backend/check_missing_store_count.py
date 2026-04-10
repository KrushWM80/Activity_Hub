import sqlite3

# Connect to the cache database
conn = sqlite3.connect('projects_cache.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("Checking for projects with zero or minimal store count...\n")

# Query the raw data to understand structure
print("Sample project data:")
cursor.execute("SELECT project_id, title, project_source, store, facility FROM projects LIMIT 3")
samples = cursor.fetchall()
for row in samples:
    print(f"  Project: {row['title']}")
    print(f"    Store: '{row['store']}' | Facility: '{row['facility']}'")

# Check which projects have '0' as store value (which might indicate no stores)
print("\n\nProjects with store='0' (potentially no stores):")
cursor.execute("""
    SELECT 
        project_id,
        intake_card,
        title,
        project_source,
        store,
        facility,
        COUNT(DISTINCT facility) as distinct_facilities
    FROM projects
    WHERE store = '0'
    GROUP BY project_id
    ORDER BY project_source, title
""")

results = cursor.fetchall()
if results:
    print(f"Found {len(results)} projects with store='0':\n")
    
    for row in results:
        print(f"  • {row['title']}")
        print(f"    ID: {row['intake_card']} | Source: {row['project_source']}")
        print(f"    Store: '{row['store']}' | Facility: '{row['facility']}'")
        print(f"    Distinct Facilities Count: {row['distinct_facilities']}")
        print()
else:
    print("No projects with store='0' found.")

conn.close()
