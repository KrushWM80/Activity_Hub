#!/usr/bin/env python3
"""
Extract Week 7 Dashboard Data from BigQuery
Date Range: 2026-02-15 to 2026-02-21
"""

from google.cloud import bigquery
import json
from datetime import datetime

client = bigquery.Client(project='athena-gateway-prod')

print("=" * 80)
print("EXTRACTING WEEK 7 DASHBOARD DATA (2026-02-15 to 2026-02-21)")
print("=" * 80)

# ============================================================================
# 1. SUMMARY DATA - Cumulative metrics through 2026-02-21
# ============================================================================
print("\n[1/5] Extracting SUMMARY DATA...")

summary_query = """
SELECT
  COUNT(DISTINCT CASE WHEN exportDate <= '2026-02-21' THEN storeId END) as totalStores,
  COUNT(DISTINCT CASE WHEN exportDate <= '2026-02-21' AND assignedTo IS NOT NULL THEN storeId END) as storesWithAssignments,
  COUNT(DISTINCT CASE WHEN exportDate <= '2026-02-21' THEN storeId END) as totalPossibleStores,
  COUNT(CASE WHEN exportDate <= '2026-02-21' THEN 1 END) as totalPossibleItems,
  COUNT(CASE WHEN exportDate <= '2026-02-21' AND assignedTo IS NOT NULL THEN 1 END) as totalAssignedItems,
  COUNT(CASE WHEN exportDate <= '2026-02-21' AND status = 'COMPLETED' THEN 1 END) as totalCompletedItems,
  ROUND(100.0 * COUNT(CASE WHEN exportDate <= '2026-02-21' AND status = 'COMPLETED' THEN 1 END) / 
        NULLIF(COUNT(CASE WHEN exportDate <= '2026-02-21' THEN 1 END), 0), 1) as overallCompletionOfMax
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  exportDate BETWEEN '2026-02-15' AND '2026-02-21'
"""

summary_results = client.query(summary_query).result()
summary_data = None
for row in summary_results:
    summary_data = {
        "totalStores": row.totalStores,
        "storesWithAssignments": row.storesWithAssignments,
        "totalPossibleStores": row.totalPossibleStores,
        "totalPossibleItems": row.totalPossibleItems,
        "totalAssignedItems": row.totalAssignedItems,
        "totalCompletedItems": row.totalCompletedItems,
        "overallCompletionOfMax": str(row.overallCompletionOfMax)
    }
    print(f"✓ Summary: {row.totalStores} stores, {row.totalAssignedItems} assigned, {row.totalCompletedItems} completed")

# ============================================================================
# 2. DIVISION STATS
# ============================================================================
print("[2/5] Extracting DIVISION STATS...")

division_query = """
SELECT
  division,
  COUNT(DISTINCT CASE WHEN exportDate <= '2026-02-21' THEN storeId END) as storeCount,
  COUNT(CASE WHEN exportDate <= '2026-02-21' AND assignedTo IS NOT NULL THEN 1 END) as assignedCount,
  COUNT(CASE WHEN exportDate <= '2026-02-21' AND status = 'COMPLETED' THEN 1 END) as completedCount,
  COUNT(CASE WHEN exportDate <= '2026-02-21' AND status = 'COMPLETED' THEN 1 END) as completedOfMaxCount,
  COUNT(CASE WHEN exportDate <= '2026-02-21' THEN 1 END) as maxPossibleCount,
  ROUND(100.0 * COUNT(CASE WHEN exportDate <= '2026-02-21' AND status = 'COMPLETED' THEN 1 END) /
        NULLIF(COUNT(CASE WHEN exportDate <= '2026-02-21' THEN 1 END), 0), 1) as completionPercentage,
  ROUND(COUNT(CASE WHEN exportDate <= '2026-02-21' THEN 1 END) / 
        NULLIF(COUNT(DISTINCT CASE WHEN exportDate <= '2026-02-21' THEN storeId END), 0), 0) as averageMaxQuestions
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  exportDate BETWEEN '2026-02-15' AND '2026-02-21'
GROUP BY
  division
ORDER BY
  division
"""

division_results = client.query(division_query).result()
division_stats = []
for row in division_results:
    division_stats.append({
        "divisionId": row.division,
        "storeCount": row.storeCount,
        "assignedCount": row.assignedCount,
        "completedCount": row.completedCount,
        "completedOfMaxCount": row.completedOfMaxCount,
        "maxPossibleCount": row.maxPossibleCount,
        "completionPercentage": row.completionPercentage,
        "averageMaxQuestions": int(row.averageMaxQuestions) if row.averageMaxQuestions else 0
    })
print(f"✓ Division stats: {len(division_stats)} divisions extracted")

# ============================================================================
# 3. FORMAT STATS
# ============================================================================
print("[3/5] Extracting FORMAT STATS...")

format_query = """
SELECT
  storeFormat,
  COUNT(DISTINCT CASE WHEN exportDate <= '2026-02-21' THEN storeId END) as storeCount,
  COUNT(CASE WHEN exportDate <= '2026-02-21' AND assignedTo IS NOT NULL THEN 1 END) as assignedCount,
  COUNT(CASE WHEN exportDate <= '2026-02-21' AND status = 'COMPLETED' THEN 1 END) as completedCount,
  COUNT(CASE WHEN exportDate <= '2026-02-21' THEN 1 END) as maxPossibleCount,
  ROUND(100.0 * COUNT(CASE WHEN exportDate <= '2026-02-21' AND status = 'COMPLETED' THEN 1 END) /
        NULLIF(COUNT(CASE WHEN exportDate <= '2026-02-21' THEN 1 END), 0), 1) as completionPercentage
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  exportDate BETWEEN '2026-02-15' AND '2026-02-21'
GROUP BY
  storeFormat
ORDER BY
  storeFormat
"""

