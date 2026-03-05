#!/usr/bin/env python3
"""
Extract Week 8 (2/28/26) data details for dashboard creation
"""

from google.cloud import bigquery
import json

client = bigquery.Client(project='athena-gateway-prod')

print('\n' + '=' * 100)
print('WEEK 8 (2/28/26) DATA EXTRACTION FOR DASHBOARD')
print('=' * 100 + '\n')

# ============================================================================
# 1. COUNT BY BUSINESS UNIT FORMAT/TYPE
# ============================================================================
print('1️⃣  BUSINESS UNIT FORMAT BREAKDOWN ON 2/28/26')
print('-' * 100)

format_query = '''
SELECT
  CASE 
    WHEN businessUnitNumber <= 1100 THEN 'NA - likely SC'
    WHEN businessUnitNumber > 1100 AND businessUnitNumber <= 1500 THEN 'Regional'
    ELSE 'Check'
  END as bu_type,
  COUNT(DISTINCT businessUnitNumber) as store_count
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-28'
GROUP BY
  bu_type
ORDER BY
  store_count DESC
'''

results = client.query(format_query).result()
for row in results:
    print(f"  {row.bu_type:<20}: {row.store_count:>6,} stores")
print()

# ============================================================================
# 2. STATUS BREAKDOWN (ASSIGNED vs COMPLETED)
# ============================================================================
print('2️⃣  ASSIGNMENT & COMPLETION STATUS ON 2/28/26')
print('-' * 100)

status_query = '''
SELECT
  status,
  COUNT(*) as record_count,
  COUNT(DISTINCT businessUnitNumber) as distinct_stores
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-28'
GROUP BY
  status
ORDER BY
  record_count DESC
'''

status_totals = {}
results = client.query(status_query).result()
for row in results:
    status_totals[row.status] = row.record_count
    print(f"  Status '{row.status:<20}': {row.record_count:>12,} records ({row.distinct_stores:>6,} stores)")

total_records = sum(status_totals.values())
print(f"\n  TOTAL RECORDS: {total_records:>12,}")
print()

# ============================================================================
# 3. ASSIGNMENT BREAKDOWN
# ============================================================================
print('3️⃣  ASSIGNMENT DETAILS ON 2/28/26')
print('-' * 100)

assign_query = '''
SELECT
  COUNT(*) as total_records,
  COUNT(CASE WHEN assignedTo IS NOT NULL AND TRIM(assignedTo) != '' THEN 1 END) as assigned_records,
  COUNT(CASE WHEN assignedTo IS NULL OR TRIM(assignedTo) = '' THEN 1 END) as unassigned_records
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-28'
'''

result = list(client.query(assign_query).result())[0]
print(f"  Total Items: {result.total_records:>12,}")
print(f"  Assigned: {result.assigned_records:>12,}")
print(f"  Unassigned: {result.unassigned_records:>12,}")
if result.total_records > 0:
    assigned_pct = (result.assigned_records / result.total_records) * 100
    print(f"  Assigned %: {assigned_pct:>12.1f}%")
print()

# ============================================================================
# 4. COMPLETION BREAKDOWN
# ============================================================================
print('4️⃣  COMPLETION STATUS ON 2/28/26')
print('-' * 100)

complete_query = '''
SELECT
  COUNT(*) as total_records,
  COUNT(CASE WHEN completionDate IS NOT NULL THEN 1 END) as completed_records,
  COUNT(CASE WHEN completionDate IS NULL THEN 1 END) as incomplete_records
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-28'
'''

complete_result = list(client.query(complete_query).result())[0]
print(f"  Total Items: {complete_result.total_records:>12,}")
print(f"  Completed: {complete_result.completed_records:>12,}")
print(f"  Incomplete: {complete_result.incomplete_records:>12,}")
if complete_result.total_records > 0:
    completed_pct = (complete_result.completed_records / complete_result.total_records) * 100
    print(f"  Completed %: {completed_pct:>12.1f}%")
print()

# ============================================================================
# 5. STORE COUNT VALIDATION
# ============================================================================
print('5️⃣  STORE PARTICIPATION ON 2/28/26')
print('-' * 100)

store_query = '''
SELECT
  COUNT(DISTINCT businessUnitNumber) as unique_stores,
  COUNT(DISTINCT checklistQuestionId) as unique_questions,
  MIN(businessUnitNumber) as min_store,
  MAX(businessUnitNumber) as max_store
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-28'
'''

store_result = list(client.query(store_query).result())[0]
print(f"  Unique Stores: {store_result.unique_stores:>12,}")
print(f"  Unique Questions: {store_result.unique_questions:>12,}")
print(f"  Store Range: {store_result.min_store:>12,} to {store_result.max_store:<12,}")
print()

# ============================================================================
# 6. SUMMARY FOR DASHBOARD
# ============================================================================
print('=' * 100)
print('SUMMARY FOR WEEK 8 (2/28/26) DASHBOARD')
print('=' * 100)
print()
print(f"Date: 2/28/26")
print(f"Most Recent Snapshot: YES - Latest BQ Date is 2026-03-05, so 2/28 data is available")
print()
print("KEY METRICS FOR DASHBOARD:")
print(f"  • Total Records (Assigned + Unassigned): {total_records:>12,}")
print(f"  • Assigned Items: {result.assigned_records:>12,}")
print(f"  • Completed Items: {complete_result.completed_records:>12,}")
print(f"  • Total Stores with Data: {store_result.unique_stores:>12,}")
print(f"  • Unique Questions: {store_result.unique_questions:>12,}")
print()
print("NEXT STEPS:")
print("  1. Query detailed division and format breakdowns")
print("  2. Extract store-level metrics")
print("  3. Validate against baseline structure (1,426,588 expected max)")
print("  4. Create WK8 dashboard files with updated dates and metrics")
print()
