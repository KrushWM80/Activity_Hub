#!/usr/bin/env python3
"""
Check actual store/question distribution on 2/23
Compare against baseline formula
"""

from google.cloud import bigquery

client = bigquery.Client(project='athena-gateway-prod')

print("=" * 100)
print("STORE/QUESTION DISTRIBUTION ANALYSIS - 2/23/26")
print("=" * 100)
print()

# Get store counts by business unit
store_query = """
SELECT
  businessUnitNumber,
  COUNT(DISTINCT checklistQuestionId) as question_count,
  COUNT(DISTINCT CONCAT(checklistQuestionId, '|', CAST(businessUnitNumber AS STRING))) as pair_count
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-23'
GROUP BY
  businessUnitNumber
ORDER BY
  businessUnitNumber
"""

print("Querying store-question distribution on 2/23...")
results = list(client.query(store_query).result())

# Try to map to formats/divisions
# SC: 3555, DIV1: 366, NHM: 674
# Need to understand the businessUnitNumber mapping

bu_totals = {}
total_pairs = 0
total_questions_across_stores = 0

print(f"\n{'BU #':<8} {'Question Count':<18} {'Pair Count':<18}")
print("-" * 44)

for row in results:
    bu = row.businessUnitNumber
    q_count = row.question_count
    pair_count = row.pair_count
    bu_totals[bu] = {'questions': q_count, 'pairs': pair_count}
    total_pairs += pair_count
    print(f"{bu:<8} {q_count:<18} {pair_count:<18}")

print("-" * 44)
print(f"{'TOTAL':<8} {' ':<18} {total_pairs:<18}")
print()

print("=" * 100)
print("BASELINE EXPECTATION (from formula)")
print("=" * 100)
print()
print("SC:   3,555 stores × 328 questions = 1,166,040")
print("DIV1:   366 stores × 327 questions =   119,682")
print("NHM:    674 stores × 209 questions =   140,866")
print("-" * 50)
print("TOTAL: 4,595 stores              = 1,426,588")
print()
print()

print("=" * 100)
print("ACTUAL ON 2/23/26")
print("=" * 100)
print()
print(f"Total unique (question, store) pairs: {total_pairs:,}")
print(f"Difference from baseline: {total_pairs - 1426588:,} extra pairs")
print()
