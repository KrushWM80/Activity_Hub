import sys
import asyncio
sys.path.insert(0, '/c/Users/krush/Documents/VSCode/Intake Hub/ProjectsinStores/backend')

from main import get_filter_options

async def test():
    result = await get_filter_options()
    print(f"Function returned type: {type(result)}")
    if isinstance(result, dict):
        print(f"Dict keys: {sorted(list(result.keys()))}")
        print(f"Dict size: {len(result)}")
    else:
        print(f"Not a dict, fields: {result}")

asyncio.run(test())
