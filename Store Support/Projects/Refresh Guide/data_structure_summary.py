#!/usr/bin/env python3
"""
Final data structure analysis - 2/23/26
"""

from google.cloud import bigquery

client = bigquery.Client(project='athena-gateway-prod')

print("=" * 100)
print("KEY FINDINGS")
print("=" * 100)
print()

# ============================================================================
# 1. EACH QUESTION HAS EXACTLY ONE RECORD ON 2/23 (confirmed above)
# ============================================================================
print("✅ FINDING #1: One Record Per Question Per Day")
print("-" * 100)
print("  Each (Question, Business Unit) pair has EXACTLY ONE record on 2/23/26")
print("  Export Date: 2026-02-23 (constant for all records)")
print("  This is a CLEAN SNAPSHOT - no duplicates or multiple timestamps")
print()
print()

# ============================================================================
# 2. FINAL STATE COUNTS ON 2/23
# ============================================================================
print("✅ FINDING #2: Final State Counts on 2/23/26")
print("-" * 100)

# We need to understand the status values being used
status_check = """
SELECT
  status,
  COUNT(*) as count
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-23'
GROUP BY
  status
ORDER BY
  count DESC
"""

print("\nBreakdown by STATUS field values:")
results = client.query(status_check).result()
status_map = {}
for row in results:
    status_map[row.status] = row.count
    print(f"  {row.status:<20} : {row.count:>12,}")

total_by_status = sum(status_map.values())
print(f"  {'TOTAL':<20} : {total_by_status:>12,}")
print()
print()

# ============================================================================
# 3. ASSIGNED TO FIELD
# ============================================================================
print("✅ FINDING #3: Breakdown by assignedTo Field")
print("-" * 100)

assigned_check = """
SELECT
  COUNT(*) as total_records,
  COUNT(CASE WHEN assignedTo IS NOT NULL AND TRIM(assignedTo) != '' THEN 1 END) as has_assignedto,
  COUNT(CASE WHEN assignedTo IS NULL OR TRIM(assignedTo) = '' THEN 1 END) as null_or_empty_assignedto
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-23'
"""

result = list(client.query(assigned_check).result())[0]
print(f"\nmeasured by assignedTo field:")
print(f"  Total Records: {result.total_records:>12,}")
print(f"  Has assignedTo value: {result.has_assignedto:>12,}")
print(f"  NULL or empty: {result.null_or_empty_assignedto:>12,}")
print()
print()

# ============================================================================
# 4. COMPLETION DATE FIELD
# ============================================================================
print("✅ FINDING #4: Completion Status")
print("-" * 100)

completion_check = """
SELECT
  COUNT(*) as total_records,
  COUNT(CASE WHEN completionDate IS NOT NULL THEN 1 END) as has_completion_date,
  COUNT(CASE WHEN completionDate IS NULL THEN 1 END) as null_completion_date
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-23'
"""

result = list(client.query(completion_check).result())[0]
print(f"\nMeasured by completionDate field:")
print(f"  Total Records: {result.total_records:>12,}")
print(f"  Has completion date: {result.has_completion_date:>12,}")
print(f"  NULL (not completed): {result.null_completion_date:>12,}")
print()
print()

# ============================================================================
# 5. STORE/UNIT COUNT
# ============================================================================
print("✅ FINDING #5: Store/Unit Distribution")
print("-" * 100)

store_check = """
SELECT
  COUNT(DISTINCT businessUnitNumber) as unique_stores,
  COUNT(DISTINCT checklistQuestionId) as unique_questions
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-23'
"""

result = list(client.query(store_check).result())[0]
print(f"\nUnique entities:")
print(f"  Business Units: {result.unique_stores:>12,}")
print(f"  Questions: {result.unique_questions:>12,}")
if result.unique_stores and result.unique_questions:
    avg = total_by_status / result.unique_stores
    print(f"  Avg questions per unit: {avg:>20.0f}")
print()
print()

# ============================================================================
# 6. SUMMARY FOR DASHBOARD
# ============================================================================
print("=" * 100)
print("SUMMARY FOR WEEK 7 DASHBOARD UPDATE")
print("=" * 100)
print()
print(f"Date: 2/23/26 (most recent snapshot)")
print(f"Total Records (= Total Possible Items): {total_by_status:,}")
print(f"Expected Baseline: 1,426,588")
print(f"Matches: {total_by_status == 1426588}")
print()
print("Status Breakdown:")
for status, count in sorted(status_map.items(), key=lambda x: -x[1]):
    pct = (count / total_by_status * 100) if total_by_status > 0 else 0
    print(f"  {status:<20} : {count:>12,} ({pct:>5.1f}%)")
print()