format_results = client.query(format_query).result()
format_stats = []
for row in format_results:
    format_stats.append({
        "format": row.storeFormat,
        "storeCount": row.storeCount,
        "assignedCount": row.assignedCount,
        "completedCount": row.completedCount,
        "maxPossibleCount": row.maxPossibleCount,
        "completionPercentage": row.completionPercentage
    })
print(f"✓ Format stats: {len(format_stats)} formats extracted")

# ============================================================================
# 4. AREA STATS
# ============================================================================
print("[4/5] Extracting AREA STATS...")

area_query = """
SELECT
  area,
  COUNT(CASE WHEN exportDate <= '2026-02-21' AND assignedTo IS NOT NULL THEN 1 END) as assigned,
  COUNT(CASE WHEN exportDate <= '2026-02-21' AND status = 'COMPLETED' THEN 1 END) as completed,
  COUNT(CASE WHEN exportDate <= '2026-02-21' THEN 1 END) as maxPossible,
  ROUND(100.0 * COUNT(CASE WHEN exportDate <= '2026-02-21' AND status = 'COMPLETED' THEN 1 END) /
        NULLIF(COUNT(CASE WHEN exportDate <= '2026-02-21' THEN 1 END), 0), 1) as completionPercentage
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  exportDate BETWEEN '2026-02-15' AND '2026-02-21'
GROUP BY
  area
ORDER BY
  area
"""

area_results = client.query(area_query).result()
area_stats = []
for row in area_results:
    area_stats.append({
        "area": row.area,
        "assigned": row.assigned,
        "completed": row.completed,
        "maxPossible": row.maxPossible,
        "completionPercentage": str(row.completionPercentage)
    })
print(f"✓ Area stats: {len(area_stats)} areas extracted")

# ============================================================================
# 5. USER ENGAGEMENT METRICS
# ============================================================================
print("[5/5] Extracting USER ENGAGEMENT METRICS...")

engagement_query = """
SELECT
  COUNT(DISTINCT CASE WHEN exportDate <= '2026-02-21' THEN assignedTo END) as workers,
  COUNT(DISTINCT CASE WHEN exportDate <= '2026-02-21' THEN assignedBy END) as managers,
  COUNT(DISTINCT CASE WHEN exportDate <= '2026-02-21' THEN CONCAT(assignedTo, assignedBy) END) as totalUsers,
  COUNT(CASE WHEN exportDate <= '2026-02-21' AND assignedTo IS NOT NULL THEN 1 END) as assignments,
  COUNT(CASE WHEN exportDate <= '2026-02-21' AND status = 'COMPLETED' THEN 1 END) as completions,
  COUNT(CASE WHEN exportDate <= '2026-02-21' THEN 1 END) as totalActions
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  exportDate BETWEEN '2026-02-15' AND '2026-02-21'
"""

engagement_results = client.query(engagement_query).result()
user_engagement = None
for row in engagement_results:
    total_users = row.workers + row.managers
    actions_per_user = round(row.totalActions / total_users, 1) if total_users > 0 else 0
    user_engagement = {
        "workers": row.workers,
        "managers": row.managers,
        "totalUsers": total_users,
        "assignments": row.assignments,
        "completions": row.completions,
        "totalActions": row.totalActions,
        "actionsPerUser": actions_per_user
    }
    print(f"✓ Engagement: {row.workers} workers, {row.managers} managers, {row.totalActions} total actions")

# ============================================================================
# OUTPUT RESULTS
# ============================================================================
print("\n" + "=" * 80)
print("WEEK 7 DASHBOARD DATA - JSON OUTPUT")
print("=" * 80)

output = {
    "week": 7,
    "dateRange": "2026-02-15 to 2026-02-21",
    "generatedAt": datetime.now().isoformat(),
    "summary": summary_data,
    "divisionStats": division_stats,
    "formatStats": format_stats,
    "areaStats": area_stats,
    "userEngagement": user_engagement
}

json_output = json.dumps(output, indent=2)
print(json_output)

# ============================================================================
# SAVE TO FILE
# ============================================================================
output_file = "week7_dashboard_data.json"
with open(output_file, 'w') as f:
    json.dump(output, f, indent=2)
print(f"\n✅ Data saved to: {output_file}")

print("\n" + "=" * 80)
print("SUMMARY STATISTICS")
print("=" * 80)
print(f"Total Stores: {summary_data['totalStores']}")
print(f"Stores with Assignments: {summary_data['storesWithAssignments']}")
print(f"Total Items Assigned: {summary_data['totalAssignedItems']}")
print(f"Total Items Completed: {summary_data['totalCompletedItems']}")
print(f"Overall Completion: {summary_data['overallCompletionOfMax']}%")
print(f"\nUser Engagement:")
print(f"  Workers: {user_engagement['workers']}")
print(f"  Managers: {user_engagement['managers']}")
print(f"  Total Users: {user_engagement['totalUsers']}")
print(f"  Total Actions: {user_engagement['totalActions']}")
print(f"  Actions per User: {user_engagement['actionsPerUser']}")
print("=" * 80)
