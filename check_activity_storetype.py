#!/usr/bin/env python3
from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

print("\n" + "="*100)
print("Analyzing Activity_Title + Store_Type combinations")
print("="*100 + "\n")

# Test: (Activity_Title, Store_Type) excluding NULL
result = client.query("""
SELECT COUNT(DISTINCT CONCAT(Activity_Title, '|', COALESCE(Store_Type, 'UNKNOWN'))) as title_storetype_pairs
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND Week = 13
    AND Activity_Title IS NOT NULL
    AND Activity_Type IS NOT NULL
    AND COALESCE(Status, Message_Status) = 'Published - Published'
""").result()

for row in result:
    print(f"1. (Activity_Title, Store_Type) with UNKNOWN for NULL: {row['title_storetype_pairs']}")

# Test: (Activity_Title, Store_Type) excluding NULL store types
result = client.query("""
SELECT COUNT(DISTINCT CONCAT(Activity_Title, '|', Store_Type)) as title_storetype_pairs
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND Week = 13
    AND Activity_Title IS NOT NULL
    AND Activity_Type IS NOT NULL
    AND COALESCE(Status, Message_Status) = 'Published - Published'
    AND Store_Type IS NOT NULL
""").result()

for row in result:
    print(f"2. (Activity_Title, Store_Type) excluding NULLs:     {row['title_storetype_pairs']}")

# Test: (Activity_Title, Business_Area)
result = client.query("""
SELECT COUNT(DISTINCT CONCAT(Activity_Title, '|', Business_Area)) as title_area_pairs
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND Week = 13
    AND Activity_Title IS NOT NULL
    AND Activity_Type IS NOT NULL
    AND COALESCE(Status, Message_Status) = 'Published - Published'
""").result()

for row in result:
    print(f"3. (Activity_Title, Business_Area):                 {row['title_area_pairs']}")

# Test: Just count all unique rows (no grouping)
result = client.query("""
SELECT COUNT(*) as total_rows
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND Week = 13
    AND Activity_Title IS NOT NULL
    AND Activity_Type IS NOT NULL
    AND COALESCE(Status, Message_Status) = 'Published - Published'
""").result()

for row in result:
    print(f"4. Total raw rows (no grouping):                   {row['total_rows']}")

print("\n" + "="*100)
print("Checking CSV format hypothesis")
print("="*100 + "\n")

# If CSV shows (Activity_Title, Store_Type), show sample
result = client.query("""
SELECT
    Activity_Title,
    Store_Type,
    COUNT(*) as row_count
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND Week = 13
    AND Activity_Title IS NOT NULL
    AND Activity_Type IS NOT NULL
    AND COALESCE(Status, Message_Status) = 'Published - Published'
    AND Store_Type IS NOT NULL
GROUP BY Activity_Title, Store_Type
ORDER BY Activity_Title, Store_Type
LIMIT 20
""").result()

print("Sample (Activity_Title, Store_Type) combinations:")
for row in result:
    print(f"  {row['Activity_Title'][:45]:45} | {row['Store_Type']:20} | Rows: {row['row_count']}")
