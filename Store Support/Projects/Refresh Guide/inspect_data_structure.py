#!/usr/bin/env python3
"""
Inspect the actual data structure on 2/23/26 to understand:
1. Are there multiple records per question per day?
2. Is exportDate consistent or varying?
3. What's the relationship between exportDate, completionDate, and status?
"""

from google.cloud import bigquery
import json

client = bigquery.Client(project='athena-gateway-prod')

print("=" * 100)
print("DATA STRUCTURE INSPECTION - 2/23/26")
print("=" * 100)
print()

# ============================================================================
# 1. GET A FEW SAMPLE RECORDS TO UNDERSTAND STRUCTURE
# ============================================================================
print("[1] Sample Records from 2/23/26 (first 10)")
print("-" * 100)

sample_query = """
SELECT
  checklistQuestionId,
  businessUnitNumber,
  status,
  assignedTo,
  completionDate,
  exportDate
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-23'
LIMIT 10
"""

results = client.query(sample_query).result()
for i, row in enumerate(results, 1):
    print(f"\nRecord {i}:")
    print(f"  Question ID: {row.checklistQuestionId}")
    print(f"  Business Unit: {row.businessUnitNumber}")
    print(f"  Status: {row.status}")
    print(f"  Assigned To: {row.assignedTo}")
    print(f"  Completion Date: {row.completionDate}")
    print(f"  Export Date: {row.exportDate}")

print()
print()

# ============================================================================
# 2. CHECK FOR DUPLICATE QUESTIONS ON 2/23
# ============================================================================
print("[2] Checking for records with SAME question on 2/23 (multiple timestamps)")
print("-" * 100)

dup_check_query = """
SELECT
  checklistQuestionId,
  businessUnitNumber,
  COUNT(*) as record_count,
  COUNT(DISTINCT exportDate) as unique_export_dates,
  ARRAY_AGG(DISTINCT exportDate ORDER BY exportDate) as export_dates
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-23'
GROUP BY
  checklistQuestionId,
  businessUnitNumber
HAVING
  COUNT(*) > 1
LIMIT 5
"""

results = list(client.query(dup_check_query).result())
if results:
    print(f"Found {len(results)} questions with multiple records on 2/23:")
    for row in results:
        print(f"\n  Question {row.checklistQuestionId} | Unit {row.businessUnitNumber}:")
        print(f"    Total records: {row.record_count}")
        print(f"    Unique export dates: {row.unique_export_dates}")
        print(f"    Dates: {row.export_dates}")
else:
    print("✅ No questions have multiple records on 2/23")
    print("   (Each question-unit pair has exactly ONE record per day)")

print()
print()

# ============================================================================
# 3. UNDERSTAND EXPORT DATE DISTRIBUTION
# ============================================================================
print("[3] Export Date Distribution on 2/23")
print("-" * 100)

date_dist_query = """
SELECT
  DATE(exportDate) as export_date_only,
  TIME(exportDate) as time_component,
  TIMESTAMP_TRUNC(exportDate, HOUR) as hourly_bucket,
  COUNT(*) as record_count
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-23'
GROUP BY
  export_date_only,
  time_component,
  hourly_bucket
ORDER BY
  hourly_bucket
"""

results = client.query(date_dist_query).result()
print(f"{'Time Bucket':<30} {'Records':<15}")
print("-" * 45)
for row in results:
    if row.hourly_bucket:
        print(f"{str(row.hourly_bucket):<30} {row.record_count:>14,}")

print()
print()

# ============================================================================
# 4. FINAL STATE SNAPSHOT ON 2/23
# ============================================================================
print("[4] Final State Summary for 2/23 (single snapshot)")
print("-" * 100)

final_summary = """
SELECT
  COUNT(*) as total_records,
  COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as completed_count,
  COUNT(CASE WHEN status = 'ASSIGNED' THEN 1 END) as assigned_count,
  COUNT(CASE WHEN status = 'UNASSIGNED' THEN 1 END) as unassigned_count,
  COUNT(CASE WHEN assignedTo IS NOT NULL THEN 1 END) as has_assignedto,
  COUNT(CASE WHEN assignedTo IS NULL THEN 1 END) as null_assignedto,
  COUNT(DISTINCT businessUnitNumber) as unique_units
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-23'
"""

result = list(client.query(final_summary).result())[0]

print(f"Total Records: {result.total_records:,}")
print(f"Based on status field:")
print(f"  - COMPLETED: {result.completed_count:,}")
print(f"  - ASSIGNED: {result.assigned_count:,}")
print(f"  - UNASSIGNED: {result.unassigned_count:,}")
print()
print(f"Based on assignedTo field:")
print(f"  - Has assignedTo: {result.has_assignedto:,}")
print(f"  - NULL assignedTo: {result.null_assignedto:,}")
print()
print(f"Unique Business Units: {result.unique_units:,}")
print()
print(f"Check: Total = {result.completed_count + result.assigned_count + result.unassigned_count}")
print(f"Expected: {result.total_records:,}")
if result.completed_count + result.assigned_count + result.unassigned_count == result.total_records:
    print("✅ Sum of statuses equals total")
else:
    print("❌ Status sum mismatch!")

print()
print("=" * 100)
