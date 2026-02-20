#!/usr/bin/env python3
"""Test partner filter implementation"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from database import DatabaseService
from models import FilterCriteria

# Create database service
db = DatabaseService()

# Test 1: Regular query (should work)
print("Test 1: Regular query without partner filter...")
filters = FilterCriteria()
filters.status = None
try:
    result = db.get_projects(filters, limit=3)
    print(f"✓ Regular query returned {len(result)} projects")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Partner filter query
print("\nTest 2: Partner filter query...")
filters_with_partner = FilterCriteria()
filters_with_partner.status = None
filters_with_partner.partners = ["Intake & Test"]
try:
    result = db.get_projects(filters_with_partner, limit=10)
    print(f"✓ Partner filter returned {len(result)} projects")
    if result:
        print(f"  First project: {result[0].title}")
        print(f"  Partner: {result[0].partner}")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
