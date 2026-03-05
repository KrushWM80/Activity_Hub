#!/usr/bin/env python3
"""
Check if question distribution changed between 2/23 and 2/28
"""

from google.cloud import bigquery

client = bigquery.Client(project='athena-gateway-prod')

print('\n' + '=' * 120)
print('INVESTIGATING QUESTION DISTRIBUTION CHANGES BETWEEN 2/23 AND 2/28')
print('=' * 120 + '\n')

# ============================================================================
# 1. COUNT UNIQUE QUESTIONS ON EACH DATE
# ============================================================================
print('📌 QUESTION COUNT BY DATE')
print('-' * 120)

date_query = '''
SELECT
  DATE(exportDate) as export_date,
  COUNT(DISTINCT checklistQuestionId) as unique_questions,
  COUNT(DISTINCT businessUnitNumber) as unique_stores,
  COUNT(*) as total_records,
  ROUND(COUNT(*) / COUNT(DISTINCT businessUnitNumber), 2) as avg_q_per_store
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) IN ('2026-02-23', '2026-02-28')
GROUP BY
  DATE(exportDate)
ORDER BY
  export_date
'''

date_results = client.query(date_query).result()
for row in date_results:
    date = row.export_date.strftime('%Y-%m-%d')
    print(f"{date}:")
    print(f"  Unique Questions: {row.unique_questions:,}")
    print(f"  Unique Stores: {row.unique_stores:,}")
    print(f"  Total Records: {row.total_records:,}")
    print(f"  Avg Questions per Store: {row.avg_q_per_store}")
    print(f"  Calculation: {row.unique_stores:,} × {int(row.avg_q_per_store * row.unique_stores / row.unique_stores):,} = {row.total_records:,}")
    print()

print()

# ============================================================================
# 2. GET THE ACTUAL QUESTIONS
# ============================================================================
print('📋 UNIQUE QUESTIONS ON 2/23')
print('-' * 120)

q_2_23 = '''
SELECT
  DISTINCT checklistQuestionId
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-23'
ORDER BY
  checklistQuestionId
'''

questions_2_23_set = set()
result = client.query(q_2_23).result()
for row in result:
    questions_2_23_set.add(row.checklistQuestionId)

print(f"Total questions on 2/23: {len(questions_2_23_set):,}")
if len(questions_2_23_set) <= 20:
    print(f"Questions: {sorted(list(questions_2_23_set))}")
print()

# ============================================================================
# 3. GET QUESTIONS ON 2/28
# ============================================================================
print('📋 UNIQUE QUESTIONS ON 2/28')
print('-' * 120)

q_2_28 = '''
SELECT
  DISTINCT checklistQuestionId
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-28'
ORDER BY
  checklistQuestionId
'''

questions_2_28_set = set()
result = client.query(q_2_28).result()
for row in result:
    questions_2_28_set.add(row.checklistQuestionId)

print(f"Total questions on 2/28: {len(questions_2_28_set):,}")
if len(questions_2_28_set) <= 20:
    print(f"Questions: {sorted(list(questions_2_28_set))}")
print()

# ============================================================================
# 4. ANALYZE QUESTION CHANGES
# ============================================================================
print('=' * 120)
print('QUESTION SET CHANGES')
print('=' * 120)

new_questions = questions_2_28_set - questions_2_23_set
removed_questions = questions_2_23_set - questions_2_28_set

print(f"New questions on 2/28 (not on 2/23): {len(new_questions):,}")
if len(new_questions) <= 50:
    print(f"  {sorted(list(new_questions))}")

print()
print(f"Questions removed by 2/28 (were on 2/23): {len(removed_questions):,}")
if len(removed_questions) <= 50:
    print(f"  {sorted(list(removed_questions))}")

print()
print(f"Questions in both dates: {len(questions_2_23_set & questions_2_28_set):,}")
print()

# ============================================================================
# 5. CALCULATE EXPECTED ITEMS
# ============================================================================
print('=' * 120)
print('MATHEMATICAL VERIFICATION')
print('=' * 120)
print()

stores_2_23 = 4459
stores_2_28 = 4460
questions_2_23 = len(questions_2_23_set)
questions_2_28 = len(questions_2_28_set)

expected_2_23 = stores_2_23 * questions_2_23
expected_2_28 = stores_2_28 * questions_2_28
actual_2_23 = 1426588
actual_2_28 = 1489640

print(f"2/23 (WK7):")
print(f"  Stores: {stores_2_23:,} × Questions: {questions_2_23:,} = {expected_2_23:,}")
print(f"  Actual in BQ: {actual_2_23:,}")
print(f"  Match: {'✓' if expected_2_23 == actual_2_23 else '✗'}")
print()

print(f"2/28 (WK8):")
print(f"  Stores: {stores_2_28:,} × Questions: {questions_2_28:,} = {expected_2_28:,}")
print(f"  Actual in BQ: {actual_2_28:,}")
print(f"  Match: {'✓' if expected_2_28 == actual_2_28 else '✗'}")
print()

if expected_2_28 == actual_2_28:
    print(f"✅ CONCLUSION: The {actual_2_28:,} items on 2/28 = {stores_2_28:,} stores × {questions_2_28} questions")
    print(f"   Increase from 2/23 because: +1 store (5927) + potentially new questions")
else:
    print(f"⚠️  MISMATCH: Expected {expected_2_28:,} but got {actual_2_28:,}")
    print(f"   Difference: {actual_2_28 - expected_2_28:,}")
print()
