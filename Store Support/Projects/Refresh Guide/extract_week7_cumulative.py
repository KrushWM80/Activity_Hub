#!/usr/bin/env python3
"""
Extract CUMULATIVE Week 1-7 (through 2026-02-23) User Engagement Metrics from BigQuery
"""

from google.cloud import bigquery

client = bigquery.Client(project='athena-gateway-prod')

print("\n" + "="*80)
print("EXTRACTING CUMULATIVE WEEK 1-7 USER ENGAGEMENT METRICS")
print("Date Range: Through 2026-02-23")
print("="*80 + "\n")

THROUGH_DATE = '2026-02-23'

# Query 1: Cumulative workers and managers (through Week 7)
query1 = f"""
SELECT
    COUNT(DISTINCT assignedTo) as workers,
    COUNT(DISTINCT assignedBy) as managers
FROM `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE exportDate <= '{THROUGH_DATE}'
"""

# Query 2: Cumulative assignment counts (through Week 7)
query2 = f"""
SELECT
    COUNT(*) as totalRecords,
    COUNT(CASE WHEN status = 'Assigned' THEN 1 ELSE 0 END) as assignedItems,
    COUNT(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completedItems,
    COUNT(CASE WHEN status IN ('Assigned', 'Completed') THEN 1 ELSE 0 END) as totalAssignments
FROM `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE exportDate <= '{THROUGH_DATE}'
"""

print("Query 1: Cumulative Workers and Managers (Week 1-7)")
print("-" * 80)

workers = 0
managers = 0

try:
    job1 = client.query(query1)
    results1 = job1.result()
    for row in results1:
        workers = row.workers
        managers = row.managers
    print(f"  Workers (assignedTo distinct):   {workers:,}")
    print(f"  Managers (assignedBy distinct):  {managers:,}")
    print()
except Exception as e:
    print(f"ERROR: {e}\n")

print("Query 2: Cumulative Assignment Counts (Week 1-7)")
print("-" * 80)

total_records = 0
assigned_items = 0
completed_items = 0
total_assignments = 0

try:
    job2 = client.query(query2)
    results2 = job2.result()
    for row in results2:
        total_records = row.totalRecords
        assigned_items = row.assignedItems
        completed_items = row.completedItems
        total_assignments = row.totalAssignments
    print(f"  Total Records:                   {total_records:,}")
    print(f"  Assigned Items (count):          {assigned_items:,}")
    print(f"  Completed Items (count):         {completed_items:,}")
    print(f"  Total Assignments (Assigned+Comp): {total_assignments:,}")
    print()
except Exception as e:
    print(f"ERROR: {e}\n")

# Calculate derived metrics
total_users = workers + managers
total_actions = total_records if total_records > 0 else (assigned_items + completed_items)
actions_per_user = (total_actions / total_users) if total_users > 0 else 0

print("\n" + "="*80)
print("CUMULATIVE WEEK 1-7 USER ENGAGEMENT SUMMARY")
print("="*80)
print(f"""
workers:        {workers:,}
managers:       {managers:,}
totalUsers:     {total_users:,}
assignments:    {total_assignments:,}
completions:    {completed_items:,}
totalActions:   {total_actions:,}
actionsPerUser: {actions_per_user:.1f}
""")

print("="*80)
print("COMPARISON WITH WEEK 6")
print("="*80)
print(f"""
Week 6 (from dashboard):
  workers:        113,500
  managers:       72,000
  totalUsers:     185,500
  assignments:    1,560,000
  completions:    1,100,127
  totalActions:   2,660,127
  actionsPerUser: 14.3

Week 7 Cumulative (calculated):
  workers:        {workers:,}
  managers:       {managers:,}
  totalUsers:     {total_users:,}
  assignments:    {total_assignments:,}
  completions:    {completed_items:,}
  totalActions:   {total_actions:,}
  actionsPerUser: {actions_per_user:.1f}
""")

print("="*80)
print("WEEK 7 DASHBOARD UPDATE VALUES")
print("="*80)
print(f"""
"userEngagement": {{
  "workers": {workers},
  "managers": {managers},
  "totalUsers": {total_users},
  "assignments": {total_assignments},
  "completions": {completed_items},
  "totalActions": {total_actions},
  "actionsPerUser": {actions_per_user:.1f}
}}
""")
print("="*80 + "\n")
