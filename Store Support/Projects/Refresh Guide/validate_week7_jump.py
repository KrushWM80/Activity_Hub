#!/usr/bin/env python3
"""
Validate Week 7 engagement jump by checking each week's distinct values
"""

from google.cloud import bigquery

client = bigquery.Client(project='athena-gateway-prod')

print("\n" + "="*80)
print("VALIDATING WEEK 7 ENGAGEMENT DATA JUMP")
print("="*80 + "\n")

# Query distinct workers/managers for EACH WEEK
query = """
SELECT
    exportDate,
    COUNT(DISTINCT assignedTo) as distinct_workers,
    COUNT(DISTINCT assignedBy) as distinct_managers,
    COUNT(*) as total_records
FROM `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE exportDate IN ('2026-01-17', '2026-01-24', '2026-01-31', '2026-02-07', '2026-02-14', '2026-02-21', '2026-02-23')
GROUP BY exportDate
ORDER BY exportDate
"""

print("Week-by-Week Distinct Counts from BigQuery:")
print("-" * 80)

try:
    job = client.query(query)
    results = job.result()
    
    weekly_data = {}
    for row in results:
        date = str(row.exportDate)
        workers = row.distinct_workers
        managers = row.distinct_managers
        records = row.total_records
        weekly_data[date] = {
            'workers': workers,
            'managers': managers,
            'records': records
        }
        print(f"{date}: Workers={workers:,} | Managers={managers:,} | Records={records:,}")
    
    print("\n" + "-"*80)
    print("Week-over-Week INCREASES (NEW distinct values per week):")
    print("-" * 80)
    
    dates_sorted = sorted(weekly_data.keys())
    for i in range(1, len(dates_sorted)):
        prev_date = dates_sorted[i-1]
        curr_date = dates_sorted[i]
        
        prev_workers = weekly_data[prev_date]['workers']
        curr_workers = weekly_data[curr_date]['workers']
        worker_increase = curr_workers - prev_workers
        
        prev_managers = weekly_data[prev_date]['managers']
        curr_managers = weekly_data[curr_date]['managers']
        manager_increase = curr_managers - prev_managers
        
        prev_records = weekly_data[prev_date]['records']
        curr_records = weekly_data[curr_date]['records']
        record_increase = curr_records - prev_records
        
        week_num = i + 1
        print(f"\nWeek {week_num} ({curr_date}):")
        print(f"  Workers:  {prev_workers:,} → {curr_workers:,} (increase: +{worker_increase:,})")
        print(f"  Managers: {prev_managers:,} → {curr_managers:,} (increase: +{manager_increase:,})")
        print(f"  Records:  {prev_records:,} → {curr_records:,} (increase: +{record_increase:,})")
        
except Exception as e:
    print(f"ERROR: {e}\n")

print("\n" + "="*80 + "\n")
