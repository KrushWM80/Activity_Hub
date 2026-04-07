#!/usr/bin/env python3
"""Test cache.get_job_codes() directly"""
import sys
sys.path.insert(0, '.')

from sqlite_cache import get_cache

cache = get_cache()
job_codes = cache.get_job_codes()

print(f"Total job codes returned: {len(job_codes)}")
if len(job_codes) > 0:
    print(f"\nFirst job code:")
    for key, value in list(job_codes[0].items())[:5]:
        print(f"  {key}: {value}")
else:
    print("ERROR: No job codes returned!")
