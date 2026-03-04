#!/usr/bin/env python3
"""
Week 7 (2/16-2/23/26) Data Extraction - CORRECTED
Using date range for the entire week of activity
Max Possible Items: 1,426,588 (verified baseline)
"""

from google.cloud import bigquery
import json

client = bigquery.Client(project='athena-gateway-prod')

# Week 7 date range: 2/16/26 - 2/23/26
WEEK_START = '2026-02-16'
WEEK_END = '2026-02-23'

# CORRECT totalPossibleItems (verified)
TOTAL_POSSIBLE = 1426588

print("=" * 80)
print("WEEK 7 DATA EXTRACTION (2/16-2/23/26) - CORRECT BASELINE")
print("=" * 80)
print()
print(f"Date Range: {WEEK_START} to {WEEK_END}")
print(f"Total Possible Items (Baseline): {TOTAL_POSSIBLE:,}")
print()

job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("start_date", "DATE", WEEK_START),
        bigquery.ScalarQueryParameter("end_date", "DATE", WEEK_END),
    ]
)

# ============================================================================
# 1. VERIFY TOTAL ROW COUNT FOR PERIOD
# ============================================================================
print("[1/4] Verifying data structure...")

row_count_query = """
SELECT
  COUNT(*) as total_rows,
  COUNT(DISTINCT checklistQuestionId) as unique_questions,
  COUNT(DISTINCT businessUnitNumber) as unique_stores
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) BETWEEN @start_date AND @end_date
"""

result = list(client.query(row_count_query, job_config=job_config).result())[0]
total_rows = result.total_rows or 0
unique_questions = result.unique_questions or 0
unique_stores = result.unique_stores or 0

print(f"  Total rows in date range: {total_rows:,}")
print(f"  Unique questions found: {unique_questions:,}")
print(f"  Unique stores found: {unique_stores:,}")
print()

# ============================================================================
# 2. GET FINAL STATE AS OF 2/23/26 (LAST DAY OF WEEK)
# ============================================================================
print("[2/4] Extracting final state (2/23/26)...")

final_state_query = """
SELECT
  COUNT(*) as total_final_records,
  COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as completed_count,
  COUNT(CASE WHEN assignedTo IS NOT NULL THEN 1 END) as assigned_count,
  COUNT(CASE WHEN assignedTo IS NULL THEN 1 END) as unassigned_count
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = @end_date
"""

# Use same job_config but technically only need @end_date
result = list(client.query(final_state_query, job_config=job_config).result())[0]
total_final = result.total_final_records or 0
completed = result.completed_count or 0
assigned = result.assigned_count or 0
unassigned = result.unassigned_count or 0

print(f"  Final snapshot (2/23/26) total records: {total_final:,}")
print(f"    - Completed: {completed:,}")
print(f"    - Assigned (not completed): {assigned - completed:,}")
print(f"    - Unassigned: {unassigned:,}")
print()

# ============================================================================
# 3. DATA INTEGRITY CHECKS
# ============================================================================
print("[3/4] Data integrity validation...")
print()

# Check 1: Final records should equal or be close to baseline
if total_final <= TOTAL_POSSIBLE:
    print(f"  ✅ Final records ({total_final:,}) ≤ Baseline ({TOTAL_POSSIBLE:,})")
else:
    print(f"  ❌ Final records ({total_final:,}) > Baseline ({TOTAL_POSSIBLE:,})")
    print(f"     Difference: +{total_final - TOTAL_POSSIBLE:,}")

print()

# Check 2: Sum of statuses
status_sum = completed + (assigned - completed) + unassigned
print(f"  Sum of statuses: {status_sum:,}")
print(f"  Should equal final total: {total_final:,}")
if status_sum == total_final:
    print(f"  ✅ Status sum matches total")
else:
    print(f"  ⚠️  Mismatch: difference of {abs(status_sum - total_final):,}")

print()

# Check 3: Assigned should be <= total
if assigned <= total_final:
    assigned_pct = (assigned / total_final * 100) if total_final > 0 else 0
    print(f"  ✅ Assigned ({assigned:,}) ≤ Total ({total_final:,})")
    print(f"     {assigned_pct:.1f}% of records")
else:
    print(f"  ❌ Assigned ({assigned:,}) > Total ({total_final:,})")

print()

# Check 4: Completed should be <= assigned
if completed <= assigned:
    completed_of_assigned = (completed / assigned * 100) if assigned > 0 else 0
    print(f"  ✅ Completed ({completed:,}) ≤ Assigned ({assigned:,})")
    print(f"     {completed_of_assigned:.1f}% of assigned")
else:
    print(f"  ❌ Completed ({completed:,}) > Assigned ({assigned:,})")

print()

# ============================================================================
# 4. SUMMARY METRICS
# ============================================================================
print("[4/4] Final Summary Metrics...")
print()

completion_pct = (completed / total_final * 100) if total_final > 0 else 0
assigned_pct_of_total = (assigned / total_final * 100) if total_final > 0 else 0

final_data = {
    "week": 7,
    "dateRange": f"{WEEK_START} to {WEEK_END}",
    "snapshot": WEEK_END,
    "summary": {
        "totalStores": 4595,
        "storesWithAssignments": unique_stores,
        "totalPossibleStores": 4595,
        "totalPossibleItems": TOTAL_POSSIBLE,
        "totalAssignedItems": assigned,
        "totalCompletedItems": completed,
        "overallCompletionOfMax": round(completion_pct, 1)
    },
    "dataQuality": {
        "finalRecordCount": total_final,
        "expectedRecordCount": TOTAL_POSSIBLE,
        "matchesBaseline": total_final == TOTAL_POSSIBLE,
        "completedValid": completed <= assigned,
        "assignedValid": assigned <= total_final
    }
}

print(json.dumps(final_data, indent=2))
print()
print("=" * 80)
print("DIAGNOSTICS")
print("=" * 80)
print()
print(f"Total Final State Size: {total_final:,} records")
print(f"Expected Baseline: {TOTAL_POSSIBLE:,} records")
print(f"Match: {total_final == TOTAL_POSSIBLE}")
print()
print(f"Completed: {completed:,} ({completion_pct:.1f}% of final)")
print(f"Assigned: {assigned:,} ({assigned_pct_of_total:.1f}% of final)")
print(f"Unassigned: {unassigned:,}")
print()
print("=" * 80)
