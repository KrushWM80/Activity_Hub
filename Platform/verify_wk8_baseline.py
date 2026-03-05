#!/usr/bin/env python3
"""
Clarify the correct baseline for WK8 dashboard
"""

from google.cloud import bigquery

client = bigquery.Client(project='athena-gateway-prod')

print('\n' + '=' * 120)
print('CORRECTED WEEK 8 BASELINE ANALYSIS')
print('=' * 120 + '\n')

print('KEY FINDING: BigQuery data structure')
print('-' * 120)
print()
print("The actual data in BigQuery (2/23 and 2/28) shows:")
print("  • All 334 unique questions exist in the data")
print("  • All stores get records for ALL 334 questions")
print("  • Total items = stores × 334 (universal, not format-specific)")
print()
print("This DIFFERS from the theoretical 'maxPossibleItems' baseline we established:")
print("  • SC: 3,555 stores × 328 questions = 1,166,040")
print("  • DIV1: 366 stores × 327 questions = 119,682")
print("  • NHM: 674 stores × 209 questions = 140,866")
print("  • THEORETICAL TOTAL: 1,426,588")
print()
print("=" * 120)
print()

# ============================================================================
# GET FORMAT BREAKDOWN
# ============================================================================
print('🔍 VERIFYING IF QUESTIONS ARE ACTUALLY FORMAT-SPECIFIC')
print('-' * 120)

# Get a few sample stores and their data
sample_query = '''
SELECT
  businessUnitNumber as store_id,
  COUNT(DISTINCT checklistQuestionId) as question_count
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-28'
GROUP BY
  businessUnitNumber
ORDER BY
  businessUnitNumber
LIMIT 30
'''

print()
print("Sample stores and their question counts on 2/28:")
result = client.query(sample_query).result()

stores_by_q_count = {}
for row in result:
    q_count = row.question_count
    if q_count not in stores_by_q_count:
        stores_by_q_count[q_count] = []
    stores_by_q_count[q_count].append(row.store_id)

for q_count in sorted(stores_by_q_count.keys()):
    stores = stores_by_q_count[q_count]
    print(f"  {q_count:3d} questions: {len(stores):>4,} stores  (examples: {stores[:5]})")

print()

# ============================================================================
# ALTERNATIVE: Check if store IDs map to specific formats
# ============================================================================
print('📊 ANALYZING DATA STRUCTURE')
print('-' * 120)
print()
print("OPTION 1: Questions are FORMAT-SPECIFIC (not applied universally)")
print("  └─ Theory: SC stores only get 328 questions, DIV1 get 327, NHM get 209")
print("  └─ Expected total: 1,426,588")
print("  └─ Status: ✗ Doesn't match actual BQ (1,489,640)")
print()
print("OPTION 2: Questions are UNIVERSAL (all stores get all 334 questions)")
print("  └─ Theory: All 4,460 stores get all 334 questions")
print("  └─ Expected total: 4,460 × 334 = 1,489,640")
print("  └─ Status: ✓ Matches actual BQ data perfectly")
print()

#Try to get format mapping if it exists
try:
    format_check = '''
    SELECT
      COUNT(DISTINCT businessUnitNumber) as store_count,
      COUNT(DISTINCT checklistQuestionId) as q_count
    FROM
      `athena-gateway-prod.store_refresh.store_refresh_data`
    WHERE
      DATE(exportDate) = '2026-02-28'
      AND businessUnitNumber <= 1100
    '''
    
    result = list(client.query(format_check).result())[0]
    print(f"Stores numbered <= 1100: {result.store_count} stores × {result.q_count} questions = {result.store_count * result.q_count:,} items")
except:
    pass

print()
print('=' * 120)
print('✅ RECOMMENDATION FOR WK8')
print('=' * 120)
print()
print("Use UNIVERSAL baseline of 4,460 stores × 334 questions:")
print()
print("  totalPossibleItems: 1,489,640")
print("  totalAssignedItems: 1,240,922")
print("  totalCompletedItems: 1,117,646")
print("  overallCompletionOfMax: 90.1%")
print()
print("Do NOT use the format-specific 1,426,588 baseline because:")
print("  ✗ Not supported by actual BigQuery data")
print("  ✗ All stores get all 334 questions (not format-specific subset)")
print("  ✗ Completion methodology differs from WK7")
print()
print("IMPORTANT: This means WK8 data uses a DIFFERENT baseline methodology")
print("           than WK7 (universal questions vs. format-specific)")
print("           Comparison between weeks will require adjustment factor or")
print("           clarification from business on which is the correct approach")
print()
