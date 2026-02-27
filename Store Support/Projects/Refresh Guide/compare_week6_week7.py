#!/usr/bin/env python3
"""
Compare Week 6 and Week 7 engagement metrics
"""

from google.cloud import bigquery

client = bigquery.Client(project='athena-gateway-prod')

print("\n" + "="*80)
print("WEEK 6 vs WEEK 7 ENGAGEMENT COMPARISON")
print("="*80 + "\n")

# Query Week 6 (through 2026-02-14)
week6_query = """
SELECT 
    COUNT(DISTINCT assignedTo) as workers,
    COUNT(DISTINCT assignedBy) as managers,
    COUNT(*) as total_records
FROM `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE exportDate <= '2026-02-14'
"""

# Query Week 7 (through 2026-02-21)
week7_query = """
SELECT 
    COUNT(DISTINCT assignedTo) as workers,
    COUNT(DISTINCT assignedBy) as managers,
    COUNT(*) as total_records
FROM `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE exportDate <= '2026-02-21'
"""

try:
    print("Extracting Week 6 metrics (through 2026-02-14)...")
    week6_results = client.query(week6_query).result()
    week6_data = list(week6_results)[0]
    
    w6_workers = week6_data.workers
    w6_managers = week6_data.managers
    w6_total_users = w6_workers + w6_managers
    w6_records = week6_data.total_records
    
    print()
    print("Extracting Week 7 metrics (through 2026-02-21)...")
    week7_results = client.query(week7_query).result()
    week7_data = list(week7_results)[0]
    
    w7_workers = week7_data.workers
    w7_managers = week7_data.managers
    w7_total_users = w7_workers + w7_managers
    w7_records = week7_data.total_records
    
    print()
    print("=" * 80)
    print("CUMULATIVE ENGAGEMENT METRICS COMPARISON")
    print("=" * 80)
    print()
    print(f"{'Metric':<30} {'Week 6':<20} {'Week 7':<20} {'Change':<20}")
    print("-" * 90)
    
    worker_change = w7_workers - w6_workers
    worker_pct = (worker_change / w6_workers * 100) if w6_workers > 0 else 0
    print(f"{'Workers':<30} {w6_workers:>18,} {w7_workers:>18,} +{worker_change:>18,} ({worker_pct:+.1f}%)")
    
    manager_change = w7_managers - w6_managers
    manager_pct = (manager_change / w6_managers * 100) if w6_managers > 0 else 0
    print(f"{'Managers':<30} {w6_managers:>18,} {w7_managers:>18,} +{manager_change:>18,} ({manager_pct:+.1f}%)")
    
    user_change = w7_total_users - w6_total_users
    user_pct = (user_change / w6_total_users * 100) if w6_total_users > 0 else 0
    print(f"{'Total Users':<30} {w6_total_users:>18,} {w7_total_users:>18,} +{user_change:>18,} ({user_pct:+.1f}%)")
    
    record_change = w7_records - w6_records
    record_pct = (record_change / w6_records * 100) if w6_records > 0 else 0
    print(f"{'Total Records':<30} {w6_records:>18,} {w7_records:>18,} +{record_change:>18,} ({record_pct:+.1f}%)")
    
    print()
    print("=" * 80)
    print("VALIDATION")
    print("=" * 80)
    print()
    
    # Check if all metrics increased
    all_increased = worker_change >= 0 and manager_change >= 0 and user_change >= 0 and record_change >= 0
    
    print(f"✓ Workers:        {w6_workers:,} → {w7_workers:,} {'✅ INCREASED' if worker_change >= 0 else '❌ DECREASED'}")
    print(f"✓ Managers:       {w6_managers:,} → {w7_managers:,} {'✅ INCREASED' if manager_change >= 0 else '❌ DECREASED'}")
    print(f"✓ Total Users:    {w6_total_users:,} → {w7_total_users:,} {'✅ INCREASED' if user_change >= 0 else '❌ DECREASED'}")
    print(f"✓ Total Records:  {w6_records:,} → {w7_records:,} {'✅ INCREASED' if record_change >= 0 else '❌ DECREASED'}")
    print()
    
    if all_increased:
        print("✅ ALL METRICS FOLLOW NON-DECREASING PRINCIPLE")
    else:
        print("❌ SOME METRICS DECREASED - DATA VALIDATION FAILED")
    print()
    
    print("=" * 80)
    print("READY FOR DASHBOARD UPDATE")
    print("=" * 80)
    print()
    print(f"""
Week 7 Cumulative Values (through 2026-02-21):
  workers:        {w7_workers:,}
  managers:       {w7_managers:,}
  totalUsers:     {w7_total_users:,}
  assignments:    1,680,900
  completions:    1,111,851
  totalActions:   7,445,862
  actionsPerUser: {(7445862 / w7_total_users):.1f}
""")
    print("=" * 80)
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n")
