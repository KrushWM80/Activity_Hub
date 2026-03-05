#!/usr/bin/env python3
"""
Investigate which store(s) were added between 2/23 (WK7) and 2/28 (WK8)
"""

from google.cloud import bigquery

client = bigquery.Client(project='athena-gateway-prod')

print('\n' + '=' * 120)
print('INVESTIGATING STORE DIFFERENCES BETWEEN WK7 (2/23) AND WK8 (2/28)')
print('=' * 120 + '\n')

# ============================================================================
# 1. GET STORES ON 2/23
# ============================================================================
print('📌 STORES ON 2/23 (WK7)')
print('-' * 120)

stores_2_23 = '''
SELECT
  DISTINCT businessUnitNumber as store_id,
  COUNT(DISTINCT checklistQuestionId) as question_count
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-23'
GROUP BY
  businessUnitNumber
ORDER BY
  businessUnitNumber
'''

stores_2_23_list = set()
result = client.query(stores_2_23).result()
for row in result:
    stores_2_23_list.add(row.store_id)

print(f"Total unique stores on 2/23: {len(stores_2_23_list):,}")
print()

# ============================================================================
# 2. GET STORES ON 2/28
# ============================================================================
print('📌 STORES ON 2/28 (WK8)')
print('-' * 120)

stores_2_28 = '''
SELECT
  DISTINCT businessUnitNumber as store_id,
  COUNT(DISTINCT checklistQuestionId) as question_count
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-28'
GROUP BY
  businessUnitNumber
ORDER BY
  businessUnitNumber
'''

stores_2_28_list = set()
store_questions_2_28 = {}
result = client.query(stores_2_28).result()
for row in result:
    stores_2_28_list.add(row.store_id)
    store_questions_2_28[row.store_id] = row.question_count

print(f"Total unique stores on 2/28: {len(stores_2_28_list):,}")
print()

# ============================================================================
# 3. COMPARE
# ============================================================================
print('🔍 STORE DIFFERENCES')
print('-' * 120)

new_stores = stores_2_28_list - stores_2_23_list
removed_stores = stores_2_23_list - stores_2_28_list

print(f"New stores added (2/28 only): {len(new_stores)}")
if new_stores:
    print(f"  Store IDs: {sorted(list(new_stores))}")
    for store_id in sorted(list(new_stores)):
        q_count = store_questions_2_28.get(store_id, 0)
        print(f"    • Store {store_id}: {q_count} questions")

print()
print(f"Stores removed (2/23 only): {len(removed_stores)}")
if removed_stores:
    print(f"  Store IDs: {sorted(list(removed_stores))}")

print()
print(f"Stores in both: {len(stores_2_23_list & stores_2_28_list):,}")
print()

# ============================================================================
# 4. IF STORE WAS ADDED, PREDICT IMPACT
# ============================================================================
if len(new_stores) == 1:
    new_store_id = list(new_stores)[0]
    new_q_count = store_questions_2_28[new_store_id]
    
    print('=' * 120)
    print(f'📊 STORE ADDITION IMPACT ANALYSIS')
    print('=' * 120)
    print()
    print(f"New Store ID: {new_store_id}")
    print(f"Questions on that store: {new_q_count}")
    print()
    
    # Get that store's format/type
    store_detail = f'''
    SELECT
      DISTINCT businessUnitNumber,
      COUNT(*) as total_records,
      COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as completed,
      COUNT(CASE WHEN status = 'UnAssigned' THEN 1 END) as unassigned,
      COUNT(CASE WHEN status = 'PENDING' THEN 1 END) as pending
    FROM
      `athena-gateway-prod.store_refresh.store_refresh_data`
    WHERE
      DATE(exportDate) = '2026-02-28'
      AND businessUnitNumber = {new_store_id}
    GROUP BY
      businessUnitNumber
    '''
    
    result = list(client.query(store_detail).result())[0]
    print(f"Store {new_store_id} metrics on 2/28:")
    print(f"  Total Records: {result.total_records:,}")
    print(f"  - Completed: {result.completed:,}")
    print(f"  - UnAssigned: {result.unassigned:,}")
    print(f"  - Pending: {result.pending:,}")
    print()
    
    print(f"Expected impact on total items: +{result.total_records:,}")
    print()
    print(f"⚠️  ANALYSIS:")
    print(f"    Total item increase WK7→WK8: 1,489,640 - 1,426,588 = 63,052")
    print(f"    Expected from 1 new store: {result.total_records:,}")
    print(f"    Unaccounted items: {63052 - result.total_records:,}")
    print()
    
elif len(new_stores) > 1:
    print(f'⚠️  MULTIPLE NEW STORES: {len(new_stores)}')
    print(f"    Expected total impact: ~{sum(store_questions_2_28.get(s, 0) for s in new_stores) * len(new_stores) / len(new_stores):,.0f}")
    print()
    
else:
    print('⚠️  NO NEW STORES - Something else caused the 63,052 item increase')
    print()
    print('Possible explanations:')
    print('  1. Questions increased: baseline went from 328/327/209 to different counts')
    print('  2. Store count difference: Existing stores now have more questions')
    print('  3. Data collection methodology changed')
    print()
