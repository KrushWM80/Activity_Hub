#!/usr/bin/env python3
"""
Check if there are duplicate (question, store) pairs on 2/23
"""

from google.cloud import bigquery

client = bigquery.Client(project='athena-gateway-prod')

print("=" * 100)
print("DUPLICATE CHECK: (checklistQuestionId, businessUnitNumber) on 2/23/26")
print("=" * 100)
print()

# Count total rows
total_query = """
SELECT COUNT(*) as total_rows
FROM `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE DATE(exportDate) = '2026-02-23'
"""

# Count unique pairs
unique_query = """
SELECT COUNT(DISTINCT CONCAT(checklistQuestionId, '|', CAST(businessUnitNumber AS STRING))) as unique_pairs
FROM `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE DATE(exportDate) = '2026-02-23'
"""

# Find pairs with duplicates
duplicates_query = """
SELECT
  checklistQuestionId,
  businessUnitNumber,
  COUNT(*) as record_count,
  ARRAY_AGG(DISTINCT status) as statuses,
  STRING_AGG(CAST(exportDate AS STRING), ', ') as export_dates
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-23'
GROUP BY
  checklistQuestionId,
  businessUnitNumber
HAVING
  COUNT(*) > 1
ORDER BY
  record_count DESC
LIMIT 20
"""

print("Query 1: Total rows on 2/23")
result = list(client.query(total_query).result())[0]
total_rows = result.total_rows
print(f"  Total rows: {total_rows:,}")
print()

print("Query 2: Unique (question, store) pairs on 2/23")
result = list(client.query(unique_query).result())[0]
unique_pairs = result.unique_pairs
print(f"  Unique pairs: {unique_pairs:,}")
print()

print("Query 3: Sample of duplicate pairs (if any exist)")
results = list(client.query(duplicates_query).result())
if results:
    print(f"  Found {len(results)} question-store pairs with duplicates:")
    for row in results:
        print(f"\n  Question {row.checklistQuestionId} | Store {row.businessUnitNumber}:")
        print(f"    Record count: {row.record_count}")
        print(f"    Statuses: {row.statuses}")
        print(f"    Export dates: {row.export_dates}")
else:
    print(f"  ✅ No duplicates found. Each (question, store) pair appears exactly once.")

print()
print("=" * 100)
print("ANALYSIS")
print("=" * 100)
print()
print(f"Total rows: {total_rows:,}")
print(f"Unique pairs: {unique_pairs:,}")
print(f"Expected baseline: 1,426,588")
print()

if total_rows == unique_pairs:
    print("✅ No duplicates - each pair appears once")
    if total_rows == 1426588:
        print("✅ Count matches baseline")
    else:
        print(f"❌ But count STILL doesn't match baseline (diff: {total_rows - 1426588:,})")
else:
    diff = total_rows - unique_pairs
    print(f"❌ DUPLICATES EXIST: {diff:,} extra records")
    print(f"   Duplicate rows: {diff:,}")
    print(f"   Unique pairs: {unique_pairs:,}")

print()
