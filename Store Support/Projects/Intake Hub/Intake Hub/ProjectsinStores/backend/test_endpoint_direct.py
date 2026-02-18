#!/usr/bin/env python3
"""Test endpoint function directly"""
import asyncio
from main import get_filter_options, sqlite_cache

async def test():
    print("Testing get_filter_options() function directly...\n")
    
    print(f"Cache valid: {sqlite_cache.is_cache_valid()}")
    print(f"Cache record count: {sqlite_cache.get_record_count()}")
    
    result = await get_filter_options()
    
    print(f"\nResult type: {type(result)}")
    print(f"Result has {len(result.model_dump())} fields")
    print("Fields:", sorted(result.model_dump().keys()))
    
    if result.owners:
        print(f"\n✓ Owners returned: {len(result.owners)} values")
    else:
        print("\n✗ Owners is empty")

asyncio.run(test())
