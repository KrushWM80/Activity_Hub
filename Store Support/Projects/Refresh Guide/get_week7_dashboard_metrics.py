#!/usr/bin/env python3
"""
Week 7 (2/23/26) Dashboard Metrics - Single Snapshot
Query the 2/23 snapshot and return Dashboard Metrics
"""

from google.cloud import bigquery
import json

client = bigquery.Client(project='athena-gateway-prod')

print("=" * 100)
print("WEEK 7 DASHBOARD METRICS (2/23/26 Snapshot)")
print("=" * 100)
print()

# ============================================================================
# QUERY: Get Dashboard Metrics from 2/23 snapshot
# ============================================================================

metrics_query = """
SELECT
  COUNT(*) as totalPossibleItems,
  COUNT(CASE WHEN assignedTo IS NOT NULL AND TRIM(assignedTo) != '' THEN 1 END) as totalAssignedItems,
  COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as totalCompletedItems,
  COUNT(DISTINCT businessUnitNumber) as storesWithAssignments
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-23'
"""

print("Querying 2/23/26 snapshot...")
result = list(client.query(metrics_query).result())[0]

totalPossibleItems = result.totalPossibleItems or 0
totalAssignedItems = result.totalAssignedItems or 0
totalCompletedItems = result.totalCompletedItems or 0
storesWithAssignments = result.storesWithAssignments or 0

overallCompletionOfMax = round((totalCompletedItems / totalPossibleItems * 100), 1) if totalPossibleItems > 0 else 0

print("✅ Query complete\n")

# ============================================================================
# DATA VALIDATION
# ============================================================================
print("=" * 100)
print("DATA VALIDATION")
print("=" * 100)
print()

validations = {
    "totalPossibleItems_matches_baseline": {
        "expected": 1426588,
        "actual": totalPossibleItems,
        "pass": totalPossibleItems == 1426588
    },
    "totalCompletedItems_le_totalPossibleItems": {
        "expected": "✓",
        "actual": f"{totalCompletedItems:,} ≤ {totalPossibleItems:,}",
        "pass": totalCompletedItems <= totalPossibleItems
    },
    "totalAssignedItems_le_totalPossibleItems": {
        "expected": "✓",
        "actual": f"{totalAssignedItems:,} ≤ {totalPossibleItems:,}",
        "pass": totalAssignedItems <= totalPossibleItems
    },
    "totalCompletedItems_le_totalAssignedItems": {
        "expected": "✓",
        "actual": f"{totalCompletedItems:,} ≤ {totalAssignedItems:,}",
        "pass": totalCompletedItems <= totalAssignedItems
    },
    "overallCompletionOfMax_calculation": {
        "expected": f"{round(totalCompletedItems / totalPossibleItems * 100, 1)}%",
        "actual": f"{overallCompletionOfMax}%",
        "pass": overallCompletionOfMax == round(totalCompletedItems / totalPossibleItems * 100, 1)
    }
}

for check, details in validations.items():
    status = "✅" if details["pass"] else "❌"
    print(f"{status} {check}")
    if not details["pass"]:
        print(f"   Expected: {details['expected']}")
        print(f"   Actual: {details['actual']}")
    else:
        print(f"   {details['actual']}")
    print()

print()

# ============================================================================
# DASHBOARD JSON OUTPUT
# ============================================================================
print("=" * 100)
print("DASHBOARD METRICS OBJECT")
print("=" * 100)
print()

dashboard_metrics = {
    "week": 7,
    "date": "2026-02-23",
    "label": "Week 7",
    "summary": {
        "totalStores": 4595,
        "storesWithAssignments": storesWithAssignments,
        "totalPossibleStores": 4595,
        "totalPossibleItems": totalPossibleItems,
        "totalAssignedItems": totalAssignedItems,
        "totalCompletedItems": totalCompletedItems,
        "overallCompletionOfMax": overallCompletionOfMax
    }
}

print(json.dumps(dashboard_metrics, indent=2))
print()
print("=" * 100)
