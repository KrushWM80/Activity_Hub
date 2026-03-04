#!/usr/bin/env python3
"""
Get Week 7 dimensional breakdowns from BigQuery
"""

from google.cloud import bigquery
import json

client = bigquery.Client(project='athena-gateway-prod')

week7_start = '2026-02-23'
week7_end = '2026-02-28'

print("=" * 80)
print("WEEK 7 DIVISION METRICS")
print("=" * 80)

# Get business unit summary to enable division mapping
bu_query = f"""
SELECT
  businessUnitNumber,
  COUNT(*) as total,
  COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as completed,
  COUNT(CASE WHEN status != 'UnAssigned' THEN 1 END) as assigned,
  COUNT(DISTINCT CASE WHEN status != 'UnAssigned' THEN SUBSTRING(assignedTo, 1, 3) END) as unique_users
FROM `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE exportDate BETWEEN '{week7_start}' AND '{week7_end}'
GROUP BY businessUnitNumber
ORDER BY businessUnitNumber
"""

result = client.query(bu_query).result()
divisions = []
total_assigned = 0
total_completed = 0
total_possible = 0

division_map = {
    3001: "SOUTHEAST BU",
    3002: "NORTH BU",
    3003: "SOUTHWEST BU",
    3004: "WEST BU",
    3005: "NHM BU",
    3006: "EAST BU",
    3007: "PR",
}

print(f"\n{'BU':<6} {'Division':<20} {'Possible':<12} {'Assigned':<12} {'Completed':<12} {'Completed %'}")
print("-" * 80)

for row in result:
    bu_num = row.businessUnitNumber
    div_name = division_map.get(bu_num, f"BU{bu_num}")
    completion_pct = (row.completed / row.total * 100) if row.total > 0 else 0
    
    print(f"{bu_num:<6} {div_name:<20} {row.total:<12,} {row.assigned:<12,} {row.completed:<12,} {completion_pct:>6.1f}%")
    
    divisions.append({
        "businessUnitNumber": bu_num,
        "divisionName": div_name,
        "total": row.total,
        "assigned": row.assigned,
        "completed": row.completed,
        "completion_pct": completion_pct
    })
    
    total_possible += row.total
    total_assigned += row.assigned
    total_completed += row.completed

print("-" * 80)
print(f"{'TOTAL':<6} {' ':<20} {total_possible:<12,} {total_assigned:<12,} {total_completed:<12,} {(total_completed/total_possible*100):>6.1f}%")

# Now let's also get some store-level data to estimate format and area stats
print("\n\n" + "=" * 80)
print("STORE LEVEL SAMPLE (for format/area estimation)")
print("=" * 80)

store_query = f"""
SELECT DISTINCT
  CAST(SUBSTR(checklistQuestionId, 1, 4) AS INT64) as storeNumber,
  COUNT(*) as total_questions,
  COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as completed_count
FROM `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE exportDate BETWEEN '{week7_start}' AND '{week7_end}'
GROUP BY storeNumber
ORDER BY storeNumber
LIMIT 100
"""

result = client.query(store_query).result()
print(f"\n{'Store':<8} {'Total Q':<10} {'Completed':<12} {'Completion %'}")
print("-" * 50)

for row in result:
    comp_pct = (row.completed_count / row.total_questions * 100) if row.total_questions > 0 else 0
    print(f"{row.storeNumber:<8} {row.total_questions:<10} {row.completed_count:<12} {comp_pct:>6.1f}%")

print("\n\n" + "=" * 80)
print("JSON STRUCTURE FOR DASHBOARD")
print("=" * 80)

dashboard_data = {
    "summary": {
        "totalPossibleItems": 8936504,
        "totalAssignedItems": 7439151,
        "totalCompletedItems": 6690229,
        "overallCompletionOfMax": "74.9"
    },
    "divisions": divisions
}

print(json.dumps(dashboard_data, indent=2))

print("\n" + "=" * 80)
print("END")
print("=" * 80)
