#!/usr/bin/env python3
from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

print("\n" + "="*100)
print("Store Type / Format Analysis")
print("="*100 + "\n")

# Check unique Store_Type values
result = client.query("""
SELECT DISTINCT Store_Type
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND Week = 13
    AND Activity_Title IS NOT NULL
    AND Activity_Type IS NOT NULL
    AND COALESCE(Status, Message_Status) = 'Published - Published'
ORDER BY Store_Type
""").result()

print("Unique Store_Type values:")
for row in result:
    print(f"  - {row['Store_Type']}")

# Count by (event_id, Store_Type)
print("\n" + "="*100)
print("Count by (event_id, Store_Type)")
print("="*100 + "\n")

result = client.query("""
SELECT COUNT(DISTINCT CONCAT(event_id, '|', Store_Type)) as event_storetype_pairs
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND Week = 13
    AND Activity_Title IS NOT NULL
    AND Activity_Type IS NOT NULL
    AND COALESCE(Status, Message_Status) = 'Published - Published'
""").result()

for row in result:
    print(f"Distinct (event_id, Store_Type):        {row['event_storetype_pairs']}")

# Show breakdown: how many events have each store type
print("\n" + "="*100)
print("Event breakdown by Store_Type")
print("="*100 + "\n")

result = client.query("""
SELECT
    Store_Type,
    COUNT(DISTINCT event_id) as event_count
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND Week = 13
    AND Activity_Title IS NOT NULL
    AND Activity_Type IS NOT NULL
    AND COALESCE(Status, Message_Status) = 'Published - Published'
GROUP BY Store_Type
ORDER BY event_count DESC
""").result()

total = 0
for row in result:
    if row['Store_Type'] is not None:
        print(f"  {row['Store_Type']:20} : {row['event_count']:3} events")
        total += row['event_count']
    else:
        print(f"  {'<NULL>':20} : {row['event_count']:3} events")

print(f"\nTotal (excluding NULL):                 {total}")

# Sample: show events with multiple store types
print("\n" + "="*100)
print("Events with multiple Store_Type variants (showing first 10)")
print("="*100 + "\n")

result = client.query("""
SELECT
    event_id,
    Activity_Title,
    COUNT(DISTINCT Store_Type) as store_type_count,
    STRING_AGG(DISTINCT Store_Type, ', ' ORDER BY Store_Type) as store_types
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND Week = 13
    AND Activity_Title IS NOT NULL
    AND Activity_Type IS NOT NULL
    AND COALESCE(Status, Message_Status) = 'Published - Published'
GROUP BY event_id, Activity_Title
HAVING COUNT(DISTINCT Store_Type) > 1
ORDER BY store_type_count DESC
LIMIT 10
""").result()

for row in result:
    print(f"  {row['Activity_Title'][:50]:50} | Types: {row['store_type_count']}")
    print(f"    → {row['store_types']}")
    print()
