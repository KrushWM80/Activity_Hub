#!/usr/bin/env python3
"""
Quick test to check how many unique project titles exist in the database
"""
import asyncio
from database import DatabaseService, FilterCriteria, ProjectStatus

async def main():
    # Initialize the database service (connects to BigQuery)
    db = DatabaseService()
    
    # Create default filters (same as what the frontend uses)
    filters = FilterCriteria()
    filters.status = ProjectStatus.ACTIVE
    
    # Get all projects with default filters
    projects = await db.get_projects(filters)
    
    print(f"Total project records returned: {len(projects)}")
    
    # Get unique titles
    unique_titles = set()
    for p in projects:
        if p.title:
            unique_titles.add(p.title)
    
    print(f"Unique project titles: {len(unique_titles)}")
    print("\nAll unique titles:")
    for i, title in enumerate(sorted(unique_titles), 1):
        # Count how many records have this title
        count = sum(1 for p in projects if p.title == title)
        print(f"  {i}. {title} ({count} store assignments)")

if __name__ == "__main__":
    asyncio.run(main())
