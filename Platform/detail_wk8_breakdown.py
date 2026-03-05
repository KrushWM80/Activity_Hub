#!/usr/bin/env python3
"""
Extract Week 8 (2/28/26) detailed breakdown by division and format
"""

from google.cloud import bigquery
import json

client = bigquery.Client(project='athena-gateway-prod')

print('\n' + '=' * 120)
print('WEEK 8 (2/28/26) DETAILED FORMAT & DIVISION BREAKDOWN')
print('=' * 120 + '\n')

# ============================================================================
# DETAILED STATUS BREAKDOWN
# ============================================================================
print('📊 DETAILED STATUS & ASSIGNMENT BREAKDOWN')
print('-' * 120)

detail_query = '''
SELECT
  status,
  COUNT(*) as item_count,
  COUNT(CASE WHEN assignedTo IS NOT NULL AND TRIM(assignedTo) != '' THEN 1 END) as with_assignee,
  COUNT(CASE WHEN completionDate IS NOT NULL THEN 1 END) as with_completion
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-28'
GROUP BY
  status
ORDER BY
  item_count DESC
'''

print('\nStatus Breakdown:')
detail_results = client.query(detail_query).result()

total_items = 0
assigned_items = 0
completed_items = 0

for row in detail_results:
    status = row.status.strip() if row.status else 'NULL'
    item_count = row.item_count
    total_items += item_count
    
    # Count as "assigned" if not in UnAssigned status
    if status != 'UnAssigned':
        assigned_items += item_count
    
    # Count as "completed" if has completion date
    completed_items += row.with_completion
    
    print(f"  {status:<20} : {item_count:>12,} items | With Assignee: {row.with_assignee:>12,} | With Completion: {row.with_completion:>12,}")

print()
print(f"TOTALS:")
print(f"  Total Items in BQ: {total_items:>12,}")
print(f"  Assigned Items (non-UnAssigned): {assigned_items:>12,}")
print(f"  Completed Items (has completionDate): {completed_items:>12,}")
print()

# ============================================================================
# VERIFY - COMPLETION PERCENTAGE CALCULATION
# ============================================================================
print('📈 COMPLETION METRICS')
print('-' * 120)

if assigned_items > 0:
    completion_pct = (completed_items / assigned_items) * 100
    print(f"  Assigned Items: {assigned_items:>12,}")
    print(f"  Completed Items: {completed_items:>12,}")
    print(f"  Completion %: {completion_pct:>12.1f}%")
else:
    print("  ERROR: No assigned items found")

print()

# ============================================================================
# STORE DISTRIBUTION CHECK
# ============================================================================
print('🏪 STORE DISTRIBUTION ANALYSIS')
print('-' * 120)

store_dist_query = '''
SELECT
  COUNT(DISTINCT businessUnitNumber) as store_count,
  COUNT(DISTINCT checklistQuestionId) as question_count,
  ROUND(COUNT(*) / COUNT(DISTINCT businessUnitNumber), 2) as avg_q_per_store
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-28'
'''

result = list(client.query(store_dist_query).result())[0]
print(f"  Unique Stores: {result.store_count:>12,}")
print(f"  Unique Questions: {result.question_count:>12,}")
print(f"  Avg Questions per Store: {result.avg_q_per_store:>12.2f}")
print()

# ============================================================================
# SUMMARY FOR DASHBOARD
# ============================================================================
print('=' * 120)
print('METRICS TO USE IN WEEK 8 (2/28/26) DASHBOARD')
print('=' * 120)
print()

print("✅ CONFIRMED WK8 DATA:")
print(f"  Export Date: 2026-02-28")
print("")
print(f"  Total Items Available: {total_items:>12,}")
print(f"  Total Assigned Items: {assigned_items:>12,}")
print(f"  Total Completed Items: {completed_items:>12,}")
print(f"  Completion Rate: {(completed_items/assigned_items*100):>12.1f}% (of assigned)")
print(f"  Total Stores: {result.store_count:>12,}")
print()
print("⚠️  IMPORTANT NOTES:")
print("  • Total Items (1,489,640) includes UnAssigned status items")
print("  • Assigned Items (1,240,922) = COMPLETED + PENDING (excludes UnAssigned)")
print("  • Completed Items (1,117,646) = items with completion dates")
print("  • This is different from WK7 baseline (1,426,588 max possible)")
print("  • Need to determine if max possible changed or if this data is cumulative/raw")
print()
