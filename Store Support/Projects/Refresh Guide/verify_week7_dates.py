#!/usr/bin/env python3
"""
Verify BigQuery data availability - check Week 7 date range (2/15-2/21)
"""

from google.cloud import bigquery
from datetime import datetime, timedelta

client = bigquery.Client(project='athena-gateway-prod')

print("\n" + "="*80)
print("VERIFYING BIGQUERY DATA AVAILABILITY FOR WEEK 7")
print("Week 7 Date Range: 2026-02-15 to 2026-02-21")
print("="*80 + "\n")

# Check overall data range
print("STEP 1: Overall Data Range in BigQuery")
print("-" * 80)

range_query = """
SELECT 
    MIN(exportDate) as earliest_date,
    MAX(exportDate) as latest_date
FROM `athena-gateway-prod.store_refresh.store_refresh_data`
"""

try:
    results = client.query(range_query).result()
    for row in results:
        print(f"Earliest date in ALL data: {row.earliest_date}")
        print(f"Latest date in ALL data:   {row.latest_date}")
except Exception as e:
    print(f"ERROR: {e}")

print()
print("STEP 2: Data Availability for Week 7 Dates (2026-02-15 to 2026-02-21)")
print("-" * 80)

# Check each day in Week 7
week7_query = """
SELECT 
    exportDate,
    COUNT(*) as record_count,
    COUNT(DISTINCT assignedTo) as workers,
    COUNT(DISTINCT assignedBy) as managers
FROM `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE exportDate BETWEEN '2026-02-15' AND '2026-02-21'
GROUP BY exportDate
ORDER BY exportDate
"""

try:
    results = client.query(week7_query).result()
    
    rows = list(results)
    
    if len(rows) == 0:
        print("❌ NO DATA FOUND FOR WEEK 7 (2026-02-15 to 2026-02-21)")
    else:
        print(f"{'Date':<15} {'Records':<15} {'Workers':<15} {'Managers':<15}")
        print("-" * 60)
        for row in rows:
            print(f"{str(row.exportDate):<15} {row.record_count:>14,} {row.workers:>14,} {row.managers:>14,}")
        
        print()
        print(f"✓ Found {len(rows)} days with data in Week 7 date range")
        
        first_date = rows[0].exportDate if rows else None
        print(f"✓ First available date: {first_date}")
        
        if first_date > datetime(2026, 2, 15).date():
            missing_days = (first_date - datetime(2026, 2, 15).date()).days
            print(f"⚠️  Missing {missing_days} day(s) at start of Week 7:")
            current = datetime(2026, 2, 15).date()
            while current < first_date:
                print(f"    {current} - NO DATA")
                current += timedelta(days=1)
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

print()
print("STEP 3: Check if 2/15 and 2/16 exist in data")
print("-" * 80)

specific_query = """
SELECT COUNT(*) as record_count
FROM `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE exportDate IN ('2026-02-15', '2026-02-16')
"""

try:
    results = client.query(specific_query).result()
    for row in results:
        if row.record_count == 0:
            print("❌ Confirmed: 2026-02-15 and 2026-02-16 have NO records")
        else:
            print(f"✓ Found {row.record_count:,} records for 2026-02-15 or 2026-02-16")
except Exception as e:
    print(f"ERROR: {e}")

print()
print("="*80)
