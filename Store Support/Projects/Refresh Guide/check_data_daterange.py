#!/usr/bin/env python3
"""
Check data date range in BigQuery
"""

from google.cloud import bigquery

client = bigquery.Client(project='athena-gateway-prod')

print("\n" + "="*80)
print("CHECKING DATA DATE RANGE")
print("="*80 + "\n")

date_query = """
SELECT 
    MIN(exportDate) as earliest_date,
    MAX(exportDate) as latest_date,
    COUNT(DISTINCT exportDate) as unique_dates,
    COUNT(*) as total_records
FROM `athena-gateway-prod.store_refresh.store_refresh_data`
"""

try:
    results = client.query(date_query).result()
    
    for row in results:
        print(f"Data Date Range:")
        print(f"  Earliest: {row.earliest_date}")
        print(f"  Latest:   {row.latest_date}")
        print(f"  Unique dates: {row.unique_dates}")
        print(f"  Total records: {row.total_records:,}")
        print()
        
except Exception as e:
    print(f"ERROR: {e}")

print("="*80)
print("\nChecking records PER DATE (sample)")
print("=" * 80)
print()

per_date_query = """
SELECT 
    exportDate,
    COUNT(DISTINCT assignedTo) as workers,
    COUNT(DISTINCT assignedBy) as managers,
    COUNT(*) as records
FROM `athena-gateway-prod.store_refresh.store_refresh_data`
GROUP BY exportDate
ORDER BY exportDate
LIMIT 20
"""

try:
    results = client.query(per_date_query).result()
    
    print(f"{'Date':<15} {'Workers':<15} {'Managers':<15} {'Records':<15}")
    print("-" * 60)
    
    for row in results:
        print(f"{str(row.exportDate):<15} {row.workers:>14,} {row.managers:>14,} {row.records:>14,}")
    
except Exception as e:
    print(f"ERROR: {e}")

print()
