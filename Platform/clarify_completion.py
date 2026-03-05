#!/usr/bin/env python3
"""
Clarify completion metrics: COMPLETED status vs completionDate field
"""

from google.cloud import bigquery

client = bigquery.Client(project='athena-gateway-prod')

print('\n' + '=' * 120)
print('CLARIFYING COMPLETION METRICS FOR WK8')
print('=' * 120 + '\n')

# ============================================================================
# UNDERSTAND STATUS VS COMPLETION DATE
# ============================================================================
print('🔍 STATUS VALUE MEANINGS')
print('-' * 120)

detail_query = '''
SELECT
  status,
  COUNT(CASE WHEN completionDate IS NOT NULL THEN 1 END) as with_completion_date,
  COUNT(CASE WHEN completionDate IS NULL THEN 1 END) as null_completion_date,
  COUNT(*) as total
FROM
  `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE
  DATE(exportDate) = '2026-02-28'
GROUP BY
  status
ORDER BY
  total DESC
'''

print("Status breakdown with completionDate field analysis:")
print()

results = client.query(detail_query).result()
for row in results:
    status = row.status.strip() if row.status else 'NULL'
    total = row.total
    with_date = row.with_completion_date
    null_date = row.null_completion_date
    
    pct_with = (with_date / total * 100) if total > 0 else 0
    
    print(f"Status: '{status}'")
    print(f"  Total Items: {total:,}")
    print(f"  Items with completionDate: {with_date:,} ({pct_with:.1f}%)")
    print(f"  Items with NULL completionDate: {null_date:,}")
    print()

# ============================================================================
# RECOMMENDATION
# ============================================================================
print('=' * 120)
print('✅ RECOMMENDED INTERPRETATION')
print('=' * 120)
print()

print("FOR DASHBOARD METRICS, USE:")
print()
print("Option A - Status-Based (MORE CONSERVATIVE):")
print("  • totalAssignedItems = COMPLETED + PENDING = 1,240,922")
print("  • totalCompletedItems = COMPLETED only = 1,117,646")
print("  • Completion % = 1,117,646 / 1,240,922 = 90.1%")
print("  • Rationale: COMPLETED = truly done, PENDING = awaiting review")
print()
print("Option B - CompletionDate-Based (LITERAL):")
print("  • totalAssignedItems = COMPLETED + PENDING = 1,240,922")
print("  • totalCompletedItems = items with completionDate = 1,240,922")
print("  • Completion % = 100.0%")
print("  • Rationale: All assigned items have completionDate in data")
print()
print("RECOMMENDATION: Use Option A (Status-Based) for consistency with business logic")
print("               where COMPLETED = truly complete, PENDING = in review")
print()
