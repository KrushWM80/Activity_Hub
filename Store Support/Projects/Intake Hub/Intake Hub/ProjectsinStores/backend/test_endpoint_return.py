import sys
import asyncio
sys.path.insert(0, '/c/Users/krush/Documents/VSCode/Intake Hub/ProjectsinStores/backend')

from main import get_filter_options, sqlite_cache

async def test():
    print(f"Cache valid: {sqlite_cache.is_cache_valid()}")
    result = await get_filter_options()
    print(f"Endpoint returned type: {type(result)}")
    print(f"Endpoint returned keys: {sorted(list(result.keys()) if isinstance(result, dict) else result.model_dump().keys())}")
    print(f"Total fields: {len(result.keys()) if isinstance(result, dict) else len(result.model_dump())}")
    
    if isinstance(result, dict):
        for key in sorted(result.keys()):
            count = len(result[key]) if result[key] else 0
            print(f"  {key}: {count} items")

asyncio.run(test())
