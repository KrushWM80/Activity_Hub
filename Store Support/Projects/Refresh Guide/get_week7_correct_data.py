#!/usr/bin/env python3
"""
Query correct Week 7 data from BigQuery
Week 7: 2/23/26 - 2/28/26
"""

from google.cloud import bigquery
from datetime import datetime, timedelta

client = bigquery.Client(project='athena-gateway-prod')

# Week 7 date range
week7_start = '2026-02-23'
week7_end = '2026-02-28'

print("=" * 80)
print("QUERYING WEEK 7 DATA FROM BIGQUERY")
print("=" * 80)
print(f"\nWeek 7 Period: {week7_start} to {week7_end}\n")

# Query 1: Overall Summary Metrics
summary_query = f"""
SELECT
  COUNT(DISTINCT businessUnitNumber) as unique_bus_units,
  COUNT(*) as total_rows,
  COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as completed_count,
  COUNT(CASE WHEN status != 'UnAssigned' THEN 1 END) as assigned_count,
  COUNT(CASE WHEN status = 'PENDING' THEN 1 END) as pending_count,
  COUNT(CASE WHEN status = 'UnAssigned' THEN 1 END) as unassigned_count
FROM `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE exportDate BETWEEN '{week7_start}' AND '{week7_end}'
"""

print("Query 1: Overall Summary")
print("-" * 80)
result = client.query(summary_query).result()
for row in result:
    print(f"Unique Business Units: {row.unique_bus_units}")
    print(f"Total Rows (questions): {row.total_rows}")
    print(f"Completed Count: {row.completed_count}")
    print(f"Assigned Count: {row.assigned_count}")
    print(f"Pending Count: {row.pending_count}")
    print(f"Unassigned Count: {row.unassigned_count}")
    print(f"\nCompletion Rate: {(row.completed_count / row.total_rows * 100):.1f}%")
    print(f"Assigned Rate: {(row.assigned_count / row.total_rows * 100):.1f}%")

# Query 2: Status breakdown
print("\n\nQuery 2: Status Distribution")
print("-" * 80)
status_query = f"""
SELECT
  status,
  COUNT(*) as count
FROM `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE exportDate BETWEEN '{week7_start}' AND '{week7_end}'
GROUP BY status
ORDER BY count DESC
"""

result = client.query(status_query).result()
for row in result:
    print(f"{row.status}: {row.count:,}")

# Query 3: By Business Unit
print("\n\nQuery 3: By Business Unit")
print("-" * 80)
bu_query = f"""
SELECT
  businessUnitNumber,
  COUNT(*) as total,
  COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as completed,
  COUNT(CASE WHEN status != 'UnAssigned' THEN 1 END) as assigned,
  ROUND(COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) / COUNT(*) * 100, 1) as completion_pct
FROM `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE exportDate BETWEEN '{week7_start}' AND '{week7_end}'
GROUP BY businessUnitNumber
ORDER BY businessUnitNumber
"""

result = client.query(bu_query).result()
total_assigned_all = 0
total_completed_all = 0
total_possible_all = 0

print(f"{'BU':<6} {'Total':<8} {'Assigned':<10} {'Completed':<10} {'Completion%'}")
print("-" * 60)
for row in result:
    print(f"{row.businessUnitNumber:<6} {row.total:<8} {row.assigned:<10} {row.completed:<10} {row.completion_pct:.1f}%")
    total_possible_all += row.total
    total_assigned_all += row.assigned
    total_completed_all += row.completed

print("-" * 60)
print(f"{'TOTAL':<6} {total_possible_all:<8} {total_assigned_all:<10} {total_completed_all:<10} {(total_completed_all/total_possible_all*100):.1f}%")

print("\n\n" + "=" * 80)
print("SUMMARY METRICS FOR DASHBOARD")
print("=" * 80)
print(f"""
totalStores: (need store count from metadata)
storesWithAssignments: (need store count from metadata)
totalPossibleStores: 4595
totalPossibleItems: {total_possible_all:,}
totalAssignedItems: {total_assigned_all:,}
totalCompletedItems: {total_completed_all:,}
overallCompletionOfMax: {(total_completed_all/total_possible_all*100):.1f}%

Assigned % of Possible: {(total_assigned_all/total_possible_all*100):.1f}%
Completed % of Assigned: {(total_completed_all/total_assigned_all*100):.1f}%
""")

# Query 4: Get date distribution
print("\n\nQuery 4: Date Distribution")
print("-" * 80)
date_query = f"""
SELECT
  exportDate,
  COUNT(*) as count,
  COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as completed
FROM `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE exportDate BETWEEN '{week7_start}' AND '{week7_end}'
GROUP BY exportDate
ORDER BY exportDate
"""

result = client.query(date_query).result()
for row in result:
    print(f"{row.exportDate}: {row.count:,} rows, {row.completed:,} completed")

print("\n" + "=" * 80)
print("END OF QUERY")
print("=" * 80)
