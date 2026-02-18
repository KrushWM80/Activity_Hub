"""Test to see what GMD projects are in the database and what the AI sees"""
from database import DatabaseService
from models import FilterCriteria, ProjectStatus
import asyncio

async def main():
    db = DatabaseService()
    
    # Get all active projects
    filters = FilterCriteria()
    filters.status = ProjectStatus.ACTIVE
    
    projects = await db.get_projects(filters, include_location=False)
    
    print(f"Total projects returned: {len(projects)}")
    
    # Find all GMD projects
    gmd_projects = [p for p in projects if 'gmd' in p.title.lower()]
    
    print(f"\nGMD projects found: {len(gmd_projects)}")
    
    # Get unique titles
    unique_gmd_titles = set([p.title for p in gmd_projects])
    print(f"Unique GMD project titles: {len(unique_gmd_titles)}")
    
    print("\nUnique GMD titles:")
    for title in sorted(unique_gmd_titles):
        count = len([p for p in gmd_projects if p.title == title])
        print(f"  - {title} ({count} stores)")

if __name__ == "__main__":
    asyncio.run(main())
