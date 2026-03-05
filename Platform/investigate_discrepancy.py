#!/usr/bin/env python3
"""
Investigate discrepancy between format-specific baseline (1,426,588) and actual BQ data (1,489,640)
"""

from google.cloud import bigquery

client = bigquery.Client(project='athena-gateway-prod')

print('\n' + '=' * 120)
print('INVESTIGATING DATA DISCREPANCY: FORMAT-SPECIFIC BASELINE vs BIGQUERY ACTUAL')
print('=' * 120 + '\n')

# ============================================================================
# BASELINE: Format-Specific Distribution (REQUIRED METHODOLOGY)
# ============================================================================
print('📐 FORMAT-SPECIFIC BASELINE (Business Requirement)')
print('-' * 120)

baseline = {
    'SC': {'stores': 3555, 'questions': 328},
    'DIV1': {'stores': 366, 'questions': 327},
    'NHM': {'stores': 674, 'questions': 209}
}

total_baseline = 0
for format_name, data in baseline.items():
    possible = data['stores'] * data['questions']
    total_baseline += possible
    print(f"  {format_name:6} : {data['stores']:>6,} stores × {data['questions']:>3} questions = {possible:>10,}")

print(f"  {'TOTAL':6}   {total_baseline:>10,}")
print()

# ============================================================================
# ACTUAL: What we're seeing in BigQuery on 2/28
# ============================================================================
print('📊 BIGQUERY ACTUAL DATA ON 2/28/26')
print('-' * 120)

actual_query = '''
SELECT
  COUNT(*) as total_records,
  COUNT(DISTINCT businessUnitNumber) as unique_stores,
  COUNT(DISTINCT checklistQuestionId) as unique_questions,
  COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as completed_count,
  COUNT(CASE WHEN status = 'PENDING' THEN 1 END) as pending_count,
  COUNT(CASE WHEN status = 'UnAssigned' THEN 1 END) as unassigned_count
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-28'
'''

result = list(client.query(actual_query).result())[0]
print(f"  Total Records in BQ: {result.total_records:,}")
print(f"  Unique Stores: {result.unique_stores:,}")
print(f"  Unique Questions: {result.unique_questions:,}")
print()
print(f"  Status Breakdown:")
print(f"    COMPLETED:  {result.completed_count:>10,}")
print(f"    PENDING:    {result.pending_count:>10,}")
print(f"    UnAssigned: {result.unassigned_count:>10,}")
print(f"    TOTAL:      {result.total_records:>10,}")
print()

# ============================================================================
# ANALYSIS: What's the difference?
# ============================================================================
print('=' * 120)
print('DISCREPANCY ANALYSIS')
print('=' * 120)
print()

difference = result.total_records - total_baseline
print(f"Expected (format-specific baseline): {total_baseline:,}")
print(f"Actual (in BigQuery):                 {result.total_records:,}")
print(f"DIFFERENCE:                           {difference:,} extra records")
print()

if difference > 0:
    print(f"⚠️  ISSUE: {difference:,} MORE records in BQ than expected")
    print()
    print("Possible causes:")
    print("  1. Store 5927 added (but should only be 334 items, not {difference:,})")
    print("  2. Questions increased per format (but we have {result.unique_questions:,}, not the expected total)")
    print("  3. Duplicate records in BigQuery")
    print("  4. Different data collection methodology than format-specific design")
    print()

# ============================================================================
# VERIFY USING FORMAT-SPECIFIC TOTALS
# ============================================================================
print('=' * 120)
print('CORRECTED CALCULATION - Using Format-Specific Baseline')
print('=' * 120)
print()

print("For WK8 (2/28/26) Dashboard:")
print()
print(f"  totalPossibleItems: {total_baseline:,}")
print(f"    └─ Based on format-specific: SC (3,555 × 328) + DIV1 (366 × 327) + NHM (674 × 209)")
print()
print(f"  totalAssignedItems: {result.pending_count:,}") 
print(f"    └─ PENDING status only (Assigned = items awaiting completion)")
print()
print(f"  totalCompletedItems: {result.completed_count:,}")
print(f"    └─ COMPLETED status only")
print()

if result.pending_count > 0:
    completion_pct = (result.completed_count / result.pending_count) * 100
    print(f"  overallCompletionOfMax: {completion_pct:.1f}%")
    print(f"    └─ {result.completed_count:,} ÷ {result.pending_count:,}")
print()

print('=' * 120)
print('STORE 5927 ANALYSIS')
print('=' * 120)
print()

store_5927_query = '''
SELECT
  businessUnitNumber,
  COUNT(DISTINCT checklistQuestionId) as question_count,
  COUNT(*) as total_records,
  COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as completed,
  COUNT(CASE WHEN status = 'PENDING' THEN 1 END) as pending,
  COUNT(CASE WHEN status = 'UnAssigned' THEN 1 END) as unassigned
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-28'
  AND businessUnitNumber = 5927
GROUP BY
  businessUnitNumber
'''

try:
    result_5927 = list(client.query(store_5927_query).result())[0]
    print(f"Store 5927 (new store on 2/28):")
    print(f"  Questions: {result_5927.question_count}")
    print(f"  Total Records: {result_5927.total_records}")
    print(f"  - Completed: {result_5927.completed}")
    print(f"  - Pending: {result_5927.pending}")
    print(f"  - UnAssigned: {result_5927.unassigned}")
    print()
    print(f"⚠️  QUESTION: What format is store 5927?")
    print(f"   Expected items if SC: 328")
    print(f"   Expected items if DIV1: 327")
    print(f"   Expected items if NHM: 209")
    print(f"   Actual items in BQ: {result_5927.question_count}")
except Exception as e:
    print(f"Store 5927 not found or error: {e}")

print()
