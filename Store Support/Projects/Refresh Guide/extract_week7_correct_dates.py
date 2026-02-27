#!/usr/bin/env python3
"""
Extract cumulative Week 7 (through 2026-02-21) engagement metrics from BigQuery
"""

from google.cloud import bigquery

client = bigquery.Client(project='athena-gateway-prod')

print("\n" + "="*80)
print("EXTRACTING WEEK 7 CUMULATIVE ENGAGEMENT METRICS")
print("Date Range: Through 2026-02-21 (Week 7 end)")
print("="*80 + "\n")

# Query cumulative metrics through Week 7 end date
query = """
SELECT 
    COUNT(DISTINCT assignedTo) as workers,
    COUNT(DISTINCT assignedBy) as managers,
    COUNT(CASE WHEN status = 'Assigned' THEN 1 END) as assigned_count,
    COUNT(CASE WHEN status = 'Completed' THEN 1 END) as completed_count,
    COUNT(*) as total_actions
FROM `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE exportDate <= '2026-02-21'
"""

try:
    print("Query: Cumulative Week 1-7 Engagement (through 2026-02-21)")
    print("-" * 80)
    
    results = client.query(query).result()
    
    for row in results:
        workers = row.workers
        managers = row.managers
        assigned_count = row.assigned_count
        completed_count = row.completed_count
        total_actions = row.total_actions
        
        total_users = workers + managers
        total_assignments = assigned_count + completed_count
        actions_per_user = total_actions / total_users if total_users > 0 else 0
        
        print(f"  Workers (distinct assignedTo):    {workers:,}")
        print(f"  Managers (distinct assignedBy):   {managers:,}")
        print(f"  Total Users:                      {total_users:,}")
        print(f"  Assigned Count:                   {assigned_count:,}")
        print(f"  Completed Count:                  {completed_count:,}")
        print(f"  Total Assignments:                {total_assignments:,}")
        print(f"  Total Actions (all records):      {total_actions:,}")
        print(f"  Actions per User:                 {actions_per_user:.1f}")
        print()
        
        print("=" * 80)
        print("WEEK 7 DASHBOARD VALUES (Cumulative through 2026-02-21)")
        print("=" * 80)
        print()
        print(f"""
UPDATE VALUES FOR userEngagement:
  "workers": {workers},
  "managers": {managers},
  "totalUsers": {total_users},
  "assignments": {total_assignments},
  "completions": {completed_count},
  "totalActions": {total_actions},
  "actionsPerUser": {actions_per_user:.1f}
""")
        print("=" * 80)
        print()
        
except Exception as e:
    print(f"ERROR: {e}\n")
    import traceback
    traceback.print_exc()

print("Query complete.")
