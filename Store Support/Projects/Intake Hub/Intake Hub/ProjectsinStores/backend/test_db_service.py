import sys
import asyncio
sys.path.insert(0, '/c/Users/krush/Documents/VSCode/Intake Hub/ProjectsinStores/backend')

from database import DatabaseService

async def test():
    service = DatabaseService()
    result = await service.get_filter_options()
    print(f"Result fields: {sorted(list(result.keys()))}")
    print(f"Result count: {len(result)}")
    for field in sorted(result.keys()):
        count = len(result.get(field, []))
        print(f"  {field}: {count} items")

asyncio.run(test())
