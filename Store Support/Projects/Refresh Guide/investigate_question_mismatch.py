#!/usr/bin/env python3
"""
Investigate the actual question count by format on 2/23/26
Compare against baseline formula expectations
"""

from google.cloud import bigquery

client = bigquery.Client(project='athena-gateway-prod')

print("=" * 100)
print("INVESTIGATION: Question Count by Format/Division")
print("=" * 100)
print()

# Get all unique questions
all_questions_query = """
SELECT DISTINCT
  checklistQuestionId
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-23'
ORDER BY
  checklistQuestionId
"""

print("Step 1: Getting all unique questions from 2/23 data...")
results = list(client.query(all_questions_query).result())
all_questions = [row.checklistQuestionId for row in results]
print(f"✓ Found {len(all_questions):,} unique questions")
print()

# Get count of stores by format (using businessUnitNumber ranges or metadata)
# First, let's see what columns we have
schema_query = """
SELECT column_name, data_type
FROM `athena-gateway-prod.store_refresh.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'store_refresh_data'
ORDER BY ordinal_position
"""

print("Step 2: Checking available columns...")
results = list(client.query(schema_query).result())
print("Available columns:")
for row in results:
    print(f"  - {row.column_name} ({row.data_type})")
print()

# Now let's get the actual distribution
distribution_query = """
SELECT
  COUNT(DISTINCT businessUnitNumber) as store_count,
  COUNT(DISTINCT checklistQuestionId) as question_count,
  COUNT(DISTINCT CONCAT(businessUnitNumber, '|', checklistQuestionId)) as pair_count
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-23'
"""

print("Step 3: Getting actual distribution on 2/23...")
result = list(client.query(distribution_query).result())[0]
actual_stores = result.store_count
actual_questions = result.question_count
actual_pairs = result.pair_count

print(f"  Unique stores: {actual_stores:,}")
print(f"  Unique questions: {actual_questions:,}")
print(f"  Total store-question pairs: {actual_pairs:,}")
print()

# Calculate implied average
if actual_stores > 0:
    avg_questions_per_store = actual_pairs / actual_stores
    print(f"  Average questions per store: {avg_questions_per_store:.1f}")
print()

# Now let's see if we can break down by format
# We'll need to check if there's a storeFormat column
format_query = """
SELECT
  storeFormat,
  COUNT(DISTINCT businessUnitNumber) as store_count,
  COUNT(DISTINCT checklistQuestionId) as question_count,
  COUNT(DISTINCT CONCAT(businessUnitNumber, '|', checklistQuestionId)) as pair_count
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-23'
GROUP BY
  storeFormat
ORDER BY
  storeFormat
"""

print("Step 4: Distribution by Format (if storeFormat column exists)...")
try:
    results = list(client.query(format_query).result())
    
    total_stores_by_format = 0
    total_pairs_by_format = 0
    
    print(f"\n{'Format':<10} {'Stores':<12} {'Questions':<14} {'Pairs':<15} {'Q/Store Avg':<15}")
    print("-" * 70)
    
    for row in results:
        fmt = row.storeFormat or 'NULL'
        stores = row.store_count or 0
        questions = row.question_count or 0
        pairs = row.pair_count or 0
        avg_q = (pairs / stores) if stores > 0 else 0
        
        total_stores_by_format += stores
        total_pairs_by_format += pairs
        
        print(f"{fmt:<10} {stores:<12,} {questions:<14,} {pairs:<15,} {avg_q:<15.1f}")
    
    print("-" * 70)
    print(f"{'TOTAL':<10} {total_stores_by_format:<12,} {' ':<14} {total_pairs_by_format:<15,}")
    print()
    
except Exception as e:
    print(f"✗ Error or storeFormat column doesn't exist: {e}")
    print()

# Compare to baseline
print("=" * 100)
print("BASELINE FORMULA")
print("=" * 100)
print()
print("SC:   3,555 stores × 328 questions = 1,166,040")
print("DIV1:   366 stores × 327 questions =   119,682")
print("NHM:    674 stores × 209 questions =   140,866")
print("-" * 60)
print("TOTAL: 4,595 stores              = 1,426,588")
print()
print()

print("=" * 100)
print("SUMMARY")
print("=" * 100)
print()
print(f"Actual pairs on 2/23:        {actual_pairs:,}")
print(f"Baseline formula:            1,426,588")
print(f"Difference:                  {actual_pairs - 1426588:,}")
print()

if actual_pairs > 1426588:
    print(f"The 2/23 data has {actual_pairs - 1426588:,} MORE pairs than the formula expects.")
    print("Possible reasons:")
    print("  1. Some stores have more questions than baseline allows")
    print("  2. New stores were added with additional questions")
    print("  3. Questions were added to existing stores")
else:
    print(f"The 2/23 data has {1426588 - actual_pairs:,} FEWER pairs than the formula expects.")
    print("Possible reasons:")
    print("  1. Some stores have fewer questions")
    print("  2. Stores were removed")

print()
