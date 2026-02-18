#!/usr/bin/env python3
from database import DatabaseService

db = DatabaseService()
filters = db.get_filter_options()

print(f"Markets: {filters['markets'][:15]}")
print(f"Total markets: {len(filters['markets'])}")
print(f"\nStores (first 15): {filters['stores'][:15]}")
print(f"Total stores: {len(filters['stores'])}")
print(f"\nRegions: {filters['regions']}")
print(f"Divisions: {filters['divisions']}")
