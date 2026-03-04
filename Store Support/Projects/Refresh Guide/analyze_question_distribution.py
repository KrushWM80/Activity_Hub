#!/usr/bin/env python3
"""
Detailed breakdown:
1. List all 334 questions
2. Check if stores are unevenly distributed
3. Understand the mismatch
"""

from google.cloud import bigquery

client = bigquery.Client(project='athena-gateway-prod')

# Get all 334 questions
questions_query = """
SELECT DISTINCT
  checklistQuestionId
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-23'
ORDER BY
  checklistQuestionId
"""

print("=" * 100)
print("ALL 334 UNIQUE QUESTIONS ON 2/23/26")
print("=" * 100)
print()

results = list(client.query(questions_query).result())
questions = [row.checklistQuestionId for row in results]

print(f"Complete list ({len(questions)} questions):")
print(", ".join(questions[:50]))  # First 50
if len(questions) > 50:
    print("...")
    print(", ".join(questions[-10:]))  # Last 10
print()

# Check if all stores have 334 questions
store_question_count_query = """
SELECT
  businessUnitNumber,
  COUNT(DISTINCT checklistQuestionId) as question_count
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-23'
GROUP BY
  businessUnitNumber
ORDER BY
  question_count DESC,
  businessUnitNumber
"""

print("=" * 100)
print("QUESTION COUNT PER STORE")
print("=" * 100)
print()

results = list(client.query(store_question_count_query).result())

question_count_distribution = {}
for row in results:
    q_count = row.question_count
    if q_count not in question_count_distribution:
        question_count_distribution[q_count] = 0
    question_count_distribution[q_count] += 1

print("Distribution of question counts:")
for q_count in sorted(question_count_distribution.keys(), reverse=True):
    store_count = question_count_distribution[q_count]
    print(f"  {q_count:3d} questions: {store_count:5,} stores (pairs: {q_count * store_count:,})")

print()

# Calculate pairs by distribution
total_pairs_calc = sum(q_count * store_count for q_count, store_count in question_count_distribution.items())
print(f"Total pairs from distribution: {total_pairs_calc:,}")
print()

# Now check if store count = 4456 or different
total_stores = sum(question_count_distribution.values())
print(f"Total stores: {total_stores:,}")
print(f"Expected baseline stores: 4,595")
print(f"Missing stores: {4595 - total_stores:,}")
print()

print("=" * 100)
print("COMPARISON")
print("=" * 100)
print()
print("Baseline Formula Expected:")
print("  4,595 stores × varying question counts = 1,426,588 pairs")
print()
print("Actual 2/23 Data:")
print(f"  {total_stores:,} stores × ~334 questions = {total_pairs_calc:,} pairs")
print()
print()

# Find stores with fewer than 334 questions
stores_with_fewer = [(row.businessUnitNumber, row.question_count) 
                     for row in results if row.question_count < 334]

if stores_with_fewer:
    print(f"Stores with fewer than 334 questions ({len(stores_with_fewer)} stores):")
    for store, q_count in stores_with_fewer[:10]:
        print(f"  Store {store}: {q_count} questions")
    if len(stores_with_fewer) > 10:
        print(f"  ... and {len(stores_with_fewer) - 10} more")
else:
    print("✓ All stores have exactly 334 questions")

print()
